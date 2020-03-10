# coding: utf-8
'''
@author: sy-records
@license: https://github.com/sy-records/v-checkin/blob/master/LICENSE
@contact: 52o@qq52o.cn
@desc: 腾讯视频好莱坞会员V力值签到，支持两次签到：一次正常签到，一次手机签到。
@blog: https://qq52o.me
'''

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests

auth_refresh_url = ''
sckey = ''

ftqq_url = "https://sc.ftqq.com/%s.send"%(sckey)
url1 = 'https://vip.video.qq.com/fcgi-bin/comm_cgi?name=hierarchical_task_system&cmd=2'
url2 = 'https://v.qq.com/x/bu/mobile_checkin'

login_headers = {
    'Referer': 'https://v.qq.com',
    'Cookie': 'tvfe_boss_uuid=********; pgv_pvid=********; video_guid=***********; video_platform=2; pgv_info=ssid=***********; pgv_pvi=*************; pgv_si=*************; _qpsvr_localtk=***************; ptisp=; ptui_loginuin=************; RK=*************; ptcz=***************; main_login=qq; vqq_access_token=****************; vqq_appid=101483052; vqq_openid=********************; vqq_vuserid=*********************; vqq_vusession=dzsfo; vqq_refresh_token=*****************; uid=**************;'
}

login = requests.get(auth_refresh_url, headers=login_headers)
cookie = requests.utils.dict_from_cookiejar(login.cookies)

if not cookie:
    print "auth_refresh error"
    payload = {'text': '腾讯视频V力值签到通知', 'desp': '获取Cookie失败，Cookie失效'}
    requests.post(ftqq_url, params=payload)

sign_headers = {
    'Cookie': 'tvfe_boss_uuid=***********; pgv_pvid=***************; video_guid=***************; video_platform=2; pgv_info=ssid=****************; pgv_pvi=****************; pgv_si=***************; _qpsvr_localtk=*************; ptisp=; ptui_loginuin=***************; RK=****************; ptcz=*********************; main_login=qq; vqq_access_token=************; vqq_appid=101483052; vqq_openid=*************; vqq_vuserid=*************; vqq_vusession=' + cookie['vqq_vusession'] + ';',
    'Referer': 'https://m.v.qq.com'
}
def start():
  sign1 = requests.get(url1,headers=sign_headers).text
  if 'Account Verify Error' in sign1:
    print 'Sign1 error,Cookie Invalid'
    status = "链接1 失败，Cookie失效"
  else:
    print 'Sign1 Success'
    status = "链接1 成功，获得V力值：" + sign1[42:-14]

  sign2 = requests.get(url2,headers=sign_headers).text
  if 'Unauthorized' in sign2:
    print 'Sign2 error,Cookie Invalid'
    status = status + "\n\n 链接2 失败，Cookie失效"
  else:
    print 'Sign2 Success'
    status = status + "\n\n 链接2 成功"

  payload = {'text': '腾讯视频V力值签到通知', 'desp': status}
  requests.post(ftqq_url, params=payload)

def main_handler(event, context):
  return start()
if __name__ == '__main__':
  start()
