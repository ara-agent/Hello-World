# Word Count Utility

`wordcount.py` prints the most common words in a text file. Words are matched
case-insensitively and ties are sorted alphabetically.

## Usage

```sh
python3 wordcount.py PATH [--top N]
```

`--top N` is optional and defaults to `10`.

## Examples

```sh
python3 wordcount.py fixtures/sample.txt
```

```text
count 2
hello 2
words 2
world 2
clearly 1
repeat 1
the 1
utility 1
```

Limit the output:

```sh
python3 wordcount.py fixtures/sample.txt --top 3
```

```text
count 2
hello 2
words 2
```

Missing files and empty inputs return a non-zero exit code and print a clear
error message to stderr.
