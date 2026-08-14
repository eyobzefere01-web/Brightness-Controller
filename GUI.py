import os
import sys
import webview
import threading
from app import app

def start_server():
    app.run(host='127.0.0.1', port=4501, debug=False, use_reloader=False)

if __name__ == '__main__':
    # Check if display is available
    display = os.environ.get('DISPLAY')
    
    # Start the Flask server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Try to create GUI window if display is available
    if display:
        try:
            webview.create_window(
                'Brightness Controller', 
                'http://127.0.0.1:4501',
                min_size=(800, 700),
                zoomable=False,
                fullscreen=False,
                frameless=False
            )
            webview.start()
        except Exception as e:
            print(f"GUI Error: {e}")
            print("Starting in headless mode...")
            print("Access the app at: http://127.0.0.1:4501")
            # Keep server running in background
            server_thread.join()
    else:
        print("No display available. Running in headless mode...")
        print("Access the app at: http://127.0.0.1:4501")
        # Keep server running indefinitely
        try:
            server_thread.join()
        except KeyboardInterrupt:
            print("\nShutting down...")
            sys.exit(0)
