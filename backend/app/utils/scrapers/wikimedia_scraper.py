from urllib.parse import quote
from typing import List
from .base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)

class WikimediaScraper(BaseScraper):
    async def search_images(self, recipe_name: str, num_images: int) -> List[str]:
        search_query = quote(recipe_name)
        url = f"https://commons.wikimedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": f"{search_query} food",
            "srnamespace": "6",  # File namespace
            "srlimit": num_images
        }
        
        try:
            async with self.session.get(url, params=params, headers=await self.get_headers()) as response:
                if response.status != 200:
                    return []
                
                data = await response.json()
                images = set()
                
                for item in data.get('query', {}).get('search', []):
                    title = item.get('title', '')
                    if title.startswith('File:'):
                        file_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(title[5:])}"
                        images.add(file_url)
                
                valid_images = []
                for img_url in images:
                    if len(valid_images) >= num_images:
                        break
                    if await self.verify_image_url(img_url):
                        valid_images.append(img_url)
                
                return valid_images
        except Exception as e:
            logger.error(f"Wikimedia scraping error: {str(e)}")
            return []