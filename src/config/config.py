from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ldap_mock_root: str
    ldap_admin_user: str
    ldap_admin_password: str
    ldap_mock_server_host: str
    ldap_mock_port: int


settings = Settings()
