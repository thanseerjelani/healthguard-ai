"""
HealthGuard AI - Main Application Entry Point

This is the main entry point for the HealthGuard AI health assistant.
Run this file to start an interactive conversation with the health agent.
"""

import os
import asyncio
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agents.health_coordinator import create_health_coordinator

# Load environment variables
load_dotenv()

# Verify API key is set
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError(
        "GOOGLE_API_KEY not found. Please create a .env file with your API key."
    )

# Configure retry options for API resilience
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


# -------------------------------------------------------------
# INTERACTIVE SESSION
# -------------------------------------------------------------
async def run_interactive_session():
    """
    Run an interactive chat session with HealthGuard AI.
    """

    print("=" * 70)
    print("🏥 HealthGuard AI - Your Personal Health Assistant")
    print("=" * 70)
    print("\nInitializing HealthGuard AI...")

    # Create the health coordinator agent
    health_coordinator = create_health_coordinator(retry_config)

    # Set up session management
    session_service = InMemorySessionService()

    # Create runner
    runner = InMemoryRunner(
        agent=health_coordinator
    )

    print("✅ HealthGuard AI is ready!\n")
    print("I can help you with:")
    print("  • Health condition research")
    print("  • Medication safety and interactions")
    print("  • Symptom assessment")
    print("\n⚠️  DISCLAIMER: I'm an AI assistant, not a doctor.")
    print("   Always consult healthcare professionals for medical advice.\n")
    print("=" * 70)
    print("\nType 'quit' or 'exit' to end the conversation.\n")

    # Interactive conversation loop
    while True:
        try:
            user_input = input("\n🧑 You: ").strip()

            # Exit commands
            if user_input.lower() in ["quit", "exit", "bye", "goodbye"]:
                print("\n👋 Thank you for using HealthGuard AI. Stay healthy!")
                break

            if not user_input:
                continue

            print("\n🤔 HealthGuard AI is thinking...\n")

            # Run the agent
            await runner.run_debug(user_input)

            print("\n" + "-" * 70)

        except KeyboardInterrupt:
            print("\n\n👋 Thank you for using HealthGuard AI. Stay healthy!")
            break

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again or type 'quit' to exit.\n")


# -------------------------------------------------------------
# DEMO MODE
# -------------------------------------------------------------
async def run_demo_queries():
    """
    Run a set of demo queries to showcase HealthGuard AI capabilities.
    """

    print("=" * 70)
    print("🏥 HealthGuard AI - Demo Mode")
    print("=" * 70)
    print("\nInitializing HealthGuard AI...\n")

    health_coordinator = create_health_coordinator(retry_config)
    session_service = InMemorySessionService()

    runner = InMemoryRunner(
        agent=health_coordinator
    )

    print("✅ HealthGuard AI is ready!\n")
    print("=" * 70)
    print("\nRunning Demo Queries...\n")

    demo_queries = [
        "I have a headache and mild fever. My current medications are Lisinopril and Metformin. What over-the-counter pain reliever can I safely take?",
        "What are the symptoms of the flu and when should I see a doctor?",
        "Can I take ibuprofen if I'm on blood pressure medication?",
    ]

    for i, query in enumerate(demo_queries, 1):
        print(f"\n{'=' * 70}")
        print(f"Demo Query {i}/{len(demo_queries)}")
        print(f"{'=' * 70}")
        print(f"\n🧑 User: {query}\n")
        print("🤔 HealthGuard AI is thinking...\n")

        try:
            await runner.run_debug(query)
            print("\n" + "-" * 70)
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")

        if i < len(demo_queries):
            await asyncio.sleep(2)

    print("\n" + "=" * 70)
    print("✅ Demo completed!")
    print("=" * 70)


# -------------------------------------------------------------
# MAIN MENU
# -------------------------------------------------------------
def main():
    """
    Main entry point with menu selection.
    """

    print("\n" + "=" * 70)
    print("🏥 HealthGuard AI")
    print("=" * 70)
    print("\nSelect mode:")
    print("  1. Interactive Chat (talk with HealthGuard AI)")
    print("  2. Run Demo Queries (see example capabilities)")
    print("  3. Exit")

    while True:
        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            asyncio.run(run_interactive_session())
            break
        elif choice == "2":
            asyncio.run(run_demo_queries())
            break
        elif choice == "3":
            print("\n👋 Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


# -------------------------------------------------------------
# ENTRY POINT CHECK
# -------------------------------------------------------------
if __name__ == "__main__":
    main()
