# 猫眼票房爬取, 突破字体反爬
import os
import re
import requests
from fontTools.ttLib import TTFont


class MaoYan:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
        }
        self.dict2 = ''

    def get_html(self, url):
        response = requests.get(url=url, headers=self.headers)
        if response.status_code == 200:
            return response.text
        return None

    def download_font(self, file_url):
        files = os.listdir('./fonts')
        if file_url not in files:
            print('该文件不在字体库中, 下载:', file_url)
            url = 'http://vfile.meituan.net/colorstone/' + file_url
            response = requests.get(url=url, headers=self.headers)
            with open('./fonts/' + file_url, 'wb') as f:
                f.write(response.content)
        font1 = TTFont('./fonts/base.woff')
        font2 = TTFont('./fonts/'+file_url)

        keys = font1.getGlyphOrder()[2:]
        values = list('7016258934')
        dict1 = dict((k, v) for k, v in zip(keys, values))

        self.dict2 = {}
        for key in font2.getGlyphOrder()[2:]:
            for k, v in dict1.items():
                if font1['glyf'][k] == font2['glyf'][key]:
                    self.dict2[key] = v
                    break

    def modify_data(self, data):
        for i in self.dict2.keys():
            k = (i.replace('uni', '&#x') + ';').lower()
            if k in data:
                data = data.replace(k, self.dict2[i])
        return data

    def start_crawl(self):
        response = self.get_html(url=self.url)
        font_file = re.findall(r"url\('//vfile.meituan.net/colorstone/(.*?)'\) format\('woff'\);", response)[0]
        self.download_font(font_file)

        name = re.findall(r'<h3 class="name">(.*?)</h3>', response)[0]

        star = re.findall(r'<span class="index-left info-num ">\s+<span class="stonefont">(.*)</span>', response)[0]
        star = self.modify_data(star)

        people = ''.join(
            re.findall(r'''<span class='score-num'><span class="stonefont">(.*?)</span>(人评分)</span>''', response)[0])
        people = self.modify_data(people)

        ticket_number = ''.join(
            re.findall(r'''<span class="stonefont">(.*?)</span><span class="unit">(.*?)</span>''', response)[0])
        ticket_number = self.modify_data(ticket_number)

        print(name)
        print('用户评分: {} 星'.format(star))
        print('评分人数: {}'.format(people))
        print('累计票房: {}'.format(ticket_number))


if __name__ == '__main__':
    m = MaoYan('http://maoyan.com/films/1198214')
    m.start_crawl()
