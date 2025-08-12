from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager
from src.data.connect_ldap_with_retry import connect_ldap_with_retry
from src.data.models import LdapEntry, LdapModifyRequest
from src.config.logger import setup_logger

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекстный менеджер для управления жизненным циклом приложения.
    Инициализирует подключение к LDAP-серверу перед запуском приложения.
    """
    ldap = await connect_ldap_with_retry()
    app.state.ldap = ldap
    yield


app = FastAPI(
    lifespan=lifespan,
    title="LDAP Management API",
    description="API для управления записями в LDAP-сервере",
)


@app.post(
    "/entries/",
    summary="Добавить новую запись в LDAP",
    response_description="Сообщение об успешном добавлении",
)
def add_entry(request: Request, entry: LdapEntry):
    ldap = request.app.state.ldap
    try:
        ldap.add_entry(entry.dn, entry.attributes)
        return {"message": f"Entry added: {entry.dn}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get(
    "/entries/",
    summary="Поиск записей в LDAP",
    response_description="Список найденных записей"
)
def search_entries(request: Request, base_dn: str, query: str = "(objectClass=*)"):
    ldap = request.app.state.ldap
    try:
        return ldap.search(base_dn, query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Search operation failed: {e}")


@app.patch(
    "/entries/{dn}",
    summary="Модификация LDAP-записи",
    response_description="Сообщение об успешном изменении",
)
def modify_entry(request: Request, dn: str, changes: LdapModifyRequest):
    ldap = request.app.state.ldap
    try:
        ldap.modify_entry(dn, changes.attributes)
        return {"message": f"Entry modified: {dn}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete(
    "/entries/{dn}",
    summary="Удалить запись из LDAP",
    response_description="Сообщение об успешном удалении",
)
def delete_entry(request: Request, dn: str):
    ldap = request.app.state.ldap
    try:
        ldap.delete_entry(dn)
        return {"message": f"Entry deleted: {dn}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
