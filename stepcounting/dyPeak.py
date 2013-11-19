
'''==================================第二篇论文，动态peak方法
'''
#数据包含慢走时，因为手机位于身体一侧，另一侧peak检测不到， 很差

# N=50
# a2=a[600:6600]
# d=lpf.lpfTest2(a2, N)

# buf=[]
# bufsz=100
# sc=0
# #论文两个系数
# C=0.68
# K=10

%cd E:\workspace\PyCeshi\curveViewer
from utils import LPF, Utils
from stepcounting.scUtils import *
from glob import glob

#debug 没用到
def getPeakMean(buf, debug=False):
    pc=0
    psum=0
    for k, v in enumerate(buf):
        if k==0 or k==len(buf)-1:
            continue
        forwardSlope=buf[k+1]-v
        backwardSlope=v-buf[k-1]
        if forwardSlope<0 and backwardSlope>0:
            pc+=1
            psum+=v
    pmean=psum*1.0/pc
    return pmean

def getStepByPmean(buf, pmean, baseTh, coeff, startp, debug=False):
    if debug:
        #plot(arange(len(buf))+startp, buf, lw=2)
        pass
    sc=0
    for k, v in enumerate(buf):
        if k==0 or k==len(buf)-1:
            continue
        forwardSlope=buf[k+1]-v
        backwardSlope=v-buf[k-1]
        if forwardSlope<0 and backwardSlope>0 and v>coeff*pmean and v>baseTh:
            sc+=1
            if debug:
                plot(startp+k, v, 'rx')
    return sc

#PARAMS scTh: 如果一次开始结束没有达到 scTh, 属于误计步，抛弃
def countStep(data, baseTh, coeff, debug, bufsz=31, varTh=0.07, scTh=5):
    assert type(bufsz)==int and bufsz>0, 'type(bufsz)==int and bufsz>0'
    if debug:
        #print(data)
        plot(data)
        #plot(Utils.getVarPrev2(data, bufsz))
        #plot(Utils.getVarPrev(data, bufsz))
    
    #peak方法需要窗口重叠，否则可能峰值恰好位于边界，漏计步
    overlap=1
    buf=[]
    sc=0
    start=False
    #-----------------'模拟生成一帧一帧信号过程'
    for i,v in enumerate(data):
        buf.append(v)
        if len(buf)==bufsz:
            va=np.var(buf)
            #方差是否足够大？
            if va<varTh:
                del buf[:]
                if start:
                    start=False
                    if sc<scTh:
                        sc=0
                    
                    if debug:
                        axvline(i, c='y')
                #continue
            #即 va>=0.1 时：
            else:
                pmean=getPeakMean(buf)
                
                if not start:
                    start=True
                    if debug:
                        axvline(i, c='r', lw=2)
                        pass
                else:
                    if debug:
                        plot([i+1-bufsz, i], [pmean]*2, 'r')
                    sc+=getStepByPmean(buf, pmean, baseTh, coeff, i+1-bufsz, debug=debug)
                
                buf[:overlap+1]=buf[-(overlap+1):]
                del buf[overlap+1:]
                
    return sc
    pass

    
def countStepByPeak(fname, look, baseTh, coeff, debug=False):
    lpf=LPF()
    if os.path.isdir(fname):
        paths=glob(os.path.join(fname, '*.xml') )
    else:
        paths=[fname]
    
    steps={}
    for path in paths:
        d=parseXml2dic(path)
        if look==0:
            accWf=getAccWf(d)
            data=accWf[2]
        elif look==1:
            data=(d[Keys.kAx]**2+d[Keys.kAy]**2+d[Keys.kAz]**2)**0.5
        #data=lpf.lpfScipy(data)
        data=lpf.lpfTest(data)
        s=countStep(data, baseTh, coeff, debug)
        #print path, s
        steps[os.path.basename(path)]=s
    return steps
    pass

figure()
fname=r'D:\Documents\Desktop\traces\oldxml\old-linear\segmented\p8.2_Male_20-29_170-179cm_Trousers_back_pocket.xml'
#fname=r'D:\Documents\Desktop\traces\oldxml\old-linear\segmented'
steps=countStepByPeak(fname, look=1, baseTh=9., coeff=0.8, debug=True)
print steps