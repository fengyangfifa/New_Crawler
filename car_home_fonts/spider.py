# 破解汽车之家字体反爬
import requests
from lxml import etree
from fontTools.ttLib import TTFont

font = TTFont('./fonts/ChcCQ1sUz2OAeAubAABj8El3-6U87..ttf')
keys = font.getGlyphOrder()[1:]
value = ['上', '五', '七', '长', '是', '少', '短', '远', '和', '低', '得', '一', '左', '六',
         '小', '二', '很', '好', '地', '大', '坏', '下', '高', '右', '多', '的', '着', '不',
         '矮', '三', '八', '近', '九', '了', '更', '十', '四', '呢']

dict1 = dict((k, v) for k, v in zip(keys, value))

headers = {
    'Host': 'club.autohome.com.cn',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
}
url = 'https://club.autohome.com.cn/bbs/thread/73ac39a287cc9678/69436529-1.html'
response = requests.get(url=url, headers=headers)
html = etree.HTML(response.text)
text = ''.join(html.xpath('//div[@class="tz-paragraph"]//text()')).encode('utf-8')
keys = [eval(r"'\u" + uni[3:] + "'").encode("utf-8") for uni in keys]
for i in range(len(keys)):
    text = text.replace(keys[i], value[i].encode('utf-8'))
print(text.decode('utf-8'))

