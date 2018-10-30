# -*- coding:utf-8 -*-
import sys
import os
import shutil
import datetime
def as_num(x):
    if 'E9' not in x:
        return float(x)
    x = x.replace('E9','')
    y = float(x) * 1000000000
    return float(y)
def divide_platform(src):
#headinfo
    hp = os.path.join(src,'headinfo.txt');
    h = open(hp,'r').read()
    if 'iOS' in h:
        return 'iOS'
    elif 'android' in h:
        return 'android'

def iphone_type(src):
    dp = os.path.join(src,'deviceinfo.txt');
    file = open(dp,'r')
    for l in file:
        ls = tuple(l.split(':'))
        if 'PhoneType' in ls[0]:
            return ls[1]
def phone_information(src):
    h = divide_platform(src)
    d = iphone_type(src)
    return (h,d)

def _copy(src,dst):
    if os.path.exists(src):
        if not os.path.exists(dst):
            os.makedirs(dst)
        shutil.copy(src,  dst)
def finge_data(namep,name):
    src = namep + '/' + 'Finger_Print'
    fl = os.listdir(src)
    for f in fl:
        if f != '.DS_Store':
            fp = os.path.join(src,f)
            print 'Finger',fp
            (h,d) = phone_information(fp)
            st = ''
            et = ''
            fId = ''
            for f1 in os.listdir(fp):
                fp1 = os.path.join(fp,f1)
                if 'df' in f1:
                    (st,et,fId) = firstAndLastLine(fp1)
                    signal_data(namep, st, et,name,fp,fId)
            if len(fId) == 0 or len(st) == 0 or len(et) == 0:
                print 'error ',fp
                continue;
            for f1 in os.listdir(fp):
                fp1 = os.path.join(fp,f1)
                nf = f + '_' + name + '_' + d
                nf = nf.replace(' ', '-')
                nf = nf.replace('\n', '')
                dst = os.path.join(sys.argv[1],'result',h,fId,nf)
                if 'df' in f1 or 'ins' in f1 or 'deviceinfo' in f1 or 'headinfo' in f1:
                    _copy(fp1, os.path.join(dst,'finger_print'))
                if 'df' not in f1 and 'ins' not in f1:
                    _copy(fp1, dst)


def copy_signal_data(src,f,name,fpp,fId):
    print 'copy signal data',f
    (h,d) = phone_information(src)
    nf = f + '_' + name + '_' + d
    nf = nf.replace(' ', '-')
    nf = nf.replace('\n', '')
    print fId
    dst = os.path.join(sys.argv[1],'result',h,fId,nf)
    print dst
    i = 1
    sdst = dst
    while True:
        if os.path.exists(sdst):
            sdst = dst + str(i)
            i = i + 1
        else:
            dst = sdst
            break
    for f in os.listdir(src):
        if f != '.DS_Store':
            fp = os.path.join(src,f)
            _copy(fp, dst)
            for fpf in os.listdir(fpp):
                if f != '.DS_Store':
                    fpfp = os.path.join(fpp, fpf)
                    if 'df' in fpf or 'ins' in fpf or 'deviceinfo' in fpf or 'headinfo' in fpf:
                        _copy(fpfp,os.path.join(dst,'finger_print'))

def signal_data(src, st, et,name,fpp,fId):
    src = src + '/' + 'signal_data'
    fl = os.listdir(src)
    for f in fl:
        if f != '.DS_Store':
            fp = os.path.join(src,f)
            for f1 in os.listdir(fp):
                if f1 == 'allsensordata.txt':
                    f1p = os.path.join(fp,f1)
                    (sst, set, fid) = firstAndLastLine(f1p)
                    sst = float(as_num(sst))
                    set = float(as_num(set))
                    st = float(st)
                    et = float(et)
                    if not(set < st or sst > et):
                    #有交集则拷贝
                        copy_signal_data(fp,f,name,fpp,fId)
def firstAndLastLine(src):
    with open(src, 'rb') as f:  # 打开文件
    # 在文本文件中，没有使用b模式选项打开的文件，只允许从文件头开始,只能seek(offset,0)
        first_line = f.readline()  # 取第一行
        offset = -50  # 设置偏移量
        while True:
            """
            file.seek(off, whence=0)：从文件中移动off个操作标记（文件指针），正往结束方向移动，负往开始方向移动。
            如果设定了whence参数，就以whence设定的起始位为准，0代表从头开始，1代表当前位置，2代表文件最末尾位置。
            """
            lines = f.readlines()  # 读取文件指针范围内所有行
            if len(lines) < 2:
                return(0,0)
            f.seek(offset, 2)  # seek(offset, 2)表示文件指针：从文件末尾(2)开始向前50个字符(-50)
            if len(lines) >= 2:  # 判断是否最后至少有两行，这样保证了最后一行是完整的
                last_line = lines[-1]  # 取最后一行
                break
        # 如果off为50时得到的readlines只有一行内容，那么不能保证最后一行是完整的
        # 所以off翻倍重新运行，直到readlines不止一行
            offset *= 2
    st = tuple(first_line.split(','))[0]
    fId = tuple(last_line.split(','))[-2]
    et = tuple(last_line.split(','))[0]
    return (st, et,fId)



def main_function(src):
    fl = os.listdir(src)
    for f in fl:
        if f not in ['.DS_Store','result']:
            print 'persion name ', f
            finge_data(os.path.join(src,f),f)
if __name__=='__main__':
    if (len(sys.argv) == 2):
        rp = os.path.join(sys.argv[1],'result')
        if os.path.isdir(rp):
            shutil.rmtree(rp)
        main_function(sys.argv[1])
    else:
        print('***Error*** :请传入数据路径')

