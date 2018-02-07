# encoding=utf8
#目的，获取http://www.doutula.com得图片到本地
#本程序的爬虫会用多线程爬取，可以学习或者借鉴。
#by 黑小马

#http://www.doutula.com/photo/list/?page=2
import urllib.request
import re
import os
import threading
import time

#请求的UA
UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
#存放图片地址的列表
img_url_list=[]
#存放页面地址
page_url_list=[]
#创建锁
glock=threading.Lock()
def init_page_url():
    mkdir('photo')
    url = "http://www.doutula.com/photo/list/?page="
    for x in range(1336):
        page_url_list.append(url+str(x))


def mkdir(path):
    # 引入模块
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print (path+' 目录已存在')
        return False


def get_img_url():
    while True:
        # 开启锁
        glock.acquire()
        page_url=page_url_list.pop()
        # 释放锁
        glock.release()
        #不要请求太快，这个网站容易崩了，加一个延时
        time.sleep(1)
        req = urllib.request.Request(page_url, headers={'User-Agent': UA})
        res = urllib.request.urlopen(req).read()
        data = res.decode('utf-8')
        reg = re.compile('data-original=".*?"')
        match = reg.findall(data)
        for colour in match:
            img_url_list.append(colour[15:-1])
        if len(page_url_list)==0:
            print("没有页面地址了")
            break


def download_img(name):
    while True:
        if len(img_url_list)==0:
            print("没有下载地址了")
            continue
        else:
            # 开启锁
            glock.acquire
            img_url=img_url_list.pop()
            # 释放锁
            glock.release
            file_name =img_url .split('/').pop()
            filename = os.path.join('photo',file_name)
            req = urllib.request.Request(img_url, headers={'User-Agent': UA})
            res = urllib.request.urlopen(req)
            with open(filename, 'wb') as f:
                f.write(res.read())
                print('线程：'+str(name)+'---下载完成: '+file_name)

if __name__=='__main__':
    #初始化爬取页面
    init_page_url()
    #开3个线程获取图片地址
    for x in range(3):
        th=threading.Thread(target=get_img_url)
        th.start()
    #开3个线程下载图片
    for x in range(3):
        th=threading.Thread(target=download_img,args=[x])
        th.start()
