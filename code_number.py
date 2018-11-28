
import requests, sys,random
n = random.randint(10000,99999)
def return_number_qw(phone,n):

    host = 'https://aliyun.chanyoo.net'
    path = '/sendsms'
    method = 'GET'
    appcode = 'a00c88e1885e43058f987d86e42d2e57'
    querys = 'mobile='+phone+'&content=您的手机号：'+phone+'，验证码：'+str(n)+'，请及时完成验证，如不是本人操作请忽略。【阿里云市场】'
    bodys = {}
    url = host + path + '?' + querys

    headers = {'Authorization': 'APPCODE ' + appcode}
    request = requests.get(url, headers=headers)



if __name__ == '__main__':
    return_number_qw('15234807096',n)

