import requests
import json
import constants
import os

def download_image(url, filename):
    '''Download an image from a direct URL and store it in the same location
       as the Python file. Filename must end with the file extension
    '''

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        file_path = os.path.join(os.path.dirname(__file__), filename)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(1024): # Writing 1KB at a time
                file.write(chunk)
        print("Image downloaded successfully.")
    else:
        print("Failed to download image.")

def handle_response(json, category):
    '''Utility function to handle JSON response of images from the SteamGridDB API
       Currently works with images in the PNG and JPG formats
    '''

    image_list = json["data"]
    image_data = image_list[0]
    image_url = image_data["url"]
    if image_data["mime"] == "image/png":
        filename = game_id + f"_{category}.png"
        download_image(image_url, filename)
    elif image_data["mime"] == "image/jpeg":
        filename = game_id + f"_{category}.jpg"
        download_image(image_url, filename)
    else:
        print("Error: The image had an unsupported filetype (must be JPG or PNG)!")

def check_response(response, category):
    if response.status_code == 200:
        json_data = response.json()
        if json_data["success"] == True:
            handle_response(json_data, category)
        else:
            print("There was an error in the JSON output!")
    else:
        print("Request failed, check your API key and try again")


game_id = input("Enter the Game ID: ")

grid_poster_url = "https://www.steamgriddb.com/api/v2/grids/game/" + game_id
hero_url = "https://www.steamgriddb.com/api/v2/heroes/game/" + game_id
logo_url = "https://www.steamgriddb.com/api/v2/logos/game/" + game_id
icon_url = "https://www.steamgriddb.com/api/v2/icons/game/" + game_id

grid_response = requests.get(grid_poster_url, params={"dimensions": "920x430", "mimes": "image/png,image/jpeg"}, headers={"Authorization": f"Bearer {constants.api_key}"})
poster_response = requests.get(grid_poster_url, params={"dimensions": "600x900", "mimes": "image/png,image/jpeg"}, headers={"Authorization": f"Bearer {constants.api_key}"})
hero_response = requests.get(hero_url, params={"mimes": "image/png,image/jpeg"}, headers={"Authorization": f"Bearer {constants.api_key}"})
logo_response = requests.get(logo_url, params={"mimes": "image/png"}, headers={"Authorization": f"Bearer {constants.api_key}"})
icon_response = requests.get(icon_url, params={"mimes": "image/png"}, headers={"Authorization": f"Bearer {constants.api_key}"})

check_response(grid_response, "grid")
check_response(poster_response, "poster")
check_response(hero_response, "hero")
check_response(logo_response, "logo")
check_response(icon_response, "icon")