#!/usr/bin/env python3

import http.cookiejar
import urllib
import base64
import getopt

import getpass

import sys
import os
import platform

from urllib.request import urlopen

#import http.client
#http.client.HTTPConnection.debuglevel=True

CJ = http.cookiejar.CookieJar()

opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CJ))
urllib.request.install_opener(opener)

def clifu_open_in_browser(url):
    if platform.system() == "Linux":
        os.system("xdg-open http://www.commandlinefu.com/" + url);
        
    if platform.system() == "Darwin":
        os.system("open http://www.commandlinefu.com/" + url);

def clifu_update_auth_cookies(username,password): 
    url = "http://www.commandlinefu.com/users/signin"
    data = bytes("username=%s&password=%s&remember=on&submit=Let+me+in!" % (username,password),"utf8");
    
    response = urlopen(url, data)
    
    if response.status != 200:
        print("Failed to login: %d - %s " % (response.status,response.read()))
    
def clifu_get_print_to_console(url,entries):
    url = "http://www.commandlinefu.com/%s" % url
    response = urlopen(url)

    if ( response.status == 200 ):
        data = bytes.decode(response.read())
        commands = data.split("\n\n")
      
        for c in range(1,entries):
            if ( len(commands) <= c ):
                break;
            print(commands[c] + "\n")
    else:
        print("Communication Failure: %d - %s" % (response.status,response.read()))

def clifu_using_get_url(query,format):
    return "/commands/using/%s/%s" % (query,format)

def clifu_matching_get_url(query,sort,format):
    queryb64 = bytes.decode(base64.b64encode(query.encode()))
    query = urllib.parse.quote(query)
    return "/commands/matching/%s/%s/%s/%s" % (query,queryb64,sort,format)
    
def clifu_tagged_get_url(query,format):
    query = urllib.parse.quote(query)
    return "/commands/tagged/163/%s/%s" % (query,format)

def clifu_favourites_get_url():
    return "/commands/favourites/plaintext/0"

def usage():
    print("clifu [-h] [-u command] [-n result_count] [-w] [string_to_match]")
    print("  -h:         this help menu")
    print("  -u command: search for commands using the specified comamnd")
    print("  -n count:   number of results to display")
    print("  -w:         open the query in the systems browser")

def main():
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hwfn:u:", ["help"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
      
    entries = 5
    matching = None
    using = None
    openwebbrowser = False
    favourites = False
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
        elif o in ("-f"):
            favourites = True 
        elif o in ("-w"):
            openwebbrowser = True
            format=""
        else:
            assert False, "Unhandled option"
    
    url = None

    if favourites:
        username = input("Username: ")
        password = getpass.getpass()
        
        url = clifu_favourites_get_url()
        clifu_update_auth_cookies(username, password)
        clifu_get_print_to_console(url, entries)
    else:
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
    