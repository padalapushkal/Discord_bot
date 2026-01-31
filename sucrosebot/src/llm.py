import os
import aiohttp
from dotenv import load_dotenv

from personas import get_persona, set_persona
from persona_llm import generate_persona
from utils.normalize_key import normalize_key

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPEN_ROUTE_API")

# ❗ Models left EXACTLY as you requested
MODEL_SLOW = "meta-llama/llama-3.3-70b-instruct:free"
MODEL_FAST = "meta-llama/llama-3.3-70b-instruct:free"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
    "X-Title": "Sucrose Discord Bot",
}


async def ask_llm(
    prompt: str,
    persona: str,
    context: str | None = None,
    fast: bool = False,
) -> str:
    """
    Ask the LLM using a dynamically generated persona.
    Persona is auto-created on first use and cached.
    """

    # 1️⃣ Normalize inputs
    persona_key = normalize_key(persona)
    context_key = normalize_key(context) if context else "fictional character"

    # 2️⃣ Fetch cached persona (if exists)
    data = get_persona(persona_key)

    if not data:
        try:
            # 3️⃣ Generate persona ONCE (lazy creation)
            persona_prompt = await generate_persona(
                persona_key,
                context_key
            )
            set_persona(persona_key, context_key, persona_prompt)
            system_prompt = persona_prompt
        except Exception:
            # 4️⃣ Safe fallback
            system_prompt = (
                "You are a helpful assistant. "
                "Answer clearly and concisely."
            )
    else:
        system_prompt = data["prompt"]

    # 5️⃣ Build OpenRouter payload
    payload = {
        "model": MODEL_FAST if fast else MODEL_SLOW,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 200,
        "temperature": 0.6,
    }

    # 6️⃣ Call OpenRouter
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=HEADERS,
            json=payload,
        ) as resp:
            if resp.status != 200:
                return "Sorry traveller, my notes are unavailable."

            data = await resp.json()
            return data["choices"][0]["message"]["content"]
