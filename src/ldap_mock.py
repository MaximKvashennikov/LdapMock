from ldap3 import Server, Connection, MOCK_SYNC, ALL_ATTRIBUTES, ALL

class LdapMock:
    def __init__(self):
        self.server = Server('mock_ldap', get_info=ALL)
        self.conn = Connection(
            self.server,
            client_strategy=MOCK_SYNC,
            user="cn=admin,dc=example,dc=com",
            password="admin",
        )
        self.conn.bind()

    def add_entry(self, dn: str, attributes: dict):
        # Преобразуем одиночные значения в списки (как требует LDAP)
        processed_attrs = {}
        for key, value in attributes.items():
            if not isinstance(value, list):
                processed_attrs[key] = [value]
            else:
                processed_attrs[key] = value
        self.conn.strategy.add_entry(dn, processed_attrs)

    def search(self, base_dn: str, query: str = "(objectClass=*)"):
        if self.conn.search(base_dn, query, attributes=ALL_ATTRIBUTES):
            return [
                {
                    "dn": entry.entry_dn,
                    "attributes": {attr: entry[attr].value for attr in entry.entry_attributes}
                }
                for entry in self.conn.entries
            ]
        return []

    def delete_entry(self, dn: str):
        self.conn.delete(dn)

    def clear(self):
        for entry in self.conn.entries:
            self.conn.delete(entry.entry_dn)
