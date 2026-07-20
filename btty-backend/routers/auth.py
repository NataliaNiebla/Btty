from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr

from database import get_db
from models.auth import User
from auth_utils import verify_password, hash_password, create_access_token, decode_token
from logger_config import logger
from dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

# Este es un diccionario para llevar el conteo de intentos fallidos por correo electrónico
# Estructura: {"correo@ejemplo.com": numero_de_intentos}
failed_attempts_counter = {}  

# Esquema Pydantic para el registro de usuario
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role_id: int | None = None

# Endpoint - registro de usuario
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )
    
    # Hashear contraseña y crear nuevo usuario
    hashed_pwd = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pwd,
        role_id=user_data.role_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "Usuario creado con éxito. Ya puedes iniciar sesión."}

# Endpoint - inicio de sesión
@router.post("/login")
def login(
    request: Request, 
    response: Response, 
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)):
    client_ip = request.client.host
    username = form_data.username

    user = db.query(User).filter(User.email == username).first()

    # Si el usuario no existe, o la contraseña es incorrecta, incrementamos el contador de intentos fallidos
    if not user:
        # Incrementar contador para este correo
        failed_attempts_counter[username] = failed_attempts_counter.get(username, 0) + 1
        attempts = failed_attempts_counter[username]
        reason = "Usuario no registrado"
        
        logger.warning(
            f"INTENTO FALLIDO - Usuario: {username} | "
            f"Motivo: {reason} | "
            f"Intentos acumulados: {attempts} | "
            f"IP: {client_ip}"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    if not verify_password(form_data.password, user.hashed_password):
        # Incrementar contador para este usuario
        failed_attempts_counter[username] = failed_attempts_counter.get(username, 0) + 1
        attempts = failed_attempts_counter[username]
        reason = "Contraseña incorrecta"
        
        logger.warning(
            f"INTENTO FALLIDO - Usuario: {username} | "
            f"Motivo: {reason} | "
            f"Intentos acumulados: {attempts} | "
            f"IP: {client_ip}"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    # Si el inicio de sesión es exitoso, reiniciar el contador de intentos
    failed_attempts_counter[username] = 0
    
    logger.info(f"LOGIN EXITOSO - Usuario: {user.email} (ID: {user.id}) | IP: {client_ip}")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint - cierre de sesión
@router.post("/logout")
def logout(request: Request, response: Response, current_user: str = Depends(get_current_user)):
    client_ip = request.client.host
    response.delete_cookie("access_token")
    
    # REGISTRO: Cierre de Sesión
    logger.info(f"LOGOUT EXITOSO - Usuario: {current_user} desde IP: {client_ip}")
    return {"message": "Sesión cerrada correctamente"}

# Endpoint - ruta protegida 
@router.get("/protected-route")
def protected_route(request: Request, current_user: str = Depends(get_current_user)):
    client_ip = request.client.host
    # REGISTRO: Acceso concedido a ruta restringida
    logger.info(f"ACCESO RESTRINGIDO PERMITIDO - Usuario: {current_user} accedió a {request.url.path} desde IP: {client_ip}")
    return {"message": f"Bienvenido {current_user}, esta es una ruta protegida."}