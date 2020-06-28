from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter import messagebox
from paqu import *
from threading import Thread

# 参数设置
root_width = 1000
root_height = 700
# 默认保存文件路径
base_path = r"F:\pictures"

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createWidgets()

    def change_tag_options(self, tag):
        self.pic_frame.pack_forget()
        self.xiaoshuo_frame.pack_forget()
        if tag == 0:
            self.pic_frame.pack(side="top", fill=Y)
        elif tag == 1:
            self.xiaoshuo_frame.pack(side="top", fill=Y)

    def createWidgets(self):
        # 创建三个子框架
        head_options_frame = Frame(self)
        head_options_frame.pack()

        tag_width = 25

        self.picture_but = Radiobutton(head_options_frame, text="图 片 下 载", width=tag_width,
                                       value=0, bd=1, indicatoron=0,command= lambda: self.change_tag_options(0))
        self.picture_but.pack(side="left", fill=Y)

        self.xiaoshuo_but = Radiobutton(head_options_frame, text="小 说 下 载", width=tag_width,
                                        value=1, bd=1, indicatoron=0,command=lambda: self.change_tag_options(1))
        self.xiaoshuo_but.pack(side="left", fill=Y)

        self.pic_frame = Frame(self)
        self.pic_frame.pack(side="top", fill=Y)
        Pic_Frame().createWidgets(self.pic_frame)

        self.xiaoshuo_frame = Frame(self)
        Content_Frame().createWidgets(self.xiaoshuo_frame)

class Pic_Frame(Frame):
    def createWidgets(self, new_frame):
        self.search_lab = Label(new_frame, text="请输入英文关键词：",font=("kaiti",15),width=20)
        self.search_lab.grid(row=0, column=0,pady=10)

        self.v1_key = StringVar()
        self.v1_key.set("sky")
        self.key_word_entry = Entry(new_frame,width=30,font=("kaiti",15),text=self.v1_key)
        self.key_word_entry.grid(row=0, column=1,ipadx=10)

        self.search_but = Button(new_frame,width=15,text="搜 索",font=("kaiti",15),command=lambda : MyThread(self.html_result))
        self.search_but.grid(row=0, column=2)

        self.search_result_text = Text(new_frame,width=100,height=30,state=DISABLED,bg="#C2FF68")
        self.search_result_text.grid(row=1, column=0,columnspan=3)

        self.num_lab = Label(new_frame, text="请输入下载页数：",font=("kaiti",15),width=20)
        self.num_lab.grid(row=2, column=0,pady=10)

        self.v2_page = StringVar()
        self.v2_page.set("2")
        self.want_download_page_num = Entry(new_frame,text=self.v2_page,font=("kaiti",15),width=30)
        self.want_download_page_num.grid(row=2, column=1)

        self.file_save_path__choice_lab = Label(new_frame, text="请选择保存文件路径：",font=("kaiti",15),width=20)
        self.file_save_path__choice_lab.grid(row=3, column=0,pady=10)

        self.file_save_path_lab = Label(new_frame, text=base_path,font=("kaiti",10),width=40)
        self.file_save_path_lab.grid(row=3, column=1)

        self.find_path_but = Button(new_frame,text="浏 览",font=("kaiti",15),width=15,command=self.save_path)
        self.find_path_but.grid(row=3, column=2)

        self.download_but = Button(new_frame,text="下 载",font=("kaiti",15),width=20,command= lambda : MyThread(self.download_txt))
        self.download_but.grid(row=4, column=0,columnspan=3)

    # 更换文件保存路径
    def save_path(self):
        path = askdirectory()
        self.file_save_path_lab["text"] = path

    # 搜索响应
    def html_result(self):
        search_key = self.v1_key.get()
        if search_key.isalpha():
            msg_list = Start_GO().search(search_key)
            self.search_result_text["state"] = NORMAL
            self.search_result_text.insert(INSERT,"搜索到{0}结果\t搜索到{1}页，共{2}张图片\n".format(search_key,msg_list[0],msg_list[1]))
            self.search_result_text["state"] = DISABLED
        else:
            messagebox.showerror(title="输入错误",message="非法输入！")

    # 定义下载函数
    def download_txt(self):
        key = self.v1_key.get()
        print("key:",key)
        savepath = self.file_save_path_lab["text"]
        print("路径：",savepath)
        want_page = self.v2_page.get()
        print("页数：",want_page)
        self.search_result_text["state"] = NORMAL
        self.search_result_text.insert(INSERT,"正在下载{0}中...\n".format(key))
        Start_GO().main(key,savepath,want_page)
        self.search_result_text.insert(INSERT,"{0}下载完成\n".format(key))
        self.search_result_text["state"] = DISABLED
        return messagebox.showinfo(title="Successed!",message="下载成功！")

