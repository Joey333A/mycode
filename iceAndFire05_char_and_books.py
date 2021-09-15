#!/usr/bin/python3
"""Alta3 Research - Exploring OpenAPIs with requests"""
# documentation for this API is at
# https://anapioficeandfire.com/Documentation

import requests
import pprint

AOIF_CHAR = "https://www.anapioficeandfire.com/api/characters/"

def main():
    ## Ask user for input
    got_charToLookup = input("Pick a number between 1 and 1000 to return info on a GoT character! " )

    ## Send HTTPS GET to the API of ICE and Fire character resource
    lookup_url = AOIF_CHAR + got_charToLookup
    print(lookup_url)
    gotresp = requests.get(lookup_url)

    ## Decode the response
    got_dj = gotresp.json()
    pprint.pprint(got_dj)

    ## Request books
    list_of_book_URLs = got_dj['books']
    for book_URL in list_of_book_URLs:
        print(book_URL)
        book_JSON = requests.get(book_URL)
        pprint.pprint(book_JSON.json()['name'])

if __name__ == "__main__":
    main()
