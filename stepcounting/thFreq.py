#dataSet: 1D np.ndarray 
def countStep(dataSet, alpha, beta, debugMode):
    if debugMode:
        #figure()
        plot(dataSet, 'b')
    
    k=0
    max=dataSet[k]
    i=k+1
    steps=0
    for i, v in enumerate(dataSet):
        #从 i=1 开始：
        if i==0 or i==len(dataSet)-1:
            continue
        if i<LPF.WINSZ-1:
            va=0
        else:
            va=np.var(dataSet[i-LPF.WINSZ+1: i])
        if va<0.015:
            continue
            
        th=alpha/(i-k)+beta
        #v 即论文中 accZ(i)
        #达到阈值，计一步：
        if v<dataSet[i+1] and max-v>=th:
            if debugMode:
                c='m'
                w=2
                if i-k<3:
                    c='r'
                    w=2
                plot(range(k, i+1), dataSet[k: i+1], c, linewidth=w)
                
                #'%d,%d'%(steps,k)
                annotate(steps, xy=(k, dataSet[k]), xycoords='data', xytext=(0,20), textcoords='offset points', 
					bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
					fontsize=12, arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=.2'))
                #print ('dataSet[k: i]:', i-k, k, i, dataSet[k:i])
                pass
            steps+=1
            k=i
            max=v
        else:
            if v>max:
                max=v
                k=i
    return steps
    pass

