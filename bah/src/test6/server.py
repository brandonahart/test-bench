# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import rpy2.robjects as robjects

hostName = "localhost"
serverPort = 8080

def run_r_test():
    try:
        # Load the R script using rpy2
        robjects.r['source']('joel_test.R')
        result = robjects.r['result'][0]
        return f'The R test script says: {result}'
    except Exception as e:
        return f'Error running R script: {e}'


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if self.path == '/test':
            run_r_test()
            self.wfile.write(bytes("<p>R test was ran</p>", "utf-8"))
        else:
            self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
