#!/usr/bin/env python
# Craig Tomkow

import pybgpstream

# 2019-11-23 00:00:00 UTC
bgp_stream = pybgpstream.BGPStream(
    from_time="1572566400",
    record_type="updates",
    filter="prefix 128.189.0.0/16"
)

for elem in bgp_stream:
    print(elem)
