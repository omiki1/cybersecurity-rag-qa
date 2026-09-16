from chat.dao import HistoryDao, ChatDao
from chat.entity.ConversationResultEntity import ConversationResultEntity
def query_history_menu(username):
    data_list = []
    results =  HistoryDao.query_history_menu(username)
    for item in results:
        data_list.append({
            "historyId": item['history_id'],
            "title": item['question'],
            "time": item['create_time'].strftime('%Y-%m-%d %H:%M:%S'),
            "action": "false",
        })
    return {
        "code": 200,
        "data": data_list,
        "msg": "success",
    }
def conversation_log(historyId):
    data_list = []
    results = HistoryDao.conversation_log(historyId)
    for item in results:
        data_list.append(
            {'role':'user','content':item['question']}
        )
        data_list.append(
            {'role':'assistant','content':item['answer']}
        )
    return {
        "code": 200,
        "data": data_list,
        "msg": "success",
    }
def deleteConversation(historyId):
    HistoryDao.conversation_delete(historyId)
    return {
        "code": 200,
        "data": 1,
        "msg": "success",
    }
def save_conversation_result(conversationResultEntity:ConversationResultEntity):
    question = conversationResultEntity.question
    parent_id = conversationResultEntity.parentId
    answer = conversationResultEntity.answer
    username = conversationResultEntity.username
    history_id = ChatDao.save_conversation_result(question, username,parent_id, answer)
    if history_id:
        return {
            'code':200,
            'msg':"成功保存",
            'data':history_id
        }
    else:
        return {
            'code':400,
            'msg':'保存失败',
            'data':None
        }
def get_summary(historyId):
    history_id_list = []
    summaries = []
    results = HistoryDao.conversation_log(historyId)
    for item in results:
        history_id_list.append(item['history_id'])
        summaries.append(item['summary'])
    return history_id_list,summaries

def update_summary(historyId:int,summary: str):
    HistoryDao.update_summary(historyId, summary)


