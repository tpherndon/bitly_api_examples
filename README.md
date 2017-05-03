# bitly_api_examples
Various scripts that do useful things with Bitly's API endpoints

## link_details.py
This script generates click counts per day for the Bitlink you specify.

The script was written to work with Python 2.7, and requires the requests
library. A requirements.txt file is included for use with pip.

The script requires you to supply three arguments, your Bitly account access
token (https://bitly.com/a/oauth_apps and generate the Generic Access Token),
the Bitlink for which you want click data by day, and the filename of the CSV
you want to hold the script's output.

To run the script:

    python link_details.py XXXXXXXXXXXXXXXXXX output.csv http://bit.ly/123ABC

## recent_links_detail_report.py
This script generates click counts per country for the most-recently-created
100 Bitlinks in your account, for the past month.

The script was written to work with Python 2.7, and requires the requests
library. A requirements.txt file is included for use with pip.

The script requires you to supply two arguments, your Bitly account access
token (https://bitly.com/a/oauth_apps and generate the Generic Access Token),
and the filename of the CSV you want to hold the script's output.

To run the script:

    python recent_links_detail_report.py XXXXXXXXXXXXXXXXXX output.csv

## shorten_links.py
This script shortens URLs and generates a CSV of the output.

The script was written to work with Python 2.7, and requires the requess
library. A requirements.txt file is included for use with pip.

The script requires two arguments, your Bitly account access token
(https://bitly.com/a/oauth_apps and generate the Generic Access Token),
and the name of the file containing the URLs you want to shorten. The URLs
should be one URL per line.

The script takes one optional argument, "rate_limit". If you are a free user,
or generally don't want to bother worrying about it, the script defaults to 
the free use rate limit of 1000 calls to shorten a URL per hour. If you are
a paid user and thus have a higher rate limit, enter your actual rate limit
and the script will run more rapidly. Input a rate limit that is higher than
your actual limit, and you will get back RATE_LIMIT_EXCEEDED errors.

To run the script:

    python shorten_links.py --access_token=XXXXXXXXXXXXXX --filename=input.txt --rate_limit=15000
