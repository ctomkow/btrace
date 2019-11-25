# Craig Tomkow
# Main web app file

import os, datetime
from os.path import join, dirname

from flask import Flask, render_template, json, request, Response
from dotenv import load_dotenv
from pybgpstream import BGPStream

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

app = Flask(__name__)

# bgp collector PoP list
pop_dict = {
        "rv_amsix": {
            "lat": 55.60498,
            "lng": 13.00382,
        },
        "rv_chicago": {
            "lat": 41.87811,
            "lng": -87.62979,
        },
}

@app.route('/')
def render():
    return render_template(
        "index.html",
        title="tracing bgp withdrawals across the world",
        map_key=os.environ.get("MAP_KEY-dev")
    )


@app.route("/api/pops/")
def api_pops():
    return json.jsonify(pop_dict)


@app.route("/api/pop/<pop_name>")
def api_pop(pop_name):
    return json.jsonify(pop_dict[pop_name])


@app.route("/api/bgp/withdrawal/stime/<s_time>/etime/<e_time>/")
def api_bgp_withdrawal_prefix(s_time, e_time):
    s_time = int(s_time)
    e_time = int(e_time)
    if e_time == 0:  # end time is now!
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    elif s_time > e_time:
        return Response("", status=400, mimetype='application/json')
    else:
        end_time = datetime.datetime.fromtimestamp(e_time).strftime('%Y-%m-%d %H:%M:%S')
    start_time = datetime.datetime.fromtimestamp(s_time).strftime('%Y-%m-%d %H:%M:%S')
    prefix = request.args.get("prefix")

    stream = BGPStream(
        from_time=start_time,
        until_time=end_time,
        record_type="updates",
        filter="prefix " + prefix
    )
    bgp_data = {}
    for elem in stream:
        print(elem, flush=True)
        if elem.type == "W":
            bgp_data[elem.time] = elem.collector

    return json.jsonify(bgp_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))
