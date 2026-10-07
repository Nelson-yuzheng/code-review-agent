from agent import CodeReviewAgent


def main():
    print("=" * 52)
    print("  代码审查 Agent (Code Review Agent)")
    print("  用法：直接粘贴代码，或输入文件路径开始审查")
    print("  输入 exit / quit / 退出 结束程序")
    print("=" * 52)

    try:
        agent = CodeReviewAgent()
    except ValueError as e:
        print(f"\n启动失败：{e}")
        return

    while True:
        try:
            user_input = input("\n你> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "退出"):
            print("再见！")
            break

        print("\nAgent 思考中...\n")
        answer = agent.run(user_input)
        print(f"Agent>\n{answer}")


if __name__ == "__main__":
    main()
