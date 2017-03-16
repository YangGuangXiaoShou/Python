# -*- coding: utf-8 -*-
'''
author chaijingjing
date 2017/3/16

'''
import os
import datetime
import hashlib
import xlwt
import zipfile
from xlwt import *

you_name = u'柴晶晶'
Android = 'Android'
virus = u'病毒'
put_lib = u'是'
apk_path = ''
virusdata = []

COMMONDDUMP = "aapt.exe dump badging "
SINGN = " | findstr application-label:"


class operateMyExcel():
    def __init__(self):
        you_name = u'柴晶晶'
        Android = 'Android'
        virus = u'病毒'
        put_lib = u'是'
        apk_path = ''
        virusdata = []
        grades = {u'Payment': u'高', u'Privacy': u'高', u'Remote': u'高', u'Spread': u'中', u'Expense': u'中',
                  u'System': u'中', u'Fraud': u'低', u'Rogue': u'低'}

    # get current time  year/month/day
    def getDate(self):
        return datetime.datetime.now().strftime('%Y/%m/%d').decode('GB18030')

    # 获取文件MD5
    def GetFileMD5(self, file):
        fileinfo = os.stat(file)
        if int(fileinfo.st_size) / (1024 * 1024) > 1000:
            return self.GetBigFileMD5(file)
        m = hashlib.md5()
        mfile = open(file, "rb")
        m.update(mfile.read())
        mfile.close()
        return m.hexdigest().upper().decode('GB18030')

    # 获取大文件MD5
    def GetBigFileMD5(self, file):
        m = hashlib.md5()
        f = open(file, 'rb')
        maxbuf = 8192
        while 1:
            buf = f.read(maxbuf)
            if not buf:
                break
            m.update(buf)
        f.close()
        return m.hexdigest().upper().decode('GB18030')

    def create_everyday_excel(self, file_name, apk_path):

        global you_name
        global Android
        global viruss
        global put_lib
        print 'create_everyday_excel'
        self.apk_path = apk_path
        print self.apk_path
        self.book = xlwt.Workbook(file_name)
        self.create_sex_sheet(apk_path)
        self.create_normal_sheet(apk_path)
        self.book.save(file_name)

    # 创建色情类样本表
    def create_sex_sheet(self, apk_path):
        '''
        @SHEEET1: 病毒sheet
        '''
        global you_name
        global Android
        global viruss
        global put_lib

        sheet1 = self.book.add_sheet(u"病毒")

        row = [u'ID', u'日期', u'样本MD5', u'恶意程序名称(英文)', u'恶意程序名称(中文)', u'主属性分类', u'其它属性分类', u'危害级别', u'影响平台', u'恶意程序种类',
               u'简要特征描述', u'控制或下载url', u'扣费SP号码', u'风险等级评分', u'是否入库', u'研判人员', u'样本来源地址', u'备注']

        for i in range(0, len(row)):  # 生成第一行
            sheet1.write(1, i, row[i], self.setFist_row_Style())
        sheet1.write_merge(0, 0, 0, len(row) - 1, u'移动高风险样本工作日报', self.set_title_Style())
        # sheet1.write_merge(0,0,0,len(row)-1,u'移动高风险样本工作日报',self.set_style('Times New Roman',300,True,True)) #合并行单元格
        sexapklist = self.get_apk_list(apk_path + "\\" + "sexapk")
        if len(sexapklist) > 0:
            cont = 2
            for apk in sexapklist:
                sheet1.write(cont, 0, cont - 1, self.setMainStyle())
                sheet1.write(cont, 1, self.getDate(), self.setMainStyle())
                # sheet1.write(cont,1,datetime.datetime.now())
                sheet1.write(cont, 2, self.GetFileMD5(apk), self.setMainStyle())
                sheet1.write(cont, 3, u'', self.setMainStyle())
                sheet1.write(cont, 4, u'', self.setMainStyle())
                sheet1.write(cont, 5, u'', self.setMainStyle())
                sheet1.write(cont, 6, u'', self.setMainStyle())
                sheet1.write(cont, 7, u'', self.setMainStyle())
                sheet1.write(cont, 8, u'Android', self.setMainStyle())
                sheet1.write(cont, 9, u'病毒', self.setMainStyle())
                sheet1.write(cont, 10, u'', self.setMainStyle())
                # sheet1.write(cont,11,u'http://baidu.com',borders_style())
                sheet1.write(cont, 11, u' ', self.setMainStyle())
                # sheet1.write(cont,12,u'SP号码',borders_style())
                sheet1.write(cont, 12, u' ', self.setMainStyle())
                sheet1.write(cont, 13, u' ', self.setMainStyle())
                sheet1.write(cont, 14, u'', self.setMainStyle())
                sheet1.write(cont, 15, you_name, self.setMainStyle())
                sheet1.write(cont, 16, u'', self.setMainStyle())
                # sheet1.write(cont,17,'',format2)
                sheet1.write(cont, 17, self.initialName(apk), self.setMainStyle())
                sheet1.write(cont, 18, u'', self.setMainStyle())
                cont = cont + 1

    # 创建非色情类表
    def create_normal_sheet(self, apk_path):
        '''
        @SHEEET2: 风险sheet
        '''
        global you_name

        row = [u'ID', u'日期', u'样本名称', u'样本MD5', u'风险等级评分', u'包含风险', u'研判人员', u'备注', u'风险英文名称', u'风险中文名称', u'受影响操作系统',
               u'危害类型', u'评分缘由']
        sheet2 = self.book.add_sheet(u'风险')
        sheet2.write_merge(0, 0, 0, len(row) - 1, u'移动高风险样本工作日报', self.set_title_Style())

        # sheet2.write_merge(0,0,0,7,u'移动高风险样本工作日报',self.set_style('Times New Roman',300,True,True)) #合并行单元格

        for i in range(0, len(row)):  # 生成第一行
            sheet2.write(1, i, row[i], self.setFist_row_Style())
        apklist = self.get_apk_list(apk_path + "\\otherapk")
        if len(apklist) > 0:
            cont = 2
            for apk in apklist:
                print "apk = " + apk
                sheet2.write(cont, 0, cont - 1, self.setMainStyle())
                sheet2.write(cont, 1, self.getDate(), self.setMainStyle())
                # sheet2.write(cont,1,datetime.datetime.now())
                sheet2.write(cont, 2, u'', self.setMainStyle())
                sheet2.write(cont, 3, self.GetFileMD5(apk), self.setMainStyle())
                sheet2.write(cont, 4, u'', self.setMainStyle())
                sheet2.write(cont, 5, u'', self.setMainStyle())
                sheet2.write(cont, 6, you_name, self.setMainStyle())
                sheet2.write(cont, 7, u'', self.setMainStyle())
                sheet2.write(cont, 8, u'', self.setMainStyle())
                sheet2.write(cont, 9, u'', self.setMainStyle())
                sheet2.write(cont, 10, u'Android', self.setMainStyle())
                sheet2.write(cont, 11, u'', self.setMainStyle())
                sheet2.write(cont, 12, self.initialName(apk), self.setMainStyle())
                cont = cont + 1

    # 设置标题格式
    def set_title_Style(self):
        # 边框
        borders = Borders()
        borders.bottom = 1
        borders.left = 1
        borders.right = 1
        borders.top = 1
        # 字体
        font = Font()
        font.bold = True
        font.name = 'SimSun'
        font.height = 400
        # 背景
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 5
        # 居中
        ali = Alignment()
        ali.horz = Alignment.HORZ_CENTER
        ali.vert = Alignment.VERT_CENTER
        style = XFStyle()
        style.borders = borders
        style.pattern = pattern
        style.font = font
        style.alignment = ali
        return style

    # 设置第一行的格式
    def setFist_row_Style(self):
        # 边框
        borders = Borders()
        borders.bottom = 1
        borders.left = 1
        borders.right = 1
        borders.top = 1
        # 字体
        font = Font()
        font.bold = True
        font.name = 'SimSun'
        font.height = 250
        # 居中
        ali = Alignment()
        ali.horz = Alignment.HORZ_CENTER
        ali.vert = Alignment.VERT_CENTER
        style0 = XFStyle()
        style0.borders = borders
        style0.font = font
        style0.alignment = ali
        return style0

    # 设置内容格式
    def setMainStyle(self):
        # 边框
        borders = Borders()
        borders.bottom = 1
        borders.left = 1
        borders.right = 1
        borders.top = 1
        # 字体
        font = Font()
        font.name = 'SimSun'
        font.height = 240
        # 居中
        ali = Alignment()
        ali.horz = Alignment.HORZ_CENTER
        ali.vert = Alignment.VERT_CENTER
        style1 = XFStyle()
        style1.borders = borders
        style1.font = font
        style1.alignment = ali
        return style1

    # 读取色情软件信息
    def read_virusdata(self, file_path):
        virusdata = []
        fo = open(file_path, 'r')
        for pattern in fo.readlines():
            virusdata.append(pattern.strip())
            fo.close()
            return virusdata

    # 获取风险apk
    def get_apk_list(self, file_path):
        apklist = []
        for parent, dirnames, apkname_list in os.walk(file_path):
            # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for apkname in apkname_list:
                if apkname.find(".apk") != -1:
                    apklist.append(parent + '\\' + apkname)
        return apklist

    # 获取安装名称
    def initialName(self, apkpath):
        istlname = ''
        try:
            file_zip = zipfile.ZipFile(apkpath, 'r')
            tr = 'AndroidManifest.xml' in file_zip.namelist()
            if tr == False:
                return istlname
            maniFest = 'aapt.exe  dump badging ' + apkpath + '>info.txt'
            info = os.system(maniFest)
            finfo = open('info.txt', 'r')
            filecontent = finfo.read()
            findposition = filecontent.find('application-label-zh_CN:')
            istlname = filecontent[findposition + 8: -1].split('\'')[1].strip()
            if istlname == '' or findposition == -1:
                findposition = filecontent.find('application-label-zh:')
                istlname = filecontent[findposition + 18: -1].split('\'')[1].strip()
                if istlname == '' or findposition == -1:
                    findposition = filecontent.find('application-label:')
                    istlname = filecontent[findposition + 18: -1].split('\'')[1].strip()
                    if istlname == '' or findposition == -1:
                        findposition = filecontent.find('  label=\'')
                    istlname = filecontent[findposition + 18: -1].split('\'')[1].strip()
            istlname = istlname.replace(' ', '')
            istlname = istlname.decode('utf-8', 'ignore').encode('GB18030', 'ignore')
            istlname = unicode(istlname, "GB18030")

            finfo.close()
            # return istlname
        except:
            pass
        return istlname
