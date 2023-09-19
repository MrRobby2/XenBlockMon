# Download the fresh script
clear
curl -o XenBlockMonitor.py -LJO https://github.com/MrRobby2/XenBlockMon/raw/main/XenBlockMon.py
echo

if [ -z "$1" ]; then
  echo "Please provide an address as an argument."
  exit 1
fi

account="$1"

echo "Starting synchronization using account: $account"
python3 XenBlockMonitor.py "$account"
