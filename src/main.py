from fastapi import FastAPI, HTTPException
from src.ldap_mock import LdapMock
from src.logger import setup_logger
from src.models import LdapEntry


logger = setup_logger(__name__)

app = FastAPI()
ldap = LdapMock()

@app.post("/entries/")
def add_entry(entry: LdapEntry):
    try:
        ldap.add_entry(entry.dn, entry.attributes)
        logger.info(f"Entry added: {entry.dn} with attributes: {entry.attributes}")
        return {"message": "Entry added"}
    except Exception as e:
        logger.error(f"Failed to add entry {entry.dn}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/entries/")
def search_entries(base_dn: str, query: str = "(objectClass=*)"):
    try:
        results = ldap.search(base_dn, query)
        logger.info(f"Searched entries under base_dn: {base_dn} with query: {query}. Results: {results}")
        return results
    except Exception as e:
        logger.error(f"Search failed for base_dn: {base_dn} with query: {query}: {str(e)}")
        raise HTTPException(status_code=400, detail="Search operation failed")

@app.delete("/entries/{dn}")
def delete_entry(dn: str):
    try:
        ldap.delete_entry(dn)
        logger.info(f"Entry deleted: {dn}")
        return {"message": "Entry deleted"}
    except Exception as e:
        logger.error(f"Failed to delete entry {dn}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/clear/")
def clear_entries():
    try:
        ldap.clear()
        logger.warning("All entries cleared")
        return {"message": "All entries cleared"}
    except Exception as e:
        logger.error(f"Failed to clear entries: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to clear entries")
