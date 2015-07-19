__author__ = 'shawn'
# flask interface to the couchdb
from db_store import DbStore
import json
from flask import Flask, request
from db_crossorigin import crossdomain

app = Flask(__name__)
couch = DbStore()


@app.route("/")
def root():
    return "luc"


@app.route("/episode<key>", methods=['POST', 'GET', 'OPTIONS'])
@crossdomain(origin='http://localhost', headers='Content-Type')
def save_episode(key):
    if request.method == 'POST':
        data = json.loads(request.data)
        doc_id = couch.save_episode(data)
        # for CORS - if return type doesn't match the request, client will get an error
        return str(doc_id)
    elif request.method == 'GET':
        query = request.args['key'] if 'key' in request.args else None
        episode = couch.get_all_episodes(query)
        return episode

@app.route("/grid", methods=['GET', 'OPTIONS'])
@crossdomain(origin='http://localhost', headers='Content-Type')
def display_grid():
    data = couch.get_all_episodes()
    transformed_data = []
    for item in data[1]['rows']:
        transformed_data.append(item['value'])
    grid_data = json.dumps(transformed_data)
    return grid_data


if __name__ == "__main__":
    app.run(debug=False)


