# Zerotier2PowerDNS

This script gets all the nodes in a Zerotier network and adds them with a common suffix to a PowerDNS zone.

## Prerequisites
* `requests`
* Zerotier API Key
* Zerotier Network ID
* PowerDNS Server with configured API access

## Setup
Just set the required parameters in the settings section in the script and run it regularly e.g. via `cron`.