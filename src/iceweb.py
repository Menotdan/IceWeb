import src.http_helpers.server

version = "0.0.1"
print("Ice web http server, version " + version)
http_server = src.http_helpers.server.Server("0.0.0.0", False, "/home/aforsyth/Desktop/Website")
http_server.bind_socket()
http_server.run_server()