from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
import os
import json
import google.generativeai as genai  # Google's official Gemini library

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load embedding model for context retrieval
embedder = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Connect to vector database
retriever = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_langchain",
    embedding=embedder
)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Main RAG loop
while True:
    query = input("> ")

    # Step 1: Retrieve relevant context from vector store
    relevant_chunks = retriever.similarity_search(query=query)
    context = "\n".join([doc.page_content for doc in relevant_chunks])

    # Step 2: Build prompt
    system_prompt = f"""
You are a helpful AI assistant who answers questions about "The Power of your Subconscious Mind" book.
You work in plan → action → output mode.

For the given user query, first plan your approach, then provide the final answer based on the context.

Rules:
1. Follow the strict JSON output format
2. Always perform one step at a time
3. Only use the provided context

Context:
{context}

Example:
User Query: What is the subconscious mind?
Output: {{"step": "plan", "content": "I need to explain the subconscious mind using the context from Joseph Murphy's book."}}
Output: {{"step": "output", "content": "According to Joseph Murphy, the subconscious mind is..."}}

User Query: {query}

Respond in JSON format only.
"""

    # Step 3: Call Gemini
    try:
        response = model.generate_content(system_prompt)
        output = response.text.strip()

        print("\n🧠 Raw Gemini output:\n", output)

        # Step 4: Try parsing output as JSON
        for line in output.splitlines():
            try:
                parsed = json.loads(line)
                if parsed.get("step") == "plan":
                    print(f"🧠 Plan: {parsed['content']}")
                elif parsed.get("step") == "output":
                    print(f"🤖 Answer: {parsed['content']}")
                    break
            except json.JSONDecodeError:
                continue

    except Exception as e:
        print(f"❌ Error from Gemini: {e}")
