import time
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.function_base import iterable
from numpy.lib.shape_base import row_stack
import pandas as pd
import os
from multiprocessing import Process,Array
import pynvml
from scipy.io import savemat
import datetime


def MatShift(mat,d):

    w,h = mat.shape
    tmp = np.zeros_like(mat).astype(type(mat[0,0]))
    if d>0:
        tmp[:,d:] = mat[:,:h-d]
    else:
        d = np.abs(d)
        tmp[:,:h-d] = mat[:,d:h]
    return tmp


def ReadMat(path):

    try:
        mat = io.loadmat(path)
    except:
        import scipy.io as io
        mat = io.loadmat(path)
    for i in mat.keys():
        if '__' not in i:
            return mat[i]


def WriteInfo_zl(path,**args):
    ppp = os.path.split(path)

    if not os.path.isdir(ppp[0]):
        os.makedirs(ppp[0])


    try:
        args = args['args']
    except:
        pass
    # in any case, don't delete this code ↓
    args['Time'] = [str(datetime.datetime.now())[:-7]]
    try:
        df = pd.read_csv(path, encoding='utf-8', engine='python')
    except:
        df = pd.DataFrame()
    df2 = pd.DataFrame(args)
    df = df.append(df2)
    df.to_csv(path, index=False)

def WriteInfo(path,**args):

    isExists = os.path.exists(path)


    try:
        args = args['args']
    except:
        pass

    args['Time'] = [str(datetime.datetime.now())[:-7]]
    try:
        df = pd.read_csv(path,encoding='utf-8',engine='python')
    except:
        df = pd.DataFrame()
    df2 = pd.DataFrame(args)
    df = df.append(df2)
    df.to_csv(path,index=False)


def GPUScan(memory=4000,multi=False):

    num = []
    pynvml.nvmlInit()
    deviceCount = pynvml.nvmlDeviceGetCount()
    for i in range(1,deviceCount+1):
        u = deviceCount - i
        handle = pynvml.nvmlDeviceGetHandleByIndex(u) 
        meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
        free_memory = meminfo.free/1024**2
        if free_memory > memory:
            num.append(u)
    if num:
        if not multi:
            return str(num[0])
        else:
            return str(num)[1:-1]
    
    print('*'*30,'No satisfied devices!','*'*30,sep='\n')
    assert False


def WeightMask(shape,Rmax=0.3,sharp=0.1):

    ny,nx = shape
    num_nx = nx + nx%2
    num_ny = ny + ny%2
    ix = np.array([i+(-nx/2) for i in range(num_nx)])
    iy = np.array([i+(-ny/2) for i in range(num_ny)])
    wx = Rmax*ix/(nx/2)
    wy = Rmax*iy/(ny/2)
    rwx,rwy = np.meshgrid(wx,wy)
    R = (rwx**2+rwy**2)**sharp
    return R.astype(np.float32)


def MultiWeightMask(shape,RmaxList,SharpList):
    try:
        x,y,c = shape
    except:
        return WeightMask(shape,RmaxList,SharpList)
    
    if c!=len(RmaxList):
        print("{} not match {}!".format(c,len(RmaxList)))
        assert False
    item = zip(RmaxList,SharpList)
    R = np.zeros(shape)
    i = 0
    for Rmax,Sharp in item:
        if Sharp == 1:
            R[...,i] = np.ones([x,y])
        else:
            R[...,i] = WeightMask([x,y],Rmax,Sharp)
        i +=1
    return R.astype(np.float32)


def DisplayBlack(data,t=3,show=True):

    data = np.abs(data)
    data[data>0]=255
    if show:
        plt.imshow(data,cmap='gray',vmin=0,vmax=255)
        plt.pause(t)
    else:
        return data



## start VCC
def circshift(matrix_ori,shiftnum1,shiftnum2):
    c,h,w = matrix_ori.shape
    matrix_new=np.zeros_like(matrix_ori)
    for k in range(c):
        u=matrix_ori[k]        
        if shiftnum1 < 0:
            u = np.vstack((u[-shiftnum1:,:],u[:-shiftnum1,:]))
        else:
            u = np.vstack((u[(h-shiftnum1):,:],u[:(h-shiftnum1),:]))
        if shiftnum2 > 0:
            u = np.hstack((u[:, (w - shiftnum2):], u[:, :(w - shiftnum2)]))
        else:
            u = np.hstack((u[:,-shiftnum2:],u[:,:-shiftnum2]))
        matrix_new[k]=u           
    return matrix_new


def self_floor1(data1):
    data=np.copy(data1)
    I,J,K = data.shape
    for i in range(K):
        data[:,:,i] = np.flipud(data[:,:,i])#duiying de
        data[:,:,i] = np.fliplr(data[:,:,i])
    return data


def VCC_siganal_creation(kspace):

    nRO,nPE,nc=kspace.shape

    VCC_signals=np.conj(self_floor1(np.copy(kspace)))

    if np.mod(nPE,2)==0:
        VCC_signals=circshift(VCC_signals,1,0)
    if np.mod(nRO,2)==0:
        VCC_signals=circshift(VCC_signals,0,1)


    # kspace_vcc=np.concatenate((kspace,VCC_signals),axis=-1)

    return kspace,VCC_signals
## end VCC


def multi_run(func,args,num_works=5):
    result = []
    for i in range(num_works):
        p = Process(target=func,args=args)
        result.append(p)
        p.start()
        time.sleep(np.random.randint(0,num_works,1)[0])
    for p in result:
        p.join()




def patch_rescale(img,patch_max=None,patch_min=None):

    if not patch_max:
        patch_max = np.max(np.max(img,-1),-1)[...,None,None]
        patch_min = np.min(np.min(img,-1),-1)[...,None,None]    
        img = (img - patch_min)/(patch_max - patch_min)
        img = img * 2. - 1.
        return img, patch_max, patch_min
    else: 
        img = (img - patch_min)/(patch_max - patch_min)
        img = img * 2. - 1.
        return img

def patch_unrescale(img,max_deg,min_deg):
    if len(max_deg.shape) == 1:
      max_deg = max_deg[...,None,None]
      min_deg = min_deg[...,None,None]
    
    img = (img + 1.) / 2.
    img = (max_deg - min_deg) * img + min_deg
    return img

# R = MultiWeightMask([188,236,32],np.array([1,2,3]),np.array([0.4,0.5,0.6]))
# write_info('./raki_result.csv',psnr =32.2,mse = 1.54,ssim= 0.9756,mae=0.12)


