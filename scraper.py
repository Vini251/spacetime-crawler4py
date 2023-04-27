import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

crawled_URLs = set()

def tokenize(url):
    # Retrieve HTML content from the URL
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract text from the HTML content
    text = soup.get_text()

    # Tokenize the text into words
    tokens = word_tokenize(text)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.lower() not in stop_words]

    # Count the frequency of each token
    token_freq = nltk.FreqDist(tokens)

    return token_freq


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    # Implementation requred.
    linkList = []
    crawled = False
    crawled_URLs = set()

    nextLinkFile = open('nextLink.txt', 'a')


    check_URL = url
    #if the last character of URL is "/" remove it
    if url[-1] == '/':
        check_URL = url[:-1]
    
    #Check if the URl is already crawled or not in the crawled_URLs set
    if check_URL in crawled_URLs:
        crawled = True
    #If it is not present we add the URL to that set
    elif check_URL not in crawled_URLs:
        crawled_URLs.add(check_URL)

    #The status between 200 and 202 are good for crawling.
    #if crawled == False and is_valid(url) and resp.status >= 200 and resp.status <= 202:
    if crawled == False and is_valid(url) and resp.status_code >= 200 and resp.status_code <= 202:
        nextLinkFile.write(url + '\n')

        #html_doc = resp.raw_response.content
        html_doc = resp.content
        soup = BeautifulSoup(html_doc, 'html.parser')

        for link in soup.find_all('a'):
            url_Link = link.get('href')
            linkList.append(url_Link)

    nextLinkFile.close()

    return linkList


def is_valid(url):
    # Decide whether to crawl this url or not.
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False

        netloc = parsed.netloc

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise

URL = "http://www.stat.uci.edu"
response = requests.get(URL)
print(tokenize(URL))

link = extract_next_links(URL, response)
for links in link:
    print(links)
print(len(link))