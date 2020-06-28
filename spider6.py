# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 17:58:50 2019
@author: yuyuko
"""
#wallhaven爬取
import os
from urllib.parse import urlencode
import time
from requests import codes
import random
import requests
from lxml import etree
def CreatePath(filepath):
    if not os.path.exists(filepath):
            os.makedirs(filepath)
            def GetUrl(keyword,category):
                params = {
        'q': keyword,
        'categories': category,
        'purity': '110',
        'sorting': 'relevance',
        'order':'desc'
    }
    base_url='https://alpha.wallhaven.cc/search?'
    url=base_url + urlencode(params)
    return url
def GetPictureNum(url):
    allpic=" "
    try:
        html = requests.get(url) 
        if codes.ok == html.status_code:
            selector = etree.HTML(html.text) 
            pageInfo = selector.xpath('//header[@class="listing-header"]/h1[1]/text()')#提取出文本
            string = str(pageInfo[0])#图片数是文本中的第一个
            numlist = list(filter(str.isdigit,string))  #有些数字是这样的，11,123,所以需要整理。
            for item in numlist:
                allpic+=item
            totalPicNum=int(allpic)  #把拼接起来的字符串进行整数化
            return totalPicNum
    except requests.ConnectionError:
        return None
    def GetLinks(url,number):
        urls=url+'&page='+str(number)
    try:
        html=requests.get(urls)
        selector=etree.HTML(html.text)
        PicLink=selector.xpath('//a[@class="preview"]/@href')#这里寻找图片的链接地址，以求得到图片编号
    except Exception as e:
        print('Error',e.args)
        def GetLinks(url,number):
            urls=url+'&page='+str(number)
    try:
        html=requests.get(urls)
        selector=etree.HTML(html.text)
        PicLink=selector.xpath('//a[@class="preview"]/@href')#这里寻找图片的链接地址，以求得到图片编号
    except Exception as e:
        print('Error',e.args)
    return PicLink
def Download(filepath,keyword,url,count,headers):#其中count是你要下载的图片数
#此函数用于图片下载。其中参数url是形如：https://alpha.wallhaven.cc/wallpaper/510308的网址
#510308是图片编号，需要构造html，html是图片的最终直接下载网址。
#因为wallheaven上只有两种格式的图片，分别是png和jpg，所以设置两种最终地址HtmlJpg和HtmlPng，通过status_code来进行判断，状态码为200时请求成功。
    string=url.strip('https://alpha.wallhaven.cc/wallpaper/')
    HtmlJpg='http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-' + string+'.jpg'
    HtmlPng='http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-' + string+'.png'
    
    try:
        pic=requests.get(HtmlJpg,headers=headers)
        if codes.ok==pic.status_code:
            pic_path=filepath+keyword+str(count)+'.jpg'           
        else:
            pic=requests.get(HtmlPng,headers=headers)
            pic_path=filepath+keyword+str(count)+'.png'
        with open(pic_path,'wb') as f:
            f.write(pic.content)
            f.close()
        print("Downloaded image:{}".format(count))
        time.sleep(random.uniform(0,3))#这里是让爬虫在下载完一张图片后休息一下，防被侦查到是爬虫从而引发反爬虫机制。
            
    except Exception as e:
        print(repr(e))
        def main():
            headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36",#请求头，这个可以通过查看你自己的浏览器得到。
        }
    filepath = ('/home/yuyuko/Pictures/')#存储路径。
    keyword=input('请输入关键词:')
    category=input('请输入图片分类，共有三种，分别为Gneral,Anime,People三种\
                   ，如果你想要只想选择Anime，就键入010,如果全选就键入111,以此类推:')
    CreatePath(filepath) #创建保存路径
    url=GetUrl(keyword,category)   #获取url
    
    PicNum=GetPictureNum(url)#总图片数
    pageNum=int(PicNum/24+1)  #求出总页面数
    print("We found:{} images.".format(PicNum))
    Num=int(input("请输入你想要爬的图片数，不能超过已找到的图片数:"))
    
    j=1
    for i in range(pageNum):
        PicUrl=GetLinks(url,i+1)
        for item in PicUrl:
            Download(filepath,keyword,item,j,headers)
            j+=1
            if(j>Num):#如果你下载的图片够用了，那就直接退出循环，结束程序。
                break
        else:
            pass
        break


 if  __name__  ==' __main__'                            
 main()
