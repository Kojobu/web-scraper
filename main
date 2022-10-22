from bs4 import BeautifulSoup
import requests
import pickle
import cv2 as cv
import numpy as np
import io
from PIL import Image
import time
import matplotlib.pyplot as plt
url = 'https://e621.net/posts?page=0&tags=dragon' #tags can be encoded here
apikey = "###YOUR API KEY###"
username = '###YOUR USER NAME###'
header = {"User-Agent": 'simple scrap v.1.0 by catfire1'}
auth = (username, apikey)
threshold = 10 # threshold = given number * number of objects on page
upper_pagelim = 1000 # stops after 

class data():
    def __init__(self,num):
        self.id = num
        self.images = []
        self.gimages = []
        self.tags = []
        self.noise_rdy = False
        return
    
    def get_id(self):
        return self.id
    
    def add(self, img, tags):
        self.images.append(img)
        self.tags.append(tags)
        
    def save(self):
        with open(f'img_{self.id}.pickle', 'wb') as handle:
            pickle.dump([self.images, self.tags], handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    def load(self):
        with open(f'img_{self.id}.pickle', 'rb') as handle:
            self.images, self.tags = pickle.load(handle)
            self.gimages = self.images
        
    def show(self, num):
        plt.axis("off")
        plt.imshow(self.images[num])
        plt.show()
        
    def get(self):
        return (self.images, self.tags)
    
    def clean(self):
        self.images = []
        self.tags = []
        
    def transform(self, size):
        nimg = np.empty((0,size,size,1))
        for img in self.images:
            max = np.argmax(img.shape)
            if max == 0:
                center = img.shape[max]
                dev = img.shape[1]
                img = img[int(center/2-dev/2):int(center/2+dev/2),:]
            else:
                center = img.shape[max]
                dev = img.shape[0]
                img = img[:,int(center/2-dev/2):int(center/2+dev/2)]
            img = cv.resize(img, (size,size) , interpolation = cv.INTER_AREA)
            img = img if len(img.shape) > 2 else np.reshape(img, (*img.shape,1))
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) if img.shape[-1]!=1 else img
            nimg = np.concatenate((nimg,np.reshape((img-img.min())/(img.max()-img.min()),(1,size,size,1))),axis=0)
        self.size = size
        self.images = nimg
        
    def add_gaussian(self, alpha):
        nimg = np.empty((0,*self.images[0].shape))
        for a, img in zip(np.abs(np.random.normal(0,alpha,len(self.images))), self.images):
            gauss = np.random.normal(0,a,img.shape)
            img = cv.add(img, gauss)
            nimg = np.concatenate((nimg,np.reshape((img-img.min())/(img.max()-img.min()),(1,*img.shape))),axis=0)
        return nimg, self.images
        
# fetch all images on one side
g = f = 0
grap = True
offset = 0
for page in np.arange(0,int(upper_pagelim/threshold),1)+offset:
    dat = data(page)
    for sides in range(threshold):
        response = requests.get(url, auth=auth,headers=header)
        soup = BeautifulSoup(response.text, "html.parser")
        for img in soup.findAll('article'):
            while grap == True:
                print(f'grabbed/fail/side/file={g}/{f}/{sides}/{page}', end="\r")
                try:
                    bytes_im = io.BytesIO(requests.get(img.get('data-large-file-url')).content)
                    dat.add(np.array(Image.open(bytes_im)), img.get('data-tags'))
                    grap = True
                    g+=1
                    break
                except:
                    time.sleep(3)
                    grap = False
                    f+=1
        #print(f'{page} '+sides*'='+'>'+(threshold-sides-1)*' '+'|', end="\r")
        # go to next side
        url = 'https://e621.net' + soup.findAll('a')[-9].get('href')
        # loop until threshold
    dat.transform(128)
    dat.save()
    dat.clean()
    dat = data(page)
