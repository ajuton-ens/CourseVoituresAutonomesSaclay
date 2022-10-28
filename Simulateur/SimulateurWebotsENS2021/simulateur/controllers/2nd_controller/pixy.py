# -*-coding:Latin-1 -* 
import numpy as np
import matplotlib.pyplot as plt

def GetPixyDatas(camera,cam_width,cam_height,Verbose=False):
	"""
	Structure des données renvoyées :
	tuple(
		array([Barycentre des pixels verts], 
		Plus grande longeur de pixels verts,
		Plus grande largeur de pixels verts
		)
		array( Idem mais pour pixels rouges)
	)

	"""
	
	imgRGB=np.fliplr(np.array(camera.getImageArray()))
	imgR = imgRGB[:,:,0]
	imgG = imgRGB[:,:,1]
	imgRG=imgR-imgG 
	mgx=0
	mrx=0
	mgy=0
	mry=0
	Mrx=0
	Mry=0
	Mgx=0
	Mgy=0
	ng=0
	nr=0
	Bg=np.array([None,None])
	Br=np.array([None,None])
	red,green=False,False
	for i in range(len(imgRG)):
		mgx=0
		mrx=0
		for j in range(len(imgRG[0])):
			if imgRG[i][j]>50:
				red=True
				if Br.any()==None:
					Br=np.array([0,0])
				mrx+=1
				Br[0]+=i
				Br[1]+=j
				nr+=1
				imgRG[i][j]=50
			elif imgRG[i][j]<-50:
				green=True
				if Bg.any()==None:
					Bg=np.array([0,0])
				mgx+=1
				Bg[0]+=i
				Bg[1]+=j
				ng+=1
				imgRG[i][j]=-50
			else :
				imgRG[i][j]=0
		if mrx>Mrx:
			Mrx=mrx
		if mgx>Mgx:
			Mgx=mgx

	for j in range(len(imgRG[0])):
		mry=0
		mgy=0
		for i in range(len(imgRG)):
			if imgRG[i][j]==50:
				mry+=1
			elif imgRG[i][j]==-50:
				mgy+=1
		if mry>Mry:
			Mry=mry
		if mgy>Mgy:
			Mgy=mgy
	if red :        
		Br=np.array(Br)/nr
	if green :
		Bg=np.array(Bg)/ng
	Green_datas=np.array([Bg,Mgx,Mgy])
	Red_datas=np.array([Br,Mrx,Mry])
	if Verbose :
		if Bg.any()!=None:
			imgRG[min(cam_height-1,int(Bg[0]+Mgy/2))][min(cam_width-1,int(Bg[1]+Mgx/2))]=30
			imgRG[min(cam_height-1,int(Bg[0]+Mgy/2))][max(0,int(Bg[1]-Mgx/2))]=30
			imgRG[max(0,int(Bg[0]-Mgy/2))][min(cam_width-1,int(Bg[1]+Mgx/2))]=30
			imgRG[max(0,int(Bg[0]-Mgy/2))][max(0,int(Bg[1]-Mgx/2))]=30
			imgRG[int(Bg[0])][int(Bg[1])]=30
		if Br.any()!=None:
			imgRG[min(cam_height-1,int(Br[0]+Mry/2))][min(cam_width-1,int(Br[1]+Mrx/2))]=-30
			imgRG[min(cam_height-1,int(Br[0]+Mry/2))][max(0,int(Br[1]-Mrx/2))]=-30
			imgRG[max(0,int(Br[0]-Mry/2))][min(cam_width-1,int(Br[1]+Mrx/2))]=-30
			imgRG[max(0,int(Br[0]-Mry/2))][max(0,int(Br[1]-Mrx/2))]=-30
			imgRG[int(Br[0])][int(Br[1])]=-30
		plt.figure()
		plt.imshow(imgRG)
		plt.show()
	
	return Green_datas,Red_datas

def GetPixyDatas2(camera,cam_width,cam_height,Verbose=False):
    """
    Structure des données renvoyées :
    tuple(
        array([Barycentre des pixels verts], 
                Plus grande longeur de pixels verts,
                Plus grande largeur de pixels verts
                )
        array( Idem mais pour pixels rouges)
    )

    """
    imgRGB=np.flipud(np.rot90(np.array(camera.getImageArray())))
    imgR = imgRGB[:,:,0]
    imgG = imgRGB[:,:,1]
    imgRG=imgR-imgG
    Mrx=0
    Mry=0
    Mgx=0
    Mgy=0
    ng=0
    nr=0
    Bg=np.array([None,None])
    Br=np.array([None,None])
    red=False
    green=False
    imgRmask=np.array(imgRG>50,dtype=int)
    imgGmask=np.array(imgRG<-50,dtype=int)

    if imgRmask.any() == 1:
        red=True
        nr=np.sum(imgRmask)
        sumRcol=np.sum(imgRmask,axis=0)
        sumRlin=np.sum(imgRmask,axis=1)
        Br=np.sum(np.array(np.where(imgRmask==1)),axis=1)/nr
        Mrx=max(sumRlin)
        Mry=max(sumRcol)

    if imgGmask.any() == 1:
        green=True
        ng=np.sum(imgGmask)
        sumGcol=np.sum(imgGmask,axis=0)
        sumGlin=np.sum(imgGmask,axis=1)
        Bg=np.sum(np.array(np.where(imgGmask==1)),axis=1)/ng
        Mgx=max(sumGlin)
        Mgy=max(sumGcol)
    Green_datas=np.array([Bg,Mgx,Mgy])
    Red_datas=np.array([Br,Mrx,Mry])

    if Verbose :
        if green:
            imgRG[min(cam_height-1,int(Bg[0]+Mgy/2))][min(cam_width-1,int(Bg[1]+Mgx/2))]=200
            imgRG[min(cam_height-1,int(Bg[0]+Mgy/2))][max(0,int(Bg[1]-Mgx/2))]=200
            imgRG[max(0,int(Bg[0]-Mgy/2))][min(cam_width-1,int(Bg[1]+Mgx/2))]=200
            imgRG[max(0,int(Bg[0]-Mgy/2))][max(0,int(Bg[1]-Mgx/2))]=200
            imgRG[int(Bg[0])][int(Bg[1])]=200
        if red:
            imgRG[min(cam_height-1,int(Br[0]+Mry/2))][min(cam_width-1,int(Br[1]+Mrx/2))]=-200
            imgRG[min(cam_height-1,int(Br[0]+Mry/2))][max(0,int(Br[1]-Mrx/2))]=-200
            imgRG[max(0,int(Br[0]-Mry/2))][min(cam_width-1,int(Br[1]+Mrx/2))]=-200
            imgRG[max(0,int(Br[0]-Mry/2))][max(0,int(Br[1]-Mrx/2))]=-200
            imgRG[int(Br[0])][int(Br[1])]=-200
        plt.figure()
        plt.imshow(imgRG)
        plt.show()
    return Green_datas,Red_datas
