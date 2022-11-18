# import required libraries
import requests
from bs4 import BeautifulSoup
import re
import math 
import csv
import time 
import sys 
from termcolor import colored

# define headers variable to be used in all requests
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

reviews_count = 0

def getHTML(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content,'lxml')
    return soup

# define a function get_number_pages that takes an url as a parameter and return the number of pages of search results
def get_number_pages(url):
    soup = getHTML(url)
    number_pages = math.ceil(int(re.findall("^\d*",soup.find('span',{"class":"qrwtg"}).text)[0]) / 30)
    return number_pages

# define a function get_hotels_links_reviews_count that takes an url as a parameter and return a list of links of all hotels
def get_hotels_links_reviews_count(url):
    data = []
    # get all hotels links with reviews count
    for i in range(0,get_number_pages(url)):
        if i!=0:
            url = re.split("-",url)
            url.insert(2,f"oa{i*30}")
            url = "-".join(url)
         
        soup = getHTML(url)
        for row in soup.find_all("div",{"class":"listing"}):
            obj = {}
            obj["link"] = row.find("div",{"class":"listing_title"}).a['href']
            obj["reviews_count"] = int(re.split(" ",row.find("a",{"class":"review_count"}).text)[0].replace(",",""))
            data.append(obj)
    print(f"{colored(len(data), 'green')} hotels founded.")
    
    return data

def get_total_reviews(data):
    total = 0
    for row in data:
        total += row["reviews_count"]
    print(f"Total Reviews: {total}\n")
    return total

# define a function get_reviews_from_hotel that takes an url as a parameter and return a list of reviews
def get_reviews_from_hotel(url,number_reviews,max_reviews=0):
    global reviews_count
    reviews = []
    pages_count = int((number_reviews/10))+1
    if max_reviews:
        pages_count = int((max_reviews/10))+1

    for i in range(0,pages_count):
        if url!=0:
            url = re.split("-",url)
            url.insert(4,f'or{i*10}')
            url = "-".join(url)
        
        soup = getHTML(url)
        for row in soup.find_all("div",{"class":"WAllg _T"}):
            if(max_reviews and len(reviews) == max_reviews):
                reviews_count += max_reviews
                return reviews[:max_reviews]
            review = {}
            review["text"]= row.find("q",{"class":"QewHA"}).text
            review["rating"] = int(re.findall("\d*$",row.find("div",{"class":"Hlmiy"}).span["class"][1])[0])/10
            reviews.append(review)
    reviews_count += len(reviews)
    return reviews

# define a function get_reviews that takes 3 parameters (url,filename,max_reviews_per_hotel) and writes the scrapper data into a csv file
def get_reviews(url,filename,max_reviews_per_hotel=0):
    with open(f"{filename}.csv",'w',encoding="utf-8") as f:
        links = get_hotels_links_reviews_count(url)
        total = get_total_reviews(links)
        
        writer = csv.DictWriter(f, fieldnames = ["text","rating"])
        writer.writeheader()
        for row in links:
            if row['reviews_count']==0:continue
            reviews = get_reviews_from_hotel(f"https://www.tripadvisor.in{row['link']}",row['reviews_count'],max_reviews_per_hotel)
            writer.writerows(reviews)
            print(f"{colored(reviews_count, 'green')} / {total} reviews.",end="\r")
            
# main Program 
if __name__ == "__main__":
    start_time = time.time()

    print(colored("Start...",'blue'))
    max_reviews = 0
    if(len(sys.argv)>3):
        max_reviews = int(sys.argv[3])

    get_reviews(sys.argv[1],sys.argv[2])
    print(colored("\nDone :)","blue"))

    print(colored("--- %s seconds ---"%(time.time() - start_time),"yellow"))