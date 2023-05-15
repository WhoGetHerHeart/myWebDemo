import json
import time

import requests

import config
import testip

sou = []
re_sou = []
pai = []
sou_data = []
pai_data = []
search_key = ''
send_config = {}


def get_key():
    global re_sou
    ua_arr = open(config.sou_suo, 'r', encoding='utf8')
    content = ua_arr.read()
    re_sou = json.loads(content)['data']


def get_pai():
    global pai
    ua_arr = open(config.fou_ci, 'r', encoding='utf8')
    content = ua_arr.read()
    pai = json.loads(content)['data']


def check_pai(e):
    global pai
    for index in pai:
        if index in e or len(e) <= 4:
            return False
    return True


def get_ip():
    global send_config
    send_config = testip.test_ip_in_int()


def get_xia_la(e):
    baseUrl = config.baseUrl + e
    r = requests.get(url=baseUrl, headers=send_config['ua'], proxies=send_config['ip'])

    cont = r.content.decode('utf-8')  # 获取返回的内容
    res = cont[7: -1]
    res_json = json.loads(res)  # json格式转换
    keys = []
    try:
        qs = res_json['g']
        for q in qs:
            if check_pai(q['q']):
                keys.append(q['q'])
                sou_data.append(q['q'])
                # 复用下拉词进行二次搜索
                re_sou.append(q['q'])
            else:
                pai_data.append(q['q'])
        print(e, keys)
    except KeyError:
        print(e, '无下拉词')


def search_key_in_int():
    global sou
    global re_sou
    for index in range(config.times):
        print("第：", index, "次搜索")
        sou = re_sou
        re_sou = []
        for i in sou:
            time.sleep(config.stop_time)
            get_xia_la(i)
        # if i == '全国治痫':
        #     break


def send_in_int():
    print("获取配置的搜索词根中。。。")
    get_key()
    print("获取配置的排除词中。。。")
    get_pai()
    print("获取可用代理Ip中。。。")
    get_ip()
    print("正在发起请求。。。")
    search_key_in_int()
    return {"sou_data": sou_data, "pai_data": pai_data}
