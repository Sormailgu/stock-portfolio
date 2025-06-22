from datetime import datetime
from typing import Any, Optional

def api_response(
    status: str = "success",
    code: int = 200,
    message: str = "",
    data: Any = None,
    errors: Optional[Any] = None,
    pagination: Optional[Any] = None
):
    return {
        "status": status,
        "code": code,
        "message": message,
        "data": data if data is not None else [],
        "errors": errors,
        "meta": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "pagination": pagination
        }
    }