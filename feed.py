#!/usr/bin/env python
# Craig Tomkow

import pybgpstream

# 2019-11-23 00:00:00 UTC
bgp_stream = pybgpstream.BGPStream(
    #from_time="2019-01-01 00:00:00 UTC",
    #until_time="2019-01-01 00:05:00 UTC",
    data_interface="singlefile"
    #filter="prefix exact 128.189.0.0/16 and elemtype withdrawals"
)

for elem in bgp_stream:
    #if elem.type == "W":
    print(elem)
