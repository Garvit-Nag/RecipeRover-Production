import logging
import asyncio
import aiohttp
import random
import re
from typing import List, Union
from app.utils.scrapers.google_scraper import GoogleScraper
from app.utils.scrapers.food_network_scraper import FoodNetworkScraper
from app.utils.scrapers.allrecipes_scraper import AllRecipesScraper
from app.utils.scrapers.wikimedia_scraper import WikimediaScraper
from app.utils.scrapers.fooddotcom_scraper import FoodDotComScraper

logger = logging.getLogger(__name__)

class ImageSearchService:
    def __init__(self):
        self.scrapers = [
            GoogleScraper(),
            FoodNetworkScraper(),
            AllRecipesScraper(),
            WikimediaScraper(),
            FoodDotComScraper()
        ]
        self.session = None
        self.placeholder_images = [
            "https://drive.google.com/file/d/1gYOjs06yiq7EUXaO19BE-L7MkrTR6wlc/view?usp=sharing",
            "https://drive.google.com/file/d/1ob4KbzVLtwsE_ckYKBu_70FLEXNCJRSr/view?usp=sharing",
            "https://drive.google.com/file/d/1UUv3zF1ouXteZVt8Oc_UXORcJrlWfRXR/view?usp=sharing"
        ]

    async def __aenter__(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
            for scraper in self.scrapers:
                scraper.session = self.session
        logger.info("ImageSearchService session initialized")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            self.session = None
        logger.info("ImageSearchService session closed")

    async def search_recipe_images(self, recipe_name: str, image_data: Union[str, float, int], num_images: int = 3) -> List[str]:
        logger.info(f"Searching images for recipe: {recipe_name}")
        
        # First try to get existing URLs from the database
        existing_urls = self.extract_urls_from_image_column(image_data)
        if existing_urls:
            logger.info(f"Found {len(existing_urls)} existing URLs")
            return existing_urls[:num_images]
        
        try:
            # Try to get images from scrapers
            all_results = []
            tasks = []
            
            for scraper in self.scrapers:
                task = asyncio.create_task(scraper.search_images(recipe_name, num_images))
                tasks.append(task)
            
            logger.info(f"Created {len(tasks)} scraper tasks")
            done, pending = await asyncio.wait(tasks, timeout=60)
            
            for task in pending:
                logger.warning(f"Cancelling pending task for {task.get_coro().__name__}")
                task.cancel()
            
            for task in done:
                try:
                    results = await task
                    logger.info(f"Scraper {task.get_coro().__name__} found {len(results)} images")
                    all_results.extend(results)
                except Exception as e:
                    logger.error(f"Error in scraper task {task.get_coro().__name__}: {str(e)}")
            
            # Get unique results
            seen = set()
            unique_results = []
            for url in all_results:
                if url not in seen:
                    seen.add(url)
                    unique_results.append(url)
            
            if unique_results:
                logger.info(f"Found {len(unique_results)} unique image URLs")
                return unique_results[:num_images]
            
            # If no images found, return random placeholder images
            logger.info("No images found, using placeholder images")
            selected_placeholders = []
            for _ in range(num_images):
                placeholder = random.choice(self.placeholder_images)
                while placeholder in selected_placeholders and len(selected_placeholders) < len(self.placeholder_images):
                    placeholder = random.choice(self.placeholder_images)
                selected_placeholders.append(placeholder)
            
            return selected_placeholders
            
        except Exception as e:
            logger.error(f"Error in image search: {str(e)}")
            # Return placeholder images even in case of error
            return random.sample(self.placeholder_images, min(num_images, len(self.placeholder_images)))

    def extract_urls_from_image_column(self, image_data: Union[str, float, int]) -> List[str]:
        logger.debug(f"Extracting URLs from image data: {image_data}")
        if image_data is None or image_data == 'NA' or isinstance(image_data, (float, int)):
            logger.debug("No valid image data found in database")
            return []
        
        try:
            image_data_str = str(image_data)
            urls = []
            if image_data_str.startswith('c(') and image_data_str.endswith(')'):
                content = image_data_str[2:-1].strip()
                parts = re.findall(r'"([^"]*)"', content)
                urls = [url for url in parts if url.startswith('http')]
            else:
                urls = re.findall(r'https?://[^\s,"\')]+', image_data_str)
            
            logger.info(f"Extracted {len(urls)} URLs from image column")
            return urls
        except Exception as e:
            logger.error(f"Error extracting URLs from image data: {str(e)}")
            return []