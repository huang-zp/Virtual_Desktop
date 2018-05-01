#!/usr/bin/env python
# encoding:utf8
# author: zeping lai
import dns.resolver


def GetArecordIp(domain_name):
    '''
     域名解析主机A记录
    :param domain_name: 输入要要解析的域名,例: www.qq.com
    :return: 如果是A记录则返回解析到的ip地址,不是A记录则返回False
    '''''
    address = []
    try:
        host_a = dns.resolver.query(domain_name, 'A')
        for i in host_a.response.answer:
            for j in i.items:
                address.append(j.address)
        return address
    except Exception as e:
        return False


if __name__ == '__main__':
    print(GetArecordIp('socmap.org'))

