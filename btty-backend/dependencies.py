from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from database import get_db
from models.auth import User
from auth_utils import SECRET_KEY, ALGORITHM, sanitize_sensitive_data
from logger_config import logger

# auto_error=False permite que la función capture cuando NO envían token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    client_ip = request.client.host
    endpoint = request.url.path
    
    # Definir la excepción de credenciales no válidas
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales no válidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        logger.warning(f"ACCESO RESTRINGIDO DENEGADO - Intento sin token desde IP: {client_ip} en ruta: {endpoint}")
        raise credentials_exception
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            safe_token = sanitize_sensitive_data(token)
            logger.warning(f"[SEGURO] TOKEN RECHAZADO - Sin campo 'sub' | Token: {safe_token} | IP: {client_ip}")
            raise credentials_exception
            
        return email

    except JWTError:
        # Comparación de validación de token (Práctica 3)
        # Inseguro: Muestra el token íntegro expirado o malformado
        logger.warning(f"[INSEGURO] TOKEN RECHAZADO - Token completo: {token} desde IP: {client_ip} en ruta: {endpoint}")
        
        # Seguro: Muestra solo una versión enmascarada del token
        safe_token = sanitize_sensitive_data(token)
        logger.warning(f"[SEGURO] TOKEN RECHAZADO - Token Enmascarado: {safe_token} desde IP: {client_ip} en ruta: {endpoint}")
        
        raise credentials_exception


# Decorador para recibir roles permitidos y verificar el nivel de acceso (Práctica 5)
def require_role(allowed_roles: list[int]):
    def role_checker(
        request: Request,
        current_user_email: str = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        client_ip = request.client.host
        endpoint = request.url.path
        
        # Buscar usuario en la BD para obtener su role_id
        user = db.query(User).filter(User.email == current_user_email).first()
        
        # Si el usuario no tiene rol asignado, asumimos 3 (Paciente)
        user_role_id = user.role_id if (user and user.role_id) else 3
        
        # Mapa exacto según la tabla catalog de tu base de datos
        role_names = {
            1: "Administrador",
            2: "Psicólogo",
            3: "Paciente"
        }
        current_role_name = role_names.get(user_role_id, "Desconocido")
        
        # SI EL ROL DEL USUARIO NO ESTÁ PERMITIDO
        if user_role_id not in allowed_roles:
            expected_roles_names = [role_names.get(r, str(r)) for r in allowed_roles]
            
            # --- REGISTRO DE ACCESO NO AUTORIZADO POR ROL ---
            logger.warning(
                f"[ACCESO NO AUTORIZADO] Usuario: {current_user_email} | "
                f"Rol Actual: {current_role_name} (ID: {user_role_id}) | "
                f"Roles Requeridos: {expected_roles_names} | "
                f"Ruta Solicitada: {endpoint} | IP: {client_ip}"
            )
            
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos suficientes para acceder a este recurso"
            )
            
        return user

    return role_checker