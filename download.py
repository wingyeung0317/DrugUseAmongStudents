import GrabGovCsv
print('Please enter the relative data.gov.hk link')
link = input()
govData = GrabGovCsv.govDataset(link)
print('Please choose a type: Print / csv / txt\nPrint would print all link to the console.\ncsv would download the csv files\ntxt would print all the csv links into ./csvList.txt')
method = input().lower()
govData.grab(method)