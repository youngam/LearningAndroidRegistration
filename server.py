from datetime import datetime
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

SERVER_PORT = 90
HOST_ADDRESS = ''


def save_data(user_email):
    file = open('users.txt', 'a+')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file.write("{}, {}".format(user_email, current_time))
    file.write("\n")
    print("save {}".format(user_email))


def get_json(data):
    try:
        return json.loads(data)
    except ValueError:
        # if user send not json --> ignore all that he sent
        return []


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("{\"hello\":\"friend\"}".encode("utf-8"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data_str = self.rfile.read(content_length).decode()

        post_data_json = get_json(post_data_str)

        email_key = "email"
        # if client didn't send email as param
        user_email = post_data_json[email_key] if email_key in post_data_json else None

        self._set_headers()
        if user_email is not None:
            save_data(user_email)
            self.wfile.write("{\"successfully\":\"registered\"}".encode("utf-8"))
        else:
            self.wfile.write("{\"error\":\"invalid request\"}".encode("utf-8"))


def run(server_class=HTTPServer, handler_class=S, port=SERVER_PORT):
    server_address = (HOST_ADDRESS, port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()


run()
