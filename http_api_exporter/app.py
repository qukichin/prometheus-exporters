from flask import Response, Flask
from prometheus_client import Gauge, generate_latest
from prometheus_client.core import CollectorRegistry
from probe import geturl

app = Flask(__name__)

reg = CollectorRegistry(auto_describe=False)

api_status = Gauge(
    'http_api_status', 'HTTP API Status',
    labelnames=['name'], registry=reg
)


def generate_metrics(data: dict):
    for name, status in data.items():
        api_status.labels(name).set(status)


@app.route("/metrics")
def handler():
    generate_metrics(geturl())

    return Response(
        generate_latest(reg),
        mimetype="text/plain"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
