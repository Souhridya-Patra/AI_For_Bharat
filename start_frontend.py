"""Start the frontend web interface."""
import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

PORT = 3000
DIRECTORY = "frontend"

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler with CORS support."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        """Add CORS headers."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests."""
        self.send_response(200)
        self.end_headers()

def main():
    """Start the frontend server."""
    print("=" * 60)
    print("AI Voice Platform - Frontend Server")
    print("=" * 60)
    print()
    
    # Check if frontend directory exists
    if not Path(DIRECTORY).exists():
        print(f"✗ Error: {DIRECTORY} directory not found")
        return
    
    # Check if index.html exists
    if not Path(f"{DIRECTORY}/index.html").exists():
        print(f"✗ Error: {DIRECTORY}/index.html not found")
        return
    
    print(f"Starting frontend server on port {PORT}...")
    print()
    print("Frontend will be available at:")
    print(f"  http://localhost:{PORT}")
    print()
    print("Make sure the backend is running:")
    print("  python start_server.py")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Start server
    with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
        # Open browser
        webbrowser.open(f"http://localhost:{PORT}")
        
        print(f"✓ Frontend server running on http://localhost:{PORT}")
        print()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nShutting down frontend server...")
            print("✓ Frontend server stopped")

if __name__ == "__main__":
    main()
