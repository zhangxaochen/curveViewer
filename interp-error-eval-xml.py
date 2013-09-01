# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import os, sys, time, glob
from utils import Keys
from scipy.interpolate import interp1d
from pylab import *
from lxml import etree

folderPath=raw_input("input the xml files folder:\n")
folderPath=folderPath if folderPath !='' else r'D:\Documents\Desktop\fff'
if not os.path.isdir(folderPath):
    sys.exit("%s is not a valid path, terminating~~"%folderPath)

os.chdir(folderPath)
print os.getcwd()

# <codecell>

import numpy as np

def wrapNdarray(arr):
    return arr if isinstance(arr, np.ndarray) else np.array(arr)

#(xarr, data) → (x, y)
#target: contains only 0/1, 0:fit; 1:test points
def errorEval(xarr, data, target, kind):
    assert hasattr(xarr, '__getitem__')
    assert hasattr(data, '__getitem__')
    assert hasattr(target, '__getitem__')
    assert set(target) == {0,1}
    
    xarr=wrapNdarray(xarr)
    data=wrapNdarray(data)
    target=wrapNdarray(target)
    
    x_fit=xarr[target==0]
    y_fit=data[target==0]
    x_test=xarr[target==1]
    y_test=data[target==1]
    
    f=interp1d(x_fit, y_fit, kind=kind)
    sum=0
    y_test_estimate=f(x_test)
    assert y_test.shape == y_test_estimate.shape
    
    error=np.sum((y_test_estimate-y_test)**2)/len(y_test)
    return error

def testErrorEval():
    xarr=[.5, 1., 1.5]
    data=[0, 3.5, 2]
    print errorEval(xarr, data, [0,1,0], 1)

testErrorEval()

# <codecell>

cntLinear=0
cntCubic=0
percent=0
tLinear=0
tCubic=0
flog=open('errorEval.log', 'w')
flog.write('===============+++++++++++square errors:\n')
# flog.close()

oldRootTag='CaptureSession'
newRootTag='session'

xmlFileList=glob.glob('*.xml')
psr=etree.XMLParser(remove_blank_text=True)
for idx, fname in enumerate(xmlFileList):
    tree=etree.parse(fname, parser=psr)
    root=tree.getroot()
    print(root.tag, fname)
    if root.tag == oldRootTag :
		print('++++++++old style xml (CaptureSession)')
		continue
	
    if root.tag != newRootTag :
		print('-----------probably wrong xml folder')
		continue

    threadList=root.find(Keys.kThreads).findall(Keys.kThread)
	#========手机只算一个节点
    assert len(threadList) is 1
    thread=threadList[0]
    channelList=thread.find(Keys.kChannels).findall(Keys.kChannel)
    assert len(channelList) is 4

    #data=dict(a=[], g=[], m=[], r=[])
    data={Keys.kA:[], Keys.kG:[], Keys.kM:[], Keys.kR:[]}
    #--------对每个传感器，目前 a, g, m, r：
    for c in channelList:
        cname=c.find(Keys.kName).text
        frameList=c.find(Keys.kFrames).findall(Keys.kFrame)
        #-------------对每一帧：
        valList=[]
        for idx, f in enumerate(frameList):
            ts=float(f.find(Keys.kTime).text)
            if idx is 0:
                #print('ts:', ts, type(ts))
                pass
            v=f.find(Keys.kValue)
            vx=float(v.find(Keys.kX).text)
            vy=float(v.find(Keys.kY).text)
            vz=float(v.find(Keys.kZ).text)
            #vw 不一定有意义：
            vw=float(v.find(Keys.kW).text)
            
            valList.append([ts, vx, vy, vz, vw])
            data[cname]=np.array(valList)
        
        #每个元件只看 x 通道
        tmp=np.array(data[cname])
        tmp=tmp if len(tmp)%2==1 else np.delete(tmp, -1, axis=0)
        tmp=tmp.T
        xarr=tmp[0]
        for k in [1,]:
            print '#####'
            yarr=tmp[k]
            target=[0 if i%2==0 else 1 for i in range(len(xarr))]
            #print target, len(xarr)
            t1=time.time()
            errLinear=errorEval(xarr, yarr, target, 1)
            t2=time.time()
            errCubic=errorEval(xarr, yarr, target, 3)
            t3=time.time()
            tLinear+=(t2-t1)
            tCubic+=(t3-t1)
        
            percent+=errLinear*1.0/errCubic
            d=errLinear-errCubic
            if d<0:
                cntLinear+=1
            else:
                cntCubic+=1
            print '+' if d>0 else '-', ' linear: ', errLinear, '\t\tcubic',  errCubic
            flog.write('%s\t%s\t%s\n'%('+' if d>0 else '-', errLinear, errCubic) )
print "=====================cntLinear, cntCubic", cntLinear, cntCubic, percent/(len(xmlFileList)*4)
print "===============tLinear, tCubic:", tLinear, tCubic
flog.write("=============cntLinear, cntCubic: %s\t%s\t%s\n"%(cntLinear, cntCubic, percent/(len(xmlFileList)*4) ))
flog.write("========tLinear, tCubic: %s\t%s"%( tLinear, tCubic) )
flog.close()
# <codecell>


