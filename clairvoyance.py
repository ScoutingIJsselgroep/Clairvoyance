#!/usr/bin/env python
import sys, socket, threading, time, json, os

from parser import parse
from solver import solve
import puzzles
import math
import requests
from rd_convert import *

# polygons = parse(os.environ.get("KML_FILENAME"))

AREAS = "Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot"

PADDING_KM = 2.0

BANNER = """  _______     _
 / ___/ /__ _(_)____  _____  __ _____ ____  _______
/ /__/ / _ `/ / __/ |/ / _ \/ // / _ `/ _ \/ __/ -_)
\___/_/\_,_/_/_/  |___/\___/\_, /\_,_/_//_/\__/\__/
                           /___/
"""


def convert_to_rdc(latitude, longitude):
    rdc = wgs_to_rd(latitude, longitude)
    rdc = (int(round(rdc[0])), int(round(rdc[1])))
    return rdc


def get_polygons(groups):
    """Get minimum and maximum for latitude and longitude for each subarea.

    Args:
            response (_type_): _description_

    Returns:
            _type_: _description_
    """
    polygons = {
        subarea: {
            "latitude": {"min": +100, "max": -100},
            "longitude": {"min": +100, "max": -100},
            "known": False,
        }
        for subarea in AREAS
    }
    for group in groups:
        group_subarea_name = group["Subarea"]["name"]

        # Ignore groups with unknown subarea
        if group_subarea_name != "Onbekend":
            polygons[group_subarea_name]["known"] = True

            for axis in ["latitude", "longitude"]:
                polygons[group_subarea_name][axis]["min"] = min(
                    polygons[group_subarea_name][axis]["min"], group[axis]
                )
                polygons[group_subarea_name][axis]["max"] = max(
                    polygons[group_subarea_name][axis]["max"], group[axis]
                )

    # Add padding to polygons
    for subarea in AREAS:
        # Latitude: (1 degree = 111.1 km), 2 km = 0,018 degree.
        polygons[subarea]["latitude"]["min"] -= PADDING_KM / 111.1
        polygons[subarea]["latitude"]["max"] += PADDING_KM / 111.1

        # Longitude: (1 degree = 111.1 x cos(latitude))
        polygons[subarea]["longitude"]["min"] -= (
            PADDING_KM
            / 111.1
            * math.cos(math.radians(polygons[subarea]["latitude"]["min"]))
        )
        polygons[subarea]["longitude"]["max"] += (
            PADDING_KM
            / 111.1
            * math.cos(math.radians(polygons[subarea]["latitude"]["max"]))
        )

    # Set unknowns
    for subarea in AREAS:
        if not polygons[subarea]["known"]:
            polygons[subarea]["latitude"]["min"] = 51.7
            polygons[subarea]["latitude"]["max"] = 52.7
            polygons[subarea]["longitude"]["min"] = 4.9
            polygons[subarea]["longitude"]["max"] = 6.5

    # Parse min max boundaries to polygons
    for subarea in AREAS:
        polygons[subarea] = [
            convert_to_rdc(
                polygons[subarea]["latitude"]["min"],
                polygons[subarea]["longitude"]["min"],
            ),
            convert_to_rdc(
                polygons[subarea]["latitude"]["min"],
                polygons[subarea]["longitude"]["max"],
            ),
            convert_to_rdc(
                polygons[subarea]["latitude"]["max"],
                polygons[subarea]["longitude"]["max"],
            ),
            convert_to_rdc(
                polygons[subarea]["latitude"]["min"],
                polygons[subarea]["longitude"]["max"],
            ),
            convert_to_rdc(
                polygons[subarea]["latitude"]["min"],
                polygons[subarea]["longitude"]["min"],
            ),
        ]

    return polygons


def get_groups():
    print("[+] Loading Groups from API")
    api_url = "{0}/api/group".format(os.environ.get("JOTIHUNT_HOST"))
    response = requests.get(api_url, timeout=(1, 1))

    if response.status_code == 200:
        print("[+] Finished updating group info")
        return response.json()
    else:
        print("[-] Failed updating group info")
        return None


def handle_connection(client_socket, address):
    print("[+] Handing connection from " + address[0])
    client_socket.send(BANNER + "[!] Ready to receive puzzle (and previous solution).")
    data = client_socket.recv(1024)

    if data:
        request = json.loads(data)
        groups = get_groups()
        polygons = get_polygons(groups)

        print("[+] Received puzzle with name " + request[0][0])
        solve(client_socket, request, polygons)

    client_socket.close()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 1337))
    s.listen(5)

    while True:
        (client_socket, address) = s.accept()
        client_socket.settimeout(60)
        threading.Thread(
            target=handle_connection, args=(client_socket, address)
        ).start()


if __name__ == "__main__":
    main()
