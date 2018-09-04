# 爬取56听书网mp3链接, 使用js2py执行JS
import re
import time
import js2py
import random
import requests
from lxml import etree


class Spider:
    def __init__(self):
        self.base_url = 'http://www.ting56.com/mp3/4704.html'
        self.chapter_urls = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/67.0.3396.99 Safari/537.36',
        }

    def get_mp3_url(self, text):
        func = js2py.eval_js("""
            function FonHen_JieMa(u){
                    var tArr = u.split("*");
                    var str = '';
                    for(var i=1,n=tArr.length;i<n;i++){
                        str += String.fromCharCode(tArr[i]);
                    }
                    return str;
                }
        """)
        return func(text).split('&')[0]

    def get_html(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                response.encoding = response.apparent_encoding
                return response.text
        except:
            return None

    def start(self):
        while True:
            response = self.get_html(self.base_url)
            if response:
                html = etree.HTML(response)
                lis = html.xpath('//div[@id="vlink_1"]/ul/li')
                for i in lis:
                    title = i.xpath('./a/@title')[0]
                    url = 'http://www.ting56.com' + i.xpath('./a/@href')[0]
                    self.chapter_urls.append({'title': title, 'url': url})
                break
            time.sleep(random.randint(2, 5))

    def run(self):
        print('开始爬取所有章节链接')
        self.start()
        time.sleep(random.randint(2, 5))
        print('开始爬取对应章节的mp3链接')
        for chapter in self.chapter_urls:
            while True:
                response = self.get_html(chapter['url'])
                if response:
                    datas = re.findall(r"<script>var datas=\(FonHen_JieMa\((.*?)\).split\('&'\)\);var datas2 = ''; "
                                       r"var part='.*?'; var play_vid='4704';</script>", response)[0]
                    mp3_url = self.get_mp3_url(datas)
                    chapter['mp3-url'] = mp3_url
                    break
                time.sleep(random.randint(2, 5))
            time.sleep(random.randint(2, 5))
        print('爬取结束')


spider = Spider()
spider.run()
