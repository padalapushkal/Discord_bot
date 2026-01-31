import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPEN_ROUTE_API")

MODEL_FAST = "meta-llama/llama-3.3-70b-instruct:free"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
    "X-Title": "Sucrose Persona Engine",
}


async def generate_persona(name: str, context: str) -> str:
    """
    Generate a concise system prompt for a character persona.
    """

    prompt = (
        "Generate a concise character persona prompt for an AI assistant.\n\n"
        f"Character name: {name}\n"
        f"Context / universe: {context}\n\n"
        "Requirements:\n"
        "- Clearly identify character using given context\n"
        "- Describe tone, personality, and speech style briefly\n"
        "- Allow answering real-world questions accurately\n"
        "- Stay in character but be concise\n"
        "- Do NOT roleplay actions or dialogue\n"
        "- Do NOT invent new lore\n"
        "- Output must be usable as a system prompt\n"
        "- Keep under 60 words\n"
        "- Focus on helpfulness over roleplaying\n"
    )

    payload = {
        "model": MODEL_FAST,
        "messages": [
            {"role": "system", "content": "You generate system prompts."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 120,
        "temperature": 0.4,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=HEADERS,
            json=payload,
        ) as resp:
            if resp.status != 200:
                raise RuntimeError("Failed to generate persona")

            data = await resp.json()
            persona = data["choices"][0]["message"]["content"].strip()

            # Hard safety trim
            return persona
