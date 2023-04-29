from collections import Counter
from urllib.parse import urlparse

#Write a domain function that counts the number of subdomains.
#How many subdomains did you find in the ics.uci.edu domain? Submit the list of subdomains ordered alphabetically
# and the number of unique pages detected in each subdomain. The content of this list should be lines containing URL,
# number, for example:
#http://vision.ics.uci.edu, 10 (not the actual number here)
def count_domain(URLListFile) -> int:
    solution = open('Solution.txt', 'a')
    subdomainDict = dict()
    for url in URLListFile:
        parsed = urlparse(url)
        netloc = parsed.netloc
        netlocList = netloc.split('.')
        subdomain = ''
        if len(netlocList) >= 4:
            subdomain = '.'.join(netlocList[1:])
        if subdomain == 'ics.uci.edu':
            if netloc in subdomainDict:
                subdomainDict[netloc] += 1
            else:
                subdomainDict[netloc] = 1

    solution.write('4. Subdomain num = ' + str(len(subdomainDict)) + '\n')
    for key, value in subdomainDict.items():
        solution.write(key + ' ' + str(value) + '\n')
    solution.close()


#Write a unique page function. - Alex
#How many unique pages did you find? Uniqueness for the purposes of this assignment is ONLY established by the URL,
# but discarding the fragment part. So, for example, http://www.ics.uci.edu#aaa and http://www.ics.uci.edu#bbb are
# the same URL. Even if you implement additional methods for textual similarity detection, please keep considering
# the above definition of unique pages for the purposes of counting the unique pages in this assignment.
def unique_page(URLListFile) -> int:
    solution = open('Solution.txt', 'a')
    unique = set()
    for url in URLListFile:
        unique.add(url)
    solution.write('1. The number of unique pages is ' + str(len(unique)) + '\n')
    solution.close()

#Write the longest page function. - Vini
#What is the longest page in terms of the number of words? (HTML markup doesn’t count as words)
def longest_page(contentFile):
    solution = open('Solution.txt', 'a')

    longest = 0
    longest_page = ''

    for length in range(1, len(contentFile), 2):
        if int(contentFile[length]) > longest:
            longest = int(contentFile[length])
            longest_page = contentFile[length - 1]

    solution.write('2. The longest page is ' + longest_page + 'with ' + str(longest) + ' words.' + '\n')
    solution.close()



#Write a common word function. - Oscar
#What are the 50 most common words in the entire set of pages crawled under these domains ? (Ignore English stop words,
#which can be found, for example, hereLinks to an external site.) Submit the list of common words ordered by frequency.
def common_words(word_list) -> list:
    frequency_list = []
    frequency = Counter(word_list)
    for word in frequency.most_common(50):
        frequency_list.append(word)
    return frequency_list

