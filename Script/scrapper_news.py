import os
import json
import aiohttp
import ssl
import certifi
from bs4 import BeautifulSoup
import time
from pathlib import Path



time = time.localtime(time.time())
sslcontext = ssl.create_default_context(cafile=certifi.where())# SSl certify(Do not disable when requested!)
url = 'https://45.ru/text/'

#Headers for the request to the site
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.0.1044 Yowser/2.5 Safari/537.36",
    "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"}

async def get_page(ur):
    async with aiohttp.ClientSession() as session:
        async with session.get(ur, headers=headers, ssl=sslcontext) as resp:
            response = await resp.text()
            print('Страница успешно получена')
            return response

async def download_image(url):
    """Upload images to a separate folder"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, ssl=sslcontext) as resp:
            response = await resp.read()
    day = (time.tm_mon, time.tm_mday)  # (month, day)
    path = Path("data", f'date_img_from_{day[0]}_{day[1]}')
    if not (os.path.exists(path)):
        os.mkdir(path)
    pathimg = Path("data", f'date_img_from_{day[0]}_{day[1]}', f"{url[48:]}")
    with open(pathimg, 'wb') as img:
        img.write(response)

async def get_page_news(resp):
    """we get today's news from the page"""
    soup = BeautifulSoup(resp, 'lxml')
    card_news = soup.find_all('article', attrs={"data-test": "archive-record-item"})
    for i in range(0, len(card_news)):
        day = time.tm_mday
        mon = time.tm_mon
        day = '0' + str(day) if day < 10 else day
        mon = '0' + str(mon) if mon < 10 else mon
        date_time = card_news[i].find('time').attrs['datetime'][:-9] #year-mon-day
        if date_time == f"{time.tm_year}-{mon}-{day}":# compare the date of the card with today's date
            continue
        else:
            return card_news[:i]

async def get_data(cards):
    """We collect data from the cards and write them to a file "data_news" """
    card_infos = []
    for i in cards:
        img_url = i.find('picture').find("img").attrs['src']
        code_img = img_url[48:]
        await download_image(img_url)
        title = i.find('h2').find("a").attrs['title']
        sub_title = i.find('h2').find_next_sibling('div').find("a").text
        sourсe = url[:-6] + i.find('h2').find("a").attrs['href']
        views = i.find('div', attrs={"data-test": "record-stats-view"}).find("span").text.split()
        date_time = i.find('time').attrs['datetime']
        card_infos.append(
            {
                'title': title,
                'sub_title': sub_title,
                'sourсe': sourсe,
                'date_time': date_time[:-9],
                'code_img': code_img,
                'views': int(''.join(views))
            }
        )
        path = Path('data','data_news.json')
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(card_infos, file, indent=4, ensure_ascii=False)

async def all_news():
    """Collecting all news and saving them to file"""
    resp_page = await get_page(f"{url}?page={1}")
    cards = await get_page_news(resp_page)
    if cards == []:
        return
    else:
        await get_data(cards)
        return True

async def top_five_news():
    """From all the news, we select the best by views and return them in the array"""
    resp_page = await get_page(f"{url}?page={1}")
    cards = await get_page_news(resp_page)
    if cards == []:
        return
    else:
        await get_data(cards)
        arr = []
        path = Path('data', 'data_news.json')
        with open(path, encoding='utf-8') as file:
            li = json.load(file)
            li.sort(key=lambda x: x['views'], reverse=True)
            count = 0
            for i in li:
                if count < 5:
                    count += 1
                    arr.append(i)
                else:
                    break

        return arr


#loop = asyncio.get_event_loop()
#loop.run_until_complete(all_news())


