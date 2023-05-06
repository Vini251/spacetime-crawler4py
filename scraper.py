import re
from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from simhash import Simhash

#set that keeps track of all the urls crawled till now
crawled_URLs = set()
#hash values on all websites
all_website_hash = []
#min word count for low value urls
MIN_WORD_COUNT = 150 


def tokenize(text):
    """This function takes in the text of the html content and tokenize the text with specific stopwords incorportated."""
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
    """Scraper function return the list of links found in the url to the frontier for it to crawl next"""
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def check_duplicate(soup):
    """detects crawler traps using simhash to get the similarity of the text of the urls"""
    soup_simhash = Simhash(soup.text)
    #Loop through the list of all hash values of the previous urls and check if the difference is less than 5. If it is discard the url, if not then move to extract_next_link().
    for shash in all_website_hash:
        if(soup_simhash.distance(shash) <= 5):
            return True
    all_website_hash.append(soup_simhash)
    return False

    
def extract_next_links(url, resp):
    """This function takes in 2 arguments url and response of url. This is function returns the list of links that it found from the the html content of the url given to it."""
    linkList = []
    crawled = False
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
    if crawled == False and is_valid(url) and resp.status >= 200 and resp.status <= 299:  
        
        #get the html doc of the response and apply Beautiful soup to parse the html content
        html_doc = resp.raw_response.content    
        soup = BeautifulSoup(html_doc, 'html.parser')

        #checks to see if hash_value already exists in all_website_hash. "False" meaning this link is unique and is not similar to previous links    
        if(check_duplicate(soup) == False):

            #tokenize the content of the soup
            content_tokenized = tokenize(soup.getText())
        
            #adds up total word cord from URL
            for value in content_tokenized.values():
                total_word_count+=value
                
            #checks word count
            if(total_word_count >= MIN_WORD_COUNT):
                #appends url and word count to contentFile.txt
                with open("contentFile.txt", "a") as contentFile:
                    contentFile.write(url + '\n' + str(total_word_count) + '\n')

                #Append the urls and the content on tokenized form to file.
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

                #find all links that are present in the html content of the current url
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
    """This function checks for the validity of the url that is passed to it as argument."""
    try:
        parsed = urlparse(url)
        #The url should have the scheme of these two or else is not accepted
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        #If the url contains "format=" discard it
        if "format=" in url:
            return False

        #This part checks with the url ends with one of these extensions or does it contain these parts in the url. if it does return False.
        #This also checks if the domain is in the 4 main given domains or not
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|mpg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|ppsx|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()) and \
            not re.search(  
               r".*\.(css|js|bmp|gif|jpe?g|ico"
               + r"|png|tiff?|mid|mp2|mp3|mp4"
               + r"|wav|avi|mov|mpeg|mpg|ram|m4v|mkv|ogg|ogv|pdf"
               + r"|ps|eps|tex|ppt|ppsx|pptx|doc|docx|xls|xlsx|names"
               + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
               + r"|epub|dll|cnf|tgz|sha1"
               + r"|thmx|mso|arff|rtf|jar|csv"
               + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.query.lower()) and \
            re.search(r".*\.(ics.uci.edu|cs.uci.edu|informatics.uci.edu|stat.uci.edu)", parsed.netloc.lower()) and \
            not re.search(r"(calendar.ics.uci.edu)", parsed.netloc.lower()) 

    #If there is a type error print this line
    except TypeError:
        print("TypeError for ", parsed)
        raise




#TESTING
# URL = "http://www.stat.uci.edu"
# response = requests.get(URL)
# #print(tokenize(URL))

# link = scraper(URL, response)
# for links in link:
#     print(links)
# print(len(link))