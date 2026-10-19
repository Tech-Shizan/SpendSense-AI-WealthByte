import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
print(f"Loaded GEMINI_API_KEY: {'Yes (Length: ' + str(len(api_key)) + ')' if api_key else 'No'}")

# Initialize model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0.2,
    max_retries=1,
    google_api_key=api_key,
)

print("Sending 'Hello' to gemini-3.5-flash...")
try:
    response = llm.invoke("Hello")
    print("\n--- Response ---")
    print(response.content)
except Exception as e:
    print(f"\n--- Error ---: {e}")
