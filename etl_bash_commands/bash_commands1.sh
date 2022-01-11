# some bash commands

: '
The command below shows how to extract the first four characters.
You should get the string 'data' as output.
'
echo "database" | cut -c1-4

: '
The command below shows how to extract 5th to 8th characters.
You should get the string 'base' as output.
'
echo "database" | cut -c5-8

: '
 Non-contiguous characters can be extracted using the comma.
 The command below shows how to extract the 1st and 5th characters.
 You get the output : 'db'
'
echo "database" | cut -c1,5

: '
 We can extract a specific column/field from a delimited text file, by mentioning
 the delimiter using the -d option, or
 the field number using the -f option.
'

: '
 The /etc/passwd is a ":" delimited file.
 The command below extracts user names (the first field) from /etc/passwd.
'
cut -d":" -f1 /etc/passwd


: '
The command below extracts multiple fields 1st, 3rd, and 6th
(username, userid, and home directory) from /etc/passwd.
'
cut -d":" -f1,3,6 /etc/passwd

: '
The command below extracts a range of fields 3rd to 6th 
(userid, groupid, user description and home directory) from /etc/passwd.
'
cut -d":" -f3-6 /etc/passwd
