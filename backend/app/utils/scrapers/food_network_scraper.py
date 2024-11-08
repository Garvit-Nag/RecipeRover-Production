from bs4 import BeautifulSoup
from urllib.parse import quote
from .base_scraper import BaseScraper
from typing import List

import logging

logger = logging.getLogger(__name__)

class FoodNetworkScraper(BaseScraper):
    async def search_images(self, recipe_name: str, num_images: int) -> List[str]:
        search_query = quote(recipe_name)
        url = f"https://www.foodnetwork.com/search/{search_query}-"
        
        try:
            async with self.session.get(url, headers=await self.get_headers()) as response:
                if response.status != 200:
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                images = set()
                
                for img in soup.find_all('img', {'data-src': True}):
                    src = img.get('data-src')
                    if src and 'thumbnail' not in src.lower():
                        images.add(src)
                
                valid_images = []
                for img_url in images:
                    if len(valid_images) >= num_images:
                        break
                    if await self.verify_image_url(img_url):
                        valid_images.append(img_url)
                
                return valid_images
        except Exception as e:
            logger.error(f"Food Network scraping error: {str(e)}")
            return []