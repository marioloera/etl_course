# This script
# Extracts data from /etc/passwd file into a CSV file.

# The csv data file contains the user name, user id and
# home directory of each user account defined in /etc/passwd

# Transforms the text delimiter from ":" to ",".
# Load

# Downlow file
wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Bash%20Scripting/ETL%20using%20shell%20scripting/web-server-access-log.txt.gz"
gunzip -f web-server-access-log.txt.gz

# Extract phase

echo "Extracting data"

# Extract the columns 1 (user name), 2 (user id) and
# 6 (home directory path) from /etc/passwd

# cut -d":" -f1,3,6 /etc/passwd
cut -d"#" -f1-4 ./web-server-access-log.txt > extracted-data2.csv

# Transform phase
echo "Transforming data"
# read the extracted data and replace the colons with commas.

tr "#" "," < extracted-data2.csv > transformed-data2.csv


# Clean table added by Mairo
# truncate table access_log;
cmd='\c template1; \\TRUNCATE TABLE access_log;'
echo $cmd | psql --username=postgres --host=localhost

Load phase
# echo "Loading data"
# Send the instructions to connect to 'template1' and
# copy the file to the table 'access_log' through command pipeline.
# COPY table_name FROM 'filename' DELIMITERS 'delimiter_character' FORMAT;
cmd="\c template1;\COPY access_log  FROM '/home/project/transformed-data2.csv' DELIMITERS ',' CSV HEADER;"
echo $cmd | psql --username=postgres --host=localhost

# show results added by Mario
cmd='\c template1; \\SELECT COUNT(*) FROM access_log;'
echo $cmd | psql --username=postgres --host=localhost
