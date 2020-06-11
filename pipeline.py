from Loggeer import log_obj
from models import SpiderDBSession, LocalDBSession


def get_user_list():
    spider_session = SpiderDBSession()
    try:
        select_str = "SELECT  user_id from jrtt_daily_account"
        conn = spider_session.execute(select_str)
        result = conn.fetchall()
        spider_session.commit()
        spider_session.close()
        return result
    except Exception as e:
        spider_session.close()
        log_obj.logger.info(e)


def get_item_id():
    spider_session = LocalDBSession()
    try:
        select_str = "select item_id from jrtt_daily_data where status =0  "
        conn = spider_session.execute(select_str,)
        result = conn.fetchall()
        spider_session.commit()
        spider_session.close()
        return result
    except Exception as e:
        spider_session.close()
        log_obj.logger.info(e)


def update_con(sql):
    spider_session = LocalDBSession()
    try:
        spider_session.execute(sql)
        spider_session.commit()
        spider_session.close()
    except Exception as e:
        spider_session.close()
        log_obj.logger.info(e)
