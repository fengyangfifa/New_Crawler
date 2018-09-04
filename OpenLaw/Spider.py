import re
import time
import execjs
import random
import requests


class Spider:
    def __init__(self):
        self.url = 'http://openlaw.cn/guidance/16444ed8fe27460bbd07732fc7d20fe4'
        self.session = requests.Session()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84'
                          ' Safari/537.36',
            'Host': 'openlaw.cn',
            'Pragma': 'no-cache',
            'Referer': self.url,
            'Upgrade-Insecure-Requests': '1',
        }
        self.file = 'decopt.js'
        self.proxies = {
            'http': 'http://190.45.92.25:21776'
        }
        self.session.headers.update(self.headers)

    def get_html(self):
        try:
            response = self.session.get(self.url, proxies=self.proxies, timeout=10)
            if response.status_code == 200:
                return response
            return None
        except:
            print('打开网页失败...')
            return None

    def get_cookie_js(self, js):
        with open(self.file, 'r', encoding='utf-8') as f:
            ctx = execjs.get().compile(f.read())
        data = ctx.call('Encrypted', js)
        func_js = data[213:-196]
        # 匹配用于计算c_token值的函数
        return func_js, data

    def get_cookie(self, value, js):
        return execjs.compile(js).call('_a', value)

    def first_time(self, response):
        set_cookie = response.headers['Set-Cookie'].split(' ')[0]
        # 匹配SESSION值
        print(response.text)
        js2 = re.findall(r'\$\.\$\(\$\.\$\(\$\.\$\$\+(.*?)\)\(\)\)\(\);', response.text, re.S)[0]
        js, data = self.get_cookie_js(js2)
        _ = re.findall(r"document.cookie='s_token='\+(.*?);", data)[0]
        # 匹配_, 用于s_token和计算c_token
        value = re.findall(r'var {} = "(.*?)";'.format(_), response.text)[0]
        # 匹配解密函数字符串
        c_token = self.get_cookie(value, js)
        self.session.headers.update({'Cookie': 's_token={}; c_token={}; {}'.format(value, c_token, set_cookie[:-1])})
        print('成功设置Cookie')

    def second_time(self, response):
        print(response.text)

    def run(self):
        response = self.get_html()
        if response:
            self.first_time(response)
        time.sleep(random.randint(2, 5))
        response = self.get_html()
        if response:
            self.second_time(response)


spider = Spider()
spider.run()
