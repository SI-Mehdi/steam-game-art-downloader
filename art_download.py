import requests
import json
import constants
import os
import sys

# For keeping track of which file types have been downloaded
download_checklist = {"Grid": False, "Poster": False, "Hero": False, "Logo": False, "Icon": False}

# def clear():
#     os.system('cls' if os.name == 'nt' else 'clear')

def check_query(input):
    """Check a string to see if it matches with a game on the SteamGridDB database

       First checks if the string is an ID, then checks for a name

       Returns empty string if nothing found
    """

    id_url = "https://www.steamgriddb.com/api/v2/games/id/" + input
    name_search_url = "https://www.steamgriddb.com/api/v2/search/autocomplete/" + input

    id_response = requests.get(id_url, headers={"Authorization": f"Bearer {constants.api_key}"})
    id_data = id_response.json()

    if id_data['success'] == True:
        data_object = id_data['data']
        print(f'Found game: {data_object["name"]}')
        game_id = data_object['id']
        return str(game_id)
    else:
        print("No Game ID found, trying to search by name now...")
    
    name_response = requests.get(name_search_url, headers={"Authorization": f"Bearer {constants.api_key}"})
    name_data = name_response.json()

    if name_data['success'] == True:
        data_list = name_data['data']
        first_match = data_list[0]
        print(f'Closest match: {first_match["name"]}')
        game_id = first_match['id']
        return str(game_id)
    else:
        print("No game name found")
    
    # Get here if there is no match

    return ""

def download_image(url, filename, category):
    '''Download an image from a direct URL and store it in the same location
       as the Python file. Filename must end with the file extension
    '''

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        file_path = os.path.join(os.path.dirname(__file__), filename)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(1024): # Writing 1KB at a time
                file.write(chunk)
        download_checklist[category.capitalize()] = True # Mark this image type as being downloaded
        print(f"{category.capitalize()} {filename} downloaded successfully.")
    else:
        print("Failed to download image.")

def handle_response(json, category):
    '''Utility function to handle JSON response of images from the SteamGridDB API
       Works with images in the PNG and JPG formats as well as ICO files for icons
    '''

    image_list = json["data"]
    found_valid = False
    index = 0

    # Iterate until we find a valid image

    while not found_valid and index < len(image_list):
        image_data = image_list[index]
        image_url = image_data["url"]

        # Images that have been taken down or are invalid end with a '?' in the image URL
        if image_url.endswith("?"):
            index = index + 1
        else:
            found_valid = True

            if image_data["mime"] == "image/png":
                filename = game_id + f"_{category}.png"
                download_image(image_url, filename, category)
            elif image_data["mime"] == "image/jpeg":
                filename = game_id + f"_{category}.jpg"
                download_image(image_url, filename, category)
            elif image_data["mime"] == "image/vnd.microsoft.icon":
                filename = game_id + f"_{category}.ico"
                download_image(image_url, filename, category)
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

query = input("Enter the name of the game or SteamGridDB Game ID: ")
game_id = check_query(query)

if not game_id:
    print("ERROR: No game was found... Try again with a more specific name or check the ID")
    sys.exit(0)

grid_poster_url = "https://www.steamgriddb.com/api/v2/grids/game/" + game_id
hero_url = "https://www.steamgriddb.com/api/v2/heroes/game/" + game_id
logo_url = "https://www.steamgriddb.com/api/v2/logos/game/" + game_id
icon_url = "https://www.steamgriddb.com/api/v2/icons/game/" + game_id

grid_response = requests.get(grid_poster_url, params={"dimensions": "920x430,460x215", "mimes": "image/png,image/jpeg"}, headers={"Authorization": f"Bearer {constants.api_key}"})
poster_response = requests.get(grid_poster_url, params={"dimensions": "600x900", "mimes": "image/png,image/jpeg"}, headers={"Authorization": f"Bearer {constants.api_key}"})
hero_response = requests.get(hero_url, params={"mimes": "image/png,image/jpeg"}, headers={"Authorization": f"Bearer {constants.api_key}"})
logo_response = requests.get(logo_url, params={"mimes": "image/png"}, headers={"Authorization": f"Bearer {constants.api_key}"})
icon_response = requests.get(icon_url, headers={"Authorization": f"Bearer {constants.api_key}"})

check_response(grid_response, "grid")
check_response(poster_response, "poster")
check_response(hero_response, "hero")
check_response(logo_response, "logo")
check_response(icon_response, "icon")


# Print total number of files downloaded, check if one type of file was not downloaded
total = 0
for key in download_checklist:
    if not download_checklist[key]:
        print(f"ERROR: {key.capitalize()} was unable to be downloaded. Images may be unavailable on SteamGridDB or another error occured")
    else:
        total = total + 1
        

print(f"{total} of 5 files downloaded")