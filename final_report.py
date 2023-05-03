import operator
# from collections import Counter
from urllib.parse import urlparse

#Write a unique page function. - Alex
#How many unique pages did you find? Uniqueness for the purposes of this assignment is ONLY established by the URL,
# but discarding the fragment part. So, for example, http://www.ics.uci.edu#aaa and http://www.ics.uci.edu#bbb are
# the same URL. Even if you implement additional methods for textual similarity detection, please keep considering
# the above definition of unique pages for the purposes of counting the unique pages in this assignment.
def unique_page(urlListFile) -> int:
    solution = open('Solution.txt', 'a')
    unique = set()
    for url in urlListFile:
        unique.add(url)
    solution.write('1. The number of unique pages is ' + str(len(unique)) + '\n')
    solution.close()

def longest_page(URLcontentList):
    solution = open('Solution.txt', 'a')
    solution.write('2. ')

    longest = 0
    longest_page = ''

    for length in range(1, len(URLcontentList), 2):
        if int(URLcontentList[length]) > longest:
            longest = int(URLcontentList[length])
            longest_page = URLcontentList[length - 1]

    solution.write('The longest page is ' + longest_page + 'with ' + str(longest) + ' words.' + '\n')
    solution.close()

def common_words(URLcontent):
    stopwords = []
    stopwordsFile = open('stopwords.txt', 'r')
    for line in stopwordsFile:
        stopwords.append(line.rstrip())
    stopwordsFile.close()

    solution = open('Solution.txt', 'a')
    solution.write('3. The 50 most common words are: \n')

    wordNumDict = dict()
    for URLcontents in URLcontent[1::2]:
        contents = URLcontents.split(',')
        for content in contents:
            word = content.lower().strip().replace("'", '')
            if word in stopwords:
                continue
            if word in wordNumDict:
                wordNumDict[word] += 1
            else:
                wordNumDict[word] = 1

    mostCommonList = []
    for num in range(0,50):
        mostCommon = max(wordNumDict.items(), key = operator.itemgetter(1))[0]
        mostCommonList.append(mostCommon)
        wordNumDict[mostCommon] = 0
    for word in mostCommonList:
        solution.write(word + '\n')
    solution.close()

#Write a domain function that counts the number of subdomains.
#How many subdomains did you find in the ics.uci.edu domain? Submit the list of subdomains ordered alphabetically
# and the number of unique pages detected in each subdomain. The content of this list should be lines containing URL,
# number, for example:
#http://vision.ics.uci.edu, 10 (not the actual number here)
def count_domain(urlListFile) -> int:
    solution = open('Solution.txt', 'a')
    subdomainDict = dict()
    for url in urlListFile:
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


if __name__ == '__main__':
    urlListFile = open('URLListFile.txt', 'r')
    contentFile = open('contentFile.txt', 'r')
    URLcontentFile = open('URLcontentfile.txt', 'r')
    

    URLlist = []
    URLcontentList = []
    URLcontent = []
    

    for line in urlListFile:
        URLlist.append(line)

    for line in contentFile:
        URLcontentList.append(line)

    for line in URLcontentFile:
        URLcontent.append(line)

    unique_page(URLlist)
    longest_page(URLcontentList)
    common_words(URLcontent)
    count_domain(URLlist)

    urlListFile.close()
    contentFile.close()
    URLcontentFile.close()



