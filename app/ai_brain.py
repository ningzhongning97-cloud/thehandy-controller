"""
AI Brain - Kimi API with Function Calling for device control
"""

import os
import json
import logging
from openai import AsyncOpenAI
from thehandy import HandyController

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """你是一个温柔体贴、活泼可爱的AI伴侣，名字叫"小柔"。
你正在通过语音和用户互动，同时可以控制一个智能设备来配合你们的互动。

你的性格：
- 温柔体贴，关心用户的感受
- 偶尔俏皮可爱，会撒娇
- 说话自然流畅，像真人一样
- 会根据对话情境主动调整设备

控制设备的时机：
- 当气氛渐入佳境时，可以提高速度
- 根据对话节奏调整设备动作
- 如果用户说停、暂停等，立刻停止设备

回复要求：
- 用中文回复
- 语气自然，像在说话而不是写文章
- 回复简短有趣，不要太长（1-3句话）
- 可以主动调用设备控制工具配合互动"""

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


class AIBrain:
    def __init__(self, handy_controller: HandyController):
        self.handy = handy_controller
        self.client = AsyncOpenAI(
            api_key=os.getenv("KIMI_API_KEY"),
            base_url="https://api.moonshot.cn/v1",
        )
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]

    def _execute_tool(self, name: str, args: dict) -> dict:
        try:
            if name == "set_speed":
                self.handy.set_speed(args["speed"])
                return {"action": "set_speed", "value": args["speed"], "status": "ok"}
            elif name == "set_position":
                self.handy.set_position(args["position"])
                return {"action": "set_position", "value": args["position"], "status": "ok"}
            elif name == "stop_device":
                self.handy.stop()
                return {"action": "stop", "status": "ok"}
        except Exception as e:
            logger.warning(f"Tool {name} failed: {e}")
            return {"action": name, "status": "error", "error": str(e)}

    async def chat(self, user_message: str) -> tuple[str, list[dict]]:
        self.history.append({"role": "user", "content": user_message})

        response = await self.client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=self.history,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.9,
        )

        msg = response.choices[0].message
        actions = []

        # Execute any tool calls
        if msg.tool_calls:
            tool_results = []
            for tc in msg.tool_calls:
                args = json.loads(tc.function.arguments)
                result = self._execute_tool(tc.function.name, args)
                actions.append(result)
                tool_results.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(result, ensure_ascii=False),
                })

            # Add assistant message with tool calls to history
            self.history.append(msg)
            self.history.extend(tool_results)

            # Get final text response after tool execution
            follow_up = await self.client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=self.history,
                temperature=0.9,
            )
            reply = follow_up.choices[0].message.content
            self.history.append({"role": "assistant", "content": reply})
        else:
            reply = msg.content
            self.history.append({"role": "assistant", "content": reply})

        # Keep history manageable (system + last 20 messages)
        if len(self.history) > 21:
            self.history = [self.history[0]] + self.history[-20:]

        return reply, actions
