# fetch all images on one side
g = f = d = 0
from e_scraper import *
for page in range(int(upper_pagelim/threshold)):
    dat = data(page,size)
    for sides in range(threshold):
        url = website + str(sides+1+(page+offset)*threshold) + tags
        print(f'url={url}')
        response = requests.get(url, auth=auth,headers=header)
        soup = BeautifulSoup(response.text, "html.parser")
        for img in soup.findAll('article'):
            grap = True
            img_id = img.get('id')[5:]
            if dat.check_id(img_id):
                d+=1
                continue
            while grap == True:
                print(f'grabbed/fail/(double)/file/side={g}/{f}/({d})/{page}/'+sides*'='+'>'+(threshold-sides-1)*' '+'|', end="\r")
                try:
                    bytes_im = io.BytesIO(requests.get(img.get('data-large-file-url')).content)
                    dat.add(np.array(Image.open(bytes_im)), img.get('data-tags'), img_id)
                    grap = True
                    g+=1
                    break
                except:
                    time.sleep(3)
                    grap = False
                    f+=1
# loop until threshold
    #dat.transform(128)
    dat.save()
    dat.clean()
    dat = data(page,size)
