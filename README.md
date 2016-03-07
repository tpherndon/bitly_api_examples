# bitly_api_examples
Various scripts that do useful things with Bitly's API endpoints

## link_details.py
The script was written to work with Python 2.7, and requires the requests
library. A requirements.txt file is included for use with pip.

The script requires you to supply two arguments, your Bitly account access
token (https://bitly.com/a/oauth_apps and generate the Generic Access Token),
and the filename of the CSV you want to hold the script's output.

To run the script:
    python link_details.py XXXXXXXXXXXXXXXXXX output.csv
