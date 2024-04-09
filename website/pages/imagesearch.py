import aiohttp
import asyncio
from lxml import html
import time

async def get_image_url(session, search_term):
    url = "https://www.bing.com/images/search?q={}".format(search_term.replace(' ', '%20'))
    response = await session.get(url)
    tree = html.fromstring(await response.text())
    image = tree.xpath('//img[@class="mimg"]')[0]
    return search_term, image.attrib['src']

async def get_first_image_url(search_terms):
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [get_image_url(session, term) for term in search_terms]
        results = await asyncio.gather(*tasks)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"The function took {elapsed_time} seconds to run.")
    return dict(results)

# Run the function with the search terms 'virat kohli pic', 'dhoni pic', and 'pm modi'
results = asyncio.run(get_first_image_url(['virat kohli pic', 'dhoni pic', 'pm modi','amit shah' , 'kapil dev' ,'geoge',' kohli pic', 'dhoi pic', 'pm ','amit ' , 'kl dev' ,'gege']))
print(results)
