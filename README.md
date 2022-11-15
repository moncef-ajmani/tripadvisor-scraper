#Tripadvisor scrapper

This is a scrapper that scrapes reviews from tripadvisor.

## Requirements

- Python 3.7.4
- BeautifulSoup 4
- requests 2.22.0
- csv
- termcolor

## Usage

- Run the following command to install the required libraries:

pip install -r requirements.txt

- Run the scrapper.py file with the following command:

python scrapper.py <url> <filename> [<max_reviews_per_hotel>]

- <url>: The URL of the search results page on tripadvisor.
- <filename>: The name of the CSV file that will be created.
- <max_reviews_per_hotel>: (optional) The maximum number of reviews to be scraped from each hotel. If not specified, all reviews will be scraped.

## Example

python scrapper.py https://www.tripadvisor.com/Hotels-g293732-Casablanca_Casablanca_Settat-Hotels.html casablanca_hotels_reviews 10

This will scrape reviews from all hotels reviews
