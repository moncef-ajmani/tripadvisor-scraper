# Tripadvisor scraper

This is a script that scrapes reviews of hotels from tripadvisor.

## Requirements

- Python 3.7.4
- BeautifulSoup 4
- requests 2.22.0
- csv
- termcolor

## Usage

- Run the following command to install the required libraries:

```
pip install -r requirements.txt
```

- Run the scraper.py file with the following command:

```
python scraper.py <url> <filename>
```

* url: The search results page URL of TripAdvisor. For example: https://www.tripadvisor.com/Hotels-g293732-Casablanca_Casablanca_Settat-Hotels.html
* filename: The name of the CSV file where the scraped data will be stored. For example: casablanca_reviews

## Example

```
python scraper.py https://www.tripadvisor.com/Hotels-g293732-Casablanca_Casablanca_Settat-Hotels.html casablanca_reviews 
```

This will scrape reviews for all hotels in Cansablanca and store up  in the file name casablanca_reviews.csv.
