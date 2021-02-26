import sqlite3
import numpy as np
import matplotlib.pyplot as plt

def displayData(passedDiction):
    """used to display graphs I have it set to display top 10 results based on frequency"""
    NamesXAxis = []
    FrequencyYAxis = []

    for i in range(0,10):#Where top ten results are gotten increase 10 to increase results
        curMax = max(passedDiction, key = passedDiction.get)
        NamesXAxis.append(curMax)
        FrequencyYAxis.append(passedDiction[curMax])
        passedDiction.pop(curMax)

    y_pos = np.arange(len(FrequencyYAxis))
    plt.bar(y_pos, FrequencyYAxis,width = 0.8)
    plt.xticks(y_pos, NamesXAxis,rotation = 80)
    plt.tight_layout()
    for index, value in enumerate(FrequencyYAxis):
        plt.text(index, value, str(value))
    plt.show()

def parse():
    """Used to see how many request each internal page makes"""

    conn = sqlite3.connect("crawl-data.sqlite")
    cur = conn.cursor()
    cur.execute("SELECT extension_session_uuid,url FROM http_requests")
    rows = cur.fetchall()
    infodict = {}
    links = open("TextFiles/revisedList.txt", 'r')
    curPage = links.readline()
    curPage = curPage.strip('\n')
    count = 1
    sumOfVisits = 0
    curId = ""
    curSum = 0

    #Have a count that goes to 5 since we only visited 5 internal pages
    for row in rows:
        #Once count reaches 5 we assume we are done with a specific websites internal pages
        #And add it to the list and reset vars
        if count == 5:
            #Dividing result by 5 to find average amount of third party requests
            infodict[curPage] = sumOfVisits/5
            curPage = links.readline()
            sumOfVisits = 0
            count = 0
        #Else Just continue counting number of third party requests.
        if curId != row[0]:
            curId = row[0]
            count += 1
            sumOfVisits += curSum
            curSum = 0   
        else:
            curSum += 1

    displayData(infodict)

def httpWebsites():
    """Gotten from my Project 2
    Used to see which type of third parties we are requesting from
    No changes made"""

    conn = sqlite3.connect("crawl-data.sqlite")
    cur = conn.cursor()
    cur.execute("SELECT extension_session_uuid,url FROM http_requests")
    rows = cur.fetchall()
    infodict = {}
    curID = ""
    curDomain = ""

    for row in rows:
        websitetemp = row[1].split("/")
        website = websitetemp[2] 
        if(curID != row[0]):
            curID = row[0]
            curDomain = website
        elif(curDomain in website):
            continue
        else:
            if(website in infodict):
                infodict[website] = infodict[website] + 1
            else:
                infodict[website] = 1
    displayData(infodict)
    
def CompareToHisList():
    """Compare my results to the HisPar List and sees how many of my internal pages
    are in HisPar List"""
    
    myList = open("TextFiles/AllSubPages.txt",'r')
    hisList = open("TextFiles/hisList.txt", 'r')

    #HisPar List opened and put into list for easier lookup
    hisListList = []
    for line in hisList:
        line = line.strip('\n')
        hisListList.append(line)

    similar = 0
    different = 0
    #Look for websites from my list in HisPar List
    for line in myList:
        line = line.strip('\n')
        if line in hisListList:
            similar += 1
        else:
            different += 1

    print(str(similar) + " InternalPages found in common")
    print(str(different) + " InternalPages unique to my lookup")

def reviseMyList():
    """Used to take out websites I was unable to visit
    From the list of top 100 Websites to make parsing earsier for me"""

    f = open("100MainPages.txt",'r')
    r = open("TextFiles/NoSubPageGet.txt", 'r')
    p = open("TextFiles/revisedList.txt", 'w')

    badURl = []
    for line in r:
        revisedLine = revisedLine.strip('\n')
        badURl.append(revisedLine)

    for line in f:
        line = line.strip('\n')
        if line in badURl:
            continue
        else:
            p.write(line)
            p.write('\n')

reviseMyList()
CompareToHisList()
parse()
httpWebsites()
