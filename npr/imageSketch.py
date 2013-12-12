# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from pylab import *
import numpy as np
from PIL import Image, ImageFilter
import os, sys

# <codecell>

#高通滤波：
def myHpfFilter(img, kernel):
	mod='L'
	img=img.convert(mod)
	px=img.load()
	w, h=img.size
	nimg=Image.new(mod, (w,h))
	npx=nimg.load()
	#kernel width:
	kw=int(kernel.size**.5)
	padding=int(kw/2)
	for x in range(padding, w-padding):
		for y in range(padding, h-padding):
			#计算px[x,y]新值：
			sum=0
			for i in range(kw):
				for j in range(kw):
					#npx[x, y]+=px[x-padding+i, y-padding+j]*kernel[i, j]
					sum+=px[x-padding+i, y-padding+j]*kernel[i, j]
			npx[x,y]=(sum)
			#print npx[x,y], sum
			
			pass
	return nimg
	pass

#霓虹处理，也高通，见“一种改进的铅笔画生成方法”
#定死 2*2：
def myNeon(img):
	mod='L'
	img=img.convert(mod)
	px=img.load()
	w, h=img.size
	nimg=Image.new(mod, (w,h))
	npx=nimg.load()
	#kernel width:
	kw=2
	padding=1
	for x in range(padding, w-padding):
		for y in range(padding, h-padding):
			sum=0
			v1=px[x,y]
			v2=px[x+1, y]
			v3=px[x, y+1]
			npx[x, y]=2*((v1-v2)**2+(v1-v3)**2)**0.5
	return nimg

def myInverse(img):
	mod='L'
	img=img.convert(mod)
	px=img.load()
	w, h=img.size
	nimg=Image.new(mod, (w,h))
	npx=nimg.load()
	for x in range(w):
		for y in range(h):
			old=px[x,y]
			#if old>28:
				#old=255
			#old*=3
			npx[x,y]=255-old
			
	return nimg
	pass

#模糊，低通滤波：
def myBlur(img, kernel):
	denom=kernel.sum()
	mod='L'
	img=img.convert(mod)
	px=img.load()
	w, h=img.size
	nimg=Image.new(mod, (w,h))
	npx=nimg.load()
	#kernel width:
	kw=int(kernel.size**.5)
	padding=int(kw/2)
	for x in range(padding, w-padding):
		for y in range(padding, h-padding):
			#计算px[x,y]新值：
			sum=0
			for i in range(kw):
				for j in range(kw):
					#npx[x, y]+=px[x-padding+i, y-padding+j]*kernel[i, j]
					sum+=px[x-padding+i, y-padding+j]*kernel[i, j]
			npx[x,y]=sum*1./denom
			#print npx[x,y], sum
			
			pass
	return nimg
	pass

#高通滤波核：
k5=array([0, -1,-2,-1, 0,
		  -1,-4,-8,-4,-1,
		  -2,-8,64,-8,-2,
		  -1,-4,-8,-4,-1,
		  0, -1,-2,-1, 0,])
k5=k5.reshape((5,5))

k2=array([3,-1,
		 -1,-1])
k2=k2.reshape((2,2))

k3=array([-1,-1,-1,
		  -1, 8,-1,
		  -1,-1,-1])
k3=k3.reshape((3,3))

#低通滤波核：
lk3=array([1,2,1,
		   2,4,2,
		   1,2,1])
lk3=lk3.reshape((3,3))

lk30=array([0,2,0,
		  2,4,2,
		  0,2,0])
lk30=lk30.reshape((3,3))


