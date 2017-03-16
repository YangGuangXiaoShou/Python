# coding=utf-8
import jsonlib
from bs4 import BeautifulSoup
import sys
import urllib
import os
from selenium import webdriver

'''
下载应用宝中官方应用
作者：sillygirl
'''
driver = webdriver.PhantomJS('phantomjs.exe')


# 判断是否还有下一页
def GetPage(newPage):
    url = 'http://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId=0&pageSize=20&pageContext=' + str(newPage)
    page = urllib.urlopen(url)
    data = page.read()
    jsonData = jsonlib.loads(data)
    if jsonData['count'] == 0:
        print "do not have more"
        driver.close()
    else:
        print "hava more"
        GetJson(newPage)


# json数据解析
def GetJson(page):
    url = 'http://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId=0&pageSize=20&pageContext=' + str(page)
    pageData = urllib.urlopen(url)
    data = pageData.read()
    jsonData = jsonlib.loads(data)
    for newLine in jsonData['obj']:
        print newLine[u'appName'] + '\t' + newLine['pkgName'] + '\t' + newLine['apkUrl']
        IfOfficial(newLine['pkgName'])
    page += 20
    print page
    GetPage(page)


# 判断是否为官方
def IfOfficial(pagName):
    url = 'http://sj.qq.com/myapp/detail.htm?apkName=' + pagName
    response = urllib.urlopen(url)
    driver.get(url)
    data = driver.page_source
    soup = BeautifulSoup(response, 'lxml')
    official = driver.find_element_by_class_name('official-text')
    appName = soup.select('.det-name-int')
    # appName = driver.find_element_by_class_name("det-name-int")
    down = soup.select('.det-down-btn')
    print 'appname  ' + appName[0].getText()
    if official.text != '':
        print 'is official'
        try:
            DownLoadApk(down[0].attrs['data-apkurl'], appName[0].getText())
        except IOError:
            print "download error" + appName[0].getText()
    else:
        print 'is not official'


# 下载
def DownLoadApk(downUrl, apkName):
    path = sys.path[0]
    newPath = path + '\\apk'
    if os.path.exists(newPath):
        print newPath
    else:
        os.makedirs(newPath)
    urllib.urlretrieve(downUrl, newPath + "\\" + apkName)


if __name__ == '__main__':
    GetJson(0)
