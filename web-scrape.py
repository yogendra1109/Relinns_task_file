import requests
from bs4 import BeautifulSoup
import _pickle
import re
from nltk.corpus import stopwords
import nltk

# Download NLTK stopwords if not already downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def clean_webpage_content(webpage_content):
    # Remove JavaScript code
    webpage_content = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', webpage_content, flags=re.DOTALL)

    # Remove HTML tags
    webpage_content = re.sub(r'<[^>]+>', '', webpage_content)

    # Remove unnecessary text
    unwanted_phrases = [
        r'.*?Claim close',
        r'Integrations arrow_right_alt.*?Key Features arrow_right_alt',
        r'ComparisonsBotPenguin Vs.*?LandbotProduct What do\?Who use it\?Where run\?',
        r'Pricing Chatbot Pricing \(except WA\) arrow_right_alt.*?Website, Telegram, Facebook Live Chat bots',
        r'Partners Partners Home arrow_right_alt.*?Earn clients happierImplementation Partners arrow_right_alt',
        r'expand_more Integrations arrow_right_alt.*?expand_more DO MORE Chat Automation!',
        re.escape(r'arrow_right_alt'),
        re.escape(r'Enter Name*Enter Email*+ expand_more Enter Phone NumberEnter Facebook Page Link*10k 100k100k 1Mn1Mn 3Mn3Mn 10Mn10Mn+ Select number followers*Less 100k100k 500k500k+ Select number FB messages get*Enter informationCancelClaimBy submitting form agree terms. View privacy policy learn use information.'),
    ]
    for phrase in unwanted_phrases:
        webpage_content = re.sub(phrase, '', webpage_content, flags=re.DOTALL)

    # Remove extra whitespaces
    webpage_content = ' '.join(webpage_content.split())

    # Remove stopwords using NLTK
    stop_words = set(stopwords.words('english'))
    words = webpage_content.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    webpage_content = ' '.join(filtered_words)

    return webpage_content

def links(website_html: str) -> list[str]:
    soup = BeautifulSoup(website_html, 'html.parser')
    return {link.get('href', ''): link.get('href', '') for link in soup.find_all('a') if link.get('href')}

def scrape_and_store(url, label):
    print(f"Scraping {label} ({url})")
    try:
        response = requests.get(url, timeout=10, verify=False)  # Disable SSL verification
        response.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Error making request to {url}: {e}")
        return None, None  # Return None, None instead of just None

    if response.status_code != 200:
        print(f"Error: non-200 status code received from {url}")
        return None, None  # Return None, None instead of just None

    soup = BeautifulSoup(response.text, 'html.parser')
    website_html = soup.prettify()
    links_list = links(website_html)
    print(f"Links Found on {label}: {len(links_list)}")
    website_content = soup.get_text()

    return website_content, links_list


if __name__=='__main__':
    
    website_urls = {"BotPenguin Homepage": "https://botpenguin.com/"}  # Using BotPenguin's website

    # Save the website text content and links in a pickled file if the file does not exist, it will create one.
    for label, url in website_urls.items():
        website_content, links_list = scrape_and_store(url, label)
        if website_content is not None and label is not None:
            cleaned_content = clean_webpage_content(website_content)
            print(cleaned_content)
            data = {'label': label, 'context': cleaned_content, 'links': links_list}
            with open('data.pkl', 'wb') as file:
                _pickle.dump(data, file)
            print(f"{label} data extracted")