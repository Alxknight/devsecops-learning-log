# ! /bin/bash
set -e

echo "Encryption demo started"

echo "Enter filename:"
read file

output=${file}.enc

if [ ! -f "$file.txt" ]; then
	echo "Error: File does not exist"
#	exit 1
fi

set -x

openssl enc -aes-256-cbc -salt -in "$file" -out "$output"
set +x

echo "$(date) : Encrypted $file" >> encrypt.log

echo "Encryption successful : $output"
