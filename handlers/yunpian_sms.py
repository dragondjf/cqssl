#!/usr/local/bin/python
#-*- coding:utf-8 -*-
# Author: jacky
# Time: 14-2-22 下午11:48
# Desc: 短信http接口的python代码调用示例
import httplib
import urllib
import logging

#服务地址
host = "yunpian.com"
#端口号
port = 80
#版本号
version = "v1"
#查账户信息的URI
user_get_uri = "/" + version + "/user/get.json"
#智能匹配模版短信接口的URI
sms_send_uri = "/" + version + "/sms/send.json"
#模板短信接口的URI
sms_tpl_send_uri = "/" + version + "/sms/tpl_send.json"

def get_user_info(apikey):
    """
    取账户信息
    """
    conn = httplib.HTTPConnection(host, port=port)
    conn.request('GET', user_get_uri + "?apikey=" + apikey)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str

def send_sms(apikey, text, mobile):
    """
    能用接口发短信
    """
    params = urllib.urlencode({'apikey': apikey, 'text': text, 'mobile':mobile})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection(host, port=port, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str

def tpl_send_sms(apikey, tpl_id, tpl_value, mobile):
    """
    模板接口发短信
    """
    params = urllib.urlencode({'apikey': apikey, 'tpl_id':tpl_id, 'tpl_value': tpl_value, 'mobile':mobile})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection(host, port=port, timeout=30)
    conn.request("POST", sms_tpl_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str

def sendsms(result):
    apikey = "25bd87c30a32e1bec18430f67acd199b "
    mobile = "13986218913"
    tpl_id = 1002491 #对应的模板内容为：您的验证码是#code#【#company#】


    message1 = "#type1#=大&#count1#=%d" % (result['large'])

    message2 = "#type2#=小&#count2#=%d" % (result['small'])
    
    message3 = "#type3#=单&#count3#=%d" % (result['odd'])

    message4 = "#type4#=双&#count4#=%d" % (result['even'])

    message = "%s&%s&%s&%s" % (message1, message2, message3, message4)

    ret = tpl_send_sms(apikey, tpl_id, message, mobile)
    logging.info(ret)


if __name__ == '__main__':
    apikey = "25bd87c30a32e1bec18430f67acd199b "
    mobile = "13986218913"
    text = "csqqc [Dan] 13"
    #查账户信息
    # print(get_user_info(apikey))
    #调用智能匹配模版接口发短信
    # print(send_sms(apikey, text, mobile))
    # #调用模板接口发短信
    tpl_id = 1002491 #对应的模板内容为：您的验证码是#code#【#company#】
    # tpl_value = '#type1#=单&#count1#=5&#type2#=双&#count2#=15&#type3#=大&#count3#=5&#type4#=小&#count4#=5'
    # print(tpl_send_sms(apikey, tpl_id, tpl_value, mobile))
