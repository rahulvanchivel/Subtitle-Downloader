import requests
import os
import time
import sys
from tqdm import tqdm

# OpenSubtitles credentials
USERNAME = "soliton"
PASSWORD = "@hd4x59u%eWDDaj"
API_KEY = "JO6ATseWoTYLvN499loNz0SnUmrOSoWS"
LANGUAGE = "cs"  # Czech language code

# App information
APP_NAME = "CzechSubtitleDownloader v1.0.0"  # Required by OpenSubtitles API

# OpenSubtitles API URLs
LOGIN_URL = "https://api.opensubtitles.com/api/v1/login"
SEARCH_URL = "https://api.opensubtitles.com/api/v1/subtitles"
DOWNLOAD_URL = "https://api.opensubtitles.com/api/v1/download"

# Function to log in and get a token
def login():
    headers = {
        "Api-Key": API_KEY, 
        "Content-Type": "application/json",
        "User-Agent": APP_NAME  # Add required User-Agent header
    }
    data = {"username": USERNAME, "password": PASSWORD}
    
    try:
        response = requests.post(LOGIN_URL, json=data, headers=headers)
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        
        if response.content:  # Check if response has content
            result = response.json()
            if "token" in result:
                return result["token"]
            else:
                print(f"Login failed: No token in response. Response: {result}")
                return None
        else:
            print("Login failed: Empty response received")
            return None
            
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        if response.content:
            try:
                print(f"Error details: {response.json()}")
            except:
                print(f"Raw response: {response.content}")
        return None
    except requests.exceptions.ConnectionError:
        print("Connection Error: Unable to connect to OpenSubtitles API")
        return None
    except requests.exceptions.Timeout:
        print("Timeout Error: The request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except ValueError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response content: {response.content}")
        return None

# Function to search for subtitles
def search_subtitles(token, query, season, episode):
    headers = {
        "Api-Key": API_KEY, 
        "Authorization": f"Bearer {token}",
        "User-Agent": APP_NAME  # Add required User-Agent header
    }
    params = {
        "query": query,
        "season_number": season,
        "episode_number": episode,
        "languages": LANGUAGE,
        "order_by": "downloads",
    }
    
    try:
        response = requests.get(SEARCH_URL, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("data"):
            print(f"No subtitles found for {query} S{season}E{episode}")
            return None
            
        if not data["data"][0].get("attributes", {}).get("files"):
            print(f"No files found in subtitles data for {query} S{season}E{episode}")
            return None
            
        return data["data"][0]["attributes"]["files"][0]["file_id"]
        
    except (requests.exceptions.RequestException, ValueError, KeyError, IndexError) as e:
        print(f"Error searching for subtitles: {e}")
        return None

# Function to download subtitle file
def download_subtitle(token, file_id, filename):
    headers = {
        "Api-Key": API_KEY, 
        "Authorization": f"Bearer {token}",
        "User-Agent": APP_NAME  # Add required User-Agent header
    }
    
    try:
        # Request download link
        response = requests.post(DOWNLOAD_URL, json={"file_id": file_id}, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        if not result.get("link"):
            print(f"No download link received for file_id: {file_id}")
            return False
            
        download_link = result["link"]
        
        # Download the actual file
        subtitle_response = requests.get(download_link)
        subtitle_response.raise_for_status()
        
        if not subtitle_response.content:
            print(f"Empty subtitle file received for {filename}")
            return False
            
        with open(filename, "wb") as f:
            f.write(subtitle_response.content)
            
        return True
        
    except (requests.exceptions.RequestException, ValueError, KeyError) as e:
        print(f"Error downloading subtitle: {e}")
        return False

# Function to validate and sanitize input
def get_valid_input(prompt, input_type=str, min_value=None, max_value=None):
    while True:
        try:
            user_input = input(prompt)
            
            if input_type == int:
                value = int(user_input)
                if min_value is not None and value < min_value:
                    print(f"Value must be at least {min_value}")
                    continue
                if max_value is not None and value > max_value:
                    print(f"Value must be at most {max_value}")
                    continue
            else:
                value = user_input
                if not value.strip():
                    print("Input cannot be empty")
                    continue
                    
            return value
            
        except ValueError:
            print(f"Please enter a valid {input_type.__name__}")

# Main function
def main():
    print("=== Czech Subtitles Downloader ===")
    print(f"API: OpenSubtitles.com | Language: {LANGUAGE}")
    
    # Login
    print("Logging in to OpenSubtitles...")
    token = login()
    if not token:
        print("Login failed. Please check your credentials or try again later.")
        return
    
    print("Login successful!")
    
    # Get user input
    show_name = get_valid_input("Enter TV Show Name: ")
    season = get_valid_input("Enter Season Number: ", int, 1)
    episodes = get_valid_input("Enter Number of Episodes: ", int, 1)

    # Create directory for subtitles
    os.makedirs("Subtitles", exist_ok=True)
    
    # Count successful and failed downloads
    successful = 0
    failed = 0

    # Download subtitles
    for episode in tqdm(range(1, episodes + 1), desc="Downloading Subtitles"):
        try:
            print(f"\nSearching for {show_name} S{season}E{episode}...")
            file_id = search_subtitles(token, show_name, season, episode)
            
            if file_id:
                filename = f"Subtitles/{show_name}_S{season}E{episode}.srt"
                print(f"Downloading to {filename}...")
                
                if download_subtitle(token, file_id, filename):
                    print(f"✅ Downloaded: {filename}")
                    successful += 1
                else:
                    print(f"❌ Failed to download subtitles for Episode {episode}")
                    failed += 1
            else:
                print(f"❌ No subtitles found for Episode {episode}")
                failed += 1

            # Respect API rate limits
            time.sleep(2)
            
        except Exception as e:
            print(f"Unexpected error processing episode {episode}: {e}")
            failed += 1

    # Summary
    print("\n=== Download Summary ===")
    print(f"Total episodes: {episodes}")
    print(f"Successfully downloaded: {successful}")
    print(f"Failed: {failed}")
    
    if successful > 0:
        print(f"\n✅ Files saved to {os.path.abspath('Subtitles')}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)