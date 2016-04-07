#!/usr/bin/env python

import argparse
import csv
from datetime import date
import time

import requests

def main(access_token, filename, link):
    link_history_url = "https://api-ssl.bitly.com/v3/user/link_history"
    params = {"access_token": access_token, "archived": "off", "limit": 100, "offset": 0, "link": link}
    print "Fetching link details..."
    response = requests.get(link_history_url, params=params)
    link_history_results = None
    if response.status_code != 200:
        print "Response: ", response["status_code"], response["status_txt"]
        print "Call to link history failed! Aborting"
        response.raise_for_status()

    try:
        link_history_results = response.json()
    except ValueError:
        print "JSON object failed to decode"
        raise

    if link_history_results["status_code"] != 200:
        print "Link history results error: ", link_history_results["status_code"], link_history_results["status_txt"]
        print "Call to link history failed! Aborting"
        return


    # JSON response envelope looks like {"status_code": 200, "status_txt": "...", "data": {"result_count": ###, "link_history": [...]}}
    # Each entry in "link_history" has relevant fields "keyword_link", "link", "tags", "long_url"
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow(("keyword_link", "link", "tags", "long_url"))
        for link in link_history_results["data"]["link_history"]:

            # Get click counts previous month's clicks for given link
            click_count_url = "https://api-ssl.bitly.com/v3/link/clicks"
            params = {"access_token": access_token, "unit": "day", "units": -1, "rollup": "false", "link": link["link"]}
            response = requests.get(click_count_url, params)
            click_count_results = None
            if response.status_code != 200:
                print "Response: ", response["status_code"], response["status_txt"]
                print "Call to click counts failed! Aborting"
                response.raise_for_status()

            try:
                click_count_results = response.json()
            except ValueError:
                print "JSON object failed to decode for click_counts for link ", link["link"]
                print "Skipping bad response"
                continue

            if click_count_results["status_code"] != 200:
                if click_count_results["status_txt"] == "RATE_LIMIT_EXCEEDED":
                    # Here's where you add a call to time.sleep() to space out calls to /v3/link/clicks, if you need to stay under the rate limit
                    time.sleep(3600)
                else:
                    print "Call to /v3/link/clicks failed: ", click_count_results["status_code"], click_count_results["status_txt"]
                    # Quit now, as you need to figure out why things are failing
                    return

            link["link_clicks"] = click_count_results["data"]["link_clicks"]

            fields = [link.get("keyword_link", ""), link["link"], ", ".join(link["tags"]) or "", link["long_url"]]
            encoded_fields = [s.encode("utf-8") for s in fields]
            writer.writerow(encoded_fields)
            writer.writerow(("date".encode("utf-8"), "clicks".encode("utf-8")))
            for day_data in link["link_clicks"]:
                fields = (date.fromtimestamp(day_data["dt"]).isoformat().encode("utf-8"), str(day_data["clicks"]).encode("utf-8"))
                writer.writerow(fields)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Write Bitlink details to a CSV")
    parser.add_argument("access_token", help="The access token for the account for which you wish to retrieve Bitlink details")
    parser.add_argument("filename", help="The name of the file to which you wish to write the CSV output")
    parser.add_argument("link", help="The Bitlink for which you want click details")
    args = parser.parse_args()
    main(args.access_token, args.filename, args.link)
