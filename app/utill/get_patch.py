from app.engines import db
from app.logger import ContextLogger
from app.models.patch import Patch

logger = ContextLogger('task_cnnvd')


def get_patch(title):
    try:
        patch = db.session.query(Patch).filter(Patch.title == title).first()
        return patch
    except Exception as e:
        logger.warning(e)
        return False


if __name__ == '__main__':
    print(get_patch('firefox-3.6.9.tests'))