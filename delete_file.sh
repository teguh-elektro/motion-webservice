#!/bin/sh

# Daftar direktori yang akan dicek
DIRECTORIES=(
    "/home/tangor/media/storage/cam1"
    "/home/tangor/media/storage/cam2"
    "/home/tangor/media/storage/cam3"
)

# Ambil tanggal tujuh hari yang lalu
THRESHOLD=$(date -d "7 days ago" "+%Y%m%d%H%M%S")

# Fungsi untuk menghapus file-file tua dalam sebuah direktori
delete_old_files() {
    DIRECTORY="$1"
    cd "$DIRECTORY" || exit

    # Loop melalui file-file dalam direktori
    for FILE in *.mp4; do
        FILE_DATE=$(echo "$FILE" | cut -c1-14)
        if [ "$FILE_DATE" -lt "$THRESHOLD" ]; then
            rm "$FILE"
            echo "File $FILE deleted."
        fi
    done
}

# Loop melalui daftar direktori dan panggil fungsi delete_old_files untuk masing-masing
for DIR in "${DIRECTORIES[@]}"; do
    delete_old_files "$DIR"
done