#Write a domain function that counts the number of subdomains.
#How many subdomains did you find in the ics.uci.edu domain? Submit the list of subdomains ordered alphabetically
# and the number of unique pages detected in each subdomain. The content of this list should be lines containing URL,
# number, for example:
#http://vision.ics.uci.edu, 10 (not the actual number here)
def count_domain(subdomain) -> int:
    pass


#Write a unique page function.
#How many unique pages did you find? Uniqueness for the purposes of this assignment is ONLY established by the URL,
# but discarding the fragment part. So, for example, http://www.ics.uci.edu#aaa and http://www.ics.uci.edu#bbb are
# the same URL. Even if you implement additional methods for textual similarity detection, please keep considering
# the above definition of unique pages for the purposes of counting the unique pages in this assignment.
def unique_page() -> int:
    pass

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
def common_words() -> int:
    pass