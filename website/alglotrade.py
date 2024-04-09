import requests
import pyttsx3

def get_cryptopanic_posts(api_token, limit=20):
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={api_token}&public=true&limit={limit}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        posts = data.get('results', [])
        return posts
    else:
        print(f"Error fetching CryptoPanic posts. Status code: {response.status_code}")
        return []

def read_aloud(text):
    engine = pyttsx3.init('sapi5')
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    api_token = "67dfdad44a266c6da5f6f1e55638de5f0cd206d2"
    
    try:
        posts = get_cryptopanic_posts(api_token)

        if posts:
            for post in posts:
                title = post.get('title', '')
                print(title)
                read_aloud(title)
    except Exception as e:
        print(f"An error occurred: {e}")
