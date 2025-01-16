#Spotify API Python Integration
A Python-based project showcasing the integration of the Spotify Web API to retrieve artist details, search for artists, and display their top 10 tracks with preview URLs. This project leverages the power of the requests library for API calls and python-dotenv for managing sensitive environment variables.

Features
Authentication: Implements Spotify's client credentials flow to securely access the API.
Artist Search: Allows searching for any artist by name.
Top Tracks Retrieval: Fetches the top 10 songs of the searched artist, including their names and preview URLs (if available).
Environment Variables: Uses .env file for securely managing sensitive information like CLIENT_ID and CLIENT_SECRET.
Technologies Used
Python:
Core programming language.
Requests:
For making HTTP requests to the Spotify API.
dotenv:
To load environment variables from a .env file.
Spotify Web API:
For fetching artist data and top tracks.

