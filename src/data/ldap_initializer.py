import json
from pathlib import Path
from typing import Dict
from ldap3 import Connection
from src.config.logger import setup_logger

logger = setup_logger(__name__)


class LdapDataInitializer:
    """Инициализатор тестовых данных LDAP"""

    def __init__(self, ldap_conn: Connection, data_path: Path):
        self.conn = ldap_conn
        self.data_path = data_path

    def initialize_from_file(self) -> Dict[str, int]:
        """Загружает и добавляет данные из JSON, пропуская существующие записи"""
        try:
            data = self._load_json_data()
            statistics = self._add_missing_entries(data)
            logger.info(f"Initialization data statistics: {statistics}")
            return statistics
        except Exception as e:
            logger.error(f"Initialization failed: {e}", exc_info=True)
            raise RuntimeError(f"Initialization failed: {e}")


    def _load_json_data(self) -> dict:
        """Загрузка данных из JSON файла"""
        path = Path(self.data_path)
        if not path.exists():
            raise FileNotFoundError(f"JSON file not found: {self.data_path}")
        return json.loads(path.read_text())

    def _add_missing_entries(self, data: dict) -> Dict[str, int]:
        """Добавляет только отсутствующие записи"""
        result = {"users_added": 0, "groups_added": 0, "skipped": 0}

        # Добавляем пользователей
        for user in data.get("users", []):
            if not self._entry_exists(user["dn"]):
                self._add_entry(user)
                result["users_added"] += 1
            else:
                result["skipped"] += 1

        # Добавляем группы (после пользователей)
        for group in data.get("groups", []):
            if not self._entry_exists(group["dn"]):
                self._add_entry(group)
                result["groups_added"] += 1
            else:
                result["skipped"] += 1

        return result

    def _entry_exists(self, dn: str) -> bool:
        """Проверяет существование записи"""
        return self.conn.search(dn, "(objectClass=*)", search_scope="BASE")

    def _add_entry(self, entry: dict):
        """Добавляет новую запись в LDAP"""
        dn = entry.pop("dn")
        attributes = entry
        self.conn.add(dn, attributes=attributes)
        if self.conn.result["result"] != 0:
            raise RuntimeError(f"Failed to add entry {dn}: {self.conn.result['message']}")
