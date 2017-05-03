#!/usr/bin/env python

import argparse
import csv
import time

import requests

def main(access_token, rate_limit, filename):

    shorten_url = "https://api-ssl.bitly.com/v3/shorten"

    print "rate_limit: ", rate_limit
    print "filename: ", filename

    # The time to sleep between calls is the inverse of the rate limit per hour divided down to seconds
    base = rate_limit / (60.0 * 60.0)
    interval = 1.0 / base

    # JSON response envelope looks like {"status_code": 200, "status_txt": "...", "data": {"global_hash": "...",
    # "hash": "...", "long_url": "...", "new_hash": 0|1, "ur": "..."}}
    outfile = 'bitlinks.csv'
    with open(outfile, 'wb') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow(("long URL", "user_hash", "global_hash", "bitlink", "new"))
        with open(filename, 'rU') as infile:
            for url in infile:
                params = {'access_token': access_token, 'longUrl': url.strip()}
                response = requests.get(shorten_url, params=params)
                if response.status_code != 200:
                    print "Shorten failed for URL '%s' with error: %s" % (url, response.status_code)
                    response.raise_for_status()
                    continue

                try:
                    shorten_results = response.json()
                except ValueError:
                    print "JSON object failed to decode for shorten results for URL ", url
                    print "Skipping bad response"
                    continue

                if shorten_results["status_code"] != 200:
                    print "Shorten failed for URL '%s' with error: %s %s" % (url, shorten_results["status_code"], shorten_results["status_txt"])
                    continue

                data = shorten_results["data"]
                fields = [data["long_url"], data["hash"], data["global_hash"], data["url"], data["new_hash"]]
                encoded_fields = [str(s).encode("utf-8") for s in fields]
                writer.writerow(encoded_fields)
                time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Write Bitlink details to a CSV")
    parser.add_argument("--access_token", help="The access token for the account for which you wish to retrieve Bitlink details")
    parser.add_argument("--rate_limit", type=int, default=1000, help="Hourly rate limit for /v3/shorten. Defaults to 1000 calls per hour, the free use rate limit")
    parser.add_argument("--filename", help="The name of the file containing the URLs you want to shorten, one per line")
    args = parser.parse_args()
    main(args.access_token, args.rate_limit, args.filename)
