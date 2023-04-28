import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests

crawled_URLs = set()

def tokenize(text):
    # Tokenize the text into words
    tokens = word_tokenize(text)
    stopwordfile = open("stopwords.txt")
    # Remove stop words
    stop_words = [word for word in stopwordfile]
    tokens = [token for token in tokens if token.lower() not in stop_words]

    # Count the frequency of each token
    token_freq = nltk.FreqDist(tokens)
    stopwordfile.close()
    return token_freq


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    linkList = []
    crawled = False
    content = []
    total_word_count = 0

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
    if crawled == False and is_valid(url) and resp.status >= 200 and resp.status <= 202:  #Use this line for crawler
    #if crawled == False and is_valid(url) and resp.status_code >= 200 and resp.status_code <= 202:
        with open("nextLink.txt", "a") as nextLinkFile:

            html_doc = resp.raw_response.content    #use this line for crawler
            #html_doc = resp.content
            soup = BeautifulSoup(html_doc, 'html.parser')

            text = soup.get_text()
            content = tokenize(text)
            with open("contentFile.txt", "a") as contentFile:
                contentFile.write(url + ' - ' + str(len(content)) + '\n')
            

            for link in soup.find_all('a'):
                urlLink = link.get('href')
                if urlLink == None:
                    continue
                if(urlLink not in linkList) and is_valid(urlLink):
                    if urlLink.find("#") != -1:
                        urlLink = urlLink[:urlLink.find("#")]
                    linkList.append(urlLink)
                    nextLinkFile.write(urlLink + "\n")

            

    return linkList


def is_valid(url):
    try:
        if "/pdf/" in url or "mailto:" in url or "@" in url:
            return False
        parsed = urlparse(url)
       
        if parsed.scheme not in set(["http", "https"]):
            return False


        if ("ics.uci.edu" in parsed.netloc or "cs.uci.edu" in parsed.netloc or "informatics.uci.edu" in parsed.netloc or "stat.uci.edu" in parsed.netloc) or (parsed.netloc == "" and str(parsed.path)[0:len("today.uci.edu/department/information_computer_sciences")] == "today.uci.edu/department/information_computer_sciences"):
            if (re.match(
                r".*\.(css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1"
                + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", url.lower())):
                    return False
            return not re.match(
                r".*\.(css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf|mpg"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1"
                + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|war|"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
        return False


    except TypeError:
        print("TypeError for ", parsed)
        raise





# URL = "http://www.stat.uci.edu"
# response = requests.get(URL)

# link = scraper(URL, response)
# for links in link:
#     print(links)
# print(len(link))
