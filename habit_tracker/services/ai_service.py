"""
AI Behavioral Coach Service
Uses an LLM (OpenAI or local) to analyze habits, chat, and predict drop-off.
"""

import os
import json
from datetime import date, timedelta
from typing import List, Dict, Optional, AsyncGenerator

from dotenv import load_dotenv
from openai import AsyncOpenAI

# Lê o arquivo .env (se existir) para que OPENAI_API_KEY e as demais variáveis funcionem
load_dotenv()

# ── Client factory ────────────────────────────────────────────────────────────

def _get_client() -> AsyncOpenAI:
    api_key = os.getenv("OPENAI_API_KEY", "")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")  # swap for Ollama
    return AsyncOpenAI(api_key=api_key, base_url=base_url)


MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = """You are an expert behavioral coach specialized in habit formation.
You use the habit-loop framework (Cue, Routine, Reward) and positive psychology.
Provide concise, encouraging, actionable advice tailored to the user's habits and data.
Keep responses under 150 words unless the user explicitly asks for more detail.
Use a warm, motivational tone. Never be condescending."""


# ── Chat ─────────────────────────────────────────────────────────────────────

async def stream_coach_response(
    history: List[Dict[str, str]],
    user_message: str,
    habit_context: Optional[str] = None,
) -> AsyncGenerator[str, None]:
    """
    Stream the coach's reply token by token.
    `history` is a list of {"role": ..., "content": ...} dicts.
    `habit_context` is a JSON summary of the user's habit stats injected as system context.
    """
    client = _get_client()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if habit_context:
        messages.append({
            "role": "system",
            "content": f"User's current habit data:\n{habit_context}",
        })

    messages.extend(history[-10:])  # keep last 10 exchanges for context window
    messages.append({"role": "user", "content": user_message})

    stream = await client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True,
        max_tokens=300,
        temperature=0.7,
    )

    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


# ── Pattern Analysis ──────────────────────────────────────────────────────────

async def analyze_patterns(habit_stats: Dict) -> str:
    """
    Send a structured summary of habit completions to the LLM and get insights.
    Returns full response text (non-streaming).
    """
    client = _get_client()
    prompt = (
        "Analyze the following habit tracking data and provide 3 concise, "
        "actionable insights. Identify patterns, risks of drop-off, and one "
        "specific intervention suggestion.\n\n"
        f"Data:\n{json.dumps(habit_stats, indent=2)}"
    )

    response = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        max_tokens=400,
        temperature=0.5,
    )
    return response.choices[0].message.content or ""


# ── Predictive Intervention ────────────────────────────────────────────────────

async def predict_dropout_risk(completion_rates: Dict[str, float]) -> List[str]:
    """
    Given a dict of {habit_name: completion_rate_last_7_days},
    return a list of habit names predicted to be at risk of dropout.
    """
    client = _get_client()
    prompt = (
        "Given these 7-day completion rates (0.0–1.0), list only the habit names "
        "that are at HIGH risk of dropout (rate < 0.5). Output a JSON array of strings.\n\n"
        f"{json.dumps(completion_rates, indent=2)}"
    )

    response = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a data analyst. Respond only with valid JSON."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=100,
        temperature=0.0,
    )
    raw = response.choices[0].message.content or "[]"
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return []


# ── Context builder ───────────────────────────────────────────────────────────

def build_habit_context(
    habits: list,
    streaks: Dict[str, int],
    completion_rates: Dict[str, float],
    total_xp: int,
    level: int,
    streak_days: int,
) -> str:
    """Serialize habit state into a compact string for LLM context."""
    data = {
        "level": level,
        "total_xp": total_xp,
        "global_streak_days": streak_days,
        "habits": [
            {
                "name": h.name,
                "cue": h.cue,
                "routine": h.routine,
                "reward": h.reward,
                "streak": streaks.get(h.name, 0),
                "30d_completion_rate": round(completion_rates.get(h.name, 0.0), 2),
            }
            for h in habits
        ],
    }
    return json.dumps(data, indent=2)
