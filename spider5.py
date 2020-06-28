import requests
from  lxml import etree
headers={
	"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0"
	}

filepath="D:/Picture/wallhaven/"  #文件路径

for i in range(1,11):  #爬取页数
	kv={"page":i}
	
	url="https://wallhaven.cc/toplist"
	try:
		r=requests.get(url,headers=headers,params=kv,timeout=200)
		
		#开始解析
		html =etree.HTML(r.text)
		srcs =html.xpath(".//li//a[@class='preview']/@href")    #获取到跳转网页
		
		for src in srcs :
			r=requests.get(src,headers=headers,timeout=200)
			html =etree.HTML(r.text)
			img_src =html.xpath(".//img[@id='wallpaper']/@src")
			for src in img_src :
				filename_1= src.split('/')[-1] #获取文件名
				response=requests.get(src,headers=headers)		
						
				with open(filepath+filename_1,'wb') as file:
					file.write(response.content)
					print(filename_1)
				print("Succe")
			continue
			print("Triumph")
