import requests
import re
from lxml import etree
import time
import random


def header():
    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    UserAgent = random.choice(user_agent_list)
    headers = {'User-Agent': UserAgent}
    print(headers)
    return headers


def ipproxies():
    f = open("ip.txt", 'r+')
    fr = f.read()
    f.close()
    ip_list = fr.split('\n')
    # 随机从ip池中选出一个ip
    proxy = random.choice(ip_list)
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy,
    }
    print(proxies)
    return proxies


def ganji():
    url = "http://www.ganji.com/index.htm"
    res = requests.get(url, headers=header(), proxies=ipproxies())
    html = etree.HTML(res.text)
    dl_list = html.xpath('//div[@class=\"all-city\"]/dl')
    for dl in dl_list:
        url_list = dl.xpath('.//dd/a/@href')
        for url in url_list:
            new_url = url + 'huangye/'
            navigation(new_url, url)
            # new_url = "http://cq.ganji.com/huangye/"


def navigation(new_url, url):
    try:
        res = requests.get(new_url, headers=header(), proxies=ipproxies())
        html = etree.HTML(res.text)
        dl_list = html.xpath('//div[@class=\"left-nav-list\"]/div/div[1]/dl')
        for dl in dl_list:
            dl_url = dl.xpath('.//dt/a/@href')[0]
            text = dl.xpath('.//dt/a/text()')[0]
            if dl_url:
                dl_url = dl_url.strip('/')
                s_url = url + dl_url + "/"
                list_datalis(s_url, text)
    except:
        print("获取分类导航错误！")


def list_datalis(ss_url, text):
    try:
        for page in range(1, 100):
            print(text, page)
            s_url = ss_url
            s_url = s_url + 'o' + str(page) + '/'
            print(s_url)
            res = requests.get(s_url, headers=header(), proxies=ipproxies())
            html = etree.HTML(res.text)
            li_list = html.xpath('//div[@class=\"txt\"]')
            for div in li_list:
                url = div.xpath('.//p/a/@href')[0]
                print(url)
                if 'ganji' in url:
                    new_url = "http:" + url
                else:
                    new_url = "http://anshan.ganji.com" + url
                get_datelis(new_url, text)

    except:
        print("获取列表错误!")


def get_datelis(new_url, text):
    res = requests.get(new_url, headers=header(), proxies=ipproxies())
    html = etree.HTML(res.text)
    title = html.xpath('//h1/text()')[0]
    characteristic = html.xpath('//div[@class=\"tcon\"]/text()')[0]
    service = html.xpath('//div[@class=\"tcon\"]/a/text()')[0]
    print(title)


if __name__ == "__main__":
    ganji()