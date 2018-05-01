from app.utill.req import BaseReq
from app.logger import ContextLogger

logger = ContextLogger('crawl')

req = BaseReq(is_crawl=False)


for ip in ips:
    data = req.get('http://ip.taobao.com/service/getIpInfo.php?ip='+ip.ip)
    data = data['data']
    ip.country = data['country'].replace('XX', '')
    ip.region = data['region'].replace('XX', '')
    ip.city = data['city'].replace('XX', '')
    ip.county = data['county'].replace('XX', '')
    ip.isp = data['isp'].replace('XX', '')
    safe_commit(ip)


