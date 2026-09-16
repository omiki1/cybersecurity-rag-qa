from chat.dao import HistorySummaryDao

def get_summary_list(history_id,username):
    result = HistorySummaryDao.get_summary(history_id,username)['data']
    summary_list = []
    if result:
        for summary in result:
            summary_list.append(summary['summary'])
    return {
        "code": 200,
        "data": summary_list,
        "msg": "success",
    }
def update_summary(history_id,username,summary):
    rs = HistorySummaryDao.update_summary(history_id,username,summary)
    if rs:
        return rs
