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
INVALID=-1000000
numtaps=10
doLpf=True
compensation=0

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
def getZeroLine(buf, begin=INVALID, end=INVALID):
    pc=0
    vc=0
    lastPeak=INVALID
    lastValley=INVALID
    
    psum=0
    vsum=0
    
    #存储波峰波谷的堆栈
    stack=[]
    pflag=1
    vflag=0
    
    if begin!=INVALID and end!=INVALID:
        buf=buf[begin: end]
        
    for k, v in enumerate(buf):
        if k==0 or k==len(buf)-1:
            continue
        forwardSlope=buf[k+1]-v
        backwardSlope=v-buf[k-1]
        
        #用stack
        # if forwardSlope*backwardSlope<0:
            # flag=pflag if forwardSlope<0 else vflag
            # if len(stack)==0:
                # stack.append([v, flag])
            # else:
                # if abs(v-stack[-1][0])<0.1:
                    # stack
            
        #一段中 pc, vc 至多算2个，防止静止时期的毛刺干扰（尽管lpf，毛刺仍存在）
        #peak:
        #abs(lastValley-v)>0.1 用于过滤掉中间没滤掉的褶皱， 下同。。
        if forwardSlope<0 and backwardSlope>0 and pc<2:# and abs(lastValley-v)>0.1:
            if abs(lastValley-v)<0.1:
                vsum-=lastValley
                vc-=1
                lastValley=INVALID
            else:
                lastPeak=v
                pc+=1
                psum+=v
                #print 'lastPeak, pc, psum:', lastPeak, pc, psum
        #valley
        if forwardSlope>0 and backwardSlope<0 and vc<2:# and abs(lastPeak-v)>0.1:
            if abs(lastPeak-v)<0.1:
                psum-=lastPeak
                pc-=1
                lastPeak=INVALID
            else:
                lastValley=v
                vc+=1
                vsum+=v
                #print 'lastValley, vc, vsum:', lastValley, vc, vsum
        

    #若波峰或波谷有一个不存在，以端点值为波峰or波谷
    if pc==0:
        #print 'if pc==0:'
        pc=2
        psum=buf[0]+buf[-1]
    #其实波峰or波谷只可能一个不存在：
    if vc==0:
        #print 'if vc==0:'
        vc=2
        vsum=buf[0]+buf[-1]
    
    pvmean=(psum*1./pc+vsum*1./vc)/2
    pvvar=var([psum*1./pc, vsum*1./vc])
    #print 'pvvar,psum,pc,vsum,vc, [psum*1./pc, vsum*1./vc]:', pvvar,psum,pc,vsum,vc, [psum*1./pc, vsum*1./vc]

    return pvmean, pvvar, 
    pass

#统计过零点次数
#PARAMS startp: 本段buf起点在全局中的位置
def getZccByZline(buf, zline, startp, debug=False, begin=INVALID, end=INVALID ):
    global lastZcrossIdx
    if debug:
        #if startp>4200:
        plot(arange(len(buf))+startp, buf, lw=2)
    
    
    if begin!=INVALID and end!=INVALID:
        buf=buf[begin: end]
    buf=asanyarray(buf)
    #zero-crossing count:
    zcc=0
    sc=0
    for k, v in enumerate(buf):
        if k==0:
            continue
        vprev=buf[k-1]
        if (v-zline)*(vprev-zline)<0 :
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
def countStep(data, varTh, bufsz, debug, scTh=5):
    global lastZcrossIdx
    lastZcrossIdx=0

    assert type(bufsz)==int and bufsz>0, 'type(bufsz)==int and bufsz>0'
    
    #data=data[:300]
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
            #if i>1200 and i<1310:
             #   print 'i:', i
            zline, va=getZeroLine(buf)
            #if i>1200 and i<1310:           
             #   print 'zline, va:', zline, va
            if debug:
                plot([i+1-bufsz, i], [va]*2, 'c')
                plot([i+1-bufsz, i], [zline]*2, 'y')
            
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
                #zcc+=getZccByZline(buf, zline, i+1-bufsz, debug)
                sc+=getZccByZline(buf, zline, i+1-bufsz, debug)
                #print 'sc:', sc
                if debug:
                    plot([i+1-bufsz, i], [zline]*2, 'r')
                    
                buf[:overlap+1]=buf[-(overlap+1):]
                del buf[overlap+1:]
    #return zcc/2
    return sc
    pass
   
#fname 可以是文件名，也可为文件夹名
def countStepByZcross(fname, look, bufsz, varTh=1, debug=False):
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
        if doLpf:
            data=lpf.lpfTest(data, numtaps)
        s=countStep(data, varTh, bufsz, debug)
        steps[os.path.basename(path)]=s+compensation
    return steps
    pass

