import asyncio
import logging
from src.ldap_service import LdapService

logger = logging.getLogger(__name__)


async def connect_ldap_with_retry(max_retries=15, retry_interval=5):
    for attempt in range(max_retries):
        logger.info(f"Attempt to connect LDAP: {attempt + 1}/{max_retries}")
        try:
            ldap = LdapService()
            ldap.conn.bind()
            if ldap.conn.bound:
                logger.info("LDAP connected.")
                return ldap
        except Exception as e:
            logger.warning(f"LDAP connection failed on attempt {attempt + 1}: {e}")
        await asyncio.sleep(retry_interval)
    msg = "Failed to connect to LDAP during startup"
    logger.error(msg)
    raise RuntimeError(msg)