# 定义多线程  
class MyThread(Thread):
    def __init__(self,func):
        super().__init__()
        self.func = func
        # 守护
        self.setDaemon(True)
        # 启动
        self.start()
    def run(self):
        self.func()

class Content_Frame(Frame):
    def createWidgets(self, new_frame):
        search_lab = Label(new_frame, text="请输入小说名")
        search_lab.grid(row=0, column=0)

if __name__ == "__main__":
    root = Tk()
    root_top = root.winfo_screenwidth() / 2 - root_width/2
    root_left = root.winfo_screenheight() / 2 - root_height / 2
    root.title("多功能使用工具")
    root.geometry("{0}x{1}+{2}+{3}".format(root_width,
                                           root_height, int(root_top), int(root_left)))
    app = Application(root)
    app.mainloop()
    from fake_useragent import UserAgent
import requests
import os
from lxml import etree

class getHtml:
    def __init__(self):
        self.headers = {"User-Agent": UserAgent().random}

    def do_get_resp(self,url):
        resp = requests.get(url, headers=self.headers)
        return resp

    def do_getHtml(self, url):
        resp = requests.get(url, headers=self.headers)
        resp.encoding = "utf-8"
        if resp.status_code == 200:
            return resp.text
        else:
            return None

class Save_pic:
    def save(self,title,resp_content,key,savepath):
        save_pic_path = savepath + r"\{0}".format(key)
        if os.path.exists(save_pic_path):
            pass
        else:
            os.makedirs(save_pic_path)
        with open(save_pic_path+r"\{0}".format(title),"wb") as f:
            f.write(resp_content)
            f.close() 

class ParseHtml:
    # 解析主页面上的更多标签
    def do_parse_search(self, html):
        e = etree.HTML(html)
        pages_all = e.xpath('//h2')[0].xpath("string(.)")
        # pages 为当前搜索结果中的总页数
        pages = pages_all[len(pages_all)-3:]
        # 获取当前搜索接种的总图片数
        all_counts = e.xpath('//h1')[0].xpath("string(.)").split("Wallpapers")[0]
        # 返回一个列表
        return [pages,all_counts]

    def do_get_pic_hrefs(self,msg_list,want_page,key):
        # 获取最大的页数
        max_page = int(msg_list[0])
        if int(want_page) <= max_page:
            max_page == int(want_page)
        elif int(want_page) > max_page:
            pass
        for i in range(1,max_page+1):
            url = "https://wallhaven.cc/search?q={0}&page={1}".format(key,i)
            html = getHtml().do_getHtml(url)
            e = etree.HTML(html)
            # 获取图片的href,并对其进行加工处理
            hrefs = e.xpath('//figure/img/@data-src')
            realy_hrefs = []
            for href_str in hrefs:
                href_str_new = href_str.replace("small","full").replace("th","w")
                realy_href = href_str_new[:int(href_str_new.rfind("/"))+1] + "wallhaven-" + href_str_new[int(href_str_new.rfind("/"))+1:]
                realy_hrefs.append(realy_href)
            return realy_hrefs

    def do_save_pics(self,href_pic_list,savepath,key):
        # 循环遍历图片链接
        for url in href_pic_list:
            resp = getHtml().do_get_resp(url)
            if resp.status_code == 200:
                # e = etree.HTML(resp.text)
                # type = resp.url[len(resp.url)-3:]
                title = resp.url[int(resp.url.rfind("wallhaven-")):]
                Save_pic().save(title,resp.content,key,savepath)
            else:
                new_url = resp.url
                new_url = new_url[:int(new_url.rfind("."))+1]+"png"
                resp = getHtml().do_get_resp(new_url)
                # e = etree.HTML(resp.text)
                # width = e.xpath('//img/@width')[0]
                # height = e.xpath('//img/@height')[0]
                # type = resp.url[len(resp.url)-3:]
                title = resp.url[int(resp.url.rfind("wallhaven-")):]
                Save_pic().save(title,resp.content,key,savepath)

class Start_GO:
    def main(self,key,savepath,want_page):
        url = "https://wallhaven.cc/search?q={0}&page=2".format(key)
        html = getHtml().do_getHtml(url)
        msg_list = ParseHtml().do_parse_search(html)
        href_pic_list = ParseHtml().do_get_pic_hrefs(msg_list,want_page,key)
        ParseHtml().do_save_pics(href_pic_list,savepath,key)

    def search(self,key):
        url = "https://wallhaven.cc/search?q={0}&page=2".format(key)
        html = getHtml().do_getHtml(url)
        msg_list = ParseHtml().do_parse_search(html)
        return msg_list
