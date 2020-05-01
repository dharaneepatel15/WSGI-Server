import threading
import multiprocessing.pool
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler


class ThreadedWSGIServer(WSGIServer):
    """WSGI-compliant HTTP server.  Dispatches requests to threads."""

    def __init__(self, *args, **kwargs):
        WSGIServer.__init__(self, *args, **kwargs)

    def processRequestThread(self, request, client_address):
        """Handle requests in seperate threads"""
        try:
            self.finish_request(request, client_address)
            self.shutdown_request(request)
        except:
            self.handle_error(request, client_address)
            self.shutdown_request(request)

    def process_request(self, request, client_address):
        """Apply request to thread and process it."""
        handle_thread = threading.Thread(
            target=self.processRequestThread, args=(request, client_address)
        )
        handle_thread.start()


def makeServer(host, port, app, handler_class=WSGIRequestHandler):
    """
    Create a threaded WSGI Server

    Parameters:
        host: host
        port: port number
        app: binded web application
        thread_count: number of threads in pool
        handler_class: request handling class

    Return:
        configured server
    """
    httpd = ThreadedWSGIServer((host, port), handler_class)
    httpd.set_app(app)
    return httpd


if __name__ == "__main__":
    httpd = makeServer("localhost", 8000, app)
    sa = httpd.socket.getsockname()
    print("Serving HTTP on", sa[0], "port", sa[1], "...")
    httpd.serve_forever()
