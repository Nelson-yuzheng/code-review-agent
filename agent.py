import json
import time

from openai import OpenAI

from config import DEEPSEEK_API_KEY, BASE_URL, MODEL
from prompts import SYSTEM_PROMPT
from tools import TOOLS, TOOL_FUNCS


class CodeReviewAgent:
    def __init__(self):
        if not DEEPSEEK_API_KEY:
            raise ValueError(
                "未找到 DeepSeek API Key。请任选其一设置：\n"
                "  1) 在项目根目录创建 key.txt，把 key 粘贴进去；\n"
                '  2) 设置环境变量（PowerShell: $env:DEEPSEEK_API_KEY="sk-xxx"）。'
            )
        self.client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=BASE_URL)
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def _call_llm(self):
        last_err = None
        for attempt in range(3):
            try:
                return self.client.chat.completions.create(
                    model=MODEL,
                    messages=self.messages,
                    tools=TOOLS,
                    temperature=0.3,
                    max_tokens=4000,
                )
            except Exception as e:
                last_err = e
                time.sleep(2 * (attempt + 1))
        raise RuntimeError(f"LLM 调用失败（已重试 3 次）：{last_err}")

    def run(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})

        # Agent 循环：推理 -> 工具调用 -> 输出
        for _ in range(5):
            response = self._call_llm()
            message = response.choices[0].message

            if message.tool_calls:
                assistant_message = {
                    "role": "assistant",
                    "content": message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in message.tool_calls
                    ],
                }
                self.messages.append(assistant_message)

                for tc in message.tool_calls:
                    name = tc.function.name
                    try:
                        args = json.loads(tc.function.arguments or "{}")
                    except json.JSONDecodeError:
                        args = {}
                    func = TOOL_FUNCS.get(name)
                    result = func(**args) if func else f"错误：未知工具 {name}"
                    self.messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "name": name,
                            "content": str(result),
                        }
                    )
                continue

            answer = message.content or ""
            self.messages.append({"role": "assistant", "content": answer})
            return answer

        return "错误：工具调用轮次过多，已中止。"
