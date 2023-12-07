import GrabGovCsv

link = input()
govData = GrabGovCsv.govDataset(link)
govData.grab()