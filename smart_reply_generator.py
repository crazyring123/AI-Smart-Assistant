import cohere
from cohere.errors import TooManyRequestsError

co = cohere.Client("SFPPbhQMlHl0AxctCLNmyzVyqC911eAtG5BVCwHb")  # ⚠️ Replace with production key if needed

def generate_reply(email_body):
    prompt = f"""You're an AI email assistant. Generate a short, professional reply to the following email:\n\n"{email_body}"\n\nReply:"""

    try:
        response = co.generate(
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        reply = response.generations[0].text.strip()
    except TooManyRequestsError as e:
        reply = f"⚠️ Rate limit hit: {e}"
    except Exception as e:
        reply = f"❌ Error generating reply: {e}"

    return reply
