from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from auth_utils import SECRET_KEY, ALGORITHM
from logger_config import logger

# auto_error=False permite que la función capture cuando NO envían token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    client_ip = request.client.host
    endpoint = request.url.path
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales no válidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Si no envió el token en la petición
    if not token:
        logger.warning(f"ACCESO RESTRINGIDO DENEGADO - Intento sin token desde IP: {client_ip} en ruta: {endpoint}")
        raise credentials_exception

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            logger.warning(f"ACCESO RESTRINGIDO DENEGADO - Token sin 'sub' desde IP: {client_ip} en ruta: {endpoint}")
            raise credentials_exception
        return email
    except JWTError:
        # REGISTRO: Acceso a ruta restringida fallido
        logger.warning(f"ACCESO RESTRINGIDO DENEGADO - Token inválido o expirado desde IP: {client_ip} en ruta: {endpoint}")
        raise credentials_exception