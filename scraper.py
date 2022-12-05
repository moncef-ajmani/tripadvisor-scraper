# import required libraries
import requests
from bs4 import BeautifulSoup
import re
import math 
import csv
import time 
import sys 
from termcolor import colored
import pandas as pd



# define headers variable to be used in all requests
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

# define a function get_number_pages that takes an url as a parameter and return the number of pages of search results
def getHTML(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content,'html5lib')
    return soup
    
# define a function get_number_pages that takes an url as a parameter and return the number of pages of search results
def get_number_pages(url):
    soup = getHTML(url)
    number_pages = math.ceil(int(re.findall("^\d*",soup.find('span',{"class":"qrwtg"}).text)[0]) / 30)
    return number_pages

def get_total_reviews(url):
    soup = getHTML(url)
    text =  soup.find('label',{'for':'LanguageFilter_1'}).find('span',{'class':'POjZy'}).text
    return int(''.join(re.findall("[0-9]+",text)))

# define a function get_hotels_links_reviews_count that takes an url as a parameter and return a list of links of all hotels
def get_hotels_links_reviews_count(url,filename):
    data = []
    total=0
    with open(f'{filename}_count.csv','w') as f:
        writer = csv.DictWriter(f, fieldnames = ["link","reviews_count"])
        writer.writeheader()
    # get all hotels links with reviews count
        
        for i in range(0,261,30):
            link=url
            if i!=0:
                link = re.split("-",url)
                link.insert(2,f"oa{i}")
                link = "-".join(link)
            print(link)
            soup = getHTML(link) 
            
            for row in soup.find_all("div",{"class":"listing"}):
                obj = {}
                obj["link"] = row.find("div",{"class":"listing_title"}).a['href']
                try:
                    obj["reviews_count"] = get_total_reviews(f'https://www.tripadvisor.in/{obj["link"]}')
                    if obj["reviews_count"]:
                        total+=obj["reviews_count"]
                        data.append(obj)
                except:
                    pass
        print(f"{colored(len(data), 'green')} hotels have reviews.")
        print(f"{colored(total, 'green')} reviews founded.")
        writer.writerows(data)
    return data

# define a function get_reviews_from_hotel that takes an url as a parameter and return a list of reviews
def get_reviews_from_hotel(url,number_reviews):
    reviews = []      
    x=0
    
    print("Number reviews: ",number_reviews)
    for i in range(0,number_reviews,10):   
        link=url
        # print(link)
        if i!=0:
            link = re.split("-",url)
            link.insert(4,f'or{i}')
            link = "-".join(link)
        
        soup = getHTML(link)
        
        x+=len(soup.find_all("div",{"class":"WAllg _T"}))
        print(f"URL: {link}")
        for row in soup.find_all("div",{"class":"WAllg"}):
            review = {}
            review["text"]= row.find("q",{"class":"QewHA"}).text
            review["rating"] = int(re.findall("\d*$",row.find("div",{"class":"Hlmiy"}).span["class"][1])[0])/10
            reviews.append(review)
        
            
    print(f"{len(reviews)}/{x}\n")
    return reviews

def get_reviews(url,filename):
    reviews_count=0
    with open(f"{filename}.csv","w",encoding='utf-8') as f:
        get_hotels_links_reviews_count(url,filename)
        df = pd.read_csv(f"{filename}_count.csv")
        df = df.drop_duplicates()
        links = df.to_numpy()
        writer = csv.DictWriter(f,fieldnames=["text","rating"])
        writer.writeheader()
        for row in links:
            reviews = get_reviews_from_hotel(f"https://www.tripadvisor.in{row[0]}",row[1])
            writer.writerows(reviews)
            reviews_count+=len(reviews)
            print(f"{colored(reviews_count,'green')} reviews added.")

# main Program 
if __name__ == "__main__":
    start_time = time.time()

    print(colored("Start...",'blue'))

    get_reviews(sys.argv[1],sys.argv[2])
    print(colored("\nDone :)","blue"))

    print(colored("--- %s seconds ---"%(time.time() - start_time),"yellow"))
