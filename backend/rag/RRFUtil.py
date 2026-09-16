def rrf(vector_a: list, vector_b,bm25_result: list):
    scores_dict = {}
    docs_dict = {}
    for index,item in enumerate(vector_a,start=1):
        scores_dict[item.id] = scores_dict.get(item.id,0)+round(1/(60+index),7)
        docs_dict[item.id] = item
    for index,item in enumerate(vector_b,start=1):
        scores_dict[item.id] = scores_dict.get(item.id,0)+round(0.7/(60+index),7)
        docs_dict[item.id] = item
    for index,item in enumerate(bm25_result,start=1):
        scores_dict[item.id] = scores_dict.get(item.id,0)+round(1/(60+index),7)
        docs_dict[item.id] = item
    rrf_sort_idx = sorted(scores_dict.items(),key = lambda items:items[1] ,reverse=True)[:30]
    result = [docs_dict[doc[0]] for doc in rrf_sort_idx]
    return result
