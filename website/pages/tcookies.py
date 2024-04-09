import json
import requests

def get_twitter_cookies(email, username, password):
    session = requests.Session()

    # Authenticate and get the cookies
    login_url = 'https://twitter.com/i/api/2/authenticate'
    login_payload = {
        'session[username_or_email]': username,
        'session[password]': password,
    }
    response = session.post(login_url, data=login_payload)

    if response.status_code != 200:
        raise Exception(f"Failed to authenticate. Status code: {response.status_code}")

    # Get the ct0 and auth_token cookies
    ct0_cookie = session.cookies.get('ct0')
    auth_token_cookie = session.cookies.get('auth_token')

    return ct0_cookie, auth_token_cookie

def save_cookies_to_file(ct0_cookie, auth_token_cookie, file_path):
    cookies_data = {
        'ct0': ct0_cookie,
        'auth_token': auth_token_cookie,
    }

    # Save the cookies to the JSON file
    with open(file_path, 'w') as file:
        json.dump(cookies_data, file)

    print("Cookies have been saved to:", file_path)

if __name__ == '__main__':
    email, username, password = 'rohitdoc15@gmail.com', 'mullokamulla', 'Suckbuddy@69'
    ct0_cookie, auth_token_cookie = get_twitter_cookies(email, username, password)
    cookies_file_path = 'twitter.cookies'
    save_cookies_to_file(ct0_cookie, auth_token_cookie, cookies_file_path)
