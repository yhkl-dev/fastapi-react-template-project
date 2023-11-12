from ldap3 import Server, Connection, ALL


class LDAPTool:
    def __init__(self, server_name: str, username: str, password: str) -> None:
        self.server = Server(server_name, get_info=ALL)
        self.conn = Connection(self.server, username, password, auto_bind=True)

    def search(self, search_base, search_filter):
        """
        conn.search('dc=example,dc=com', '(objectclass=person)')
        """
        self.conn.search(search_base, search_filter)
        return self.conn.entries
