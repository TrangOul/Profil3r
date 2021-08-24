#!/bin/bash

# This script is used to test the program during development. 
# usage : ./scripts/install.sh && profil3r -p john doe -r ./OSINT

echo "[+] Deleting older sources..."
rm -rf "`pip3 show profil3r| grep "Location: *"|sed "s/Location: //g"`/profil3r"
echo "[+] Uninstalling previous versions of Profil3r..."
yes | pip3 uninstall profil3r
echo "[+] Deleting older wheels..."
rm dist/*
echo "[+] Building..."
poetry build
echo "[+] Installing Profil3r..."
find ./dist -name 'profil3r-1.*.*.whl' -exec pip3 install {} \;
echo "[+] Installation completed"