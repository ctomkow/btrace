# Craig Tomkow

import pybgpstream

bgp_stream = pybgpstream.BGPStream(
    from_time="2019-11-23 00:00:00 UTC",
    record_type="updates",
    filter="prefix 128.189.0.0/16"
)

for elem in bgp_stream:
    print(elem)
