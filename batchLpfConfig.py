#coding=utf-8
'''
batchLpf.py 对应配置脚本
随你怎么改参数
'''

#acc, gyro, mag, rotation
#若需单独对 mag 滤波， 则 sensors='m' 即可， 默认四个全滤波
sensors='agmr'

assert set(sensors) <= set('agmr'), "must be combinations of char 'a', 'g', 'm', 'r'"


#LPF hamming 窗口长度
#即 scipy.signal.firwin 参数 numtaps, 其余参数固定为 cutoff=40, nyq=800， 见 utils.py
winsz=10


#原始数据目录：
olddir=r'D:\Documents\Desktop\t'

#另存至目录：
newdir=r'D:\Documents\Desktop\t/shit'




