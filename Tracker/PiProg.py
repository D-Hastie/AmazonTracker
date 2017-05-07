#!/usr/bin/env python
import sys
import directories
trackerdirectory = directories.trackerdir
sys.path.insert(0, '%s' % trackerdirectory)

from urllib2 import HTTPError
import ids
import csv
import bottlenose as BN
import lxml
import datetime
import os
from bs4 import BeautifulSoup
import numpy
import time
import random

def error_handler(err):
    ex = err['exception']
    if isinstance(ex, HTTPError) and ex.code == 503:
        time.sleep(random.expovariate(0.1))
        return True

amazon = BN.Amazon(ids.AWSKEY,ids.AWSSECRET,ids.AWSID,Region='UK', MaxQPS=0.8, ErrorHandler=error_handler)

i = 0
##starttime = time.time()
isbns = open(directories.isbnlistdir, 'r')
print "Number", "ISBN:","Retail:","New Price:","Used Price:", "Sales Rank:"
for line in isbns:
    isbnclean = line.strip()
#    print isbnclean
#    print type(isbnclean)
    response = amazon.ItemLookup(ItemId=isbnclean, ResponseGroup="Large")
    soup = BeautifulSoup(response, "xml")
    
    try:
        newprice=soup.LowestNewPrice.Amount.string
        print 'new price type ', type(newprice), ' Value ', newprice
    except AttributeError:
        newprice=0
    try:
        usedprice=soup.LowestUsedPrice.Amount.string
    except AttributeError:
        usedprice=0
    try:
        itmisbn =soup.find('ISBN').contents[-1].strip()
    except AttributeError:
        itmisbn = soup.find('ASIN').contents[-1].strip()
    try:
        retailprice=soup.Price.Amount.string
    except AttributeError:
        retailprice= 0
    try:
        salesrank=soup.find('SalesRank').contents[-1].strip()
    except AttributeError:
        salesrank=0

    
    CallTime = datetime.datetime.now().strftime("%Y/%m/%d:%H:%M:%S")
    outfile = open(directories.datafiledir+'%s.txt' % itmisbn, 'a')
    AmznIds = open('amznids.txt', 'a')
    if os.stat(directories.datafiledir+'%s.txt' % itmisbn).st_size==0:
        outfile.write('{0} {1} {2} {3} {4} {5}\n'.format('Time:', 'ISBN:', 'Retail-Price:', 'Lowest-New-Price:', 'Lowest-Used-Price:','Sales-Rank'))
        outfile.write('{0} {1} {2} {3} {4} {5}\n'.format(time, itmisbn, retailprice,newprice,usedprice,salesrank))
        outfile.close()
    else:
        outfile.write('{0} {1} {2} {3} {4} {5}\n'.format(time, itmisbn, retailprice,newprice,usedprice,salesrank))
        outfile.close()
    ##If new items have been added to isbns.txt, delete all entries from amznids.txt and then
    ##include the following two lines.   
    AmznIds.write('{0}\n'.format(itmisbn))
    AmznIds.close()
    
    i = i + 1
    print i, CallTime, itmisbn, retailprice, newprice, usedprice, salesrank

##endtime = time.time()
##progtime =endtime-starttime
##
##print 'RUN TIME:', progtime









