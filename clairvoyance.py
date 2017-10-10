#!/usr/bin/env python
import sys, socket, threading, time, json

from parser import parse
from solver import solve
import puzzles

#TODO: laten werken als een gebied offline is

KML_FILE = "jotihunt-2016.kml"
polygons = parse(KML_FILE)

BANNER = """  _______     _                                     
 / ___/ /__ _(_)____  _____  __ _____ ____  _______ 
/ /__/ / _ `/ / __/ |/ / _ \/ // / _ `/ _ \/ __/ -_)
\___/_/\_,_/_/_/  |___/\___/\_, /\_,_/_//_/\__/\__/ 
		           /___/
"""

def handle_connection(client_socket, address):
	print("[+] Handing connection from " + address[0])
	client_socket.send(BANNER)
	client_socket.send("[!] Ready to receive puzzle.\n")
	json_puzzle = client_socket.recv(1024)

	if json_puzzle:
		parsed_puzzle = json.loads(json_puzzle)
		print("Received puzzle with name " + parsed_puzzle[0])
		solve(client_socket, parsed_puzzle, polygons)

	client_socket.close()

def main():

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(("127.0.0.1", 1337))
	s.listen(5);

	while True:
		(client_socket, address) = s.accept()
		client_socket.settimeout(60)
		threading.Thread(target = handle_connection, args=(client_socket, address)).start()

if __name__ == "__main__":
	main()