# 破解神漫画js
import re
import requests


def get_html():
    url = 'https://www.shenmanhua.com/shenyinwangzuo/333.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/68.0.3440.106 Safari/537.36'
    }

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.text
    return None


def get_path(imgpath, pageid):
    path = ''
    for i in range(len(imgpath)-1):
        if (imgpath[i] == '\\' and imgpath[i+1] == '\\') or (imgpath[i] != '\\' and imgpath[i+1] != '\\') or (imgpath[i] != '\\' and imgpath[i+1] == '\\'):
            path += chr(ord(imgpath[i]) - pageid % 10)
    if imgpath[-1] == '\\' and imgpath[-2] == '\\':
        pass
    else:
        path += chr(ord(imgpath[-1]) - pageid % 10)
    return path


text = get_html()
info = re.findall(r'mh_info={imgpath:"(.*?)",.*,totalimg:(.*?),.*,pageid:(.*?),.*}', text)
imgpath = info[0][0]
totalimg = info[0][1]
pageid = info[0][2]
path = get_path(imgpath, int(pageid))

for page in range(1, int(totalimg) + 1):
    img_url = 'https://mhpic.cnmanhua.com/comic/' + path + str(page) + '.jpg-smh.middle.webp'
    print(img_url)
