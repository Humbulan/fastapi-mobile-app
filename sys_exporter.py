import prometheus_client
from flask import Flask, Response
import psutil

app = Flask(__name__)
REGISTRY = prometheus_client.CollectorRegistry()

cpu_usage = prometheus_client.Gauge('system_cpu_usage', 'CPU usage %', registry=REGISTRY)
mem_usage = prometheus_client.Gauge('system_mem_usage', 'Memory usage %', registry=REGISTRY)

@app.route('/metrics')
def metrics():
    cpu_usage.set(psutil.cpu_percent())
    mem_usage.set(psutil.virtual_memory().percent)
    return Response(prometheus_client.generate_latest(REGISTRY),
                    mimetype=prometheus_client.CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9103)
