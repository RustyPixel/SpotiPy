import dotenv
import requests
import json
import urllib.parse

def get_image_from_id(album_id, access_token):
    """
    Gets the album image from its ID.

    Args:
        album_id (str): The album ID.
        access_token (str): The user's access token.

    Returns:
        str: The image URL.
    """
    # Finds and loads .env file
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)

    # General headers for API
    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }

    # Send request to Spotify API
    album_response = requests.get(f'https://api.spotify.com/v1/albums/{album_id}', headers=headers)

    # Load the response data to JSON
    album_data = json.loads(album_response.text)

    # Alternative SVG image
    alternative_svg = '''<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"
 "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
<svg version="1.0" xmlns="http://www.w3.org/2000/svg"
 width="1462.000000pt" height="1462.000000pt" viewBox="0 0 1462.000000 1462.000000"
 preserveAspectRatio="xMidYMid meet">

<g transform="translate(0.000000,1462.000000) scale(0.100000,-0.100000)"
fill="#000000" stroke="none">
<path d="M8365 14598 c-1693 -50 -3313 -848 -4421 -2178 -847 -1017 -1338
-2302 -1383 -3623 -34 -1026 167 -1973 614 -2882 781 -1592 2237 -2767 3956
-3194 504 -125 915 -175 1454 -175 629 0 1139 74 1735 251 642 190 1298 519
1840 921 411 305 815 693 1132 1087 969 1204 1438 2751 1302 4294 -247 2818
-2439 5100 -5239 5456 -333 42 -616 55 -990 43z m390 -4128 c580 -55 1103
-366 1418 -845 725 -1102 149 -2577 -1133 -2900 -511 -129 -1067 -30 -1515
270 -566 378 -892 1048 -837 1717 40 479 231 890 568 1220 110 107 172 157
294 238 349 229 789 339 1205 300z"/>
<path d="M8455 9194 c-340 -74 -561 -412 -490 -749 50 -238 251 -441 486 -491
95 -20 240 -14 329 15 91 29 182 85 254 157 72 74 118 146 154 246 23 64 26
89 27 198 0 139 -18 214 -78 320 -70 126 -231 251 -377 294 -81 24 -221 29
-305 10z"/>
<path d="M2114 10338 c-404 -685 -670 -1456 -778 -2253 -60 -438 -64 -1006
-10 -1480 223 -1989 1479 -3777 3274 -4684 699 -353 1408 -555 2200 -627 229
-21 760 -24 975 -5 790 67 1529 273 2220 619 139 69 427 230 460 257 l20 17
-20 -7 c-167 -54 -631 -156 -885 -194 -412 -62 -987 -88 -1390 -62 -1082 71
-2087 380 -3000 924 -705 420 -1336 976 -1846 1627 -1071 1367 -1563 3095
-1373 4827 40 367 130 823 223 1126 8 26 13 47 11 47 -2 0 -38 -60 -81 -132z"/>
<path d="M849 9078 c-224 -378 -431 -845 -564 -1273 -202 -647 -285 -1278
-263 -1990 69 -2286 1479 -4365 3593 -5300 602 -266 1229 -427 1916 -491 218
-21 760 -24 974 -5 790 67 1529 273 2220 619 139 69 427 230 460 257 l20 16
-20 -5 c-11 -3 -78 -21 -149 -41 -408 -111 -863 -185 -1326 -216 -219 -14
-786 -6 -997 15 -875 87 -1664 313 -2408 692 -1725 877 -2987 2456 -3455 4324
-143 570 -210 1169 -197 1755 7 289 17 430 52 710 39 305 105 636 184 918 21
75 37 137 36 137 -2 0 -36 -55 -76 -122z"/>
</g>
</svg>'''

    # Encode the SVG image as a data URI
    encoded_svg = urllib.parse.quote(alternative_svg)
    image_url = 'data:image/svg+xml,' + encoded_svg

    # Check if 'images' key exists and is not empty
    if 'images' in album_data and album_data['images']:
        # Gets image URL from data
        # Get the first image URL from the list
        image_url = album_data['images'][0]['url']

    return image_url
