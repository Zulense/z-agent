import pathlib
from google import genai
from zagent.client import BreakdownClient
from dotenv import load_dotenv
import os 
load_dotenv()
api_key = os.getenv("API_KEY")



def main():
    print("Hello from eduly!")

    # Initialize Gemini client
    gemini_client = genai.Client(api_key=api_key)

    # ═══════════════════════════════════════════════════
    # Step 1: Break down a PDF into atomic topics
    # ═══════════════════════════════════════════════════
    breakdown_client = BreakdownClient(gemini_client)

    breakdown, _ = breakdown_client.breakdown(
        file_path=pathlib.Path("./attention_is_all_you_need.pdf"),
        model="gemini-2.5-flash",
        # thinking_level="high"
    )

    print(f"Document: {breakdown.document_title}")
    for i, topic in enumerate(breakdown.topics):
        print(f"  Topic {i}: {topic.name}")


if __name__ == "__main__":
    main()