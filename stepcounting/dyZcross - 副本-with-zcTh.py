#===============================================自己用动态过零点方法

# N=50
# a2=a[600:6600]
# d=lpf.lpfTest2(a2, N)
# #plot(a2)
# plot(d)

# buf=[]
# bufsz=101
# INVALID=-1000000
# zline=INVALID
# sc=0
# zcc=0

%cd E:\workspace\PyCeshi\curveViewer
from utils import LPF, Utils
from stepcounting.scUtils import *
from glob import glob

lastZcrossIdx=0

#计算buf对应的新零线：
def getZeroLineOld(buf):
    #peak and valley
    pvc=0
    pvsum=0
    for k, v in enumerate(buf):
        if k==0 or k==len(buf)-1:
            continue
        forwardSlope=buf[k+1]-v
        backwardSlope=v-buf[k-1]
        if forwardSlope<0 and backwardSlope>0 or forwardSlope>0 and backwardSlope<0:
            pvc+=1
            pvsum+=v
    pvmean=pvsum/pvc
    return pvmean
    pass

#计算buf对应的新零线
#pmean 求解方法不要 peak-valley 统一算均值，分开算：
def getZeroLine(buf):
    pc=0
    vc=0
    psum=0
    vsum=0
    for k, v in enumerate(buf):
        if k==0 or k==len(buf)-1:
            continue
        forwardSlope=buf[k+1]-v
        backwardSlope=v-buf[k-1]
        #peak:
        if forwardSlope<0 and backwardSlope>0:
            pc+=1
            psum+=v
        if forwardSlope>0 and backwardSlope<0:
            vc+=1
            vsum+=v

    #若波峰或波谷有一个不存在，以端点值为波峰or波谷
    if pc==0:
        pc=2
        psum=buf[0]+buf[-1]
    #其实波峰or波谷只可能一个不存在：
    if vc==0:
        vc=2
        vsum=buf[0]+buf[-1]
    pvmean=(psum*1./pc+vsum*1./vc)/2
    pvvar=var([psum*1./pc, vsum*1./vc])

    return pvmean, pvvar, 
    pass

#统计过零点次数
#PARAMS zcTh: 过零点前后两点高度差
def getZccByZline(buf, zline, zcTh, startp, debug=False):
    global lastZcrossIdx
    if debug:
        #if startp>4200:
        plot(arange(len(buf))+startp, buf, lw=2)
    
    buf=asanyarray(buf)
    #zero-crossing count:
    zcc=0
    sc=0
    for k, v in enumerate(buf):
        if k==0:
            continue
        vprev=buf[k-1]
        if (v-zline)*(vprev-zline)<0 and abs(v-vprev)>zcTh:
            zcc+=1
            if v-zline<0 and startp+k-lastZcrossIdx>2.0:
                sc+=1
                lastZcrossIdx=startp+k
                #此buf起点在全局的位置：
                #print 'startp, k:', startp, k
                if debug:
                    plot([startp+k-1, startp+k], [vprev, v], 'r', lw=3.5)
    #return zcc
    return sc
    pass

#PARAMS scTh: 如果一次开始结束没有达到 scTh, 属于误计步，抛弃
def countStep(data, zcTh, varTh, debug, bufsz=31, scTh=5):
    global lastZcrossIdx
    lastZcrossIdx=0

    assert type(bufsz)==int and bufsz>0, 'type(bufsz)==int and bufsz>0'
    
    #data=data[:385]
    if debug:
        plot(data)

    #zcross方法也需要窗口重叠，否则可能下降线恰好穿过边界，漏计步
    overlap=01
    buf=[]
    sc=0
    zcc=0
    start=False
    #-----------------'模拟生成一帧一帧信号过程'
    for i,v in enumerate(data):
        buf.append(v)
        if len(buf)==bufsz:
            #va=np.var(buf)
            zline, va=getZeroLine(buf)
            if debug:
                plot([i+1-bufsz, i], [va]*2, 'c')
            
            if va<varTh:
                del buf[:]
                if start:
                    start=False
                    #if zcc<2*scTh:
                     #   zcc=0
                    if sc<scTh:
                        sc=0
                    if debug:
                        axvline(i, c='y')
            #即 va>=varTh 时：
            else:
                if not start:
                    start=True
                    if debug:
                        axvline(i+1-bufsz, c='r', lw=2)
                        pass
                
                #zline=getZeroLine(buf)
                #zcc+=getZccByZline(buf, zline, zcTh, i+1-bufsz, debug)
                sc+=getZccByZline(buf, zline, zcTh, i+1-bufsz, debug)
                #print 'sc:', sc
                if debug:
                    plot([i+1-bufsz, i], [zline]*2, 'r')
                    
                buf[:overlap+1]=buf[-(overlap+1):]
                del buf[overlap+1:]
    #return zcc/2
    return sc
    pass
   
#fname 可以是文件名，也可为文件夹名
def countStepByZcross(fname, look, zcTh, varTh=1, debug=False):
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
        s=countStep(data, zcTh, varTh, debug)
        steps[os.path.basename(path)]=s
    return steps
    pass

figure()
fname=r'D:\Documents\Desktop\traces\oldxml\old-linear\segmented\p13.4_Female_20-29_160-169cm_Backpack.xml'
fname=r'D:\Documents\Desktop\step-counting-data\old-linear\segmented\slow\ZC30slow_a9_0.xml'
#zcTh不应作为评判误计步的依据，暂时置零
steps=countStepByZcross(fname, look=1, zcTh=0.0, varTh=0.1, debug=True)
print steps