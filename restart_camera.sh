#!/bin/bash

# Ganti dengan alamat IP atau URL kamera Anda
CAMERA_IP="192.168.18.26"

# Lakukan ping ke kamera dan simpan outputnya ke dalam variabel
PING_RESULT=$(ping -c 1 $CAMERA_IP)

# Tunggu 10 detik
sleep 10

# Ambil tanggal dan waktu saat ini
current_datetime=$(date +"%Y-%m-%d %H:%M:%S")

# Periksa hasil ping setelah 10 detik
if echo "$PING_RESULT" | grep -q "1 packets transmitted, 0 received, +1 errors, 100% packet loss, time 0ms\|Destination Host Unreachable"
then
    echo "[$current_datetime] Koneksi ke kamera terputus. Memicu API."
    curl -X POST http://192.168.18.111/trigger
else
    echo "[$current_datetime] Koneksi ke kamera stabil."
fi
