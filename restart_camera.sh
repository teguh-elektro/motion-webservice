#!/bin/bash

# Ganti dengan alamat IP atau URL kamera Anda
CAMERA_IP="192.168.18.26"

# Uji koneksi ke kamera
if ping -c 1 $CAMERA_IP &> /dev/null
then
    echo "Koneksi ke kamera stabil."
else
    echo "Koneksi ke kamera terputus. Memicu API."
    curl -X POST http://192.168.18.111/trigger
fi