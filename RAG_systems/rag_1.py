import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI

load_dotenv()

client = OpenAI()

pdf_path=Path(__file__).parent / 'The Power of your Subconscious Mind by Joseph Murphy.pdf'
loader=PyPDFLoader(file_path=pdf_path)

docs=loader.load()

text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

split_docs=text_splitter.split_documents(documents=docs)

embedder=OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=os.environ['OPENAI_API_KEY']
)

# vector_store=QdrantVectorStore.from_documents(
#     documents=[],
#     url='http://localhost:6333',
#     collection_name="learning_langchain",
#     embedding=embedder
# )

# vector_store.add_documents(documents=split_docs)

retriver=QdrantVectorStore.from_existing_collection(
    url='http://localhost:6333',
    collection_name="learning_langchain",
    embedding=embedder
)

question = input("Enter your question: ")


context=retriver.similarity_search(
    query=question
)

system_prompt = f"""You are a helpful assistant that provides information based on the provided context.

you will be given a context and a question. Your task is to answer the question based on the context provided.
If the context does not provide enough information to answer the question, respond with "I don't know".

Context: {context}


"""

result = client.chat.completions.create(
    model="gpt-4",
    messages=[
        { "role": "system", "content": system_prompt},
        { "role": "user", "content": question }
    ]
)

print(result.choices[0].message.content)