from app.engines import db
from app.models import Patch, Vulner
from app.logger import ContextLogger

logger = ContextLogger('task')


def switch_id(patch):
    if patch == '暂无':
        return 0
    else:
        patch_ids = ''

        for key, value in patch.items():

            try:
                patch_id = db.session.query(Patch.id).filter_by(title=key).first()
                if patch_id:
                    patch_ids += str(patch_id)
            except Exception as e:
                logger.warning('补丁:{0}查询报错'.format(patch)+str(e))
        return patch_ids


if __name__ == '__main__':
    patch = db.session.query(Vulner.patch).filter_by(id=5555).first()[0]
    print(switch_id(patch))
