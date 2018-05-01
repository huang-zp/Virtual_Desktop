from app.engines import db
from app.models import Show
from datetime import datetime, timedelta
from app.logger import ContextLogger

logger = ContextLogger('show')


def calc_ip_show_update_count(count):
    format_time = datetime.now().strftime("%Y-%m-%d")
    show = db.session.query(Show).filter_by(format_time=format_time, type='ip').first()
    if show:
        show.update_of_count = show.update_of_count + count
    else:
        try:
            show = Show()
            show.type = 'ip'
            show.update_of_count = count
        except Exception as e:
            logger.warning("计算展示数据更新次数出错"+str(e))

    safe_commit(show)


def calc_domain_show_update_count(count):
    format_time = datetime.now().strftime("%Y-%m-%d")
    show = db.session.query(Show).filter_by(format_time=format_time, type='domain').first()
    if show:
        show.update_of_count = show.update_of_count + count
    else:
        try:
            show = Show()
            show.type = 'domain'
            show.update_of_count = count
        except Exception as e:
            logger.warning("计算展示数据更新次数出错"+str(e))

    safe_commit(show)


def safe_commit(show):
    try:
        db.session.add(show)
        db.session.commit()
        logger.info('计算展示中更新数据：', show.format_time, ':',  show.type)
    except Exception as e:
        logger.warning(e)
        db.session.rollback()
