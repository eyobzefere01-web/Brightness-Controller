import webview
import threading
from app import app

def start_server():
    app.run(host='127.0.0.1', port=4501, debug=False, use_reloader=False)

if __name__ == '__main__':
    # 1. Start the Flask server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    webview.create_window(
        'Brightness Controller', 
        'http://127.0.0.1:4501',
        min_size=(800, 700),
        zoomable=False,
        fullscreen=False,
        frameless=False
    )
    
    webview.start()
