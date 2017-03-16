# -*- coding: utf-8 -*-

'''
suthor chaijingjing
date:2017.3.14
'''
import sys
import subprocess
import os
import shutil

COMMONDINSTALL = "adb.exe install "
COMMONDUNINSTALL = "adb.exe uninstall "
COMMONDDUMP = "aapt.exe dump badging "
SINGNINSTALL = " | findstr Success "
SINGNPACKAGE = " | findstr package:"


def unstallapk(packagename):
    commandunstall = COMMONDUNINSTALL + packagename
    p = subprocess.Popen(commandunstall, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                         shell=True)
    (output, err) = p.communicate()
    print output


def getPackageName(apkpath):
    commanddump = COMMONDDUMP + apkpath + SINGNPACKAGE
    print commanddump
    p = subprocess.Popen(commanddump, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                         shell=True)
    (output, err) = p.communicate()
    # print "output" + output
    # data = re.findall("package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)'", str(output))
    packagename = output.split("'")[1]
    unstallapk(packagename)


def installApk(apkdir, apkpath):
    installPath = apkdir + "\\" + apkpath
    commondinstall = COMMONDINSTALL + installPath + SINGNINSTALL
    okDir = os.getcwd() + "\\" + "can_installed"
    noDir = os.getcwd() + "\\" + "can_not_installed"
    print commondinstall
    p = subprocess.Popen(commondinstall, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                         shell=True)
    (output, err) = p.communicate()
    if output != "":
        print "install success"
        if not os.path.exists(okDir):
            os.makedirs(okDir)
        newpath = okDir + "\\" + apkpath
        shutil.move(installPath, newpath)
        getPackageName(newpath)

    else:
        print "install failure"
        if not os.path.exists(noDir):
            os.makedirs(noDir)
        newpath1 = noDir + "\\" + apkpath
        shutil.move(installPath, newpath1)


if __name__ == "__main__":
    apk_dir = sys.argv[1]
    for root, dirs, apkfile in os.walk(apk_dir):
        for apkpath in apkfile:
            installApk(apk_dir, apkpath)
