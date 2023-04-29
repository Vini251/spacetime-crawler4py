import re
from urllib.parse import urlparse
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

#detects crawler traps
def trap_detection(soup):
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
    if crawled == False and is_valid(url) and resp.status >= 200 and resp.status <= 202:  #Use this line for crawler
    #if crawled == False and is_valid(url) and resp.status_code >= 200 and resp.status_code <= 202:
        with open("nextLink.txt", "a") as nextLinkFile:

            html_doc = resp.raw_response.content    #use this line for crawler
            #html_doc = resp.content
            soup = BeautifulSoup(html_doc, 'html.parser')
            #checks to see if hash_value already exists in all_website_hash
            #tokenize function
            if(trap_detection(soup)):
                content_tokenized = tokenize(soup.getText())
                #adds up total word cord from URL
                for value in content_tokenized.values():
                    total_word_count+=value
            #checks word count
                if(total_word_count >= MIN_WORD_COUNT):
                    #appends url and word count to contentFile.txt
                    with open("contentFile.txt", "a") as contentFile:
                        contentFile.write(url + '\n' + str(total_word_count) + '\n')
                    #appends url to URLListFile.txt
                    with open("URLListFile.txt", "a") as urlListFile:
                        urlListFile.write(url + "\n")

                    #find all links to url
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
            not re.search(  #remove all urls with any queries that match the ending.
               r".*\.(css|js|bmp|gif|jpe?g|ico"
               + r"|png|tiff?|mid|mp2|mp3|mp4"
               + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
               + r"|ps|eps|tex|ppt|ppsx|pptx|doc|docx|xls|xlsx|names"
               + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
               + r"|epub|dll|cnf|tgz|sha1"
               + r"|thmx|mso|arff|rtf|jar|csv"
               + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.query.lower()) and \
            re.search( #url must contain one of the domains
                r".*\.(ics.uci.edu|cs.uci.edu|informatics.uci.edu|stat.uci.edu|"
                + r"today.uci.edu/department/information_computer_sciences)", parsed.netloc.lower()) and \
            not (re.search(r"\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])", parsed.path.lower()) and #remove urls that are from WICS calendar by path examination
                 re.search(r"(wics\.)", parsed.netloc.lower())) and \
            not re.search(r"(calendar.ics.uci.edu)", parsed.netloc.lower()) and \
            not re.search(r"(replytocom=)", parsed.query.lower()) and \
            not re.search(r"(version=)", parsed.query.lower()) and \
            not re.search(r"(share=)", parsed.query.lower()) and \
            not re.search(r"(wics-hosts-a-toy-hacking-workshop-with-dr-garnet-hertz)", parsed.path.lower()) and \
            not (re.search(r"(isg\.)", parsed.netloc.lower()) and re.search(r"(action=)", parsed.query.lower())) and \
            not (re.search(r"(mt-live\.)", parsed.netloc.lower()) and re.search(r"(events)", parsed.path.lower())) and \
            not (re.search(r"(mt-live\.)", parsed.netloc.lower()) and re.search(r"(filter)", parsed.query.lower()))


    except TypeError:
        print("TypeError for ", parsed)
        raise





# URL = "http://www.stat.uci.edu"
# response = requests.get(URL)
# print(tokenize(URL))

# link = scraper(URL, response)
# for links in link:
#     print(links)
# print(len(link))