#根据 slic 结果 segments，计算向量场，
#方法：当前点向下，向右走到与自己不一致的位置，计算走步数纵横比。
#若上下、左右某方向完全变了，则往反方向走：
def getVectorFromSeg(seg):
	seg=np.asarray(seg)
	#宽高反的：
	h, w=seg.shape
	uu=np.zeros((h, w)).astype(np.float32)
	vv=np.zeros((h, w)).astype(np.float32)
	for x in range(w):
		for y in range(h):
			v=seg[y, x]
			#初始化，假设能走一步：
			xlen=1
			ylen=1
			#同一列走：
			while y+ylen<h and v==seg[y+ylen, x]:
				ylen+=1
			#走了零步：
			if ylen==1 :
				ylen=-1
				#while y+ylen>=0 and v==seg[y+ylen, x]:
					#ylen-=1
				#若纵向是孤立点，最终 ylen ==-1
			
			#同一行走：
			while x+xlen<w and v==seg[y, x+xlen]:
				xlen+=1
			#走了零步：
			if xlen==1:
				xlen=-1
				#while x+xlen>=0 and v==seg[y, x+xlen]:
					#xlen-=1
				#若横向是孤立点，最终 xlen ==-1
			
			#vec=ylen*1.0/xlen
			#res[y, x]=vec
			uu[y,x]=xlen
			vv[y,x]=ylen
	#return res
	return uu,vv
	pass

#ndarray 归一化：
def normArray(a, low=0, high=1.0):
	amin=np.min(a)
	amax=np.max(a)
	arange=amax-amin
	res=1.0*(a-amin)*(high-low)/arange+low
	return res.astype(np.float32)

def getWhiteNoise(a, sigma):
	# print 'a.shape:', a.shape
	ar=a.ravel()
	res=[np.random.normal(loc=v, scale=sigma) for v in ar]
	res=np.asarray(res, dtype=np.float32)
	res=res.reshape(a.shape)
	# print 'res.shape:', res.shape, a.shape
	return res
	pass
	
# <codecell>


def main():
	fname=None
	if len(sys.argv)>1:
		fname=sys.argv[1]
	else: fname=r'D:\Documents\Desktop\3.png'
	print (fname)
	mainFname, ext=os.path.splitext(fname)

	#边缘检测：
	img=Image.open(fname)
	krnl=k2
	hpfImg=myHpfFilter(img, krnl)
	hpfImg=myInverse(hpfImg)
	
	neonImg=myNeon(img)
	neonImg=myInverse(neonImg)
	
	edge=Image.blend(hpfImg, neonImg, 0.5)
	
	# edge=neonImg
	edge.show()
	edgeFname=mainFname+'.edge'+ext
	edge.save(edgeFname)

	
	#转换灰度图，图像分割：
	from skimage.segmentation import slic
	grayimg=img.convert('L')
	arrimg=np.array(grayimg)
	arrimg[arrimg>168]=240
	#imshow(arrimg)
	seg=Image.fromarray(arrimg).filter(ImageFilter.MinFilter(11))
	seg.show()
	seg=slic(np.array(seg), sigma=0.5, n_segments=10, ratio=20)
	# imshow(seg)
	# show()
	# return
	
	#生成向量场：
	u,v=getVectorFromSeg(seg)
	
	#线积分卷积 LIC：
	from scikits import vectorplot
	texture=normArray(arrimg)
	texture=getWhiteNoise(texture, sigma=0.6)
	Image.fromarray(normArray(texture, high=255)).show()
	# return
	#黑白图假装白噪声，巨丑：
	#texture=Image.fromarray(arrimg).convert('1')
	#texture=np.asarray(texture, dtype=np.float32)
	#print texture.dtype
	
	kernel=np.array([1]*13).astype(np.float32)
	licimg=vectorplot.line_integral_convolution(u, v, texture, kernel)
	licimg=normArray(licimg, high=255)
	#print 'licimg:', licimg
	lic=Image.fromarray(licimg)
	lic.show()
	lic=lic.convert('L')
	edge=edge.convert('L')
	#print lic.size, edge.size, lic.mode, edge.mode
	#lic.show()
	#edge.show()
	result=Image.blend(edge, lic, 0.208)
	result.show()
	result.save(mainFname+'.out'+ext)
	pass
	

# <codecell>

if __name__=='__main__':
	main()

