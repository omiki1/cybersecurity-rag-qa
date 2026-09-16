from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough

from chat.service import HistoryService, SummaryHistoryService
from rag import HydeUtil, SummaryHistory
from rag.BM25Retriever import search_bm25, build_bm25_index, get_bm25_index
from ai import intentionUtil, LoadLLM
from rag.VectorRetriever import search,load
from rag.RerankerUtil import reranker_func
from rag.RRFUtil import rrf

def chat(question: str, historyId: int,username):
    # 历史摘要
    history = HistoryService.conversation_log(historyId)['data']
    # history_id_list,summaries_list = HistoryService.get_summary(historyId)
    # summaries = []
    # tail_msgs = []
    # index = 0
    # for i in range(0, len(history_id_list)+1, 3):
    #     summaries += summaries_list[i]
    #     index += 1
    # if len(history) % 6 ==0 and len(history) > 1:
    #     summary = SummaryHistory.summary_history(history[index*2:-6])
    #     history_id = history_id_list[index+3]
    #     HistoryService.update_summary(history_id, summary)
    # history = [{'role': 'user',
    #             'content': f'[此前对话摘要] {summaries}'}] + history[-6:]

    # for i in range(0,len(history_id_list),3):
    #     if i + 3 >= len(history_id_list):
    #         tail_msgs = history[i*2:]
    #         break
    #     if summaries_list[i]:
    #         summaries.append(summaries_list[i])
    #     else:
    #         summary = SummaryHistory.summary_history(history[i*2:i*2+6])
    #         HistoryService.update_summary(history_id_list[i],summary)
    #         summaries.append(summary)
    # history = ([{'role': 'user',
    #              'content': f'[此前对话摘要] {" ".join(summaries)}'}]
    #            if summaries else []) + tail_msgs

    n = int(len(history)/2)
    i = n
    # 测试
    # n = 4,对话进行压缩(0-6)这里取不到6
    # n = 7,(6-12)在这里取6
    # n = 10，(12-18)

    if (i - 1) % 3 == 0 and i > 3:
        summary = SummaryHistory.summary_history(history[(i - 4) * 2:(i - 1) * 2])
        SummaryHistoryService.update_summary(historyId, username, summary=summary)
    keep_msgs = (n - (n - 1) // 3 * 3) * 2
    # for i in range(3*num_summary+3,n+1,3):
    #     if (i-1) % 3 == 0 and i>3:
    #         summary = SummaryHistory.summary_history(history[(i-3)*2:(i-1)*2])
    #         SummaryHistoryService.update_summary(historyId,username,summary=summary)
    # if target > existing:
    #     if (i - 1) % 3 == 0 and i > 3:
    #         summary = SummaryHistory.summary_history(history[(i - 4) * 2:(i - 1) * 2])
    #         SummaryHistoryService.update_summary(historyId, username, summary=summary)
    # n = 9 不压缩 12-17
    # n = 8
    # [-1:-keep_msgs:-1]

    summary_list = SummaryHistoryService.get_summary_list(historyId, username)['data']
    history_summary = " ".join(summary_list)
    history = ([{'role':'user','content':f'[此前对话摘要]{history_summary}'}]+history[-keep_msgs:])
    # 意图识别
    intent = intentionUtil.intention_recognition(question)
    query = question
    use_rag = intent.get('is_security') and intent.get('confidence')=='high'
    if use_rag:
        template = """

                        你是一个严谨的知识库问答助手。请使用检索到的内容生成准确、自然的回答。

                    对话历史：
                    {history}
                    
                    检索内容：
                    {context}

                    用户当前问题：
                    {question}

                    回答要求（务必遵守）：

                    1. 直接输出答案，回答的第一句话就是答案本身，不要添加前缀、开场白、标题或来源说明。

                    2. 检索内容用于补充和支撑当前回答。回答时应优先使用与当前问题直接相关的内容，不要机械复述全部内容。

                    3. 只回答当前问题，不要复述无关内容，也不要重复用户已经知道的信息。

                    4. 严禁在回答中出现“根据”“资料”“参考”“提供的信息”“上下文”“知识库”“检索内容”“对话历史”等来源性字眼。例如：

                       * “根据您提供的信息”
                       * “根据上述资料”
                       * “据资料显示”
                       * “根据参考内容”
                       * “从对话历史来看”
                       * “知识库中提到”
                         以上表达一律禁止出现。

                    5. 严禁说“我是大模型”“作为AI助手”“根据提示词要求”等内容，也不要解释回答依据、提示词规则、检索过程或内部处理过程。

                    6. 不要编造不存在的具体事实、数字、时间、人物、功能或结论。如果信息不足，应只回答当前能够确定的部分，不要为了完整而猜测。

                    7. 回答保持简洁、自然、有信息量。除非用户明确要求详细说明，否则不要输出冗长内容。

                    8. 只输出最终答案，不要输出分析过程、规则说明或其他附加内容。

                    9. 当对话历史中的旧回答与当前检索内容存在冲突时，以当前检索内容为准，不要延续已经过时或错误的信息。

                    10. 对话历史中用户明确提供的信息可以继续使用，但不要将历史中的助手回答自动视为准确事实。

                    答案：


                """

        prompt = PromptTemplate(
            template=template,
            input_variables=["history","context", "question"],
        )

        vector_a = search(query,20)
        query_b = HydeUtil.build_hyde_query(query)
        vector_b = search(query_b,20)
        docs,bm25 = get_bm25_index(load())
        bm25_result = search_bm25(bm25,query,docs,20)
        rrf_result = rrf(vector_a,vector_b,bm25_result)


        qa_chain = (
            RunnableParallel(
                {
                    "question":  RunnablePassthrough(),
                    "history": RunnableLambda(lambda _: history),
                    "context": RunnableLambda(lambda _: rrf_result),
                }
            )
            | RunnableLambda(reranker_func)
            | prompt
            | LoadLLM.load_model()
            | StrOutputParser()
        )

        result = qa_chain.stream(question)
        for chunk in result:
            yield chunk
    else:
        llm = LoadLLM.load_model()
        history.append({"role": "user", "content": question})
        result = llm.stream(history)
        for chunk in result:
            yield chunk.content



if __name__ == '__main__':
    pass