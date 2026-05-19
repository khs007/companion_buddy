import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

print("API KEY FOUND:", bool(os.getenv("GOOGLE_API_KEY")))

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

print("Sending embedding request...")

result = embeddings.embed_query("hello world")

print("SUCCESS!")
print("Vector length:", len(result))
print(result[:5])