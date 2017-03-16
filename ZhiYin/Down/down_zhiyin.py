# -*- coding: utf-8 -*-

from os import path as osPath
import os, sys
from selenium import webdriver
import urllib
from selenium.common.exceptions import NoSuchElementException

"""
author sillygirl
date 2017 2
"""


class DownLoad:
    def __init__(self, mainUrl, begin=0, end=-1, driver=None):
        """
        :param mianUrl: 漫画首地址
        :param begin: 章节开始
        :param end: 章节结束
        :param save_folder:
        :param driver: 驱动
        """
        self.mainUrl = mainUrl
        self.begin = begin
        self.end = end
        self.folder = sys.path[0] + "\\result"
        self.browser = webdriver.PhantomJS(driver)
        self.chapter = []

        # 创建文件夹
        if not osPath.exists(self.folder):
            os.makedirs(self.folder)
        self.get_chapter()

    # 获取章节
    def get_chapter(self):
        self.browser.get(self.mainUrl)
        chapterList = self.browser.find_elements_by_css_selector("#chapterList li a")
        chapterList.reverse()  # 倒序
        for chapter in chapterList:  # chapter 章节
            self.chapter.append((chapter.text, chapter.get_attribute('href')))  # 章节和相应的链接

    @staticmethod
    def downloadImage(imageUrl, saveImageFolder):
        try:
            urllib.urlretrieve(imageUrl, saveImageFolder)
        except Exception, et:
            print et.message

    # 下载特定章节
    def download_chapter(self, chapter_id):
        downloadUrl = self.chapter[chapter_id][1]
        downloadChapter = self.chapter[chapter_id][0]
        saveFolder = osPath.join(self.folder, downloadChapter)
        if not osPath.exists(saveFolder):
            os.makedirs(saveFolder)
        self.browser.get(downloadUrl)
        datapage = 1
        while True:
            imageUrl = self.browser.find_elements_by_class_name("comicimg")[0].get_attribute("src")  # 图片的下载地址
            saveImageFolder = osPath.join(saveFolder, str(datapage) + ".jpg")
            print imageUrl + "     " + saveImageFolder
            self.downloadImage(imageUrl, saveImageFolder)
            self.browser.find_element_by_link_text("下一页").click()
            try:
                pageNum = self.browser.find_elements_by_xpath("//option[@selected='']")[0].text
                # print isinstance(pageNum,unicode)
                if unicode(pageNum)[1:-1].split("/")[0] == unicode(pageNum)[1:-1].split("/")[1]:
                    datapage += 1
                    imageUrl = self.browser.find_elements_by_class_name("comicimg")[0].get_attribute("src")  # 图片的下载地址
                    saveImageFolder = osPath.join(saveFolder, str(datapage) + ".jpg")
                    self.downloadImage(imageUrl, saveImageFolder)
                    break
                else:
                    datapage += 1
            except NoSuchElementException:
                print "error"

    def main(self):
        begin = self.begin if self.begin >= 0 else 0
        end = self.end if self.end >= 0 else len(self.chapter)
        for chapterid in xrange(begin, end):
            self.download_chapter(chapterid)
