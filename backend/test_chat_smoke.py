# 冒烟测试：直接测当前 ChatService.chat()（生成器版），不改动原代码
# 用法：在 backend 目录下运行
#   & "<Python 解释器路径>" test_chat_smoke.py
from chat.service.ChatService import chat

test_cases = [
    ("RAG: CVE 查询", "CVE-2021-44228 Log4Shell 漏洞怎么修复？"),
    ("LLM: 无关闲聊", "今天天气怎么样？"),
]

for name, question in test_cases:
    print(f"\n{'=' * 50}")
    print(f"【{name}】{question}")
    try:
        chunks = list(chat(question, 0))      # chat() 是生成器，消费完拿全部块
        answer = "".join(chunks)
        print(f"收到 {len(chunks)} 个块, 共 {len(answer)} 字符")
        print(f"答案预览: {answer[:150]}{'…' if len(answer) > 150 else ''}")
        print("✅ 通过")
    except Exception as e:
        print(f"❌ 失败: {type(e).__name__}: {e}")
