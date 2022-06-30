import requests
import bs4
import time
import os

def details(link):    
    
    time.sleep(1)
    response = requests.get(link, headers=headers)
    soup = bs4.BeautifulSoup(response.content,'lxml')
    thumbnail = soup.select_one('img.thumb').get('src')
    filename = thumbnail.split('/')[-1]
    if not os.path.exists(f'images/{filename}'):
        thumbnail_large = f'{thumbnail}?w=5000'
        
        print(f'\t[-] Processing: images/{filename}')
        with open(f'images/{filename}', 'wb') as f:
            image_binary = requests.get(thumbnail_large, headers=headers)
            f.write(image_binary.content)
            f.close()
        print(f'\t[*] Saved: {filename}')
    else:
        print('[*] Image already downloaded!')
    time.sleep(1)
    
def main_link():
    
    ''' scraps items from pages list and download the images big size '''
    
    with open('freepik_links.txt','r') as f:
        links = f.readlines()
        for link in links:
            details(link.strip())
    

def main():
    
    ''' scraps items from pages list and download the images big size '''
    
    page_number = 1
    while True:
        print(f'[*] Working on page: {page_number}')
        url = f'https://www.freepik.com/collection/autumn-worksheet-for-childern/2070905/{page_number}'

        response = requests.get(url, headers=headers)
        soup = bs4.BeautifulSoup(response.content,'lxml')

        items = soup.select('figure.showcase__item')
        
        ''' check if items aren't enough to go on '''
        if len(items) < 1:
            break
        
        for item in items:
            link = item.select_one('a.showcase__link').get('href')
            details(link)
        
        page_number +=1

if __name__ == '__main__':
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
    main_link()