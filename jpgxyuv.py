import cv2
import glob
import re
import os
import numpy as np
import sys
from sys import argv,exit
from tqdm import tqdm

def read_img(path):
  img = cv2.imread(path)
  return img, path

def jpg2yuv(img,path,dir_path,color):
  height,width,c = img.shape
  b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
  cal_arr = np.array([[0.256788,0.504129,0.097906],
                      [0.148223,0.290993,0.439216],
                      [0.439216,0.367788,0.071427]])
  if color == 444:
    #Slowest code (20s/photo)
    #yuv = np.zeros((height*3,width),np.uint8)
    #for i in range(height):
    #  for j in range(width):
    #    r = r_channel[i,j]
    #    g = g_channel[i,j]
    #    b = b_channel[i,j]
    #    y = 0.256788*r+0.504129*g+0.097906*b
    #    u = -0.148223*r-0.290993*g+0.439216*b
    #    v = 0.439216*r-0.367788*g-0.071427*b
    #    yuv[i,j]=(y).astype(np.uint8)+16
    #    yuv[i+height,j]=(u).astype(np.uint8)+128
    #    yuv[i+height*2,j]=(v).astype(np.uint8)+128

    #Fastest code (0.03s/photo)
    y = (cal_arr[0,0]*r+cal_arr[0,1]*g+cal_arr[0,2]*b).astype(np.uint8)+16
    u = ((-1)*cal_arr[1,0]*r-cal_arr[1,1]*g+cal_arr[1,2]*b).astype(np.uint8)+128
    v = (cal_arr[2,0]*r-cal_arr[2,1]*g-cal_arr[2,2]*b).astype(np.uint8)+128
    yuv = np.r_["0",y,u,v]
    return path, dir_path, yuv, str(width), str(height), str(color)
  elif color == 440:
    y = (cal_arr[0,0]*r+cal_arr[0,1]*g+cal_arr[0,2]*b).astype(np.uint8)+16
    u = ((-1)*cal_arr[1,0]*r-cal_arr[1,1]*g+cal_arr[1,2]*b).astype(np.uint8)+128
    v = (cal_arr[2,0]*r-cal_arr[2,1]*g-cal_arr[2,2]*b).astype(np.uint8)+128
    u = np.delete(u,slice(None,None,2),axis=0)
    v = np.delete(v,slice(None,None,2),axis=0)
    write_img(path,dir_path,y,str(width),str(height),str(color))
    write_img_(path,dir_path,u,str(width),str(height),str(color))
    write_img_(path,dir_path,v,str(width),str(height),str(color))
    return
  elif color == 422:
    y = (cal_arr[0,0]*r+cal_arr[0,1]*g+cal_arr[0,2]*b).astype(np.uint8)+16
    u = ((-1)*cal_arr[1,0]*r-cal_arr[1,1]*g+cal_arr[1,2]*b).astype(np.uint8)+128
    v = (cal_arr[2,0]*r-cal_arr[2,1]*g-cal_arr[2,2]*b).astype(np.uint8)+128
    u = np.delete(u,slice(None,None,2),axis=1)
    v = np.delete(v,slice(None,None,2),axis=1)
    write_img(path,dir_path,y,str(width),str(height),str(color))
    write_img_(path,dir_path,u,str(width),str(height),str(color))
    write_img_(path,dir_path,v,str(width),str(height),str(color))
    return
  elif color == 420:
    y = (cal_arr[0,0]*r+cal_arr[0,1]*g+cal_arr[0,2]*b).astype(np.uint8)+16
    u = ((-1)*cal_arr[1,0]*r-cal_arr[1,1]*g+cal_arr[1,2]*b).astype(np.uint8)+128
    v = (cal_arr[2,0]*r-cal_arr[2,1]*g-cal_arr[2,2]*b).astype(np.uint8)+128
    u = np.delete(u,slice(None,None,2),axis=1)
    v = np.delete(v,slice(None,None,2),axis=1)
    u = np.delete(u,slice(None,None,2),axis=0)
    v = np.delete(v,slice(None,None,2),axis=0)
    write_img(path,dir_path,y,str(width),str(height),str(color))
    write_img_(path,dir_path,u,str(width),str(height),str(color))
    write_img_(path,dir_path,v,str(width),str(height),str(color))
    return
  elif color == 411:
    y = (cal_arr[0,0]*r+cal_arr[0,1]*g+cal_arr[0,2]*b).astype(np.uint8)+16
    u = ((-1)*cal_arr[1,0]*r-cal_arr[1,1]*g+cal_arr[1,2]*b).astype(np.uint8)+128
    v = (cal_arr[2,0]*r-cal_arr[2,1]*g-cal_arr[2,2]*b).astype(np.uint8)+128
    u = np.delete(u,slice(None,None,4),axis=1)
    v = np.delete(v,slice(None,None,4),axis=1)
    write_img(path,dir_path,y,str(width),str(height),str(color))
    write_img_(path,dir_path,u,str(width),str(height),str(color))
    write_img_(path,dir_path,v,str(width),str(height),str(color))
    return
  elif color == 410:
    y = (cal_arr[0,0]*r+cal_arr[0,1]*g+cal_arr[0,2]*b).astype(np.uint8)+16
    u = ((-1)*cal_arr[1,0]*r-cal_arr[1,1]*g+cal_arr[1,2]*b).astype(np.uint8)+128
    v = (cal_arr[2,0]*r-cal_arr[2,1]*g-cal_arr[2,2]*b).astype(np.uint8)+128
    u = np.delete(u,slice(None,None,4),axis=1)
    v = np.delete(v,slice(None,None,4),axis=1)
    u = np.delete(u,slice(None,None,4),axis=0)
    v = np.delete(v,slice(None,None,4),axis=0)
    write_img(path,dir_path,y,str(width),str(height),str(color))
    write_img_(path,dir_path,u,str(width),str(height),str(color))
    write_img_(path,dir_path,v,str(width),str(height),str(color))
    return
  else:
    y = (cal_arr[0,0]*r+cal_arr[0,1]*g+cal_arr[0,2]*b).astype(np.uint8)+16
    return path, dir_path, y, str(width), str(height), str(color)

