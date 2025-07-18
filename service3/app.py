import logging
import os
from typing import List, Any

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import PGVector
from langchain_openai import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate
)
import openai
from openai import RateLimitError

from pydantic import BaseModel


ROLE_CLASS_MAP = {
    "assistant": AIMessage,
    "user": HumanMessage,
    "system": SystemMessage
}

load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")
CONNECTION_STRING = "postgresql+psycopg2://admin:admin@postgres:5432/vectordb"
COLLECTION_NAME = "vectordb"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)    


class Message(BaseModel):
    role: str
    content: str


class Conversation(BaseModel):
    conversation: List[Message]


embeddings = OpenAIEmbeddings()
chat = ChatOpenAI(temperature=0)
store = PGVector(
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
    embedding_function=embeddings,
    use_jsonb=True
)
retriever = store.as_retriever()

prompt_template = """As a FAQ Bot for our hospital, you have the following information about our hospital:

{context}

Please provide the most suitable response for the users question.
Answer:"""

prompt = PromptTemplate(
    template=prompt_template, input_variables=["context"]
)
system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)


def create_message(conversation: List[Message]):
    return [ROLE_CLASS_MAP[message.role](content=message.content) for message in conversation]


def format_docs(docs) -> Any:
    formatted_docs: List[Any] = []
    for doc in docs:
        formatted_doc = "Source: " + doc.metadata['source']
        formatted_doc.append(formatted_doc)
    return '\n'.join(formatted_docs)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/service3/{conversation_id}")
async def service3(conversation_id: str, conversation: Conversation) -> dict[str, Any]:
    try:
        query = conversation.conversation[-1].content
        docs = retriever.invoke(input=query)
        docs = format_docs(docs=docs)
        prompt = system_message_prompt.format(context=docs)
        messages = [prompt] + create_message(conversation=conversation.conversation)

        result = chat(messages)
        return {"id": conversation_id, "reply": result.content}
    
    except RateLimitError:
        raise HTTPException(status_code=429, detail="OpenAI rate limit exceeded.")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
