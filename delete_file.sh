#!/bin/sh

# Daftar direktori yang akan dicek
DIRECTORY1="/home/tangor/media/storage/motion/cam1"
DIRECTORY2="/home/tangor/media/storage/motion/cam2"
DIRECTORY3="/home/tangor/media/storage/motion/cam3"

# Ambil tanggal tujuh hari yang lalu
SEVEN_DAYS_AGO=$(date -d "now - 7 days" "+%Y%m%d%H%M%S")

# Fungsi untuk menghapus file-file tua dalam sebuah direktori
delete_old_files() {
    DIRECTORY="$1"
    cd "$DIRECTORY" || exit

    # Loop melalui file-file dalam direktori
    for FILE in *.mp4; do
        FILE_DATE=$(echo "$FILE" | cut -c1-14)
        if [ "$FILE_DATE" -lt "$SEVEN_DAYS_AGO" ]; then
            rm -f "$FILE"
            echo "File $FILE deleted."
        fi
    done
}

# Panggil fungsi delete_old_files untuk setiap direktori
delete_old_files "$DIRECTORY1"
delete_old_files "$DIRECTORY2"
delete_old_files "$DIRECTORY3"
