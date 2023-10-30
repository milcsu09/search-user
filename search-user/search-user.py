#!/usr/bin/env python3

# modules
import json, time
import argparse
import requests
from threading \
  import Thread

# 'global' variables
parser: any = argparse.ArgumentParser()
parser.add_argument('username', type=str,
  help='TARGET USERNAME')
args: any = parser.parse_args() # kwargs

# 'const' 'global' colors
ENDC: str = '\033[0m'
GREY: str = '\033[30m'
BLUE: str = '\033[36m'

# swap GREY && BLUE, split by ':'
def format(*text: list[str]) -> str: # list[str]
  return f' {ENDC}: '.join([(BLUE + x) if k % 2 else
    (GREY + x) for k, x in enumerate(text)]) + ENDC

# 'static' variables
class instance: # search instance
  target:    str   = ''  # target username
  timeout:   float = 0.0 # legal max. time
  threshold: float = 0.0 # illegal min. time

# 'global' functions
def load(file: str) -> dict: # json
  return json.load(open(file, 'r'))

def check(site: dict) -> None: # thread
  if not isinstance(site, dict): return # null
  root: str = site['root'] # 'main' url
  target: str = site['target'].\
    replace('USERNAME', instance.target)
  errors: str = site['error'] # messages

  headers: dict = {"accept-language":
    "en-US,en;q=0.9"} # only 'en' response
  response: requests.Request = None # default
  start: float = time.time() # start threshold
  try: response = requests.get(target, # not user
    headers=headers,timeout=instance.timeout)
  finally: # 'fall' through, check for errors
    if not response: return # null, no response
    elif time.time() - start < instance.threshold:
      return # null, elapsed time < threshold
    elif isinstance(errors, list): # by message
      if [error in response.text # check errors
        for error in errors]: return # null
    elif instance.target not in response.text:
      return # null, username not in response
    elif not 300 <= response.status_code < 200:
      print(format(root, target)) # defined at top
    else: return # null, nothing happend, default

def search(sites: dict) -> None: # start
  if not isinstance(sites, dict): return # null
  threads: list = [Thread(target=check,  # call
    args=[sites[id]], daemon=1) for id in sites]
  for thread in threads: thread.start() # start
  for thread in threads: thread.join()  # join

# 'options'
if __name__ == '__main__': # 'main'
  instance.target    = args.username
  instance.timeout   = 3     # seconds
  instance.threshold = 0.25  # seconds
  sites = load('websites.json') # json
  search(sites)  # search loaded sites