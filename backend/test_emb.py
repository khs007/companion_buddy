import os
from dotenv import load_dotenv
from langchain_community.embeddings import JinaEmbeddings

load_dotenv()

print("API KEY FOUND:", bool(os.getenv("JINA_API_KEY")))

if not os.getenv("JINA_API_KEY"):
    print("❌ JINA_API_KEY not set in .env")
    exit(1)

embeddings = JinaEmbeddings(
    model_name="jina-embeddings-v2-base-en",
    api_key=os.getenv("JINA_API_KEY")
)

print("Sending embedding request...")

try:
    result = embeddings.embed_query("hello world")
    print("✅ SUCCESS!")
    print("Vector length:", len(result))
    print("First 5 values:", result[:5])
except Exception as e:
    print(f"❌ Error: {e}")