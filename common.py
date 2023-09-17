from bs4 import BeautifulSoup
import requests


def extract_predicted_age(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    result_div = soup.find('div', class_='aging41_results')
    h2_tag = result_div.find('h2')
    if h2_tag:
        text = h2_tag.get_text()
        # Extract the numeric value from the text
        age = float(text.split(":")[1].strip().split(" ")[0])
        return age
    return None


def send_post_request(data, headers):
    url = "http://aging.ai/aging-v3/?m=us"

    response = requests.post(
        url, headers=headers, data=data,
        verify=False)  # verify=False is equivalent to --insecure
    return response


def request_age(data):
    headers = {
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language":
        "en-US,en;q=0.9",
        "Cache-Control":
        "max-age=0",
        "Connection":
        "keep-alive",
        "Content-Type":
        "application/x-www-form-urlencoded",
        "Cookie":
        "csrftoken=4SdAofEdCaohTw7FZ2uHprZ7z4GAHhRZ",
        "DNT":
        "1",
        "Origin":
        "http://aging.ai",
        "Referer":
        "http://aging.ai/aging-v3/?m=us",
        "Upgrade-Insecure-Requests":
        "1",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    response = send_post_request(data, headers)

    html_content = response.text
    predicted_age = extract_predicted_age(html_content)
    return predicted_age
