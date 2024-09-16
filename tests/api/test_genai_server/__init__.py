import unittest
import threading
import time
import os
import signal
import socket
import psutil
from setup import stack


def run_server(port):
    stack.run_server(host="127.0.0.1", port=port)


def find_free_port(initial_port):
    port = initial_port
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", port))
            return port
        except OSError:
            port += 1


def start_server():
    free_port = find_free_port(5600)
    server_thread = threading.Thread(target=run_server, args=(free_port,))
    server_thread.start()
    time.sleep(6)
    return free_port


def stop_server(port):
    try:
        for conn in psutil.net_connections():
            if conn.laddr.port == port:
                os.kill(conn.pid, signal.SIGTERM)
                break
    except (ProcessLookupError, psutil.NoSuchProcess):
        pass
    time.sleep(2)


class TestCaseServer(unittest.TestCase):

    host = None
    server_port = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.server_port = start_server()
        cls.host = "127.0.0.1"
        cls.base_url = f"http://{cls.host}:{cls.server_port}/api/"

    @classmethod
    def tearDownClass(cls) -> None:
        stop_server(cls.server_port)

