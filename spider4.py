import requests
import re
import os

header = {}
header['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'


class Wallpaper:

    def __init__(self):
        for root, dirs, files in os.walk('D:/wallpaper/imgs/'):     # 删除目录下已存在的图片（是你幻灯片存放所在的目录）
            for i in files:
                path = 'D:/wallpaper/imgs/' + i                     # 这里也要改
                os.remove(path)
        self.get_picture_url('https://alpha.wallhaven.cc/random')

    def get_picture_url(self, url):
        try:
            response = requests.get(url, headers=header)
        except requests.exceptions.ConnectionError:
            print('get wrong')
            return
        res = r'class="preview" href=".+?"  target="_blank"  >'
        res = re.compile(res)
        res_text = re.findall(res, response.text)
        for i in res_text:
            res = re.compile(r'https.+?"')
            res = re.findall(res, i)
            res = res[0][0:-1]
            self.spider(res)

    def spider(self, url):
        try:
            response = requests.get(url, headers=header)
        except requests.exceptions.ConnectionError:
            print('get wrong')
            return
        res = r'<meta property="og:image" content=".+?" />'
        res = re.compile(res)
        res_text = re.findall(res, response.text)
        for i in res_text:
            res = re.compile(r'//wallpapers.+?"')
            res = re.findall(res, i)
            res = 'https:' + res[0][:-1]
            self.download(res)

    @staticmethod
    def download(url):
        try:
            response = requests.get(url, headers=header)
        except requests.exceptions.ConnectionError:
            print('get wrong')
            return
        file = 'D:/wallpaper/imgs/' + url[-20:]   # url[-20:]为图片的名字，前面为其目录，可自行更改
        try:
            with open(file, 'wb') as f:
                f.write(response.content)
        except:
            print('save wrong')
        text = url + '  正在下载，请不要关闭'
        print(text)


wallpaper = Wallpaper()
