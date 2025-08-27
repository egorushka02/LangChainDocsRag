import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse
import time
from typing import List, Dict
import re

class LangChainDocsScraper:
    def __init__(self, base_url: str = "https://python.langchain.com"):
        self.base_url = base_url
        self.visited_urls = set()
        self.documents = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def is_valid_url(self, url: str) -> bool:
        """Check is url valid"""
        parsed = urlparse(url)
        if not parsed.netloc.endswith('langchain.com'):
            return False
        if parsed.fragment:  # Игнорируем якоря
            return False
        if any(exclude in url for exclude in ['/api/', '/_api/', '/_static/']):
            return False
        return True

    def clean_text(self, text: str) -> str:
        """Clean text from spaces and symbols"""
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text

    def extract_content(self, soup: BeautifulSoup) -> Dict:
        """Extract content from page"""
        # Удаляем ненужные элементы
        for element in soup.find_all(['nav', 'footer', 'aside', 'script', 'style']):
            element.decompose()

        # Извлекаем заголовок
        title = soup.find('h1')
        title_text = title.get_text().strip() if title else "No Title"

        # Извлекаем основной контент
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile('content|main'))
        
        if not main_content:
            main_content = soup.body

        text_content = self.clean_text(main_content.get_text()) if main_content else ""

        return {
            'title': title_text,
            'content': text_content,
            'text': f"{title_text}\n\n{text_content}"
        }

    def scrape_page(self, url: str) -> List[Dict]:
        """Scrape one page and return document"""
        if url in self.visited_urls:
            return []
        
        print(f"Scraping: {url}")
        self.visited_urls.add(url)

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            content = self.extract_content(soup)
            
            if content['content'] and len(content['content']) > 100:  # Минимальная длина контента
                document = {
                    'url': url,
                    'title': content['title'],
                    'content': content['content'],
                    'text': content['text'],
                    'source': 'langchain-docs'
                }
                self.documents.append(document)
            
            # Ищем ссылки на другие страницы
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(url, href)
                
                if (self.is_valid_url(full_url) and 
                    full_url not in self.visited_urls and
                    not full_url.endswith(('.pdf', '.zip', '.jpg', '.png'))):
                    links.append(full_url)
            
            return links

        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return []

    def scrape_site(self, start_url: str = None, max_pages: int = 300):
        """Recursively scrape site"""
        if start_url is None:
            start_url = self.base_url
        
        to_visit = [start_url]
        
        while to_visit and len(self.visited_urls) < max_pages:
            current_url = to_visit.pop(0)
            new_links = self.scrape_page(current_url)
            
            # Добавляем новые ссылки в очередь
            for link in new_links:
                if link not in self.visited_urls and link not in to_visit:
                    to_visit.append(link)
            
            time.sleep(0.5)  # Вежливая задержка

    def save_documents(self, filename: str = "data/langchain_docs.json"):
        """Save docs in JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.documents, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(self.documents)} documents to {filename}")

def main():
    scraper = LangChainDocsScraper()
    scraper.scrape_site(max_pages=200)  # Ограничим для начала
    scraper.save_documents("data/langchain_documents.json")

if __name__ == "__main__":
    main()