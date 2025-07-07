# LangChain Hospital Chatbot

This project is a full-stack FAQ chatbot for a hospital, built using [LangChain](https://github.com/langchain-ai/langchain), FastAPI, PostgreSQL with pgvector, Redis, and a React frontend. It provides users with answers to hospital-related questions using a vector database of FAQ documents and OpenAI's language models.

## Features

- **Frontend**: React app with Tailwind CSS for a modern chat interface.
- **Backend**: FastAPI microservices for conversation management and LLM-powered responses.
- **Vector Search**: Uses pgvector extension in PostgreSQL to store and retrieve document embeddings.
- **Persistence**: Redis for conversation state management.
- **Containerized**: Docker and docker-compose for easy local development and deployment.
- **Kubernetes-ready**: Includes deployment manifests for Kubernetes.

## Getting Started

### Prerequisites

- Docker & Docker Compose
- OpenAI API key (set in `.env`)

### Setup

1. **Clone the repository**  
    ```
    git clone https://github.com/haha1250/LangChainChatbot.git
    cd LangChainChatbot
    ```

2. **Set up environment variables**  
    Create a `.env` file with your OpenAI API key and database credentials:
    ```
    OPENAI_API_KEY=your-openai-key
    DB_HOST=postgres
    DB_PORT=5432
    DB_NAME=vectordb
    DB_USER=admin
    DB_PASSWORD=admin
    ```

3. **Build and start all services**  
    ```
    docker-compose up --build
    ```

4. **Insert FAQ data into the vector database**  
In a new terminal:
    ```
    docker-compose run --rm service2 python insert_data.py
    ```

5. **Access the frontend**  
Open [http://localhost:3000](http://localhost:3000) in your browser.

## Usage

- Ask questions in the chat interface.
- The backend retrieves relevant FAQ entries using vector search and generates answers with OpenAI.
- Conversation history is stored in Redis.

## Deployment on local Docker Kubernetes

1. **Run Registry as Docker Container**
    ```
    docker run -d -p 5000:5000 --name local-registry registry:2
    ```

2. **Build all images locally**
    ```
    docker build -t mypostgres ./postgres
    docker build -t myservice2 ./service2
    docker build -t myservice3 ./service3
    docker build -t myfrontend ./frontend
    ```

3. **Tag and push images**
    ```
    # For Postgres
    docker tag mypostgres localhost:5000/mypostgres
    docker push localhost:5000/mypostgres

    # For Service2
    docker tag myservice2 localhost:5000/myservice2
    docker push localhost:5000/myservice2

    # For Service3
    docker tag myservice3 localhost:5000/myservice3
    docker push localhost:5000/myservice3

    # For Frontend
    docker tag myfrontend localhost:5000/myfrontend
    docker push localhost:5000/myfrontend
    ```

4. **Kubernetes deployment**
- For Kubernetes, use the manifests in [all-deployments.yaml](all-deployments.yaml), specify the images' name accordingly.
- Deploy:
    ```
    kubectl apply -f all-deployments.yaml
    ```
- For local testing, expose service by `kubectl port-forward`. For example, exposing frontend with:
    ```
    kubectl port-forward deployment/frontend 3000:3000
    ```
- Then open `http://localhost:3000` from a browser.

## Acknowledgments

This project is based on concepts from the [Langchain-Production-Project](https://github.com/Coding-Crashkurse/Langchain-Production-Project.git).
