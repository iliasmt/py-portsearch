#!/usr/bin/env python
# -*- coding: utf-8 -*-

# port parser from wikipedia
# https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers

import argparse
import requests
from bs4 import BeautifulSoup as BS

URL = "https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers"


def parser(soup):
    info_tr = []
    table = soup.find_all("tbody")
    tr = table[5]
    tr.extend(table[6])
    info = tr.find_all("tr")

    for i in info:
        info_tr.append(i.get_text().lstrip().replace("\n", " "))
    return info_tr


def find_data(html, ports, url):
    soup = BS(html, "html.parser")
    info = parser(soup)

    for port in ports:
        for item in info:
            if str(port) in item:
                print(item)


def fetch_url(session, ports, url):
    header = {"User-Agent": "Mozilla/5.0"}
    with session.get(url, headers=header) as response:
        resp = response.text
    if response.status_code != 200:
        print("FAILURE to get {} error code {}".format(url, response.status_code))
    find_data(resp, ports, url)
    return resp


def main():
    parser = argparse.ArgumentParser(
        description="""Search Wikipedia for a port and it's description
    Example Usage: python aspy_posearch.py 3389 3306"""
    )
    parser.add_argument(
        "port", metavar="p", type=int, nargs="+", help="port number as integer"
    )
    args = parser.parse_args()
    ports = args.port

    with requests.Session() as session:
        fetch_url(session, ports, URL)


main()
