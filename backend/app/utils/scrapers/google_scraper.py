from bs4 import BeautifulSoup
import re
from urllib.parse import quote, unquote
from .base_scraper import BaseScraper
import logging
from typing import List


logger = logging.getLogger(__name__)

class GoogleScraper(BaseScraper):
    async def search_images(self, recipe_name: str, num_images: int) -> List[str]:
        search_query = f"{recipe_name} recipe food"
        url = f"https://www.google.com/search?q={quote(search_query)}&tbm=isch"
        
        try:
            async with self.session.get(url, headers=await self.get_headers()) as response:
                if response.status != 200:
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                images = set()

                # Extract from JSON-like data in scripts
                for script in soup.find_all('script'):
                    if script.string and 'AF_initDataCallback' in script.string:
                        urls = re.findall(r'(https?://\S+\.(?:jpg|jpeg|png))', script.string)
                        images.update(unquote(url) for url in urls)

                # Verify URLs and take only valid ones
                valid_images = []
                for img_url in images:
                    if len(valid_images) >= num_images:
                        break
                    if await self.verify_image_url(img_url):
                        valid_images.append(img_url)

                return valid_images
        except Exception as e:
            logger.error(f"Google scraping error: {str(e)}")
            return []