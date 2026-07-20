from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models.auth import User
from auth_utils import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["Auth"])

# Esquema de validación para registro de usuario (pydantic - REQ-AUTH-01)
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role_id: int
    
# Endpoint temporal para registrar un nuevo usuario (REQ-AUTH-01)
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # 1. Verificar si el usuario ya existe
    exists = db.query(User).filter(User.email == user_in.email).first()
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El correo electrónico ya está en uso.")

    # 2. Crear el nuevo usuario con contraseña hasheada y rol asignado
    new_user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        role_id=user_in.role_id,
        is_2fa_enabled=False,  # Por defecto, 2FA deshabilitado
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Verificar si el usuario existe
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Correo o contraseña incorrectos."
        )
    
    # 2. Generar la data del token
    token_data = {"sub": user.email, "role_id": user.role_id}
    access_token = create_access_token(data=token_data)
    refresh_token = create_refresh_token(data=token_data)
    
    # 3. Guardar el Refresh Token en una Cookie HttpOnly y Secure (Protección XSS)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,  # Cambiar a False solo si estás probando en HTTP sin SSL local
        samesite="lax",
        max_age=7 * 24 * 60 * 60  # 7 días
    )
    
    # El Access Token va directo al frontend en el cuerpo de la respuesta
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh")
def refresh_session(request: Request, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No hay token de sesión activo.")
    
    payload = decode_token(refresh_token, expected_type="refresh")
    email = payload.get("sub")
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no válido.")
    
    # Emitir un Access Token nuevo por otros 15 minutos
    new_access_token = create_access_token(data={"sub": user.email, "role_id": user.role_id})
    return {"access_token": new_access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(response: Response):
    # Revocamos la sesión borrando la cookie HttpOnly
    response.delete_cookie(key="refresh_token", httponly=True, secure=True, samesite="lax")
    return {"detail": "Sesión cerrada de manera segura."}