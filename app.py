from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'devops-secret-key!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Background thread to emit real-time system/app metrics
def background_metrics():
    count = 0
    while True:
        time.sleep(2)  # Every 2 seconds
        count += 1
        # Emitting real-time updates to all connected clients
        socketio.emit('metrics_update', {
            'ping_count': count,
            'status': 'Healthy',
            'timestamp': time.strftime('%H:%M:%S')
        })

@app.route('/')
def index():
    # Simple HTML page with WebSocket client
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask Realtime App - DevOps Dashboard</title>
        <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
        <style>
            body { font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; }
            .card { background: #1e293b; padding: 20px; border-radius: 8px; width: 350px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
            .status { color: #22c55e; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>🚀 Live Pipeline & App Metrics</h2>
            <p>Status: <span class="status" id="status">Connecting...</span></p>
            <p>Live Pings Received: <strong id="ping-count">0</strong></p>
            <p>Last Update: <span id="timestamp">--:--:--</span></p>
        </div>

        <script>
            const socket = io();

            socket.on('connect', () => {
                document.getElementById('status').innerText = 'Connected (Realtime Active)';
            });

            // Listen for 'metrics_update' event from backend
            socket.on('metrics_update', function(data) {
                document.getElementById('ping-count').innerText = data.ping_count;
                document.getElementById('timestamp').innerText = data.timestamp;
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    # Start background thread for realtime metric pushing
    thread = threading.Thread(target=background_metrics)
    thread.daemon = True
    thread.start()

    # Run SocketIO server instead of app.run()
    socketio.run(app, host='0.0.0.0', port=5000)