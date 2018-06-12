#!/usr/bin/python

import sys
import time
import requests

test_url = "https://www.facebook.com"

if len(sys.argv) > 1:
    loop_count = int(sys.argv[1])
else:
    loop_count = 3

def getRemoteUrl():
    url = requests.head(test_url, allow_redirects=True)
    res = requests.get(url.url)
    ret_status = res.status_code
    print("Status %s : Response time %s" % (str(ret_status), str(res.elapsed.total_seconds())))
    
def main():
    for i in range(0,loop_count):
        getRemoteUrl()
        time.sleep(2);

if __name__ == "__main__":
    main()
