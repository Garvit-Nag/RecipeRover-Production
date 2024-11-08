import random
import aiohttp
from abc import ABC, abstractmethod
from typing import List
import logging

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        ]
        self.session = None

    async def get_headers(self):
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
        }

    @abstractmethod
    async def search_images(self, recipe_name: str, num_images: int) -> List[str]:
        pass

    async def verify_image_url(self, url: str) -> bool:
        try:
            async with self.session.head(url, allow_redirects=True, timeout=60) as response:
                content_type = response.headers.get('content-type', '')
                return (response.status == 200 and 
                       'image' in content_type and 
                       not any(x in url.lower() for x in ['placeholder', 'default', 'missing']))
        except:
            return False