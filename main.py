
import langchain
langchain.debug = True

import pathlib
from google import genai
from zagent.client import BreakdownClient
from dotenv import load_dotenv
import os 
load_dotenv()
api_key = os.getenv("API_KEY")
from zagent.client import AnimationClient


def my_progress_tracker(topic_index, iteration, message):
    print(f"⏳ [Topic {topic_index} | Attempt {iteration}] {message}")


def main():
    print("Hello from z-agent!")

    # Initialize Gemini client
    gemini_client = genai.Client(api_key=api_key)

    # ═══════════════════════════════════════════════════
    # Step 1: Break down a PDF into atomic topics
    # ═══════════════════════════════════════════════════
    breakdown_client = BreakdownClient(gemini_client)

    breakdown, _ = breakdown_client.breakdown(
        file_path=pathlib.Path("./deepseek_mhc.pdf"),
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
        api_key=api_key
    )

    animation_client = AnimationClient(
        langchain_model=langchain_model,
        agent_workspace_path="./examples/agent_workspace/"
    )
    

    # ---------------------------------------------------------------------------------------------------------
    # # Dynamically search for the "Multi-Head" topic
    # target_index = -1
    # target_topic_name = ""

    # for i, topic in enumerate(breakdown.topics):
    #     if "Multi-Head" in topic.name:
    #         target_index = i
    #         target_topic_name = topic.name
    #         break # Stop searching once we find it

    # # Safety check in case the LLM didn't generate that specific topic this time
    # if target_index == -1:
    #     print("❌ Error: Could not find a topic containing 'Multi-Head' in this run.")
    #     return # Exit the program gracefully

    # print(f"\n🎯 Found target at index {target_index}: {target_topic_name}")

    target_index = 4
    target_topic_name = breakdown.topics[target_index].name

    # Animate a single topic
    result = animation_client.animate_single(
        breakdown=breakdown,
        storyboard=storyboards[target_topic_name],
        topic_index=target_index,
        max_iterations=3,
        on_progress=my_progress_tracker
    )

    if result.success:
        print(f"Video saved to: {result.video_path}")
    else:
        print(f"Failed: {result.error_message}")


if __name__ == "__main__":
    main()