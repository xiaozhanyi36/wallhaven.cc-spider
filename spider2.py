from requests_html import HTMLSession   # 用于数据请求、数据提取、相较于其他库更加简洁方便
from urllib import request              # 本例中该库只用于下载保存图片

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}  # 请求头，用于反反爬

session = HTMLSession()

urls = []

for i in range(1, 3):
    # r = session.get('https://wallhaven.cc/toplist?page={}'.format(i))
    r = session.get('https://wallhaven.cc/search?categories=110&purity=100&topRange=1y&sorting=toplist&order=desc&page={}'.format(i))
    urls = r.html.links
    print(urls)



def down_pic(image_url):

    try:
        path = 'D:\爬取内容\一年榜\{}'.format((image_title.split('/')[-1]) + (image_url.split('/')[-1]))
        print(path)
        opener = request.build_opener()
        opener.addheaders = [('User-Agent',
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36')]
        request.install_opener(opener)
        request.urlretrieve(image_url, path)
    except Exception as m:
        print(m)


for url in urls:
    try:
        session1 = HTMLSession()
        r1 = session1.get(url)
        sr = r1.html.find("img#wallpaper", first=True)
        image_url = sr.attrs['src']
        image_title = sr.attrs['alt']
        print(image_url)
        print(image_title)
        down_pic(image_url)
    except BaseException as e:
        print(e)
