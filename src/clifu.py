#!/usr/bin/env python3

import http.client
import urllib
import base64
import getopt

import sys
import os
import platform

def clifu_open_in_browser(url):
    if platform.system() == "Linux":
        os.system("xdg-open http://www.commandlinefu.com/" + url);
        
    if platform.system() == "Darwin":
        os.system("open http://www.commandlinefu.com/" + url);
    
def clifu_get_print_to_console(url,entries):
    httpconn = http.client.HTTPConnection("www.commandlinefu.com")
   
    url = url;
    httpconn.request("GET", url)
    response = httpconn.getresponse()
    
    data = bytes.decode(response.read())
    commands = data.split("\n\n")
  
    for c in range(1,entries):
        if ( len(commands) <= c ):
            break;
        print(commands[c] + "\n")

def clifu_using_get_url(query,format):
    return "/commands/using/%s/%s" % (query,format)

def clifu_matching_get_url(query,sort,format):
    queryb64 = bytes.decode(base64.b64encode(query.encode()))
    query = urllib.parse.quote(query)
    return "/commands/matching/%s/%s/%s/%s" % (query,queryb64,sort,format)
    
def clifu_tagged_get_url(query,format):
    query = urllib.parse.quote(query)
    return "/commands/tagged/163/%s/%s" % (query,format)

def usage():
    print("clifu [-h] [-u command_name_to_search] [-n number_of_results] [string_to_match]")

def main():
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hwn:u:", ["help"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
      
    entries = 5
    matching = None
    using = None
    openwebbrowser = False
    format = "plaintext"
    
    if len(args) > 0:
        matching = args[0]
    
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-u"):
            using = a
        elif o in ("-n"):
            entries = int(a); 
        elif o in ("-w"):
            openwebbrowser = True
            format=""
        else:
            assert False, "Unhandled option"
    
    url = None

    if matching != None: 
        url = clifu_matching_get_url(matching,"sort-by-votes",format) 
        
    if using != None:
        url = clifu_using_get_url(using,format)
        
    if not(url):
        usage()
        sys.exit(2)
        
    if openwebbrowser:
        clifu_open_in_browser(url)
    else:
        clifu_get_print_to_console(url, entries)
         
if __name__ == "__main__":
    main()