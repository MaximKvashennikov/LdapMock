from fastapi import FastAPI, HTTPException
from src.ldap_service import LdapService
from src.models import LdapEntry
from src.config.logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI()
ldap = LdapService()

@app.post("/entries/")
def add_entry(entry: LdapEntry):
    try:
        ldap.add_entry(entry.dn, entry.attributes)
        return {"message": f"Entry added: {entry.dn}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/entries/")
def search_entries(base_dn: str, query: str = "(objectClass=*)"):
    try:
        return ldap.search(base_dn, query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Search operation failed: {e}")

@app.delete("/entries/{dn}")
def delete_entry(dn: str):
    try:
        ldap.delete_entry(dn)
        return {"message": f"Entry deleted: {dn}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
