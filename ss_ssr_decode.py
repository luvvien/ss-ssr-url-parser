#!/usr/bin/python
# -*- coding: UTF-8 -*-

import base64

__author__ = 'Vien'

'''
A method of decoding ss url and ssr url.
'''


def fill(b64):
    return b64 + "=" * (4 - len(b64) % 4)


def clear_ssr(deb64):
    pos = deb64.rfind('/')
    return deb64[:pos] if pos > 0 else deb64


def clear_ss(deb64):
    pos = deb64.rfind('#')
    return deb64[:pos] if pos > 0 else deb64


def ssr_parse(txt):
    # ssr://server:port:protocol:method:obfs:password_base64/?params_base64
    conf = clear_ssr(bytes.decode(base64.urlsafe_b64decode(fill(txt)))).split(':')
    conf_dict = dict()
    conf_dict["ip"] = conf[0]
    conf_dict["port"] = conf[1]
    conf_dict["protocol"] = conf[2]
    conf_dict["method"] = conf[3]
    conf_dict["obfs"] = conf[4]
    conf_dict["password"] = clear_ssr(bytes.decode(base64.urlsafe_b64decode(fill(conf[5]))))
    return conf_dict


def ss_parse(txt):
    # method:password@server:port
    conf = clear_ss(bytes.decode(base64.urlsafe_b64decode(fill(txt))))
    conf_list = []
    for part in conf.split('@'):
        conf_list += part.split(':')
    conf_dict = dict()
    conf_dict["method"] = conf_list[0]
    conf_dict["password"] = conf_list[1]
    conf_dict["ip"] = conf_list[2]
    conf_dict["port"] = conf_list[3]
    return conf_dict


def parse(txt):
    if 'ssr://' in txt:
        return ssr_parse(txt.replace('ssr://', ''))
    if 'ss://' in txt:
        return ss_parse(txt.replace('ss://', ''))
    raise Exception('ss url or ssr url format error.')


if __name__ == '__main__':
    print(parse('ss://YWVzLTEyOC1jdHI6dmllbmNvZGluZy5jb21AMTUyLjg5LjIwOC4xNDY6MjMzMw'))
    print(parse('ssr://MTUyLjg5LjIwOC4xNDY6MjMzMzphdXRoX3NoYTFfdjQ6YWVzLTEyOC1jdHI6cGxhaW46ZG1sbGJtTnZaR2x1Wnk1amIyMA'))
