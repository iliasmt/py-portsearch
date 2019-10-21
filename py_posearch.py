#!/usr/bin/env python
# -*- coding: utf-8 -*-

#port parser from wikipedia
#https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers


import argparse
import requests
from bs4 import BeautifulSoup


SYM = "#"
URL = "https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers"


def my_print(*args):
    """
    This function is a custom print implementation,
    Args:
        args :port number (int), description (string), if is official or not (string)
    Returns:
        nothing
    """
    line="{}: {} : {} ".format(args[0], args[1], args[2].strip("\n"))
    print(line.ljust(110, SYM))


def get_port_information(port):
    """
    This function takes a port number and searches for information
    Args:
        port (int) : port number
    Returns:
        nothing
    """
    try:
        my_port=ports.find("td", text=port).find_next_siblings("td")
        my_print(port, my_port[2].get_text(), my_port[3].get_text())
    except AttributeError:
        my_print(port, "N/A", "N/A")


if __name__ == "__main__":
    # define argument parser
    parser = argparse.ArgumentParser(description="""Search Wikipedia for a port and it's description
    Example Usage: python py_posearch.py 3389 3306""")
    parser.add_argument('port', metavar='p', type=int, nargs='+',
                        help='port number as integer')
    args = parser.parse_args()
    port_numbers=args.port

    # make request to url & start scrapping
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find_all("tbody")
    ports = table[5]
    ports.extend(table[6])
    print(SYM.ljust(110, SYM))

    for port in port_numbers:
        get_port_information(port)
    print(SYM.ljust(110, SYM))
