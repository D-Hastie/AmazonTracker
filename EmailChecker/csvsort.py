import csv
import time
import datetime
import os
import lxml
import numpy
import pandas as pd
import MailImport
import ids
from bs4 import BeautifulSoup
import bottlenose as BN
from urllib2 import HTTPError

def error_handler(err):
    ex = err['exception']
    if isinstance(ex, HTTPError) and ex.code == 503:
        time.sleep(random.expovariate(0.1))
        return True

amazon = BN.Amazon(ids.AWSKEY,ids.AWSSECRET,ids.AWSID, Region='UK', MaxQPS=0.8, ErrorHandler=error_handler)



print 'Beginning CSV Evaluation'
i = 0
j = 0

# Open an output file to save the CSV data points and the data extracted from Amazon API.
FoundProductData = open('ProductData.txt', 'w')
FoundProductData.write('{0} {1} {2} {3} {4} {5} {6} \n'.format('Number', 'ISBN', 'FoundCost', 'AmUsed','AmNew', 'AmRetail', 'AmRank'))

FileChoose = 1 
if FileChoose == 1:
	filepath = MailImport.file_path
else:
	filepath = './MailAttach/Oxfam_Berko.csv'

with open(filepath, 'r') as csvfile:
    csvdata = pd.read_csv(csvfile ,dtype={'A': object})
    csvRow = csvdata['Row#']
    csvISBN= csvdata['A']
    csvPrice = csvdata['B']
    # csvAll = csvdata[['Row#', 'A','B']]
    # csvAll.rename(columns ={'A':'ISBN', 'B':'Price'}, inplace =True)
    
#Row extract and then price check on amazon.
    while j < len(csvdata):
        print 'New iter'
        FoundCost = csvPrice[j]*100
        # print csvRow[j], ' ',csvISBN[j], ' ',csvPrice[j], ' '
        isbn=csvISBN[j].strip()
        response = amazon.ItemLookup(ItemId=isbn, ResponseGroup="Large", IdType="ISBN", SearchIndex="Books")
        soup = BeautifulSoup(response, "xml")
        # print response
        try:
            newprice=soup.LowestNewPrice.Amount.string
            # print 'New price type ', type(newprice), ' value ', newprice
        except AttributeError:
            newprice=0
        try:
            usedprice=soup.LowestUsedPrice.Amount.string
            # print 'Used Type', type(usedprice), ' value ', usedprice
        except AttributeError:
            usedprice=0
        try:
            itmisbn =soup.find('ISBN').contents[-1].strip()
            # print type(itmisbn)
        except AttributeError:
            itmisbn =0
        try:
            retailprice=soup.Price.Amount.string
            # print 'retail type ', type(retail) ,' value ', retail
        except AttributeError:
            retailprice= 0
        try:
            salesrank=soup.find('SalesRank').contents[-1].strip()
        except AttributeError:
            salesrank=0
        
        j = j+ 1
        
        FoundProductData.write('{0} {1} {2} {3} {4} {5} {6} \n'.format( j, isbn, FoundCost, usedprice, newprice, retailprice, salesrank))
        print j, 'End of iter'

FoundProductData.close()

        
        
# extracteddata = open ('extracteddata.txt', 'w')
# extracteddata.write
# extracteddata.write('{0} {1} {2} \n'.format('Row:', 'ISBN:', 'StorePrice:'))
# extracteddata.write('{0} {1} {2} \n'.format(csvRow, csvISBN.values, csvPrice))
#print csvRow
    #print csvISBN
    #print csvPrice
    
print 'Data extracted from CSV its corresponding Amazon API lookup data have been placed into a data file.'



