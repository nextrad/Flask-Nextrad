from app import app, app
from app import ConManager



if __name__ == '__main__':
    ConManager.socketio.run(app, host='10.0.0.111', port=5000)
    # ConManager.socketio.run(app)
    # app.run(host='10.0.0.111', threaded=True)
