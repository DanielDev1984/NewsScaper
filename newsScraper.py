import os
from bs4 import BeautifulSoup
import requests

os.system('color')
os.system("Cls") #clears screen



#### code for the logo BEGIN
# todo: try to understand the coloring in its entirety
rainbow_colors = ['#FF0900', '#FF7F00', ' #FFEF00', '#00F11D', ' #0079FF', ' #A800FF'] #for rainbow colored prints

def print_rainbow_colors_loop(string):
	global rainbow_currently_at #global value
	currently_in_function = 0 #change data per function call
	for letter in string: #per letter string
		printC(letter, color=rainbow_colors[rainbow_currently_at], end='') #print color
		#change rainbow color
		if currently_in_function % 2 == 0:
			rainbow_currently_at += 1
			if rainbow_currently_at % 6 == 0:
				rainbow_currently_at = 0
		currently_in_function += 1

rainbow_currently_at=0 #global rainbow value

valid_hex = '0123456789ABCDEF'.__contains__ #constrains for printing colors

#clean the hex code
def clean_hex(data):
	return ''.join(filter(valid_hex, data.upper())) #better hex code


#Print Colors
def printC(text, color='#ffffff', end='\n'):
	hexint = int(clean_hex(color), 16) #get int of hexcode
	print("\x1B[38;2;{};{};{}m{}\x1B[0m".format(hexint>>16, hexint>>8&0xFF, hexint&0xFF, text),end=end) #prints color in the cmd window

with open('logo.txt', 'r') as f:
    for line in f:
        print_rainbow_colors_loop(line)
f.close()
print("\n")
#### code for the logo END

#### code for the scraper BEGIN
page_to_scrape = requests.get("https://www.rheinfelden.de/de/aktuell/Staedtische-Nachrichten")
soup = BeautifulSoup(page_to_scrape.text, "html.parser")
# date of the articles
dates = soup.findAll("div", attrs={"class":"cNews_rowDate"})
# title of the articles
headers = soup.findAll("div", attrs={"class":"cNews_rowTitle"})
# preview / teaser of the articles
teasers = soup.findAll("div", attrs={"class":"cNews_rowTeaser"})
# links to the referenced articles -> needed for extracting the articleID to allow for determining whether there are new articles available
links = soup.findAll("a", attrs={"class":"cNews_rowLink"})

# really simple / volatile way of determining which articles already have been read / displayed by the scraper
# read ID of last read entry from previous session
f = open("lastID.txt", "r")
lastID = int(f.read())
f.close()

# safe ID of most recent entry of the current fetch / get
mostRecetID = int(links[0]['href'].split('&id=')[1])
# always persist most recent entry
f = open("lastID.txt", "w")
f.write(str(mostRecetID))
f.close()   

# determine wether there has been a new article pusblished since the last time the script has been executed
updateAvailable = (mostRecetID > lastID) 

# helper index to iterate over all fetched arrays
# todo: isnt there an easier way to iterate over all of the relevant data?
i=0
for header in headers:
    #
    # last read entry, only highlighted when an update is available
    if updateAvailable and (lastID == int(links[i]['href'].split('&id=')[1])):
        print( dates[i].text + '\33[101m' + header.text + '\033[0m')
    else:
        # entry newer than last read, visual indication
        if lastID < int(links[i]['href'].split('&id=')[1]):
            print( dates[i].text + '\33[100m' + header.text + '\033[0m')
        # entry older than last read, headers are visually taken out of the readers focus
        else:
            print( dates[i].text + '\33[90m' + header.text + '\033[0m')
    print(teasers[i].text + "\n")
    i = i + 1
#### code for the scraper END
