from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager
from src.data.connect_ldap_with_retry import connect_ldap_with_retry
from src.data.models import LdapEntry
from src.config.logger import setup_logger

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    ldap = await connect_ldap_with_retry()
    app.state.ldap = ldap
    yield

app = FastAPI(lifespan=lifespan)


@app.post("/entries/")
def add_entry(request: Request, entry: LdapEntry):
    ldap = request.app.state.ldap
    try:
        ldap.add_entry(entry.dn, entry.attributes)
        return {"message": f"Entry added: {entry.dn}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/entries/")
def search_entries(request: Request, base_dn: str, query: str = "(objectClass=*)"):
    ldap = request.app.state.ldap
    try:
        return ldap.search(base_dn, query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Search operation failed: {e}")


@app.delete("/entries/{dn}")
def delete_entry(request: Request, dn: str):
    ldap = request.app.state.ldap
    try:
        ldap.delete_entry(dn)
        return {"message": f"Entry deleted: {dn}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
