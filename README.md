# Steam Art Downloader
Python script to download Steam art for games and programs via SteamGridDB. This is particularly useful for adding non-Steam games or programs to Steam as these will require art to be provided manually

# Instructions

Clone the repository and create a file called ```constants.py``` at the root

In this file add a variable for your SteamGridDB API key like so:
``` 
api_key = # YOUR API KEY HERE #
```
To get your API key, log in to SteamGridDB and go to the Preferences page of your profile and select the API tab

Then simply run the script in your terminal:

```
python art_download.py
```
You can then search for a title by Game ID or game/app name

All images downloaded by this program are owned by their respective creators
