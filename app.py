# Scrape reviews from tripadvisor
import requests
from bs4 import BeautifulSoup
import re
import math 
import csv

headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

url = "https://www.tripadvisor.com/Hotels-g293732-Casablanca_Casablanca_Settat-Hotels.html"

# get number of pages from url link of hotel search
def get_number_pages(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content,'html5lib')
    number_pages = math.ceil(int(re.findall("^\d*",soup.find('span',{"class":"qrwtg"}).text)[0]) / 30)
    return number_pages


# get hotels links from the url and write them into a txt file
def get_hotels_link_rating(filename,url):
    data = []

    # get all hotels links
    for i in range(0,get_number_pages(url)):
        if i!=0:
            url = re.split("-",url)
            url.insert(2,f"oa{i*30}")
            url = "-".join(url)
        
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content,'html5lib')
        for row in soup.find_all("div",{"class":"listing"}):
            obj = {}
            obj["link"] = row.find("div",{"class":"listing_title"}).a['href']
            obj["reviews_count"] = int(re.split(" ",row.find("a",{"class":"review_count"}).text)[0].replace(",",""))
            data.append(obj)
    # write into a csv file all hetels link
    with open(filename,'w') as f:
        writer = csv.DictWriter(f, fieldnames = ["link","reviews_count"])
        writer.writeheader()
        writer.writerows(data)


def get_reviews_from_hotel(url,number_reviews):
    reviews = []
    for i in range(0,int(number_reviews/10)):
        if url!=0:
            url = re.split("-",url)
            url.insert(4,f'or{i*10}')
            url = "-".join(url)

        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content,'html5lib')
        for row in soup.find_all("div",{"class":"WAllg _T"}):
            review = {}
            review["text"]= row.find("q",{"class":"QewHA"}).text
            review["rating"] = int(re.findall("\d*$",row.find("div",{"class":"Hlmiy"}).span["class"][1])[0])/10
            reviews.append(review)
    
    # # write into a csv file all hetels link
    # with open("reviews.csv",'w') as f:
    #     writer = csv.DictWriter(f, fieldnames = ["text","rating"])
    #     writer.writeheader()
    #     writer.writerows(reviews)
    return reviews

def get_reviews():
    pass



