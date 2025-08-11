from pathlib import Path

from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, AUTO_BIND_TLS_BEFORE_BIND
from src.config.config import settings
from src.config.logger import setup_logger
from src.data.ldap_initializer import LdapDataInitializer

logger = setup_logger(__name__)


class LdapService:
    def __init__(self):
        self.server = Server(
            host=settings.ldap_mock_server_host,
            port=settings.ldap_mock_port,
            get_info=ALL,
            use_ssl=True,
            connect_timeout=50
        )
        self.conn = Connection(
            self.server,
            user=f"{settings.ldap_admin_user},{settings.ldap_mock_root}",
            password=settings.ldap_admin_password,
            lazy=True,
            auto_bind=True
        )

        logger.info("Connected to LDAP server")
        self.initialize_test_data()

    def initialize_test_data(self, json_path: Path = settings.ldap_initial_data) -> dict:
        """Инициализация тестовыми данными"""
        initializer = LdapDataInitializer(self.conn, data_path=json_path)
        return initializer.initialize_from_file()

    def add_entry(self, dn: str, attributes: dict) -> None:
        logger.debug(f"Adding entry: {dn}")
        try:
            self.conn.add(dn, attributes=attributes)
            if self.conn.result['result'] != 0:
                raise Exception(self.conn.result['message'])
            logger.info(f"Successfully added entry: {dn}")
        except Exception as e:
            logger.error(f"Failed to add entry {dn}: {e}")
            raise

    def search(self, base_dn: str, query: str = "(objectClass=*)"):
        logger.info(f"Searching in base DN: {base_dn} with filter: {query}")
        if self.conn.search(base_dn, query, attributes=ALL_ATTRIBUTES):
            return [
                {
                    "dn": entry.entry_dn,
                    "attributes": {attr: entry[attr].value for attr in entry.entry_attributes}
                }
                for entry in self.conn.entries
            ]
        logger.warning(f"No entries found for base DN: {base_dn}, filter: {query}")
        return []

    def delete_entry(self, dn: str) -> None:
        logger.warning(f"Deleting entry: {dn}")
        try:
            self.conn.delete(dn)
            if self.conn.result['result'] != 0:
                raise Exception(self.conn.result['message'])
            logger.warning(f"Deleted entry: {dn}")
        except Exception as e:
            logger.error(f"Failed to delete entry {dn}: {e}")
            raise


ldap = LdapService()
