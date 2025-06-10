from fastapi.responses import JSONResponse
from datetime import datetime
import uuid
from functools import wraps
from app.models.stock_query import StockQuery

def mcp_response(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        try:
            result = await f(*args, **kwargs)
            response = {
                "data": result if isinstance(result, list) else [],
                "metadata": {
                    "request_id": str(uuid.uuid4()),
                    "timestamp": datetime.now(UTC).isoformat(),
                    "status": "success",
                    "endpoint": f.__name__,
                    "query_params": kwargs.get('query', StockQuery()).model_dump() if hasattr(kwargs.get('query', StockQuery()), 'model_dump') else {}
                },
                "errors": []
            }
            return JSONResponse(content=response, status_code=200)
        except Exception as e:
            response = {
                "data": [],
                "metadata": {
                    "request_id": str(uuid.uuid4()),
                    "timestamp": datetime.now(UTC).isoformat(),
                    "status": "error",
                    "endpoint": f.__name__,
                    "query_params": kwargs.get('query', StockQuery()).model_dump() if hasattr(kwargs.get('query', StockQuery()), 'model_dump') else {}
                },
                "errors": [{"message": str(e), "code": 500}]
            }
            return JSONResponse(content=response, status_code=500)
    return decorated_function