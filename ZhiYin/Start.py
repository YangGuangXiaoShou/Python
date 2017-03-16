# -*- coding: utf-8 -*-

"""
autor:sillgirl
date :2017 2
下载知音漫客中的网游之近战法师 漫画
如需下载其他漫画   更改mianUrl
"""
from Down import down_zhiyin as downloadZhiyin

if __name__ == "__main__":
    mainUrl = "http://www.zymk.cn/14/"
    download = downloadZhiyin.DownLoad(mainUrl, 0, -1,'phantomjs.exe')
    download.main()