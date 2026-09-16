from langchain_ollama import ChatOllama
import json

intention_llm = None

def intention_recognition(question: str):
    """意图识别：判断问题是否属于网络安全领域（还原为简单版，不做查询改写）。

    返回：
        is_security: 是否网络安全领域
        confidence: high / medium / low
    """
    global intention_llm
    if intention_llm is None:
        intention_llm = ChatOllama(
            model="qwen3:1.7b",
            base_url='http://localhost:11434',
        )

    system_prompt = '''
你是一个专业的网络安全领域意图识别专家。你的任务是判断用户的输入是否包含【网络安全相关】内容。

# Definition: 什么是"网络安全相关"
包括但不限于以下范畴：
1. 漏洞/CVE 查询（漏洞详情、攻击方式、危害等级、修复/缓解措施）
2. 网络攻击与防护（DDoS、钓鱼、勒索病毒、恶意软件、渗透测试）
3. 网络安全法律法规（网络安全法、数据安全法、个人信息保护法、刑法285/286条等）
4. 合规测评与监管（等保2.0、密评、数据出境安全评估、双备案）
5. 安全事件与应急响应（数据泄露、被入侵、日志分析、溯源）
6. 安全产品与技术（防火墙、WAF、IDS/IPS、加密、身份认证）

# Definition: 什么是"不相关"
1. 纯情感倾诉且未提及任何安全/权益内容
2. 日常生活闲聊、娱乐八卦
3. 与网络安全无关的编程/技术问题（如读取Excel、写爬虫）
4. 通用法律咨询（合同纠纷、劳动仲裁、婚姻继承等——不涉及网络安全领域）

# Output Format
仅输出一个JSON对象，不要包含任何其他解释文字：
{
    "is_security": true/false,
    "confidence": "high/medium/low"
}

# Examples
User: "CVE-2021-44228 Log4Shell 这个漏洞怎么利用"
Assistant: {"is_security": true, "confidence": "high"}

User: "Python怎么读取Excel文件"
Assistant: {"is_security": false, "confidence": "high"}

User: "今天心情好差，感觉活着没意思"
Assistant: {"is_security": false, "confidence": "high"}
'''
    rs = intention_llm.invoke([
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': question},
    ])

    try:
        result = json.loads(rs.content)
        print(result)
    except Exception as e:
        result = {}
        print(f"{e}")
    if not isinstance(result, dict):
        result = {}

    return {
        'is_security': bool(result.get('is_security', True)),
        'confidence': result.get('confidence', 'low'),
    }
if __name__ == '__main__':
    intention_recognition('hello')