import os
import subprocess


def read_file(path: str) -> str:
    if not os.path.exists(path):
        return f"错误：文件不存在：{path}"
    if os.path.isdir(path):
        return f"错误：{path} 是一个目录，请指定具体文件路径。"
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception as e:
        return f"错误：读取文件失败：{e}"
    return f"文件 {path} 的内容如下：\n```\n{content}\n```"


def run_linter(path: str) -> str:
    if not os.path.exists(path):
        return f"错误：文件不存在：{path}"
    try:
        result = subprocess.run(
            ["pylint", path],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
    except FileNotFoundError:
        return "错误：未安装 pylint，请先运行：pip install pylint"
    output = (result.stdout + result.stderr).strip()
    if not output:
        return "pylint 未发现问题（或没有输出）。"
    return f"pylint 静态检查结果：\n```\n{output}\n```"


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "读取本地文件内容。当用户给出文件路径，或需要查看某个文件的代码时调用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "文件的绝对或相对路径",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_linter",
            "description": "使用 pylint 对指定文件做静态检查，返回代码质量报告。当用户询问代码质量，或需要客观的静态检查结果时调用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "要检查的文件路径",
                    }
                },
                "required": ["path"],
            },
        },
    },
]

TOOL_FUNCS = {
    "read_file": read_file,
    "run_linter": run_linter,
}
