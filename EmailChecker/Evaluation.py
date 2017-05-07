# Beginning Analysis of found products.
import pandas as pd

ProductData = 'ProductData.txt'

pddata = pd.read_csv(ProductData, delimiter = '\s+')

print pddata
FlatFees = 118
FlatPay = 280
DeliveryCost = 275

j = 0
RowNum = pddata['Number']
isbn = pddata['ISBN']
FoundCost = pddata['FoundCost']
AmUsed = pddata['AmUsed']
AmNew = pddata['AmNew']
AmRetail = pddata['AmRetail']
AmRank = pddata['AmRank']
# print AmRank, 'Rank Data'

print AmRank

# while j < len(pddata):
while j < 2:
    # print ' '
    # print j, ' ', isbn[j], ' ', FoundPrice[j], ' ', AmUsed[j], ' ', AmNew[j], ' ', AmRetail[j], ' ', AmRank[j]
    # print type(j), ' ', type(isbn[j]), ' ', type(FoundPrice[j]), ' ', type(AmUsed[j]), ' ', type(AmNew[j]), ' ', type(AmRetail[j]), ' ', type(AmRank[j])
    PriceArray = [AmUsed[j], AmNew[j], AmRetail[j]]
    minPrice = min(i for i in PriceArray if i > 0)
    # print minPrice
    # print type(LowestSellValue), 'lowest sell value type.', ' Value :', LowestSellValue

    VariableFee = 0.15* minPrice
    TotalFee = FlatFees+VariableFee
    # print TotalFee


    PotentialEarning = minPrice - TotalFee - DeliveryCost + FlatPay - FoundCost[j]
    # print PotentialEarning
    # Profitability = (Gross Sales - (Operations & Sales Costs) / (Sales Price)
    # ^^ Which in this code becomes P = PotentialEarning/FoundCost[j]
    Profitability = PotentialEarning/FoundCost[j]*100
    ProfitabilityRounded = round(Profitability,4)
    if AmRank[j] > 1000000:
        pass
    if AmRank[j]<1000000 and Profitability > 0.15:
        print 'Item :', isbn[j], ' has potential of percentage profit: ', ProfitabilityRounded,'.With Potential Earning: ', PotentialEarning
        print 'The Sales Rank is : ', AmRank[j]
        print 'The lowest price is: ', minPrice
        print 'The purchase price is ', FoundCost[j], 'with fees of ', TotalFee
        if (AmRetail[j] == 0) or (AmUsed[j] == 0) or (AmNew[j] == 0):
            print 'Warning: One or more selling variables are null for: ', isbn[j]
        if AmRank[j] > 500000:
            print 'Warning, Sales Rank is HIGH'
    else:
        pass
        # print 'Item : ', isbn[j], ', did not meet required potential profit margin.'
    j=j+1
    print ' '
print 'End Evaluation Loop'
