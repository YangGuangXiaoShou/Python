# -*- coding: utf-8 -*-
'''
author chaijingjing
date 2017/3/16

'''
import sys
import os
import subprocess
from os import path as osPath
import shutil
from operateExcel import operateMyExcel

COMMONDDUMP = "aapt.exe dump badging "
SINGN = " | findstr application-label:"
excelPath = ""
optexcel = operateMyExcel()


# remove apk
def removeSexApk(apkpath):
    newpath = osPath.dirname(apkpath) + "\\sexapk"
    if not osPath.exists(newpath):
        os.makedirs(newpath)
    shutil.move(apkpath, newpath)


# 移除非匹配到的apk
def removeOtherApk(apkpath):
    newpath = osPath.dirname(apkpath) + "\\otherapk"
    if not osPath.exists(newpath):
        os.makedirs(newpath)
    shutil.move(apkpath, newpath)


# read txt
def readTxt(apkpath, apkname):
    flag = False
    file = open(os.getcwd() + "\\SexApkname.txt")
    lines = file.readlines()
    for line in lines:
        # print "apkname = " + apkname
        # print "line = " + line.decode('gb2312').encode('utf8')
        try:
            if line.decode('gb2312').encode('utf8').strip() in apkname:
                flag = True
                break
        except Exception, e:
            print "error"
    return flag


# get apkname
def getApkName(apkpath):
    commanddump = COMMONDDUMP + apkpath + SINGN
    p = subprocess.Popen(commanddump, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                         shell=True)
    (output, err) = p.communicate()
    if output != "":
        apkname = output[19:-3]
        if (readTxt(apkpath, apkname)):
            removeSexApk(apkpath)
        else:
            removeOtherApk(apkpath)
    else:
        print "apkname read error"


if __name__ == "__main__":
    apk_dir = sys.argv[1]
    excelPath = apk_dir + "\\" + u"移动高风险工作日报.xls".encode("gb2312")
    for root, dirs, apkfile in os.walk(apk_dir):
        for apkpath in apkfile:
            getApkName(root + "\\" + apkpath)
    optexcel.create_everyday_excel(excelPath, apk_dir)
