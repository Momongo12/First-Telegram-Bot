import aiohttp
import certifi
import ssl
from bs4 import BeautifulSoup

async def get_page(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.0.1044 Yowser/2.5 Safari/537.36",
            "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"}, ssl=ssl.create_default_context(cafile=certifi.where())) as response:
            resp = await response.text()
            return resp

async def get_data_corona():
    """Getting information about the coronavirus"""
    region_page = await get_page('https://gogov.ru/covid-news/kurgan')
    soup = BeautifulSoup(region_page, 'lxml')
    total_in_region = {}
    block = soup.find('div', class_="entry-content").find('div', {
        'style': "display:flex; justify-content:space-around; flex-wrap:wrap;"})
    p = block.find("p")
    br_total_in_region = p.find_all("b")
    br_today_in_region = p.find_next_sibling('p').find_all("b")
    total_in_region['all_cases'] = br_total_in_region[0].text
    total_in_region['died'] = br_total_in_region[1].text
    total_in_region["cured"] = br_total_in_region[2].text
    total_in_region['all_cases_today'] = br_today_in_region[0].text
    total_in_region['died_today'] = br_today_in_region[1].text
    total_in_region["cured_today"] = br_today_in_region[2].text
    return total_in_region
