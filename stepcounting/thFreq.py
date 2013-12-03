doLpf=False
baseTh=0
compensation=0
varTh=0.5
numtaps=10

#dataSet: 1D np.ndarray 
def countStep(dataSet, alpha, beta, debugMode):
    if debugMode:
        #figure()
        plot(dataSet, 'b')
        plot(Utils.getMmvarPrev(dataSet, LPF.WINSZ), 'y')
    
    k=0
    max=dataSet[k]
    i=k+1
    steps=0
    start=False
    for i, v in enumerate(dataSet):
        #从 i=1 开始：
        if i==0 or i==len(dataSet)-1:
            continue
#        if i<LPF.WINSZ-1:
#            va=0
#        else:
#            va=np.var(dataSet[i-LPF.WINSZ+1: i])
#        if va<0.015:
#            continue
        if Utils.maxMinVar(dataSet[i: i+numtaps])<varTh:
            #if i<80:
             #   print i, 'if Utils.maxMinVar(dataSet[i: i+LPF.WINSZ])<varTh:'
            #if not start:
             #   start
            continue
        #if i<80:
         #   print i, k, '--------------'
        th=alpha/(i-k)+beta
        #v 即论文中 accZ(i)
        #达到阈值，计一步：
        if v<dataSet[i+1] and max-v>=th and max-v>baseTh:
            if debugMode:
                c='m'
                w=2
                if i-k<3:
                    c='r'
                    w=2
                plot(range(k, i+1), dataSet[k: i+1], c, linewidth=w)
                plot(k, dataSet[k], 'rx')
                if steps%3==0:
                    annotate(steps, xy=(k, dataSet[k]), xycoords='data', xytext=(0,20), textcoords='offset points', \
                        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5), \
                        fontsize=12, arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=.2'))
                #print ('dataSet[k: i]:', i-k, k, i, dataSet[k:i])
                pass
            steps+=1
            k=i
            max=v
        else:
            if v>max:
                #if i<80:
                 #   print i, k,'if v>max:'
                max=v
                k=i
    return steps
    pass

def getThFreqFromDataFile(fname, look=0, baseTh=1.000, debugMode=False, labelManually=True):
    d=parseXml2dic(fname)
    if look==0:
        accWf=getAccWf(d)
        data=accWf[2]
    elif look==1:
        data=(d[Keys.kAx]**2+d[Keys.kAy]**2+d[Keys.kAz]**2)**0.5

    if labelManually:
        labelFname=fname.replace('.xml', '.x')
        pairs=parseThLabelFile(labelFname)
        #print pairs
        if debugMode:
            print("pairs [1]-[0]:", pairs[:,1]-pairs[:,0])
    else:
        pairs=None
    
    if doLpf:
        lpf=LPF()
        #data=lpf.lpfScipy(data)
        data=lpf.lpfTest(data, numtaps)
        #data=data[1010:1040]
    th_freq=getThFreqPointSet(data, pairs, baseTh, debugMode)
    ##print(data.shape, pairs, baseTh, debugMode)
    ##plot(th_freq[0], th_freq[1], 'ro')
    return th_freq

#批处理xml文件，得到所有 point set
def getThFreqFromDataFolder(folderPath, look=0, baseTh=1.000, debugMode=False, labelManually=True):
    res=array([[],[]])
    paths=glob(os.path.join(folderPath, '*.xml'))
    #print [os.path.basename(path) for path in paths]
    for path in paths:
        th_freq=getThFreqFromDataFile(path, look, baseTh, debugMode, labelManually)
        if debugMode:
            plot(th_freq[0], th_freq[1], 'o', label=os.path.basename(path))
        #res[0].extend(th_freq[0])
        #print('res.shape, th_freq.shape:', res.shape, th_freq.shape, path)
        res=np.append(res, th_freq, axis=1)
        #print res.shape
    legend()
    return res
    pass


#fname 可以是 fileName, 也可以是 folderName
#look: 0, look at accWF[2] (Z axis); 1, look at totalAccBF
def stepCountingTrain(fname, look=0, baseTh=1.0, debugMode=False, labelManually=True):
    if os.path.isdir(fname):
        func=getThFreqFromDataFolder
    else:
        func=getThFreqFromDataFile
    th_freq=func(fname, look, baseTh, debugMode, labelManually)
    pts=array([th_freq[0], th_freq[1]]).T
    return getInfimumParams(pts, doPlot=debugMode)
    pass

#fname 可以是 fileName, 也可以是 folderName
#return steps counted from file 'fname'
def stepCountingTest(fname, alpha, beta, look=0, debugMode=False):
    lpf=LPF()
    if os.path.isdir(fname):
        paths=glob(os.path.join(fname, '*.xml'))
        pass
    else:
        paths=[fname]
    
    #steps=[]
    steps={}
    for path in paths:
        d=parseXml2dic(path)
        if look==0:
            accWf=getAccWf(d)
            data=accWf[2]
        elif look==1:
            data=(d[Keys.kAx]**2+d[Keys.kAy]**2+d[Keys.kAz]**2)**0.5
        
        if doLpf:
            #data=lpf.lpfScipy(data)
            data=lpf.lpfTest(data, numtaps)
        s=countStep(data, alpha, beta, debugMode)
        s+=compensation
        #steps.append(s)
        steps[os.path.basename(path)]=s
    return steps
    pass

#print countStep(accWf[2], alpha, beta)
#print countStep(totalAcc, alpha, beta)