import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque

def find_and_store_specific_words(url, words_to_find, output_file):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        # Send a GET request to the URL with custom headers
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Get the text content of the page
            page_text = soup.get_text()
            
            # Search for each word in the list within the page text
            found_words = []
            for word in words_to_find:
                if word.lower() in page_text.lower():
                    found_words.append(word)
            
            # Write the found words to the output file
            with open(output_file, 'a') as file:
                if found_words:
                    file.write(f'Found on {url}:\n')
                    file.write(', '.join(found_words) + '\n\n')
                    
            # Extract all hyperlinks from the page
            links = [urljoin(response.url, link.get('href')) for link in soup.find_all('a')]
            
            return links
        else:
            print(f'Failed to retrieve the webpage ({response.status_code}): {url}')
    except Exception as e:
        print(f'An error occurred while visiting {url}: {e}')
    return []

def crawl_from_website(seed_url, words_to_find=None, output_file='found_words.txt', max_pages=None):
    visited_urls = set()
    queue = deque([seed_url])
    
    while queue:
        current_url = queue.popleft()
        
        if current_url not in visited_urls:
            visited_urls.add(current_url)
            
            print(f'Crawling: {current_url}')
            linked_urls = find_and_store_specific_words(current_url, words_to_find, output_file)
            
            if max_pages is not None and len(visited_urls) >= max_pages:
                print("Reached maximum pages limit.")
                break
            
            for linked_url in linked_urls:
                if linked_url not in visited_urls:
                    queue.append(linked_url)

# Example usage:
seed_url = 'https://example.com'  # Replace this with the starting website URL
words_to_find = ['money', 'fraud', 'scam']  # Specify the words you want to find
output_file = 'found_words.txt'  # Specify the name of the output file
max_pages = 100  # Maximum number of pages to crawl
crawl_from_website(seed_url, words_to_find=words_to_find, output_file=output_file, max_pages=max_pages)

