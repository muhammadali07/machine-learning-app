from fastapi import APIRouter, Depends, HTTPException

from helpers import JWTBearer

jwt_bearer = JWTBearer()

router = APIRouter(prefix="/v2/system", tags=["System"])

@router.get("/secure-endpoint/")
async def secure_endpoint(current_user: str = Depends(jwt_bearer)):
    return {"message": f"Hello {current_user}, this is a secure endpoint!"}
