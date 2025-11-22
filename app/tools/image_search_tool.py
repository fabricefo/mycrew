# tools/image_search_tool.py
import os
import json
import requests
import random
import time
from typing import Optional
from crewai.tools import BaseTool
from pydantic import Field
from dotenv import load_dotenv
load_dotenv()

class PexelsCoverImageTool(BaseTool):
    name: str = "Cover Image Finder"
    description: str = "Find perfect cover images from Google DeepMind profile with smart fallback"
    
    api_key: Optional[str] = Field(default=None, exclude=True)
    base_url: Optional[str] = Field(default=None, exclude=True)
    deepmind_queries: Optional[list] = Field(default=None, exclude=True)
    fallback_queries: Optional[list] = Field(default=None, exclude=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = os.getenv('PEXELS_API_KEY')
        if not self.api_key:
            raise ValueError("PEXELS_API_KEY environment variable is required")
        self.base_url = "https://api.pexels.com/v1"
        
        # Queries most likely to return Google DeepMind photos
        self.deepmind_queries = [
            "Google DeepMind",
            "artificial intelligence research",
            "machine learning technology", 
            "neural networks",
            "AI research",
            "deep learning"
        ]
        
        # Tech fallback queries
        self.fallback_queries = [
            "technology innovation",
            "computer science",
            "robotics technology",
            "data science",
            "software development"
        ]
    
    def _run(self, topic: str, attempts: int = 2) -> str:
        """
        Search strategy:
        1. Try Google DeepMind specific searches first
        2. Filter results for Google DeepMind photographer
        3. Randomize selection from Google DeepMind results
        4. Fallback to general tech if needed
        """
        
        # PRIORITY 1: Search Google DeepMind specific queries
        deepmind_result = self._search_deepmind_photos(topic)
        if deepmind_result:
            return json.dumps({
                'success': True,
                'cover_image': deepmind_result,
                'message': f"Found Google DeepMind cover image for '{topic}'"
            }, indent=2)
        
        # PRIORITY 2: General search with DeepMind filtering
        general_result = self._search_with_deepmind_filter(topic)
        if general_result:
            return json.dumps({
                'success': True,
                'cover_image': general_result,
                'message': f"Found tech cover image for '{topic}'"
            }, indent=2)
        
        # PRIORITY 3: Fallback to broader tech search
        if attempts >= 2:
            fallback_query = random.choice(self.fallback_queries)
            fallback_result = self._search_with_deepmind_filter(fallback_query)
            if fallback_result:
                return json.dumps({
                    'success': True,
                    'cover_image': fallback_result,
                    'message': f"Found fallback tech cover image: '{fallback_query}'"
                }, indent=2)
        
        return json.dumps({
            'success': False,
            'error': f"No suitable cover image found after {attempts} attempts",
            'topic': topic
        })
    
    def _search_deepmind_photos(self, topic: str) -> Optional[dict]:
        """Specifically search for Google DeepMind photos"""
        
        # Try multiple DeepMind-focused queries
        queries_to_try = self.deepmind_queries.copy()
        random.shuffle(queries_to_try)  # Randomize order of queries
        
        for query in queries_to_try[:3]:  # Try top 3 randomized queries
            try:
                url = f"{self.base_url}/search"
                headers = {"Authorization": self.api_key}
                params = {
                    "query": query,
                    "per_page": 50,  # Get many results to filter from
                    "orientation": "landscape"
                }
                
                response = requests.get(url, headers=headers, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                photos = data.get('photos', [])
                
                # Filter for Google DeepMind photographer
                deepmind_photos = [
                    photo for photo in photos 
                    if 'google deepmind' in photo.get('photographer', '').lower() or
                       'deepmind' in photo.get('photographer', '').lower()
                ]
                
                if deepmind_photos:
                    # Randomize selection from available Google DeepMind photos
                    random.shuffle(deepmind_photos)
                    
                    # Try to find suitable dimensions from randomized list
                    for photo in deepmind_photos[:10]:  # Check up to 10 random photos
                        result = self._check_image_suitability(photo, query, is_deepmind=True)
                        if result:
                            return result
                
            except Exception as e:
                print(f"Error searching DeepMind photos: {e}")
                continue
        
        return None
    
    def _search_with_deepmind_filter(self, query: str) -> Optional[dict]:
        """Search general query but prefer Google DeepMind results"""
        try:
            url = f"{self.base_url}/search"
            headers = {"Authorization": self.api_key}
            params = {
                "query": query,
                "per_page": 40,
                "orientation": "landscape",
                "page": random.randint(1, 3)  # Light randomization - early pages only
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            photos = data.get('photos', [])
            if not photos:
                return None
            
            # First check for Google DeepMind photos
            deepmind_photos = [
                photo for photo in photos 
                if 'google deepmind' in photo.get('photographer', '').lower() or
                   'deepmind' in photo.get('photographer', '').lower()
            ]
            
            # Prefer DeepMind photos, fallback to general
            candidates = deepmind_photos if deepmind_photos else photos
            random.shuffle(candidates)  # Randomize selection
            
            # Try to find suitable image from candidates
            for photo in candidates[:8]:  # Check up to 8 candidates
                is_deepmind = photo in deepmind_photos if deepmind_photos else False
                result = self._check_image_suitability(photo, query, is_deepmind=is_deepmind)
                if result:
                    return result
            
            return None
            
        except Exception as e:
            print(f"Error in general search: {e}")
            return None
    
    def _check_image_suitability(self, photo: dict, search_query: str, is_deepmind: bool = False) -> Optional[dict]:
        """Check if image meets requirements"""
        width = photo['width']
        height = photo['height']
        
        if width >= 600 and height >= 300:
            aspect_ratio = width / height
            if 1.5 <= aspect_ratio <= 4.0:
                cover_image = {
                    'id': photo['id'],
                    'cover_url': photo['src']['large2x'],
                    'alt_text': photo.get('alt') or f"Cover image for {search_query}",
                    'dimensions': {'width': width, 'height': height},
                    'aspect_ratio': round(aspect_ratio, 2),
                    'photographer': photo['photographer'],
                    'photographer_url': photo['photographer_url'],
                    'pexels_url': photo['url'],
                    'attribution': f"Photo by {photo['photographer']} from Pexels",
                    'search_query': search_query,
                    'source': 'pexels',
                    'is_google_deepmind': is_deepmind,
                    'size_optimized': width >= 1000 and 400 <= height <= 450,
                    'selection_time': int(time.time())
                }
                return cover_image
        
        return None

# Create the tool instance
pexels_cover_tool = PexelsCoverImageTool()