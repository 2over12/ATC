import os
import argparse
import json
import urllib2
import gzip
from StringIO import StringIO
import httplib
import time
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Preform a Naive Baise on a given dataset of good and bad sits');
    parser.add_argument("DIRS", help="Directories for each class paired with the name of the stackexchange subdir", nargs="+", type=str)
    parser.add_argument('-n', '--num', nargs='?', type=int, help='how many pages to pull')
    args=parser.parse_args()

    if len(args.DIRS)<1 or (len(args.DIRS)%2!=0):
        print "Check your dir pairs format: (DIR1 URL1 DIR2 URL2...)"
        exit()
    numPages=5
    if args.num:
        numPages=args.num
    urls=[]
    dirs=[]
    for i in range(0,len(args.DIRS),2):
        dirs.append(args.DIRS[i])
        urls.append(args.DIRS[i+1])

    for i in range(0, len(urls)):
        if not os.path.exists(dirs[i]):
            os.makedirs(dirs[i])
        countedItems=0
        currUrl="https://"+urls[i]+"stackexchange.com"
        conn=httplib.HTTPSConnection(urls[i]+".stackexchange.com",443)
        for page in range(1,numPages+1):
            url="http://api.stackexchange.com/2.2/questions?page="+str(page)+"&pagesize=100&order=desc&sort=activity&site="+urls[i]
            hdr = { 'User-Agent' : 'bot by 2over12 for grabbing samples for text classification' }
            req=urllib2.Request(url, headers=hdr)
            response=urllib2.urlopen(req)
            buf = StringIO(response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = json.loads(f.read())
            for item in data["items"]:
                nhdr = { 'User-Agent' : 'bot by 2over12 for grabbing samples for text classification' }
                it=item["link"].replace(currUrl,"")
                print it
                conn.request('GET', it, headers=nhdr)
                dat=conn.getresponse().read()
    #            dat=presp.read()
                pth=os.path.join(dirs[i],str(countedItems)+".html")
                countedItems+=1
                htmlFile=open(pth,"w")
                htmlFile.write(dat)
                htmlFile.close()
