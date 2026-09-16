from ai import LoadLLM2

HYDE_SYSTEM_PROMPT = """你是网络安全知识库的检索助手。请根据用户的问题，写一段 100~200 字的"假设性文档"，
模拟知识库中可能收录的相关条目（法条原文、漏洞描述、处置建议、合规要求等）。
要求：
1. 使用正式、书面化的表述，贴近法条/技术文档的文体；
2. 只输出假设文档内容本身，不要任何解释、标题或前缀；
3. 内容要与问题相关，不要编造具体编号（如不知道编号就不要写 CVE-XXXX）。
"""

def build_hyde_query(question: str):
    llm = LoadLLM2.load_model()
    rs = llm.bind(max_tokens=300).invoke([
        {'role': 'system', 'content': HYDE_SYSTEM_PROMPT},
        {'role': 'user', 'content': f'用户问题：{question}\n假设文档：'},
    ])
    doc = rs.content.strip()
    return doc if doc else question