#!/usr/bin/env python

import datetime
import requests

todayts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

kibana_endpoint = "http://<elasticsearch-load-balancer-endpoint>.ap-southeast-1.elb.amazonaws.com:9200"

cutoffdays = 14

try:
    # Determine dates
    cutoffdate = datetime.date.fromordinal(datetime.date.today().toordinal()-cutoffdays).strftime("%Y.%m.%d")

    # Get available snapshots
    ra = requests.get(url = "%s/_snapshot/s3repo/_all" % kibana_endpoint)
    ra_result = ra.json()['snapshots']
    snapshots_to_delete = []
    for snapshot in ra_result:
        snapshot_date = snapshot['snapshot'][-10:]
        print "%s %s < %s ... ? " % (todayts, snapshot_date, cutoffdate)
        # Mark snapshots older than cutoff days for deletion
        if snapshot_date < cutoffdate:
            print "%s Marking %s for deletion" % ( todayts, snapshot['snapshot'] )
            snapshots_to_delete.append(snapshot['snapshot'])

    # Make sure snapshots are available for yesterday up to cut-off days ago
    for nday in range(1, cutoffdays+1):

        # Take snapshot of ndayts's data
        ndayts = datetime.date.fromordinal(datetime.date.today().toordinal()-nday).strftime("%Y.%m.%d")
        print "%s Taking snapshot of %s data" % ( todayts,ndayts )
        snapshot_json = "{ \"indices\": \"filebeat-%s,topbeat-%s\", \"region\": \"ap-southeast-1\", \"base_path\": \"snapshots\" }" % (ndayts, ndayts)
        rs = requests.put(url = "%s/_snapshot/s3repo/data-%s?wait_for_completion=true" % (kibana_endpoint, ndayts),
          data = snapshot_json)

    # Delete marked snapshots
    for delsnapshot in snapshots_to_delete:
        print "%s Deleting %s" % ( todayts, delsnapshot )
        rd = requests.delete(url = "%s/_snapshot/s3repo/%s" % (kibana_endpoint, delsnapshot) )
        rfilebeat = requests.delete(url = "%s/%s" % (kibana_endpoint, delsnapshot.replace("data-", "filebeat-")))
        rtopbeat = requests.delete(url = "%s/%s" % (kibana_endpoint, delsnapshot.replace("data-", "topbeat-")))

except Exception as e:

    print "%s Exception: %s" % ( todayts, str(e) )

print "%s Done" % todayts
