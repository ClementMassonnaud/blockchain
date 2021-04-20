import cbpro
import json
import subprocess
import os
import sys
from datetime import datetime

public_client = cbpro.PublicClient()
prices_file = f'/home/{os.getlogin()}/.tmp/last-prices.json'
products = ['BTC', 'ADA', 'ETH']
threshold_pump = 5
threshold_dump = -5
delayNotif = int(sys.argv[1]) # seconds

# Read last prices
with open(prices_file) as f:
    last_prices = json.load(f)


# Get current prices
prices = {}
req = public_client.get_product_ticker
for p in products:
    prices[p] = [req(product_id=f'{p}-{base}')["price"] for base in ['USD','EUR']]

stats = {}
req = public_client.get_product_24hr_stats
for p in products:
    stats[p] = req(product_id=f'{p}-USD')

# Compute difference
def compute_diff(i,j):
    return round(((i / j) - 1)*100, 1)

diffs = {}
for p in products:
    diffs[p] = [compute_diff(float(i),float(j)) for i,j in zip(prices[p], last_prices[p])]


# Compute time interval
tnow = datetime.now().strftime("%H:%M:%S")
tlast = last_prices["time"]
FMT = '%H:%M:%S'
tdelta = datetime.strptime(tnow, FMT) - datetime.strptime(tlast, FMT)

    
# Notif
for p in products:
    if diffs[p][0] > threshold_pump:
        notif = f'{p}: +{diffs[p][0]} %'
        subprocess.call(["/home/cmasso6/src/notif-crypto", "pump", notif])
    elif diffs[p][0] < threshold_dump:
        notif = f'{p}: {diffs[p][0]} %'
        subprocess.call(["/home/cmasso6/src/notif-crypto", "dump", notif])

if tdelta.seconds > delayNotif:
    notif = f'BTC: {prices["BTC"][0]} / {prices["BTC"][1]}\nETH: {prices["ETH"][0]} / {prices["ETH"][1]}\nADA: {prices["ADA"][0]} / {prices["ADA"][1]}'
    subprocess.call(["/home/cmasso6/src/notif-crypto", "notif", notif])

# Write new prices
prices["time"] = tnow
with open(prices_file, 'w') as f:
	json.dump(prices, f)
