from fastapi import APIRouter, Depends, HTTPException
from helpers import JWTBearer, configure_firebase, get_current_active_user
from schema import User

router = APIRouter(prefix="/v2/auth", tags=["Manage User"])

jwt_bearer = JWTBearer()


@router.get("/users/list")
async def get_users(
        token: str = Depends(jwt_bearer),
):
    db = configure_firebase()
    try:
        users = db.stream()
        # Konversi setiap dokumen ke dictionary
        all_users = [user.to_dict() for user in users]

        if not all_users:
            raise HTTPException(status_code=404, detail="Tidak ada data pengguna yang ditemukan.")

        return {"users": all_users}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kesalahan server: {e}")


@router.get("/users/profile")
async def get_profile(
        token: str = Depends(jwt_bearer),
        current_user: dict = Depends(get_current_active_user)
):
    """
    Mendapatkan profil pengguna berdasarkan JWT token.
    """
    db = configure_firebase()
    email = current_user.get('sub')
    try:
        # Ambil data pengguna dari Firestore
        user_doc = db.document(email).get()

        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="Pengguna tidak ditemukan.")

        return user_doc.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kesalahan server: {e}")


@router.put("/users/profile")
async def update_profile(
        profile: User,
        token: str = Depends(jwt_bearer),
        current_user: dict = Depends(get_current_active_user)
):
    """
    Memperbarui profil pengguna berdasarkan JWT token.
    """
    db = configure_firebase()
    email = current_user.get('sub')
    try:
        # Perbarui data pengguna di Firestore
        user_ref = db.document(email)
        user_doc = user_ref.get()

        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="Pengguna tidak ditemukan.")

        # Perbarui data pengguna
        user_ref.update(profile.dict())
        return {"message": "Profil berhasil diperbarui."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kesalahan server: {e}")
