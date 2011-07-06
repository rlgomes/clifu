#!/usr/bin/env python3

import http.client
import urllib
import base64
import getopt
import sys

def clifu_query_matching(query,sort,format,entries):
    httpconn = http.client.HTTPConnection("www.commandlinefu.com")
   
    queryb64 = bytes.decode(base64.b64encode(query.encode()))
    query = urllib.parse.quote(query)
    url = "/commands/matching/%s/%s/%s/%s" % (query,queryb64,sort,format)
    httpconn.request("GET", url)
    response = httpconn.getresponse()
    
    data = bytes.decode(response.read())
    commands = data.split("\n\n")
  
    for c in range(1,entries):
        if ( len(commands) <= c ):
            break;
        print(commands[c] + "\n")

def clifu_query_tagged(query,format,entries):
    httpconn = http.client.HTTPConnection("www.commandlinefu.com")
   
    query = urllib.parse.quote(query)
    url = "/commands/tagged/163/%s/%s" % (query,format)
    httpconn.request("GET", url)
    response = httpconn.getresponse()
    
    data = bytes.decode(response.read())
    commands = data.split("\n\n")
  
    for c in range(1,entries):
        if ( len(commands) <= c ):
            break;
        print(commands[c] + "\n")

def usage():
    print("clifu [-h] [-t tag] [-n number_of_commands] [string_to_match]")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:n:", ["help"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
      
    entries = 5
    matching = args[0]
    tagged = None
    
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-t"):
            tagged = a
        elif o in ("-n"):
            entries = int(a); 
        else:
            assert False, "Unhandled option"
           
    if matching != None: 
        clifu_query_matching(matching,"sort-by-votes","plaintext",entries) 
    
    if tagged != None:
        clifu_query_tagged(tagged, "plaintext", entries)
         
if __name__ == "__main__":
    main()