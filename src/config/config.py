from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ldap_mock_root: str
    ldap_admin_user: str
    ldap_admin_password: str
    ldap_mock_server_host: str
    ldap_mock_port: int
    ldap_initial_data: Path = Path(__file__).parent.parent / "data" / "initial_data.json"


settings = Settings()
