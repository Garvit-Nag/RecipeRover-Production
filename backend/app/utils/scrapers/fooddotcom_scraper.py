from bs4 import BeautifulSoup
import re
from typing import List
from urllib.parse import quote
from .base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)

class FoodDotComScraper(BaseScraper):
    async def search_images(self, recipe_name: str, num_images: int) -> List[str]:
        search_query = quote(recipe_name)
        url = f"https://www.food.com/search/{search_query}?pn=1"
        
        try:
            async with self.session.get(url, headers=await self.get_headers()) as response:
                if response.status != 200:
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                images = set()
                
                # Look for recipe cards which usually contain the main images
                recipe_cards = soup.find_all('div', {'class': 'recipe-card'})
                for card in recipe_cards:
                    # Check for lazy-loaded images
                    img_tags = card.find_all('img', {'data-src': True})
                    for img in img_tags:
                        src = img.get('data-src')
                        if src:
                            # Food.com often uses different image sizes, try to get the largest
                            # Replace size parameters in URL to get larger images
                            src = re.sub(r's\d+-c', 's800-c', src)
                            images.add(src)
                    
                    # Check for regular images
                    img_tags = card.find_all('img', {'src': True})
                    for img in img_tags:
                        src = img.get('src')
                        if src and not any(x in src.lower() for x in ['icon', 'logo', 'advertisement']):
                            src = re.sub(r's\d+-c', 's800-c', src)
                            images.add(src)
                
                # If no recipe cards found, try finding images in the main content
                if not images:
                    img_tags = soup.find_all('img', {'class': 'recipe-image'})
                    for img in img_tags:
                        src = img.get('src') or img.get('data-src')
                        if src:
                            src = re.sub(r's\d+-c', 's800-c', src)
                            images.add(src)
                
                valid_images = []
                for img_url in images:
                    if len(valid_images) >= num_images:
                        break
                    if await self.verify_image_url(img_url):
                        valid_images.append(img_url)
                
                return valid_images
                
        except Exception as e:
            logger.error(f"Food.com scraping error: {str(e)}")
            return []