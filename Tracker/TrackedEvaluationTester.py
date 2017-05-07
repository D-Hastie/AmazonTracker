#!/usr/bin/env python
import sys
import directories
trackerdirectory = directories.trackerdir
sys.path.insert(0, '%s' % trackerdirectory)
# Beginning Analysis of found products.
from urllib2 import HTTPError
import csv
import bottlenose as BN
import lxml
import os
from bs4 import BeautifulSoup
import numpy
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import pylab
from datetime import datetime
import pandas as pd
import statistics

item_list = open(directories.fileiddir, 'r')
print 'Set opening file ids to variable '
pd_item_list = pd.read_csv(item_list)
print 'Read ids to list'
file_id = pd_item_list['file-id']
print ' Place ids to list'
i = 0
j = 0
k = 0

print 'File ID now accessible by file_id[x]'
    
FlatFees = 118
FlatPay = 280
DeliveryCost = 275
# len(pd_item_list)
while j < 1:
    item_location = directories.datafiledir+('%s.txt' % file_id[j])
    j+=1
    if not os.path.isfile(item_location):
        pass
    with open(item_location) as item_file:
        item_data = pd.read_csv(item_file, delimiter = '\s+')
        # print item_data
        # print j
  #       print 'Opened and read product datafile'
        d_time = item_data['Time:']
        print d_time
        d_id = item_data['ISBN:']
        print d_id
        print 'Sorted ID: '
        data_retail = item_data['Retail-Price:']
        print data_retail[3]
        print 'Sorted retail'
        data_new = item_data['Lowest-New-Price:']
        print data_new[12]
        print 'Sorted New'
        data_used = item_data['Lowest-Used-Price:']
        print data_used[19]
        print 'Sorted Used'
        data_rank = item_data['Sales-Rank']
        print data_rank
        print 'Sorted rank'
        print 'sorted data'
        
        #Item_array length for finding last row.
        ial = len(item_data)
        # Last row will be this length minus 1 due to starting at index 0.
        print ial, '-- array length'
        
        # Find Lowest Current Price that isn't zero
        current_price_array = [data_new[ial-1],data_used[ial-1],data_retail[ial-1]]
        #lowest current price 
        lcp = min(i for i in current_price_array if i > 0)
        # print lcp
        
        # Find the lowest price in each row of array.
        lowest_price_all =[]
        while k < len(item_data):
            price_at_k = [data_new[k],data_used[k],data_retail[k]]
            lowest_price_at_k = min(i for i in price_at_k if i > 0)
            lowest_price_all.extend([lowest_price_at_k])
            # print lowest_price_all
            k +=1
        print lowest_price_all
        median_lowest_price = statistics.median(lowest_price_all)
        
        print median_lowest_price
           #
        # # We now need to find the appropriate sale price across the range of data. i.e What is the best selling price at points of high demand.
        # # Either we can try use date time function to get a rolling period of time. Or now that the tracker is automated, we should be able to use fixed number of data points.
        # # We should be getting 24 data points per day, so a 2 week average would be across 336 points.
        # median_rolling_length = 336
        # median_used_price = data_used.median()
        # item_rolling_median = pd.rolling_median(lowest_price_all,20)
        # print item_rolling_median
        # # print median_price
        
        close()
        
        VariableFee = 0.15* median_lowest_price
        TotalFee = FlatFees+VariableFee
        PotentialEarning = minPrice - TotalFee - DeliveryCost + FlatPay - FoundCost[j]
        
        
# while j < len(pddata):
#     print ' '
#     # print j, ' ', isbn[j], ' ', FoundPrice[j], ' ', AmUsed[j], ' ', AmNew[j], ' ', AmRetail[j], ' ', AmRank[j]
#     # print type(j), ' ', type(isbn[j]), ' ', type(FoundPrice[j]), ' ', type(AmUsed[j]), ' ', type(AmNew[j]), ' ', type(AmRetail[j]), ' ', type(AmRank[j])
#     PriceArray = [AmUsed[j], AmNew[j], AmRetail[j]]
#     minPrice = min(i for i in PriceArray if i > 0)
#     # print minPrice
#     # print type(LowestSellValue), 'lowest sell value type.', ' Value :', LowestSellValue
#     if (AmRetail[j] == 0) or (AwmUsed[j] == 0) or (AmNew[j] == 0):
#         print 'Warning: One or more selling variables are null for: ', isbn[j]
#
#     VariableFee = 0.15* minPrice
#     TotalFee = FlatFees+VariableFee
#     # print TotalFee
#
#
#     PotentialEarning = minPrice - TotalFee - DeliveryCost + FlatPay - FoundCost[j]
#     # print PotentialEarning
#     # Profitability = (Gross Sales - (Operations & Sales Costs) / (Sales Price)
#     # ^^ Which in this code becomes P = PotentialEarning/FoundCost[j]
#     Profitability = PotentialEarning/FoundCost[j]
#     ProfitabilityRounded = round(Profitability,4)
#     if AmRank[j] > 1000000:
#         pass
#     if AmRank[j]<1000000 and Profitability > 0.15:
#         print 'Item :', isbn[j], ' has potential of percentage profit: ', ProfitabilityRounded,'.With Potential Earning: ', PotentialEarning
#         print 'The Sales Rank is : ', AmRank[j]
#         print 'The lowest price is: ', minPrice
#         print 'The purchase price is ', FoundCost[j], 'with fees of ', TotalFee
#         if AmRank[j] > 500000:
#             print 'Warning, Sales Rank is HIGH'
#     else:
#         print 'Item : ', isbn[j], ', did not meet required potential profit margin.'
#     j=j+1
#     print ' '
print 'End Evaluation Loop'