usage: generate.py [-h] [--abuse-ratio ABUSE_RATIO] lines

Generate some random application logs, useful to teach e.g. AWK.

positional arguments:
  lines                 How many lines to generate

optional arguments:
  -h, --help            show this help message and exit
  --abuse-ratio ABUSE_RATIO
                        How many times on average an abuser will do a request
                        per [abuse ratio] requests
