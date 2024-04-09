import requests
from bs4 import BeautifulSoup

def scrape_tweet(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tweet_text_box = soup.find("div", {"class": "tweet-text"})
    tweet_text = tweet_text_box.text

    return tweet_text

url = 'https://twitter.com/foggymedia_/status/1681958197664555008'
print(scrape_tweet(url))
