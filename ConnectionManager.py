import logging
from threading import Thread, Lock
from termcolor import colored

class ConnectionManager:


    def __init__(self):
        self.connections = {}
        self.lock = Lock()
        self.next_id = 1

    def add_connection(self, connection, address):
        with self.lock:
            conn_id = self.next_id
            self.next_id += 1
            self.connections[conn_id] = {'connection': connection, 'address': address, 'active': True}
            print(colored('[+] ', 'magenta') + f'New Talon from {address}')
            return conn_id

    def remove_connection(self, conn_id):
        with self.lock:
            if conn_id in self.connections:
                del self.connections[conn_id]

    def get_connection(self, conn_id):
        with self.lock:
            return self.connections.get(conn_id, None)
    def list_active_connections(self):
        with self.lock:  # Assuming there's a lock for thread-safe operation
            return [
                (conn_id, details['address'], details['active'])
                for conn_id, details in self.connections.items()
                if details['active']
            ]