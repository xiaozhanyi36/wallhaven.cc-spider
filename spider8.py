import os,lxml,requests,sys,time
from lxml import etree
from requests.adapters import HTTPAdapter
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED
os.system('title 电脑壁纸爬虫程序 @xiaozhanyi')#设置窗口标题
#coding:utf-8
path = '壁纸'
if not os.path.exists(path):
    os.makedirs(path)

def toplist(url):#排行
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    s = requests.session()#加入会话保持系统
    s.mount('http://', HTTPAdapter(max_retries=10))#http和https都为最大重试10次
    s.mount('https://', HTTPAdapter(max_retries=10))
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    x = 0
    while x < 10:#while错误重试10次,与上面的max_retries相同,加起来等于每个链接重试21次
        try:
            r = s.get(url,headers=headers,timeout = (20,20))
            if r.status_code == 200:
                print('该地址已经return')
                return r.text

        except requests.exceptions.RequestException as e:#必须加入except,否则程序爆出的错误让你无法定位,之前没加我的程序报我语法错误,且错误在pagenum()
            print(e)
            x += 1
            print('开始重试.')
            print(time.strftime('%Y-%m-%d %H:%M:%S'))

def fenxi(html):#获得当前页面的所有Url
    html = etree.HTML(html)
    #下边是在首页里找到最大翻页数量
    result = html.xpath('//*[@id="thumbs"]/section[1]/ul/li/figure/a/@href')
    return result

def down_pic(picurl):#下载每条链接内的图片
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    html = etree.HTML(picurl)
    result = html.xpath('//*[@id="wallpaper"]/@src')[0]
    picname = html.xpath('//*[@id="wallpaper"]/@data-wallpaper-id')[0]
    try:
        jpgget = requests.get(result,timeout = (20,20))
    except requests.exceptions.RequestException as e:
        print('下载超时!',e)
    pass
    try:
        with open(f'{path}/{picname}.jpg','wb') as f:
            f.write(jpgget.content)
            print(f'已完成{picname}的下载')
    except:
        print('下载超时!')
        pass

if __name__ == "__main__":
    while   True:
        w = int(input('请问你要下载哪一个分辨率:\n1:2560x1440\n2:2560*1080\n3:1280*800\n4:3840x3072\n5:3840x2160\n请输入:'))
        i = input('请问你要下载第几页: ')
        if w == 1:
            url = f'https://wallhaven.cc/search?categories=111&purity=111&resolutions=2560x1440&sorting=date_added&order=desc&page={i}'
        elif w == 2:
            url = f'https://wallhaven.cc/search?categories=111&purity=111&resolutions=2560x1440&sorting=date_added&order=desc&page={i}'
        elif w == 3:
            url = f'https://wallhaven.cc/search?categories=111&purity=111&resolutions=2560x1440&sorting=date_added&order=desc&page={i}' 
        elif w == 4:
            url = f'https://wallhaven.cc/search?categories=111&purity=111&resolutions=2560x1440&sorting=date_added&order=desc&page={i}'
        elif w == 5:
            url = f'https://wallhaven.cc/search?categories=111&purity=111&resolutions=3840x2160&sorting=date_added&order=desc&page={i}'
        else:
            print('请正确输入数字')

        html = toplist(url)
        ex = ThreadPoolExecutor(max_workers=24)#多线程处理模块,开启24线程赋值给变量ex
        future = [ex.submit(down_pic,toplist(url)) for url in fenxi(html)]
        wait(future,return_when=ALL_COMPLETED)
        print('所有图片下载完成!')
