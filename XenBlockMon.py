import json
import os
import requests
import time
import sys
from datetime import datetime

# Function to display banner
def display_banner():
    banner = """

██╗░░██╗███████╗███╗░░██╗  ██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗░██████╗
╚██╗██╔╝██╔════╝████╗░██║  ██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝██╔════╝
░╚███╔╝░█████╗░░██╔██╗██║  ██████╦╝██║░░░░░██║░░██║██║░░╚═╝█████═╝░╚█████╗░
░██╔██╗░██╔══╝░░██║╚████║  ██╔══██╗██║░░░░░██║░░██║██║░░██╗██╔═██╗░░╚═══██╗
██╔╝╚██╗███████╗██║░╚███║  ██████╦╝███████╗╚█████╔╝╚█████╔╝██║░╚██╗██████╔╝
╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝  ╚═════╝░╚══════╝░╚════╝░░╚════╝░╚═╝░░╚═╝╚═════╝░
    """
    print(banner)
    print("Created by TreeCityWes.eth.")
# Function to query RPC
def send_rpc_request(method, params=None, request_id=1):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": params if params is not None else []
    }
    
    response = requests.post(RPC_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return None

#X.BLK
RPC_URL = "http://xenminer.mooo.com:5555"
CUSTOM_SERVER_URL = "http://xenminer.mooo.com"
#XUNI
url_xuni = "http://xenminer.mooo.com/get_xuni_counts"
url_blocks_per_day = "http://xenminer.mooo.com/blockrate_per_day"
# Function to query custom server
def send_custom_request(endpoint, params=None):
    url = f"{CUSTOM_SERVER_URL}/{endpoint}"
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Display banner
os.system("clear")
display_banner()

# Check if an account address was provided as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python3 XenBlockMonitor.py <account_address>")
    sys.exit(1)

# Get the account address from the command-line argument
account = sys.argv[1]
account = account.lower()

while True:
    # Initialize variables
    total_network_blocks = 0
    total_account_blocks = 0
    blocks_per_day = 0
    balance_xblk = 0
    balance_xuni = 0
    balance_XNM = 0
    account_rank = 0

    # Query total number of blocks in the network
    response = send_custom_request("total_blocks")
    if response:
        total_network_blocks = response.get('total_blocks_top100')
 
    # Query total number of blocks for the account
    response = send_custom_request("total_blocks2", {"account": account})
    if response:
        total_account_blocks = response.get('total_blocks')

    
    # Query super block balance
    response = requests.get(f"{CUSTOM_SERVER_URL}/get_super_blocks/{account}")
    if response:
        super_block_data = response.json()
        balance_xblk = super_block_data.get("super_blocks")
        balance_wei = int(requests.get(f"{CUSTOM_SERVER_URL}/get_balance/{account}").json().get("balance", 0))
        balance_XNM = balance_wei
        
   
    # Query XUNI balance
    response = requests.get(url_xuni)
    if response:
        xuni_data = response.json()
        for item in xuni_data:
            account_tmp = item["account"].lower()
            count = item["count"]
            if account == account_tmp:
                balance_xuni = count
                break

    # Query balance of the account XUNI
    response = requests.get(url_blocks_per_day)
    if response:
        xuni_data = response.json()
        for item in xuni_data:
            account_tmp = item["account"].lower()
            count = item["num_blocks"]
            if account == account_tmp:
                blocks_per_day = count
                break



    # Display all information
    print(f"\r🕒 Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📈 Blocks in the network: \033[93m{total_network_blocks}\033[0m")
    print(f"")
    #print(f"💸 RANK: \033[93m{account_rank} \033[0m")
    print(f"📈 TOTAL BLOCKS MINED:\t\033[93m{total_account_blocks}\033[0m")
    print(f"💸 XENIUM ($XNM):\t\033[93m{balance_XNM} \033[0m")
    print(f"💸 XUNI BLOCKS: \t\033[93m{balance_xuni}\033[0m")
    print(f"💸 SUPER BLOCKS:\t\033[93m{balance_xblk}\033[0m")
    print(f"📈 BLOCKRATE PER DAY:\t\033[93m{blocks_per_day}\033[0m")
    print("◼️" * 30)

    # Countdown for next update on the same line
    sys.stdout.write("Next update in: ")
    for i in range(30, 0, -1):
        sys.stdout.write(f"\rNext update in: {i} ")
        sys.stdout.flush()
        time.sleep(1)
    print("\rRefreshing now... ")
    
