# 代码审查 Agent（Code Review Agent）

一个基于 DeepSeek 大模型的代码审查助手，是「Homework 1」的作业实现。它能分析代码质量、发现潜在 Bug、给出改进建议，并支持调用工具（读取文件、运行 pylint 静态检查）。

## 功能特性

- **代码审查**：分析正确性、可读性、可维护性、性能、安全性
- **工具集成**：
  - `read_file`：读取本地文件内容
  - `run_linter`：调用 pylint 做静态检查，结合客观结果给出审查意见
- **Agent 循环**：输入 → 推理 → 工具调用 → 输出
- **上下文记忆**：支持多轮对话，可基于上一轮结果继续追问
- **错误处理与重试**：LLM 调用失败自动重试（最多 3 次）
- **命令行交互**：简单易用

## 目录结构

```
code-review-agent/
├── main.py         # 入口：命令行交互
├── agent.py        # Agent 核心：LLM 调用 + 工具循环
├── tools.py        # 工具：read_file / run_linter
├── prompts.py      # 系统提示词（Prompt 设计）
├── config.py       # 配置：读取 API Key、模型、地址
├── requirements.txt
├── README.md
└── Design.md
```

## 快速开始

### 1. 安装依赖

```powershell
pip install -r requirements.txt
```

### 2. 配置 API Key（二选一）

**方式 A（推荐）**：在项目根目录新建 `key.txt`，把你的 DeepSeek Key 粘贴进去。

**方式 B**：设置环境变量

```powershell
$env:DEEPSEEK_API_KEY="sk-你的key"
```

> `key.txt` 已被加入 `.gitignore`，不会上传到 GitHub，请放心。

### 3. 运行

```powershell
python main.py
```

### 4. 使用示例

```
你> 请审查下面这段代码：
def divide(a, b):
    return a / b
```

```
你> 读取 D:\test\demo.py 并审查它
```

```
你> 检查一下 agent.py 的代码质量
```

输入 `exit` 退出。

## 技术栈

- 语言：Python
- LLM：DeepSeek（OpenAI 兼容接口）
- 框架：OpenAI 原生 API（未使用 LangChain）
- 静态检查：pylint
