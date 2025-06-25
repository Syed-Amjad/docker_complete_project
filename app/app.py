from flask import Flask, render_template
from prometheus_flask_exporter import PrometheusMetrics
import redis

app = Flask(__name__)

# Initialize Prometheus metrics (this automatically adds /metrics)
metrics = PrometheusMetrics(app)

# Redis setup
cache = redis.Redis(host='redis', port=6379)

@app.route('/')
def index():
    count = cache.incr('hits')
    return render_template('index.html', count=count)

@app.route('/custom_metrics')
def custom_metrics():
    count = cache.get('hits') or 0
    return f"hits_total {count.decode() if isinstance(count, bytes) else count}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)

