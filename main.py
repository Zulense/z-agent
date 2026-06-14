import pathlib
from google import genai
from zagent.client import BreakdownClient
from dotenv import load_dotenv
import os 
load_dotenv()
api_key = os.getenv("API_KEY")
from zagent.client import AnimationClient


def main():
    print("Hello from z-agent!")

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


    # ═══════════════════════════════════════════════════
    # Step 2: Generate storyboards for each topic
    # ═══════════════════════════════════════════════════
    storyboards = {}
    for topic in breakdown.topics:
        storyboard, _ = breakdown_client.storyboard(
            topic=topic,
            model="gemini-2.5-flash",
            # thinking_level="high"
        )
        storyboards[topic.name] = storyboard
    print("==============> [storyboards]", storyboards)

    # ═══════════════════════════════════════════════════
    # Step 3: Animate storyboards with the Manim agent
    # ═══════════════════════════════════════════════════
    from langchain_google_genai import ChatGoogleGenerativeAI

    langchain_model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=1.0,
    )

    animation_client = AnimationClient(
        langchain_model=langchain_model,
        agent_workspace_path="./examples/agent_workspace/"
    )

    # Animate a single topic
    result = animation_client.animate_single(
        breakdown=breakdown,
        storyboard=storyboards["Multi-Head Attention"],
        topic_index=3,
        max_iterations=5
    )

    if result.success:
        print(f"Video saved to: {result.video_path}")
    else:
        print(f"Failed: {result.error_message}")


if __name__ == "__main__":
    main()