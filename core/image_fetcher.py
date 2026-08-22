import requests
from django.core.files.base import ContentFile
import urllib.parse

def get_wikipedia_image_url(query):
    """
    Searches Wikipedia for the query and returns the main image URL of the top result.
    Returns None if no image is found.
    """
    try:
        headers = {
            "User-Agent": "GlobeTrotterApp/1.0 (Contact: admin@globetrotter.com)"
        }
        # Step 1: Search for the title
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "utf8": "1",
            "format": "json",
            "srlimit": 1
        }
        
        search_resp = requests.get(search_url, params=search_params, headers=headers, timeout=5)
        search_data = search_resp.json()
        
        results = search_data.get('query', {}).get('search', [])
        if not results:
            return None
            
        title = results[0]['title']
        
        # Step 2: Get the summary page for this title to extract the image
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
        summary_resp = requests.get(summary_url, headers=headers, timeout=5)
        summary_data = summary_resp.json()
        
        # Wikipedia provides a 'thumbnail' or 'originalimage' object
        # We prefer 'originalimage' for higher quality, fallback to 'thumbnail'
        image_obj = summary_data.get('originalimage') or summary_data.get('thumbnail')
        
        if image_obj and 'source' in image_obj:
            return image_obj['source']
            
        return None
        
    except Exception as e:
        print(f"Error fetching Wikipedia image for '{query}': {e}")
        return None

def download_and_save_image(image_url, model_instance, field_name, filename):
    """
    Downloads an image from a URL and saves it to a Django ImageField.
    """
    if not image_url:
        return False
        
    try:
        headers = {
            "User-Agent": "GlobeTrotterApp/1.0 (Contact: admin@globetrotter.com)"
        }
        resp = requests.get(image_url, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            # Get the field (e.g. instance.cover_image)
            image_field = getattr(model_instance, field_name)
            # Save the content
            image_field.save(filename, ContentFile(resp.content), save=True)
            return True
            
        return False
        
    except Exception as e:
        print(f"Error downloading image from '{image_url}': {e}")
        return False