figure()

fname=r'D:\Documents\Desktop\step-counting-data\old-linear\segmented\slow\ZC40slow_a9_1.xml'
fname=r'D:\Documents\Desktop\segmented-mixed\p3.1_Male_20-29_170-179cm_Hand_held.xml'
fname=r'D:\Documents\Desktop\step-counting-data\zcrun\old-linear\segmented\ZCrun120_a9_5.xml'
fname=r'D:\Documents\Desktop\segmented-mixed\LH31fast_a9_0.xml'
fname=r'D:/Documents/Desktop/step-counting-data/old-linear/segmented/HY60fast_a9_0.xml'

numtaps=10
doLpf=True
compensation=-0
steps=countStepByZcross(fname, look=1, varTh=0.5, bufsz=33, debug=True)
print steps





















#-----------------------------------------dyZcrossOnline

varTh=0.5

bufsz=10
s2ns=1000

i=0
steps=0
start=False
fps=INVALID
winsz=INVALID

cbufts=[]
cbufv=[]
cbufvlpf=[]

hamwin=[]
overlap=1
lastZcrossIdx=0

tmp=[]

def getHammingWin(n):
    res=[]
    sum=0;
    for i in range(n):
        res.append(0.54-0.46*np.cos(2*np.pi*i/(n-1)) )
        sum+=res[-1]
    res=np.asanyarray(res)
    res/=sum
    return res

#返回 idx=-1 对应的lpf后的值
def getDataLpf(buf, hamwin):
    n=len(buf)-1
    y=0
    for i, v in enumerate(hamwin):
        if n<i:
            break
        y+=v*buf[n-i]
    return y
    pass

def getDataLpf2(buf, hamwin):
    n=len(buf)-1
    if n<len(hamwin)-1:
        return mean(buf)
    y=0
    for i, v in enumerate(hamwin):
        y+=v*buf[n-i]
    return y
    pass

def dyZcrossOnline(value, ts, doLpf=False):
    global fps
    global winsz
    
    global i
    global steps
    global hamwin
    global start
    
    global tmp
    
    #print 'i', i
    if len(cbufv) !=0:
        tmp.append(cbufvlpf[-1])
    
    #这次假设没有‘第一帧’问题
    if i<bufsz:
        cbufts.append(ts)
    elif fps==INVALID:
        fps=int(s2ns*(bufsz-1)*1.0/(cbufts[bufsz-1]-cbufts[0]))
        winsz=int(fps/3);
        hamwin=getHammingWin(winsz)
        
    cbufv.append(value)
    if fps==INVALID:
        cbufvlpf.append(value)
    else:
        cbufvlpf.append(getDataLpf2(cbufv, hamwin))
    
    if fps==INVALID or len(cbufv)<winsz*2:
        i+=1
        return steps
    #若 i>=winsz*2:
    if doLpf:
        buf=cbufvlpf
    else:
        buf=cbufv
    
    va=Utils.maxMinVar(buf[:winsz])
    va=max(Utils.maxMinVar(buf[:winsz]), Utils.maxMinVar(buf[winsz-1:winsz*2-1]) )
    zline=getZeroLine(buf, 0, winsz)[0]
    plot([i+1-winsz*2, i-winsz], [va]*2, 'c')
    plot([i+1-winsz*2, i-winsz], [zline]*2, 'y')
    
    #print 'winsz', winsz
    if va<varTh:# \
    #and Utils.maxMinVar(buf[winsz-1:winsz*2-1])<varTh:
        del cbufv[:winsz]
        del cbufvlpf[:winsz]
        if start:
            start=False
            axvline(i, c='y')
    else:
        if not start:
            start=True
            axvline(i+1-winsz*2, c='r', lw=2)
            
        steps+=getZccByZline(buf, zline, i+1-winsz*2, debug=True, begin=0, end=winsz)
        del cbufv[:winsz-overlap]
        del cbufvlpf[:winsz-overlap]
    i+=1
    return steps


#fname=r'D:/Documents/Desktop/step-counting-data/old-linear/segmented/ZC30fast_a9_0.xml'
figure()
d=parseXml2dic(fname)
data=(d[Keys.kAx]**2+d[Keys.kAy]**2+d[Keys.kAz]**2)**0.5
lpf=LPF()
dlpf=lpf.lpfTest(data)
d11=lpf.lpfTest(data, 11)
tslist=d[Keys.kTs]
#plot(tslist, data)
#plot(data, 'b', dlpf, 'r')
#plot(d11, 'g')
plot(dlpf, 'r')

#diff(tslist)
for j in range(len(tslist)):
    s2=dyZcrossOnline(data[j], tslist[j], True)

#plot(tmp, 'c')
print "online:", s2
