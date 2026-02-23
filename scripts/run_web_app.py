#!/usr/bin/env python3
"""
Pyrl Web Application Server

A Python wrapper that runs Pyrl web applications as HTTP servers.
The Pyrl application defines routes and handlers, and this wrapper
handles the actual HTTP server functionality.

Usage:
    python run_web_app.py [options]

Options:
    --port PORT      Server port (default: from env PYRL_PORT or 8080)
    --host HOST      Server host (default: from env PYRL_HOST or 0.0.0.0)
    --file FILE      Pyrl application file (default: examples/web_app.pyrl)

Environment Variables:
    PYRL_PORT        Server port
    PYRL_HOST        Server host
    PYRL_SECRET      Secret key for sessions
"""
import os
import sys
import json
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.vm import PyrlVM, PyrlFunction, PyrlInstance, PyrlRuntimeError


class PyrlWebApp:
    """Wrapper for Pyrl web applications."""
    
    def __init__(self, pyrl_file: str):
        self.pyrl_file = pyrl_file
        self.vm = PyrlVM(debug=False)
        self.app_instance = None
        self.handle_func = None
        self.routes = {}
        self.load_app()
    
    def load_app(self):
        """Load the Pyrl application file."""
        print(f"Loading Pyrl application: {self.pyrl_file}")
        
        # Read and execute the Pyrl file
        with open(self.pyrl_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        self.vm.run(code)
        
        # Get the application instance or handle function
        try:
            # Try to get $app variable
            app_var = self.vm.get_variable('app')
            if app_var is not None:
                print(f"Found $app variable: {type(app_var).__name__}")
                # Check if it has a 'handle' key (for dict-style app)
                if isinstance(app_var, dict) and 'handle' in app_var:
                    self.handle_func = app_var['handle']
                    print("Using handle function from $app")
                else:
                    self.app_instance = app_var
            else:
                # Try to get handle_request function directly
                self.handle_func = self.vm.env.get('&handle_request')
                print("Using &handle_request function directly")
        except Exception as e:
            print(f"Warning: Could not get app instance: {e}")
            # Try handle_request as fallback
            try:
                self.handle_func = self.vm.env.get('&handle_request')
            except:
                pass
    
    def handle_request(self, method: str, path: str, headers: dict, body: str) -> dict:
        """Handle an HTTP request through the Pyrl application."""
        # If we have a handle function, use it directly
        if self.handle_func is not None:
            return self.handle_func(method, path, headers, body)
        
        # If we have an app instance with a handle method
        if self.app_instance is not None:
            from src.core.vm import PyrlInstance
            if isinstance(self.app_instance, PyrlInstance):
                handle_method = self.app_instance.get_method('handle')
                return handle_method(method, path, headers, body)
        
        # Fallback
        return {
            'status': 404,
            'headers': {},
            'body': 'Not Found - No app or handle function found'
        }


class PyrlRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler that routes through Pyrl application."""
    
    web_app = None  # Class variable to hold the PyrlWebApp instance
    
    def log_message(self, format, *args):
        """Log HTTP requests."""
        print(f"[HTTP] {args[0]}")
    
    def send_pyrl_response(self, response: dict):
        """Send a response from Pyrl handler."""
        status = response.get('status', 200)
        headers = response.get('headers', {})
        body = response.get('body', '')
        
        # Send status
        self.send_response(status)
        
        # Send headers
        for key, value in headers.items():
            self.send_header(key, value)
        
        # Always send Content-Length if we have a body
        if body and 'Content-Length' not in headers:
            body_bytes = body.encode('utf-8') if isinstance(body, str) else body
            self.send_header('Content-Length', len(body_bytes))
        
        self.end_headers()
        
        # Send body
        if body:
            body_bytes = body.encode('utf-8') if isinstance(body, str) else body
            self.wfile.write(body_bytes)
    
    def get_headers(self) -> dict:
        """Get request headers as a dictionary."""
        headers = {}
        for key, value in self.headers.items():
            headers[key] = value
        return headers
    
    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        headers = self.get_headers()
        
        print(f"[GET] {path}")
        
        response = self.web_app.handle_request('GET', path, headers, '')
        self.send_pyrl_response(response)
    
    def do_POST(self):
        """Handle POST requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        headers = self.get_headers()
        
        # Read body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else ''
        
        print(f"[POST] {path} (body: {len(body)} bytes)")
        
        response = self.web_app.handle_request('POST', path, headers, body)
        self.send_pyrl_response(response)
    
    def do_HEAD(self):
        """Handle HEAD requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        headers = self.get_headers()
        
        response = self.web_app.handle_request('HEAD', path, headers, '')
        
        # Send headers only
        status = response.get('status', 200)
        headers = response.get('headers', {})
        
        self.send_response(status)
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()


def run_server(host: str, port: int, pyrl_file: str):
    """Run the HTTP server with the Pyrl application."""
    print("=" * 60)
    print("Pyrl Web Application Server")
    print("=" * 60)
    print()
    
    # Set environment variables for the Pyrl app
    os.environ['PYRL_PORT'] = str(port)
    os.environ['PYRL_HOST'] = host
    
    # Load the Pyrl application
    web_app = PyrlWebApp(pyrl_file)
    PyrlRequestHandler.web_app = web_app
    
    # Create the HTTP server
    server_address = (host, port)
    httpd = HTTPServer(server_address, PyrlRequestHandler)
    
    print()
    print("=" * 60)
    print(f"Server starting on http://{host}:{port}")
    print("=" * 60)
    print()
    print("Available routes:")
    print("  GET  /           - Login page")
    print("  POST /login      - Process authentication")
    print("  GET  /dashboard  - Dashboard (requires auth)")
    print("  POST /logout     - Logout user")
    print("  GET  /api/status - API status endpoint")
    print()
    print("Test credentials:")
    print("  admin / admin123 - Administrator")
    print("  user  / user123  - Regular user")
    print("  demo  / demo     - Demo user")
    print()
    print("Press Ctrl+C to stop the server.")
    print("=" * 60)
    print()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Server stopped.")
        httpd.shutdown()


def main():
    parser = argparse.ArgumentParser(description='Pyrl Web Application Server')
    parser.add_argument('--port', type=int, 
                        default=int(os.environ.get('PYRL_PORT', 8080)),
                        help='Server port (default: 8080)')
    parser.add_argument('--host', type=str,
                        default=os.environ.get('PYRL_HOST', '0.0.0.0'),
                        help='Server host (default: 0.0.0.0)')
    parser.add_argument('--file', type=str,
                        default='examples/web_app.pyrl',
                        help='Pyrl application file')
    
    args = parser.parse_args()
    
    run_server(args.host, args.port, args.file)


if __name__ == '__main__':
    main()
