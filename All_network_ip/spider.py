# 爬取全网代理ip网站, 破解页面port反爬(js)
import requests
from lxml import etree


def get_html():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/67.0.3396.99 Safari/537.36',
    }
    url = 'http://www.goubanjia.com/'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except:
        return None


def get_ip_port(response):
    html = etree.HTML(response)
    trs = html.xpath('//table[@class="table table-hover"]/tbody/tr')
    ip_port = []
    for i in trs:
        value = i.xpath('.//td[@class="ip"]//text()')
        port_class = i.xpath('.//td[@class="ip"]/span[last()]/@class')[0]
        ip = analysis_ip(value[:-1])
        port = analysis_port(port_class)
        ip_port.append(ip + port)
    return ip_port


def analysis_ip(value):
    ip = ''
    for m, n in enumerate(value):
        if m > 0:
            if value[m] != value[m - 1]:
                ip += n
        else:
            ip += n
    return ip


def analysis_port(port_class):
    port = 0
    for i in port_class.split(" ")[1]:
        port = port * 10 + 'ABCDEFGHIZ'.index(i)
    port = port >> 3
    return str(port)


if __name__ == '__main__':
    response = get_html()
    if response:
        for i in get_ip_port(response):
            print(i)
    else:
        print('爬取页面源码失败')


"""
页面js反混淆函数, 得到正确的port
var _$ = ['\x2e\x70\x6f\x72\x74', "\x65\x61\x63\x68", "\x68\x74\x6d\x6c", "\x69\x6e\x64\x65\x78\x4f\x66", '\x2a', "\x61\x74\x74\x72", '\x63\x6c\x61\x73\x73', "\x73\x70\x6c\x69\x74", "\x20", "", "\x6c\x65\x6e\x67\x74\x68", "\x70\x75\x73\x68", '\x41\x42\x43\x44\x45\x46\x47\x48\x49\x5a', "\x70\x61\x72\x73\x65\x49\x6e\x74", "\x6a\x6f\x69\x6e", ''];
解密前函数
$(function () {
    $(_$[0])[_$[1]](function () {
        var a = $(this)[_$[2]]();
        if (a[_$[3]](_$[4]) != -0x1) {
            return
        };
        var b = $(this)[_$[5]](_$[6]);
        try {
            b = (b[_$[7]](_$[8]))[0x1];
            var c = b[_$[7]](_$[9]);
            var d = c[_$[10]];
            var f = [];
            for (var g = 0x0; g < d; g++) {
                f[_$[11]](_$[12][_$[3]](c[g]))
            };
            $(this)[_$[2]](window[_$[13]](f[_$[14]](_$[15])) >> 0x3)
        } catch (e) {}
    })
})
解密后函数
$(function() {
    $('.port').each(function() {
        var a = $(this).html();
        if (a.indexOf('*') != -0x1) {
            return
        };var b = $(this).attr('class');
        try {
            b = (b.split(" "))[0x1];
            var c = b.split("");
            var d = c.length;
            var f = [];
            for (var g = 0x0; g < d; g++) {
                f.push('ABCDEFGHIZ'.indexOf(c[g]))
            }
            ;$(this).html(window.parseInt(f.join('')) >> 0x3)
        } catch (e) {}
    })
})
"""
# 使用execjs运行js反混淆函数, 实现对port的解析
# import execjs
#
# ctx = execjs.compile("""
#      function sss(b) {
#         b = (b.split(" "))[0x1];
#         var c = b.split("");
#         var d = c.length;
#         var f = [];
#         for (var g = 0x0; g < d; g++) {
#             f.push('ABCDEFGHIZ'.indexOf(c[g]))
#         }
#         return f.join('');
#      }
#  """)
# result = ctx.call("sss", "port ECGCEI")
# print(int(result) >> 3)
