from satellite import listen_for_tasks

host = "127.0.0.1"
port = 65433

if __name__ == "__main__":
    listen_for_tasks(host, port)
