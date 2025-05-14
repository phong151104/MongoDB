import requests
from bs4 import BeautifulSoup
import time

def get_html_from_url(url):
    """
    Crawl HTML content from URL
    Returns empty string if URL is invalid or request fails
    """
    if not url:
        return ""
        
    try:
        # Add delay to avoid being blocked
        time.sleep(1)
        
        # Set headers to mimic browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Make request
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text
        html_content = soup.prettify()
        return html_content
        
    except Exception as e:
        print(f"Error crawling {url}: {str(e)}")
        return "" 