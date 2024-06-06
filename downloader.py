from ZtreamHub.extractor import *
import sys

params = sys.argv[1:]

if len(params) == 0:
    print("No URL provided")
    sys.exit(1)

url = params[0]

print(ZtreamHub().getData(url))