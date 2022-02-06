: '
Exercise 2 - Transforming data using tr.
tr is a filter command used to translate, squeeze, and/or delete characters.

2.1. Translate from one character set to another
The command below translates all lower case alphabets to upper case.
'
echo "Shell Scripting" | tr "[a-z]" "[A-Z]"

: '
You could also use the pre-defined character sets also for this purpose:
'
echo "Shell Scripting" | tr "[:lower:]" "[:upper:]"

: '
The command below translates all upper case alphabets to lower case.
'
echo "Shell Scripting" | tr  "[A-Z]" "[a-z]"


: '
2.2. Squeeze repeating occurrences of characters
The -s option replaces a sequence of a repeated characters with a single occurrence of that character.
The command below replaces repeat occurrences of 'space' in the output of ps command with one 'space'.
the space character within quotes can be replaced with the following : "[:space:]".

'
ps | tr -s " "


: '
2.3. Delete characters
We can delete specified characters using the -d option.
The command below deletes all digits.
The output will be : 'My login pin is'
'
echo "My login pin is 5634" | tr -d "[:digit:]"
