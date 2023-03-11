from bs4 import BeautifulSoup
import requests
import pickle
import cv2 as cv
import numpy as np
#import skimage
import io
from PIL import Image
import time
import matplotlib.pyplot as plt

apikey = '' # enter your api key here
username = '' # enter your username here
header = {"User-Agent": 'simple scrap v.1.1'}
auth = (username, apikey)
threshold = 20 # pages per data file (ramsize dependent)
upper_pagelim = 1020 # just leave it, e only allow up to 750 pages anyway
size = 128 # size of image (all images are rescaled to 1:1 !)
offset = 0 # start at specific page, startpage = offset*threshold
website = 'https://e621.net/posts?page='
tags = '' # enter tag url like e.g. '&tags=rating%3As+dragon+-absurd_res'

class data():
    def __init__(self,num,size):
        self.id = num
        self.images = []
        self.gimages = []
        self.tags = []
        self.img_id = []
        self.noise_rdy = False
        self.size = size
        return
    
    def get_id(self):
        return self.id
    
    def add(self, img, tags, img_id):
        img = self.transform(img)
        self.images.append(img)
        self.tags.append(tags)
        self.img_id.append(int(img_id))
        
    def save(self):
        with open(f'img_{self.id}.pickle', 'wb') as handle:
            pickle.dump([self.images, self.tags, self.img_id], handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    def load(self):
        with open(f'img_{self.id}.pickle', 'rb') as handle:
            self.images, self.tags, self.img_id = pickle.load(handle)
            self.gimages = self.images
        
    def show(self, num):
        plt.axis("off")
        plt.imshow(self.images[num])
        plt.title(self.img_id[num])
        plt.show()
        
    def get(self):
        return (self.images, self.tags, self.img_id)
    
    def clean(self):
        self.images = []
        self.tags = []
        self.img_id = []

    def check_id(self, img_id):
        return int(img_id) in self.img_id
        
    def transform(self, img):
        max = np.argmax(img.shape)
        if max == 0:
            center = img.shape[max]
            dev = img.shape[1]
            img = img[int(center/2-dev/2):int(center/2+dev/2),:]
        else:
            center = img.shape[max]
            dev = img.shape[0]
            img = img[:,int(center/2-dev/2):int(center/2+dev/2)]
        img = cv.resize(img, (self.size,self.size) , interpolation = cv.INTER_AREA)
        img = np.expand_dims(img,axis=-1) if len(img.shape) == 2 else img
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) if img.shape[-1]!=1 else img
        img = np.reshape((img-img.min())/(img.max()-img.min()),(1,size,size,1))
        return img
        
    def add_gaussian(self, alpha):
        nimg = np.empty((0,*self.images[0].shape))
        for a, img in zip(np.abs(np.random.normal(0,alpha,len(self.images))), self.images):
            gauss = np.random.normal(0,a,img.shape)
            img = cv.add(img, gauss)
            nimg = np.concatenate((nimg,np.reshape((img-img.min())/(img.max()-img.min()),(1,*img.shape))),axis=0)
        return nimg, self.images
