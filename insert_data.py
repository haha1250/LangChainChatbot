from dotenv import find_dotenv, load_dotenv
from langchain_community.vectorstores import PGVector
from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters.character import CharacterTextSplitter

load_dotenv(find_dotenv())

embeddings = OpenAIEmbeddings()
loader = DirectoryLoader(
    "./FAQ", glob="**/*.txt", loader_cls=TextLoader, show_progress=True
)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

CONNECTION_STRING = "postgresql+psycopg2://postgres:vidi@127.0.0.1:5432/vectordb"
COLLECTION_NAME = "vectordb"

PGVector.from_documents(
    documents=docs,
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING
)