def write_img(img_path,dir_path,yuv,w,h,c):
  img_path_re = os.path.split(img_path)[1].rstrip('.JPG')
  img_new_path = dir_path + re.sub("\.j.*$", "", img_path_re) +'('+w+'x'+h+',YUV'+c+').yuv'
  with open(img_new_path,'wb') as f:
    f.write(yuv)

def write_img_(img_path,dir_path,yuv,w,h,c):
  img_path_re = os.path.split(img_path)[1].rstrip('.JPG')
  img_new_path = dir_path + re.sub("\.j.*$", "", img_path_re) +'('+w+'x'+h+',YUV'+c+').yuv'
  with open(img_new_path,'ab') as f:
    f.write(yuv)

def main(color):
  new_dir_name = 'image_yuv/'
  isfile1 = 'image_yuv'
  isfile2 = 'image_original'
  image_path = 'image_original/*'
  # path founding
  er = 'ERROR: Path Not Found. Create the directory and exit.'
  if (os.path.isdir(isfile1) == False or
    os.path.isdir(isfile2) == False):
    if (os.path.isdir(isfile1) == False and
      os.path.isdir(isfile2) == False):
      os.mkdir(isfile1)
      os.mkdir(isfile2)
      print(er)
      exit()
    elif os.path.isdir(isfile1) == False:
      os.mkdir(isfile1)
      print(er)
      exit()
    else:
      os.mkdir(isfile2)
      print(er)
      exit()
  files = glob.glob(image_path)
  if len(files) == 0:
    print('INFO: IMAGES NOT FOUND.')
    exit()
  for file in tqdm(files, desc='JPEG 2 YUV'+str(color)+' Processing'):
    img_data = read_img(file)
    if img_data[0] is None:
      print('ERROR: Image Not Found.')
      exit()
    write_data = jpg2yuv(*img_data,new_dir_name,color)
    if color == 444 or color == 400:
      write_img(*write_data)
  print('COMPLETED')

if __name__ == '__main__':
  # ERROR output
  er = '''
  ERROR: Incorrect argument entered. Please enter CORRECT argument.
  Correct command: python jpgxyuv.py [YUV-format]
  ex) python jpgxyuv.py 444
    - 444 : JPEG convert to YUV444 (4:4:4)
    - 440 : JPEG convert to YUV440 (4:4:0)
    - 422 : JPEG convert to YUV422 (4:2:2)
    - 420 : JPEG convert to YUV420 (4:2:0)
    - 411 : JPEG convert to YUV411 (4:1:1)
    - 410 : JPEG convert to YUV410 (4:1:0)
    - 400 : JPEG convert to YUV400 (4:0:0)
  '''
  arglen = sys.argv
  if len(arglen) < 2:
    print(er)
    exit()
  args = int(arglen[1])
  if (args == 444 or args == 440 or args == 422 or args == 420 or args == 411
  or args == 410 or args == 400):
    main(args)
    exit
  else:
    print(er)
    exit
