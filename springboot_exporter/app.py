from flask import Response, Flask
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry
import prometheus_client
import json
import os
import requests

app = Flask(__name__)

url = os.environ.get('SPRINGBOOT_URL')
url = url if url else "http://127.0.0.1:8080/management/health"

reg = CollectorRegistry(auto_describe=False)
springboot_status = Gauge(
    'springboot_status', 'Service Status',
    labelnames=['name'], registry=reg
)


def get_health(url: str):
    content = json.loads(requests.get(url).content)
    services = content['details']

    return {
        service: 1 if detail['status'].upper() == 'UP' else 0
        for service, detail in services.items()
    }


def generate_metrics(data: dict):
    for name, status in data.items():
        springboot_status.labels(name).set(status)


@app.route("/metrics")
def handler():
    result = get_health(url)
    generate_metrics(result)

    return Response(
        prometheus_client.generate_latest(reg),
        mimetype="text/plain"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
