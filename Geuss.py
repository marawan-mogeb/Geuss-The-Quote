import requests
from bs4 import BeautifulSoup
from csv import writer
from time import sleep
from random import choice, randint

# Function to fetch a webpage with headers
def fetch_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to scrape quotes from all pages
def scrape_quotes():
    all_quotes = []
    base_url = "http://quotes.toscrape.com"
    url = "/page/1"

    while url:
        print(f"Now scraping: {base_url}{url}")
        soup = fetch_page(f"{base_url}{url}")
        if not soup:
            break

        quotes = soup.find_all(class_="quote")
        for quote in quotes:
            try:
                all_quotes.append({
                    "text": quote.find(class_="text").get_text(),
                    "author": quote.find(class_="author").get_text(),
                    "bio-link": base_url + quote.find("a")["href"]
                })
            except AttributeError:
                print("Skipped a quote due to missing data.")
        
        next_btn = soup.find(class_="next")
        url = next_btn.find("a")["href"] if next_btn else None

        sleep(randint(1, 3))  
    return all_quotes

def play_game(quotes):
    quote = choice(quotes)
    remaining_guesses = 4
    print("\nWelcome to the Quote Guessing Game!")
    print("Here's your quote:")
    print(f"\"{quote['text']}\"")

    guess = ''
    while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
        guess = input(f"\nWho said this quote? Guesses remaining: {remaining_guesses}\n").strip()
        if guess.lower() == quote["author"].lower():
            print("\n🎉 CONGRATULATIONS!!! YOU GOT IT RIGHT 🎉")
            break
        remaining_guesses -= 1

        if remaining_guesses > 0:
            if remaining_guesses == 3:
                print("\nHint 1: Let me tell you something about the author...")
                bio_soup = fetch_page(quote["bio-link"])
                if bio_soup:
                    birth_date = bio_soup.find(class_="author-born-date").get_text()
                    birth_place = bio_soup.find(class_="author-born-location").get_text()
                    print(f"The author was born on {birth_date} {birth_place}.")
            elif remaining_guesses == 2:
                print(f"\nHint 2: The author's first name starts with '{quote['author'][0]}'.")
            elif remaining_guesses == 1:
                last_initial = quote["author"].split(" ")[1][0]
                print(f"\nHint 3: The author's last name starts with '{last_initial}'.")
        else:
            print(f"\n😞 Sorry, you're out of guesses. The correct answer was: {quote['author']}.")

    print("\nThank you for playing! 🎭")

if __name__ == "__main__":
    print("Initializing scraper...")
    quotes = scrape_quotes()
    if quotes:
        play_game(quotes)
    else:
        print("Failed to fetch quotes. Please try again later.")
