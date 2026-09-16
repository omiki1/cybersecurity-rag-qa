MAX_SUMMARY_LEN = 300    # 摘要硬截断
from ai.LoadLLM2 import load_model as load_glm
def summary_history(history_list):
    history_content = []
    llm = load_glm()
    for history in history_list:
        role = history['role']
        history_content.append(f"{role}:{history['content']}")
    raw = "\n".join(history_content)
    raw = raw[-3500:]

    prompt = f"""你是对话历史压缩助手。下面是一段用户与助手的多轮对话记录，请把它压缩成简洁的摘要，供后续对话作为上下文使用。

    输出格式：3~6 个要点，每点一行，以"- "开头，不要写开头语。

    规则：
    1. 合并同类信息，不要逐条复述对话；
    2. 数字、价格、期限、结论等关键事实必须保留；
    3. 丢弃客套话和已解决的细节过程；
    4. 总字数 200 字以内。

    对话记录：
    {raw}

    摘要："""
    rs = llm.bind(temperature=0.2, max_tokens=300).invoke(
        [{'role': 'user', 'content': prompt}]
    )
    return rs.content.strip()[:MAX_SUMMARY_LEN]