import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as BS4
from urllib.parse import urljoin, urlparse

def check_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)
    
def get_all_images(url):
    scrape = BS4(requests.get(url).content, "html.parser")

    urls = []
    for img in tqdm(scrape.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:
            continue

        img_url = urljoin(url, img_url)

        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass

        if check_valid_url(img_url):
            urls.append(img_url)
    return urls

def get_all_images_by_target(url, target):
    scrape = BS4(requests.get(url).content, "html.parser")

    # urls = []
    # for img in tqdm(scrape.select_one(''), "Extracting images"):
    #     img_url = img.attrs.get("src")
    #     if not img_url:
    #         continue

    #     img_url = urljoin(url, img_url)

    #     try:
    #         pos = img_url.index("?")
    #         img_url = img_url[:pos]
    #     except ValueError:
    #         pass

    #     if check_valid_url(img_url):
    #         urls.append(img_url)
    # return urls
    # dom = etree.HTML(str(scrape))
    # imgs = dom.xpath(target)

    # for img in imgs:
        # print(img.img)
    # # item = dom.xpath('/html/body/div[5]/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/main/div[2]/div[3]/div[2]/div/div/div/div/div/div/div[1]/div[2]/div/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/div/a[1]/div/div/picture/img')
    # # print(item.img['class'])
    # print(scrape.find_all(''))

    #TODO: to be continue fixing scrape with target

def download(url, pathname):
    if not os.path.isdir(pathname):
        os.makedirs(pathname)

    response = requests.get(url, stream=True)
    file_size = int(response.headers.get("Content-Length", 0))
    filename = os.path.join(pathname, url.split("/")[-1])

    # progress bar tqdm
    progress = tqdm(
        response.iter_content(1024), 
        f"Downloading Image {filename}", 
        total=file_size, unit="B", 
        unit_scale=True, 
        unit_divisor=1024
    )

    with open(filename, "wb") as f:
        for data in progress.iterable:
            f.write(data)
            progress.update(len(data))

def main(url, path, state, target):

    #TODO: to be continue fixing get all images by target method
    #TODO: will continue fixing states 


    # imgs = get_all_images(url) if state == 'ALL_IMAGES' else get_all_images_by_target(url, target)
    imgs = get_all_images(url)

    for img in imgs:
        download(img, path)

    print ("Download Complete")
    os.chdir("../")
    return {
        'path'    : "flask-rest-api/downloads/" + path,
        'message' : "downloaded " + str(len(imgs)) + ' Images',
        'status'  : "success",
        'state'   : state
    }