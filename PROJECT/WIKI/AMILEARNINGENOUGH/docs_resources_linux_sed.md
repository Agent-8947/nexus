# SED

This document provides a collection of useful one-line scripts for `sed`, the Unix stream editor.  These commands are designed for quick manipulation and modification of text files directly from the command line.

## Text Transformations

* **Inserting Blank Lines:**

    * `sed G`: Double-space a file by inserting a blank line after each line.
    * `sed '/^$/d;G'`: Double-space a file, preserving existing single blank lines.
    * `sed 'G;G'`: Triple-space a file.
    * `sed '/regex/{x;p;x;}'`: Insert a blank line *before* each line matching `regex`.
    * `sed '/regex/G'`: Insert a blank line *after* each line matching `regex`.

* **Removing Whitespace:**

    * `sed 's/^[ \t]*//'`: Remove leading whitespace (spaces and tabs).
    * `sed 's/[ \t]*$//'`: Remove trailing whitespace.
    * `sed 's/^[ \t]*//;s/[ \t]*$//'`: Remove both leading and trailing whitespace.

* **Centering/Aligning Text:**

    * `sed -e :a -e 's/^.\{1,78\}$/ &/;ta'`: Right-align text within a 79-character width.
    * `sed  -e :a -e 's/^.\{1,77\}$/ & /;ta'`: Center text within a 79-character width (method 1, leading spaces significant).
    * `sed  -e :a -e 's/^.\{1,77\}$/ &/;ta' -e 's/\( *\)\1/\1/'`: Center text (method 2, leading spaces discarded).


## Line Numbering and Counting

* `sed = filename | sed 'N;s/\n/\t/'`: Number each line, left-aligned, using tabs for spacing.
* `sed = filename | sed 'N; s/^/     /; s/ *\(.\{6,\}\)\n/\1  /'`: Number each line, left-aligned, right-justified numbers.
* `sed '/./=' filename | sed '/./N; s/\n/ /'`: Number only non-blank lines.
* `sed -n '$='`: Count the number of lines in a file (similar to `wc -l`).

## String Manipulation and Substitution

* `sed 's/foo/bar/'`: Replace the first instance of "foo" with "bar" on each line.
* `sed 's/foo/bar/g'`: Replace all instances of "foo" with "bar" on each line.
* `sed 's/\(.*\)foo/\1bar/'`: Replace only the last occurrence of "foo" with "bar" on each line.
* `sed 's/scarlet/red/g;s/ruby/red/g;s/puce/red/g'`: Replace multiple words ("scarlet", "ruby", "puce") with "red".
* `gsed 's/scarlet\|ruby\|puce/red/g'`:  Same as above, using GNU sed's alternation feature.
* `sed '$!N;s/\n/ /'`: Join consecutive lines with a space. Useful for formatting or combining data.
* `gsed ':a;s/\B[0-9]\{3\}\>/,&/;ta'`: Insert commas into numbers (e.g., 1234567 becomes 1,234,567) using GNU sed.


## Line and Paragraph Manipulation

* `sed '1!G;h;$!d'`: Reverse the order of lines in a file (similar to `tac`).
* `sed -e :a -e '/\\$/N; s/\\\n//; ta'`: Join lines ending with a backslash with the next line. Useful for handling multi-line entries.
* `sed -n '/^$/{p;h;};/./{x;/./p;}'`: Delete the last line of each paragraph (paragraphs separated by blank lines).

## Content Filtering and Extraction

* `sed 10q`: Print only the first 10 lines (similar to `head`).
* `sed -n '8,12p'`: Print lines 8 through 12.
* `sed '52!d'`: Print only line 52.
* `sed -n '/regexp/p'`: Print only lines matching the regular expression `regexp` (similar to `grep`).
* `sed '/regexp/d'`: Delete lines matching the regular expression `regexp`.
* `sed -n '/Iowa/,/Montana/p'`: Print the block of lines starting with a line containing "Iowa" and ending with a line containing "Montana".
* `sed '/Iowa/,/Montana/d'`: Delete the block of lines between "Iowa" and "Montana".
* `sed '$!N; /^\(.*\)\n\1$/!P; D'`: Remove duplicate, consecutive lines (similar to `uniq`).

## Newline Conversion

* `sed 's/.$//'`: Convert DOS/Windows newlines (CRLF) to Unix newlines (LF).  Assumes all lines end in CRLF.
* `sed 's/$/\r/'`: Convert Unix newlines (LF) to DOS/Windows newlines (CRLF).

## Special Applications

* `sed "s/.`echo \\\b`//g"`: Remove nroff overstrikes (often seen in older man pages).
* `sed '/^$/q'`: Extract the header of an email message (up to the first blank line).


##  Sed Execution and Quoting

Sed commands can be piped or applied directly to files:

```bash
sed 'command' filename          # Applies the command to the file
cat filename | sed 'command'   # Equivalent command using pipes
sed 'command' filename > output # Redirects output to a new file
```

Use single quotes (`'...'`) around `sed` commands to prevent shell interpretation of special characters like `$` and backticks. Double quotes are usually required in DOS versions of `sed`.


## Performance Optimization

For large files, using an address range or the `q` command can dramatically improve speed.  For example:

```bash
sed -n '51q;45,50p' filename  #  Prints lines 45-50 and quits, much faster for large files.
```

Placing the pattern before the `s` command in substitutions can also improve performance:

```bash
sed '/foo/s/foo/bar/g' filename # Faster than sed 's/foo/bar/g' filename
```

This cheat sheet provides a starting point for using `sed`.  For more advanced usage and a deeper understanding of regular expressions, consult the `sed` man page (`man sed`) and dedicated resources on regular expressions.