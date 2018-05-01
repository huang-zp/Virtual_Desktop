import requests
from app.engines import db
from app.logger import ContextLogger


class BaseReq:
    def __init__(self, is_crawl=True):
        self.ses = db.session
        self.is_crawl = is_crawl
        self.logger = ContextLogger('crawl')

    def _request(self, url, method='post', timeout=20, retry=5, **kwargs):
        if kwargs.get('headers'):
            headers = kwargs['headers']
        else:
            headers = {}
        if kwargs.get('cookies'):
            cookies = kwargs['cookies']
        else:
            cookies = {}

        try:
            resp = requests.request(method, '{}'.format(url), timeout=timeout, headers=headers,
                                    cookies=cookies, **kwargs)
        except Exception as e:
            self.logger.warning(e)
            if retry > 0:
                return self._request(url, method, timeout, retry=retry-1, **kwargs)
            else:
                return None
        if resp.status_code != 200 and retry > 0:
            return self._request(url, method, timeout, retry=retry-1, **kwargs)
        if self.is_crawl:
            return resp.text
        else:
            try:
                data = resp.json()
            except Exception as e:
                self.logger.warning(e)
                data = None
            return data

    def get(self, url, **kwargs):
        return self._request(url, method='get', **kwargs)

    def post(self, url, **kwargs):
        return self._request(url, method='post', **kwargs)

