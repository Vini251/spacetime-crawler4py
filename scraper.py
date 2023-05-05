import re
from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import hashlib


crawled_URLs = set()
#hash values on all websites
all_website_hash = []
MIN_WORD_COUNT = 150


def tokenize(text):
    # Tokenize the text into words
    tokens = word_tokenize(text)
    
    # Remove non-alphabetic tokens
    tokens = [token for token in tokens if re.match("^[a-zA-Z]+$", token)]
    
    # Convert tokens to lowercase
    tokens = [token.lower() for token in tokens]
    
    # Remove stop words
    stopwordfile = open("stopwords.txt")
    stop_words = [word.strip() for word in stopwordfile]
    tokens = [token for token in tokens if token not in stop_words]
    stopwordfile.close()
    
    # Count the frequency of each token
    token_freq = nltk.FreqDist(tokens)
    return token_freq


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

#detects crawler traps
def trap_detection(url, threshold):
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.strip('/').split('/')
    path_set = set(path_segments)
    path_length = len(path_segments) - len(path_set)
    if(path_length >= threshold):
        return True
    else:
        return False

def check_duplicate(soup):
    global all_website_hash
    hash = hashlib.md5()
    #updates hash value for every key in tokenized_words
    hash.update(soup.getText().encode())
    #checks to see if hash value is in all_website_hash
    if(hash.hexdigest() in all_website_hash):
        return False  
    else:
        all_website_hash.append(hash.hexdigest())  
        return True

        
    
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
    if crawled == False and is_valid(url) and resp.status >= 200 and resp.status <= 299 and trap_detection(url, 1) == False:  #Use this line for crawler
    #if crawled == False and is_valid(url) and resp.status_code >= 200 and resp.status_code <= 202:
        html_doc = resp.raw_response.content    #use this line for crawler
        #html_doc = resp.content
        soup = BeautifulSoup(html_doc, 'html.parser')
        #checks to see if hash_value already exists in all_website_hash
        #tokenize function
        if(check_duplicate(soup)):
            content_tokenized = tokenize(soup.getText())
            #print(content_tokenized)
            #adds up total word cord from URL
            for value in content_tokenized.values():
                total_word_count+=value
        #checks word count
            if(total_word_count >= MIN_WORD_COUNT):
                #appends url and word count to contentFile.txt
                with open("contentFile.txt", "a") as contentFile:
                    contentFile.write(url + '\n' + str(total_word_count) + '\n')

                with open("URLcontentfile.txt", "a") as URLcontentFile:
                    text = soup.get_text()
                    tokens = word_tokenize(text)
                    with open("stopwords.txt") as stopwordfile:
                        # Remove non-alphabetic tokens
                        tokens = [token for token in tokens if re.match("^[a-zA-Z]+$", token)]
                        # Convert tokens to lowercase
                        tokens = [token.lower() for token in tokens]
                        stop_words = [word.strip() for word in stopwordfile]
                        tokens = [token for token in tokens if token not in stop_words]
                        URLcontentFile.write(url + '\n' + str(tokens) + '\n')
                    
                #appends url to URLListFile.txt
                with open("URLListFile.txt", "a") as urlListFile:
                    urlListFile.write(url + "\n")

                #find all links to url
                for link in soup.find_all('a'):
                    urlLink = link.get('href')
                    if urlLink == None:
                        continue
                    if urlLink.find("#") != -1:
                        urlLink = urlLink[:urlLink.find("#")]
                    absolute = urljoin(url, urlLink)
                    linkList.append(absolute)

    return linkList

def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|ppsx|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()) and \
            not re.search(  
               r".*\.(css|js|bmp|gif|jpe?g|ico"
               + r"|png|tiff?|mid|mp2|mp3|mp4"
               + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
               + r"|ps|eps|tex|ppt|ppsx|pptx|doc|docx|xls|xlsx|names"
               + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
               + r"|epub|dll|cnf|tgz|sha1"
               + r"|thmx|mso|arff|rtf|jar|csv"
               + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.query.lower()) and \
            re.search(r".*\.(ics.uci.edu|cs.uci.edu|informatics.uci.edu|stat.uci.edu)", parsed.netloc.lower()) and \
            not re.search(r"(calendar.ics.uci.edu)", parsed.netloc.lower())
            

    except TypeError:
        print("TypeError for ", parsed)
        raise





# URL = "http://www.stat.uci.edu"
# response = requests.get(URL)
# #print(tokenize(URL))

# link = scraper(URL, response)
# for links in link:
#     print(links)
# print(len(link))
