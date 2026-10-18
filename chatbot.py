import os


SYSTEM_INSTRUCTIONS = """
You are a helpful AI Chatbot Assistant.

Your responsibilities:
1. Answer questions clearly.
2. Explain difficult topics in simple language.
3. Help with programming and everyday tasks.
4. Give examples when useful.
5. Admit when you are uncertain.
6. Never claim that you performed an action
   that you did not actually perform.
"""


def get_bot_reply(message, history):
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    # Offline demo mode
    if not api_key:
        return offline_reply(message)

    # Connect to the AI API
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-5-mini")

    conversation = []

    for item in history:
        role = item.get("role")
        content = item.get("content", "")

        if role in ("user", "assistant") and content:
            conversation.append({
                "role": role,
                "content": content
            })

    conversation.append({
        "role": "user",
        "content": message
    })

    response = client.responses.create(
        model=model,
        instructions=SYSTEM_INSTRUCTIONS,
        input=conversation,
        max_output_tokens=800
    )

    answer = response.output_text.strip()

    if not answer:
        return "I could not generate an answer. Please try again."

    return answer


def offline_reply(message):
    text = message.lower().strip()

    if any(word in text for word in ["hello", "hi", "hey"]):
        return (
            "Hello! Welcome to AI Chatbot Assistant. "
            "How can I help you today?"
        )

    if "your name" in text:
        return "I am AI Chatbot Assistant, built using Python and Flask."

    if "python" in text:
        return (
            "Python is a programming language used for AI, "
            "web development, automation, and data analysis.\n\n"
            "Example:\nprint('Hello, world!')"
        )

    if "help" in text:
        return (
            "I can answer a few demo questions while offline. "
            "Configure OPENAI_API_KEY in your .env file to enable "
            "AI-generated answers."
        )

    return (
        "I am currently running in offline demo mode. "
        "Add a valid AI API key to your .env file to enable "
        "full AI-generated answers."
    )