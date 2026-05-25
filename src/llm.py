import os
import json

# ---- FIX SSL ISSUE ----
os.environ.pop("SSL_CERT_FILE", None)
os.environ.pop("SSL_CERT_DIR", None)

import truststore
truststore.inject_into_ssl()

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

# ✅ Load from ENV
BASE_URL = os.getenv("LLM_BASE_URL")
API_KEY = os.getenv("LLM_API_KEY")
MODEL = os.getenv("LLM_MODEL", "openai.gpt-5.2")

print("LLM BASE URL:", BASE_URL)
print("LLM MODEL:", MODEL)

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)


def parse_requirement(requirement: str) -> dict:
    prompt = f"""
    Extract:
    - document name
    - container name

    Request: {requirement}

    Return STRICT JSON:
    {{
        "document": "...",
        "container": "..."
    }}
    """

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        print("\n🤖 LLM RAW OUTPUT:\n", content)

        return json.loads(content)

    except Exception as e:
        print("❌ LLM ERROR:", str(e))
        return {}