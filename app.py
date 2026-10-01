from flask import Flask, render_template
from flask_socketio import SocketIO
import random
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'devops-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

def generate_live_metrics():
    while True:
        time.sleep(2)
        socketio.emit('system_metrics', {
            'cpu': round(random.uniform(15.0, 65.0), 1),
            'memory': round(random.uniform(40.0, 80.0), 1),
            'active_pods': random.randint(3, 8)
        })

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Live metrics generator thread
    thread = threading.Thread(target=generate_live_metrics)
    thread.daemon = True
    thread.start()
    
    # allow_unsafe_werkzeug=True allows running inside container
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)