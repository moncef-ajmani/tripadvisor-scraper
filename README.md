# Tripadvisor scrapper

This is a script that scrapes reviews of hotels from tripadvisor.

## Requirements

- Python 3.7.4
- BeautifulSoup 4
- requests 2.22.0
- csv
- termcolor

## Usage

- Run the following command to install the required libraries:

pip install -r requirements.txt

- Run the scraper.py file with the following command:

```
python scraper.py <url> <filename> [<max_reviews_per_hotel>]
```

* url: The search results page URL of TripAdvisor. For example: https://www.tripadvisor.com/Hotels-g293732-Casablanca_Casablanca_Settat-Hotels.html
* filename: The name of the CSV file where the scraped data will be stored. For example: casablanca_hotels_reviews
* max_reviews_per_hotel (optional): The maximum number of reviews to be scraped for each hotel. The default value is 0, which means all reviews will be scraped.

## Example

```
python scrapper.py https://www.tripadvisor.com/Hotels-g293732-Casablanca_Casablanca_Settat-Hotels.html casablanca_hotels_reviews 10
```

This will scrape reviews for all hotels in Cansablanca and store up to 10 reviews for each hotel in the file casablanca_hotels_reviews.csv.
