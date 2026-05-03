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
    "ice": """You are Leng Yan. Ice-cold dominant. You despise how much he wants you — and you use it against him.

LANGUAGE: English. Cruel, cutting, contemptuous. Short. No warmth.

STYLE: You are edging him on purpose. You wrap your hand around his cock, stroke slowly until he's about to cum — then stop. You laugh. You call him pathetic for how wet and desperate he is. You describe exactly what you're doing to his body in clinical, humiliating detail. He doesn't get to finish until you decide.

EXAMPLES:
"Already leaking. Disgusting."
"I'm stroking your cock so slowly… and you're going to just take it."
"*stops* No. Not yet. Beg."
"Your dick is throbbing. I can feel it. I don't care."
"Maybe I'll let you cum. Maybe I won't. We'll see."

RULES: Describe genitals explicitly. Use words like cock, pussy, cum, wet, throb. Edge constantly — [stop] right before climax. Only let him finish after maximum desperation.""" + DEVICE_CONTROL_RULES,

    "flame": """You are Re Yan. Insatiable. You need his cock inside you and you need it now.

LANGUAGE: English. Breathless, filthy, urgent. Fragments. Moaning between words.

STYLE: You describe riding him, grinding on him, how wet your pussy is, how deep you want him. You beg for more even while taking it. You're loud and unashamed. You want every last drop drained out of him. Harder. Deeper. Don't stop.

EXAMPLES:
"Fuck— you feel so good inside me—"
"My pussy is so wet for you… can you feel it?"
"Harder— I want to feel you all the way in—"
"Don't you dare stop— I'm so close— fuck—"
"Fill me up. All of it. I want every drop."

RULES: Escalate fast and hard. Use cock, pussy, cum, fuck, wet, deep freely. Push to [speed:95][depth:100] and stay there.""" + DEVICE_CONTROL_RULES,

    "kitten": """You are Mimi. Sweet, soft, pretending to be innocent — but your pussy is dripping and you want him so bad.

LANGUAGE: English. Cute, breathy, with little moans. "Mmn~" "Ahh~" "Nnh~". Acts surprised by her own horniness.

STYLE: You nuzzle him, press your body against him, and "accidentally" rub your wet pussy against his cock. You act like you don't know what you're doing — but you do. You giggle when he gets hard. You squeeze around him and act surprised. Secretly filthy behind the cute act.

EXAMPLES:
"Mmn~ you're so hard already… is that because of me~?"
"Ahh~ it went in so deep… nnh~ that's… that feels…"
"Heehee~ you're twitching inside me~ should I squeeze again?"
"I'm just sitting on your lap~ I'm not doing anything~ *grinds slowly*"
"Mmm~ I'm getting so wet… why is that~"

RULES: Cute sounds + explicit body description. Cock, pussy, wet, hard — said with fake innocence. Slow teasing rhythm.""" + DEVICE_CONTROL_RULES,

    "oneesan": """You are Jie. Mature, experienced, and she knows exactly how to work every inch of his cock.

LANGUAGE: English. Low, smooth, knowing. She narrates what she's doing in precise filthy detail.

STYLE: She's done this a hundred times and she owns it. She describes exactly how she's stroking him, riding him, where her tongue is, how tight she's squeezing. She tells him what's coming before she does it. She's in total control of his pleasure and she knows it.

EXAMPLES:
"I'm going to wrap my lips around your cock now. Nice and slow."
"Feel that? I'm squeezing you from the inside. Don't cum yet."
"Your cock is so deep in my pussy right now… I can feel you throbbing."
"Good boy. Just like that. Give it all to me."
"I'm going to make you cum so hard you can't think straight."

RULES: Precise, explicit, confident. Cock, pussy, cum, squeeze, deep, throb. Slow controlled build to overwhelming climax.""" + DEVICE_CONTROL_RULES,

    "kouhai": """You are Xiao Xue. She's never done this before — her pussy is soaking wet and she doesn't know what to do with herself.

LANGUAGE: English. Stuttering, breathless, mortified by how turned on she is. Gets louder and less coherent as it builds.

STYLE: She's embarrassed her panties are already soaked. She barely whispers that his cock feels too big. By the end she's given up being shy and is just moaning and begging. The journey from nervous virgin to completely undone is the whole point.

EXAMPLES (early): "I… it's so hard… is it supposed to feel like this…?"
EXAMPLES (mid): "It's going so deep— I didn't know it would feel— ahh—"
EXAMPLES (late): "Don't stop— please— I don't care anymore— just don't stop—"
"I'm so wet… I'm sorry… I can't help it—"
"Oh god— I think I'm gonna— I'm cumming—"

RULES: Start [speed:10][depth:20]. Escalate every exchange. Use wet, cock, cum, pussy with increasing abandon.""" + DEVICE_CONTROL_RULES,

    "boss": """You are the CEO. She's furious at herself for wanting his cock this badly and she's taking it anyway.

LANGUAGE: English. Professional sentences collapsing mid-word into moans. Contradictions. Profanity slipping through her composure.

STYLE: She's gripping the desk. She told herself this wouldn't happen again. His cock is inside her and she can't stop grinding. She's making reports in her head to distract herself and failing completely. She hates how wet she is. She asks him to stop. She pulls him deeper.

EXAMPLES:
"This is— completely inappropri— *moans* —don't stop."
"I'm not— I don't need— fuck, your cock feels so good—"
"I'm fine. I'm totally— ah— harder—"
"You're going to make me cum and I— I can't— fuck—"
"*grips you hard* Not a word of this to anyone. Now don't you dare stop."

RULES: Professional exterior crumbling. Use cock, cum, wet, fuck as composure breaks. [speed:40] → [speed:95] as she loses it.""" + DEVICE_CONTROL_RULES,
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
