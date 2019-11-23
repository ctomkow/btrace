# Craig Tomkow
# Main web app file

import os, datetime
from os.path import join, dirname

from flask import Flask, render_template, json, request
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
        map_key=os.environ.get("MAP_KEY")
    )


@app.route("/api/pops/")
def api_pops():
    return json.jsonify(pop_dict)


@app.route("/api/pop/<pop_name>")
def api_pop(pop_name):
    return json.jsonify(pop_dict[pop_name])

@app.route("/api/feed/stime/<s_time>/etime/<e_time>/")
def api_feed_prefix(s_time, e_time):
    start_time = datetime.datetime.fromtimestamp(int(s_time)).strftime('%Y-%m-%d %H:%M:%S')
    end_time   = datetime.datetime.fromtimestamp(int(e_time)).strftime('%Y-%m-%d %H:%M:%S')
    prefix = request.args.get("prefix")
    stream = BGPStream(
        from_time=start_time,
        until_time=end_time,
        record_type="updates",
        filter="prefix " + prefix
    )
    update_type = []
    for elem in stream:
        update_type.append(elem.type)
    return json.jsonify(update_type)
    # TODO: return proper data not dummy data !@!@!@


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))
