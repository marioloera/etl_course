# Exercise 1 - Extracting data using cut command
The filter command cut helps us extract selected characters or

fields from a line of text.

## 1.1 Extracting characters.

The command below shows how to extract the first four characters.

```
echo "database" | cut -c1-4
```


You should get the string 'data' as output.

The command below shows how to extract 5th to 8th characters.
```
echo "database" | cut -c5-8
```
You should get the string 'base' as output.

Non-contiguous characters can be extracted using the comma.

The command below shows how to extract the 1st and 5th characters.
```
echo "database" | cut -c1,5
```
You get the output : 'db'

## 1.2. Extracting fields/columns

We can extract a specific column/field from a delimited text file, by mentioning

the delimiter using the -d option, or
the field number using the -f option.

The /etc/passwd is a ":" delimited file.

The command below extracts user names (the first field) from /etc/passwd.
```
cut -d":" -f1 /etc/passwd
```
The command below extracts multiple fields 1st, 3rd, and 6th

(username, userid, and home directory) from /etc/passwd.
```
cut -d":" -f1,3,6 /etc/passwd
```
The command below extracts a range of fields 3rd to 6th 

(userid, groupid, user description and home directory) from /etc/passwd.
```
cut -d":" -f3-6 /etc/passwd
```