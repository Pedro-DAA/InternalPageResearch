import urllib.request
from bs4 import BeautifulSoup
import random


def GetSubPages(mainPages):
    """Used to look at landing Pages and look for internal pages
    Stores results in text files
    AllSubPages.txt contains all the internal pages we found
    SubPageLess.txt cotains 5 randomly chosen internal pages from what we found
    NoSubPageGet.txt contains all the websites that we were unable to get internal pages from"""

    file = open(mainPages, "r")
    allPages = open("TextFiles/AllSubPages.txt", "w")
    lessSubPages = open("SubPagesLess.txt", "w")
    noSubPage = open("TextFiles/NoSubPageGet.txt", "w")

    for mainPageLink in file:
        SubPageList = []
        mainPageLink = mainPageLink.strip('\n')

        #trying to requests the html file from the websites
        try:
            response = urllib.request.urlopen(mainPageLink)
        except:
            noSubPage.write(mainPageLink)
            noSubPage.write("\n")
            continue
        html_doc = response.read()

        soup = BeautifulSoup(html_doc,'html.parser')
        
        #Looking for all instances of <a href = ""> Since that is a common way websites store url
        for link in soup.find_all('a'):
            url = link.get('href')
            if url == None:
                continue
            #I found that if a link contained // at the beginning that usually meant it was from a third party so I ignored those
            if(url[:2] == '//'):
                continue
            #Some internal pages also started with / and did not have a domain so I added that here
            elif(url[:1] == '/'):
                url = mainPageLink+url
            
            #Checking to see if it is a third party url if so ignore
            if(mainPageLink in url):
                SubPageList.append(url)
            else:
                continue
        #Checking to see if we have at least 5 internal pages
        #If so randomly choose 5 and at them to the list
        if(len(SubPageList) >= 5):
            for link in SubPageList:
                allPages.write(link)
                allPages.write('\n')
            for i in range(5):
                lessSubPages.write(random.choice(SubPageList))
                lessSubPages.write('\n')
        else: 
            noSubPage.write(mainPageLink)
            noSubPage.write('\n')

GetSubPages("100MainPages.txt")
