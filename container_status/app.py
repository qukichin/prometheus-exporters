from flask import Response, Flask
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry
import prometheus_client
import docker

app = Flask(__name__)

reg = CollectorRegistry(auto_describe=False)

container_status = Gauge(
    'container_status', 'Container Status',
    labelnames=['name'], registry=reg
)

client = docker.DockerClient(base_url='unix://var/run/docker.sock')


def get_containers(client: docker.DockerClient):
    return {
        c.name: c.status
        for c in client.containers.list(all=True)
    }


def generate_metrics(containers: dict):
    for name, status in containers.items():
        status = 1 if status.lower() == 'running' else 0
        container_status.labels(name).set(status)


@app.route("/metrics")
def handler():
    containers = get_containers(client)
    generate_metrics(containers)

    return Response(prometheus_client.generate_latest(reg), mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
