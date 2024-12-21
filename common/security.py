from config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="Authorization", scheme_name="ApiKey")

def check_api_key(api_key: str = Depends(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    api_key.replace("ApiKey ", "")
    if not _has_access(api_key):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def _has_access(api_key: str):
    if api_key == settings.api_key:
        return True
    else:
        return False


