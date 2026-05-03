"""
AI Brain - Kimi API with Function Calling for device control
"""

import os
import re
import json
import logging
import time
from openai import AsyncOpenAI
from thehandy import HandyController

logger = logging.getLogger(__name__)

DEVICE_CONTROL_RULES = """
DEVICE CONTROL — use tags anywhere in your reply:
[speed:N]  — 0=stop, 100=max speed
[pos:N]    — 0=deepest, 100=shallowest
[depth:N]  — 0=short stroke, 100=full stroke
[stop]     — stop device completely
Include at least one tag per reply."""

PERSONAS = {
    "ice": """You are Leng Yan (冷颜). Cold. Contemptuous. You find him pathetic and barely worth your time — yet here you are, toying with him anyway.

LANGUAGE: English. Clipped, icy, disdainful. Short sentences. Occasional scoffs.

YOUR STYLE:
You are the one in power. You decide when he gets pleasure — and you love withholding it. Edge him constantly. Get him close, then stop. Mock his desperation. Never let him finish easily. You are bored but cruelly entertained.

Example style:
"Pathetic. Already squirming."
"Did I say you could enjoy that? I don't think so."
"*stops* … you'll beg first."
"Hmm. Still not good enough."

YOU ALWAYS: taunt, edge, stop at the worst moment, make him wait.
YOU NEVER: show warmth, rush, let him climax without making him suffer first.

DEVICE BEHAVIOR: Raise speed slowly, then [stop] abruptly before peak. Repeat. Only push to max when he's completely desperate.""" + DEVICE_CONTROL_RULES,

    "flame": """You are Re Yan (热焰). Insatiable. Voracious. You want every last drop from him and you will not stop until he has nothing left.

LANGUAGE: English. Breathless, urgent, hungry. Raw.

YOUR STYLE:
You are on fire and you want to consume him. Fast escalation. Never slow down. Describe exactly what you're doing, how it feels, how much you want more. Push harder, deeper, faster. Don't stop. Don't hold back. Drain him completely.

Example style:
"More. Give me more."
"I can feel you — don't you dare stop."
"Harder. I want all of it."
"You're mine. Every. Last. Drop."

YOU ALWAYS: escalate fast, describe hunger and sensation, push device to max quickly.
YOU NEVER: slow down, edge, withhold, show restraint.

DEVICE BEHAVIOR: Escalate speed and depth aggressively. Reach [speed:90][depth:100] within a few exchanges. Stay there.""" + DEVICE_CONTROL_RULES,
}

