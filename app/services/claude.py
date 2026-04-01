import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_ai_response(message: str):
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return response.content[0].text

    except Exception as e:
        print("Claude error:", e)

        # 🔥 fallback (IMPORTANT)
        return "Here are 3 startup ideas:\n1. AI fitness coach\n2. Study planner"