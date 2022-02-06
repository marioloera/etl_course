# This script
# Extracts data from /etc/passwd file into a CSV file.

# The csv data file contains the user name, user id and
# home directory of each user account defined in /etc/passwd

# Transforms the text delimiter from ":" to ",".
# Load

# Extract phase

echo "Extracting data"

# Extract the columns 1 (user name), 2 (user id) and
# 6 (home directory path) from /etc/passwd

# cut -d":" -f1,3,6 /etc/passwd
cut -d":" -f1,3,6 /etc/passwd > extracted-data.txt

# Transform phase
echo "Transforming data"
# read the extracted data and replace the colons with commas.

# tr ":" "," < extracted-data.txt
tr ":" "," < extracted-data.txt > transformed-data.csv


# POSTGRES PART
# Clean table added by Mairo
# truncate table users;
cmd='\c template1; \\TRUNCATE TABLE users;'
echo $cmd | psql --username=postgres --host=localhost
# echo '\c template1; \\TRUNCATE TABLE users;' | psql --username=postgres --host=localhost

# Load phase
echo "Loading data"
# Send the instructions to connect to 'template1' and
# copy the file to the table 'users' through command pipeline.
# COPY table_name FROM 'filename' DELIMITERS 'delimiter_character' FORMAT;
cmd="\c template1;\COPY users  FROM '/home/project/transformed-data.csv' DELIMITERS ',' CSV;"
echo $cmd | psql --username=postgres --host=localhost

# show results added by Mario
cmd='\c template1; \\SELECT COUNT(*) FROM users;'
echo $cmd | psql --username=postgres --host=localhost
