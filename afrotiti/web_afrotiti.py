from webserver import Webserver
import os


def handle_comments(http_request):
    print(http_request.payload)
    print(http_request.path)


def handle_orders(http_request):
    print(http_request.payload)
    print(http_request.path)


def main():
    server = Webserver("0.0.0.0", 80, 5, os.path.dirname(os.path.abspath(__file__)) + "/static")

    server.add_handler(handle_comments, "POST", "/comments")
    server.add_handler(handle_orders, "POST", "/orders")
    server.run()


if __name__ == '__main__':
    main()