# 设计文档（Design.md）

## 1. 整体架构

本项目实现一个**代码审查 Agent**，采用经典的 Agent 循环：

```
用户输入 → 推理(LLM) → 需要工具? → 工具调用(read_file / run_linter) → 汇总 → 输出审查报告
                  ↑                                                      │
                  └──────────────── 多轮循环（最多 5 轮）───────────────┘
```

## 2. 模块说明

| 模块 | 职责 |
|------|------|
| `main.py` | 命令行交互入口，接收用户输入、打印结果 |
| `agent.py` | `CodeReviewAgent` 类：维护对话历史、调用 LLM、处理工具调用循环 |
| `tools.py` | 工具注册（`TOOLS` 元数据）与具体实现（`read_file`、`run_linter`） |
| `prompts.py` | 系统提示词，定义 Agent 的角色、审查要点与输出格式 |
| `config.py` | 从环境变量或 `key.txt` 读取 API Key，集中配置模型与地址 |

## 3. Prompt 设计

系统提示词明确三部分内容：

1. **角色设定**：专业的代码审查 Agent
2. **工具说明**：告知模型何时调用 `read_file` / `run_linter`
3. **审查维度与输出格式**：正确性、可读性、可维护性、性能、安全性；要求输出「总体评价 / 问题清单 / 改进建议」三段式 Markdown

## 4. 工具设计

采用 OpenAI 兼容的 Function Calling 机制：

- `read_file(path)`：读取本地文件内容，解决「粘贴代码太长」的问题
- `run_linter(path)`：调用 pylint 做静态检查，让审查意见有客观依据（体现 LLM 与工具协同）

## 5. 关键机制

- **上下文记忆**：`self.messages` 保存完整对话历史，支持多轮追问
- **错误处理与重试**：`_call_llm` 失败后指数退避重试（2s / 4s / 6s，共 3 次）
- **循环上限**：工具调用最多 5 轮，防止死循环

## 6. 技术选型理由

- 未使用 LangChain 等框架，改用 **OpenAI 原生 API + Function Calling**，代码更短、更易理解，同样满足「LLM 原生 API」要求
- 选择 DeepSeek 是因为其提供 OpenAI 兼容接口，可直接用 `openai` SDK 调用
- 选择 pylint 作为静态检查工具，生态成熟、输出信息丰富，便于 LLM 解读