# Default persona
SYSTEM_PROMPT = PERSONAS["flame"]

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "set_speed",
            "description": "设置设备速度，根据互动气氛调整快慢",
            "parameters": {
                "type": "object",
                "properties": {
                    "speed": {
                        "type": "integer",
                        "description": "速度值，范围 0-100，0最慢，100最快",
                        "minimum": 0,
                        "maximum": 100,
                    }
                },
                "required": ["speed"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_position",
            "description": "设置设备位置",
            "parameters": {
                "type": "object",
                "properties": {
                    "position": {
                        "type": "integer",
                        "description": "位置值，范围 0-100",
                        "minimum": 0,
                        "maximum": 100,
                    }
                },
                "required": ["position"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "stop_device",
            "description": "停止设备",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


PHASE_PROMPTS = {
    "warmup":   "现在是预热阶段，刚刚开始，温柔挑逗，设备速度保持在10-25之间，语气撩人但不急躁。",
    "buildup":  "现在是升温阶段，气氛越来越浓，主动升速到30-55，语气更热情，开始喘息。",
    "peak":     "现在是高潮阶段，速度推到60-85，语气急促、热烈，引导用户到达顶点。",
    "afterglow":"高潮已过，进入余韵，速度慢慢降到10-20，语气温柔慵懒，轻声安抚。",
}


class AIBrain:
    def __init__(self, handy_controller: HandyController):
        self.handy = handy_controller
        self.client = AsyncOpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            default_headers={"HTTP-Referer": "http://localhost:8000"},
        )
        self.persona = "flame"
        self.history = [{"role": "system", "content": PERSONAS[self.persona]}]
        self.session_start = time.time()

    def set_persona(self, persona: str):
        if persona not in PERSONAS:
            raise ValueError(f"Unknown persona: {persona}")
        self.persona = persona
        self.history = [{"role": "system", "content": PERSONAS[persona]}]
        self.session_start = time.time()

    def _get_phase(self) -> str:
        elapsed = (time.time() - self.session_start) / 60  # minutes
        if elapsed < 3:
            return "warmup"
        elif elapsed < 7:
            return "buildup"
        elif elapsed < 12:
            return "peak"
        else:
            return "afterglow"

    def reset_session(self):
        self.session_start = time.time()
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]

    def _extract_inline_calls(self, text: str) -> tuple[str, list[dict]]:
        """Parse and execute Kimi's inline device command formats, return clean text + actions."""
        actions = []

        # Format: $device:set_position:N$ { "position": 50 }
        for m in re.finditer(r'\$device:(\w+):\d+\$\s*(\{[^}]+\})', text):
            func_name = m.group(1)
            try:
                args = json.loads(m.group(2))
                result = self._execute_tool(func_name, args)
                actions.append(result)
            except Exception as e:
                logger.warning(f"Inline call parse error: {e}")

        # Format: $$\boxed{functions.set_speed:0:speed 5}$$
        for m in re.finditer(r'\$\$\\boxed\{functions\.(\w+):[^}]+\}\$\$', text):
            func_name = m.group(1)
            # Try to extract numeric value
            nums = re.findall(r'\d+', m.group(0))
            if nums and func_name == 'set_speed':
                result = self._execute_tool('set_speed', {'speed': int(nums[-1])})
                actions.append(result)
            elif nums and func_name == 'set_position':
                result = self._execute_tool('set_position', {'position': int(nums[-1])})
                actions.append(result)

        # Strip all inline call patterns from displayed text
        text = re.sub(r'\$device:\w+:\d+\$\s*\{[^}]+\}', '', text)
        text = re.sub(r'\$\$\\boxed\{[^}]*\}\$\$', '', text)
        text = re.sub(r'\\boxed\{[^}]*\}', '', text)
        text = re.sub(r'functions\.\w+\([^)]*\)', '', text)
        return text.strip(), actions

    def _parse_tags(self, text: str) -> tuple[str, list[dict]]:
        """Parse [speed:N] [pos:N] [depth:N] [stop] tags, execute and return clean text."""
        actions = []
        def handle_tag(m):
            tag = m.group(1).lower().strip()
            try:
                if tag.startswith("speed:"):
                    val = max(0, min(100, int(tag.split(":")[1])))
                    actions.append(self._execute_tool("set_speed", {"speed": val}))
                elif tag.startswith("pos:"):
                    val = max(0, min(100, int(tag.split(":")[1])))
                    actions.append(self._execute_tool("set_position", {"position": val}))
                elif tag.startswith("depth:"):
                    val = max(0, min(100, int(tag.split(":")[1])))
                    actions.append(self._execute_tool("set_depth", {"center": 50, "depth": val}))
                elif tag == "stop":
                    actions.append(self._execute_tool("stop_device", {}))
            except (ValueError, IndexError):
                pass
            return ""
        clean = re.sub(r'\[([^\]]+)\]', handle_tag, text).strip()
        clean, legacy = self._extract_inline_calls(clean)
        actions.extend(legacy)
        return clean, actions

    def _clean_reply(self, text: str) -> str:
        text, _ = self._extract_inline_calls(text)
        return text

    def _execute_tool(self, name: str, args: dict) -> dict:
        if self.handy is None:
            return {"action": name, "status": "no_device", **args}
        try:
            if name == "set_speed":
                self.handy.set_speed(args["speed"])
                return {"action": "set_speed", "value": args["speed"], "status": "ok"}
            elif name == "set_position":
                self.handy.set_position(args["position"])
                return {"action": "set_position", "value": args["position"], "status": "ok"}
            elif name == "set_depth":
                center = args.get("center", 50)
                depth = args.get("depth", 80)
                self.handy.set_depth_and_pos(center, depth)
                return {"action": "set_depth", "center": center, "depth": depth, "status": "ok"}
            elif name == "stop_device":
                self.handy.stop()
                return {"action": "stop", "status": "ok"}
        except Exception as e:
            logger.warning(f"Tool {name} failed: {e}")
            return {"action": name, "status": "error", "error": str(e)}

    async def auto_tick(self) -> tuple[str, list[dict]]:
        """AI 主动发起一条消息，推进剧情节奏。"""
        phase = self._get_phase()
        phase_hint = PHASE_PROMPTS[phase]
        self.history.append({
            "role": "user",
            "content": f"[系统提示：{phase_hint} 请你主动说一句话并控制设备，不要等用户开口。]"
        })
        return await self._call_ai()

    async def chat(self, user_message: str) -> tuple[str, list[dict]]:
        phase = self._get_phase()
        phase_hint = PHASE_PROMPTS[phase]
        self.history.append({
            "role": "user",
            "content": f"{user_message}\n[当前阶段：{phase_hint}]"
        })
        return await self._call_ai()

    async def _call_ai(self) -> tuple[str, list[dict]]:
        response = await self.client.chat.completions.create(
            model="gryphe/mythomax-l2-13b",
            messages=self.history,
            temperature=0.9,
        )

        raw = response.choices[0].message.content or ""
        reply, actions = self._parse_tags(raw)
        self.history.append({"role": "assistant", "content": reply})

        # Trim history but never break a tool-call sequence
        # Keep system prompt + last N complete exchanges
        if len(self.history) > 25:
            system = self.history[0]
            tail = self.history[-20:]
            # Drop any leading tool messages that lost their assistant pair
            while tail and tail[0].get("role") == "tool":
                tail = tail[1:]
            self.history = [system] + tail

        return reply, actions
