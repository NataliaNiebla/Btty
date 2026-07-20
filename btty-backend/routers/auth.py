from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr

from database import get_db, db_log_event
from models.auth import User
from auth_utils import verify_password, hash_password, create_access_token, decode_token, sanitize_sensitive_data
from logger_config import logger
from dependencies import get_current_user, require_role

router = APIRouter(prefix="/auth", tags=["Auth"])

# Este es un diccionario para llevar el conteo de intentos fallidos por correo electrónico
failed_attempts_counter = {}  

# Esquema Pydantic para el registro de usuario
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role_id: int | None = None
    
# Esquema Pydantic para la actualización de perfíl
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    role_id: int | None = None

# Endpoint - Registro de usuario
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    logger.debug(f"Procesando intento de registro para: {user_data.email}")
    # Verificar si el usuario ya existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        logger.warning(f"INTENTO DE REGISTRO FALLIDO - Correo ya registrado: {user_data.email}")
    # if existing_user:
    #     logger.error(f"ERROR DE REGISTRO - Correo ya registrado: {user_data.email}") # Cambiar de warning a error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )
    
    try:
        hashed_pwd = hash_password(user_data.password)
        new_user = User(
            email=user_data.email,
            hashed_password=hashed_pwd,
            role_id=user_data.role_id
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Log de nivel INFO (Operación exitosa)
        logger.info(f"USUARIO REGISTRADO - ID: {new_user.id} | Email: {new_user.email}")
        
        db_log_event(
            db=db,
            action="REGISTRO_USUARIO",
            user_id=new_user.id,
            resource_id=f"Correo registrado: {new_user.email} | Role ID: {new_user.role_id}"
        )
        
        return {"message": "Usuario creado con éxito. Ya puedes iniciar sesión."}
    
    except Exception as e:
        # Log de nivel ERROR (Excepción en el servidor o BD)
        logger.error(f"ERROR AL REGISTRAR USUARIO - Excepción: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al registrar el usuario"
        )

# Endpoint - inicio de sesión
# @router.post("/login")
# def login(
#     request: Request, 
#     response: Response, 
#     form_data: OAuth2PasswordRequestForm = Depends(), 
#     db: Session = Depends(get_db)):
#     client_ip = request.client.host
#     username = form_data.username

#     user = db.query(User).filter(User.email == username).first()

#     # Si el usuario no existe, o la contraseña es incorrecta, incrementamos el contador de intentos fallidos
#     if not user:
#         # Incrementar contador para este correo
#         failed_attempts_counter[username] = failed_attempts_counter.get(username, 0) + 1
#         attempts = failed_attempts_counter[username]
#         reason = "Usuario no registrado"
        
#         logger.warning(
#             f"INTENTO FALLIDO - Usuario: {username} | "
#             f"Motivo: {reason} | "
#             f"Intentos acumulados: {attempts} | "
#             f"IP: {client_ip}"
#         )
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Credenciales incorrectas"
#         )

#     if not verify_password(form_data.password, user.hashed_password):
#         # Incrementar contador para este usuario
#         failed_attempts_counter[username] = failed_attempts_counter.get(username, 0) + 1
#         attempts = failed_attempts_counter[username]
#         reason = "Contraseña incorrecta"
        
#         logger.warning(
#             f"INTENTO FALLIDO - Usuario: {username} | "
#             f"Motivo: {reason} | "
#             f"Intentos acumulados: {attempts} | "
#             f"IP: {client_ip}"
#         )
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Credenciales incorrectas"
#         )

#     # Si el inicio de sesión es exitoso, reiniciar el contador de intentos
#     failed_attempts_counter[username] = 0
    
#     logger.info(f"LOGIN EXITOSO - Usuario: {user.email} (ID: {user.id}) | IP: {client_ip}")
    
#     access_token = create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login")
def login(
    request: Request, 
    response: Response, 
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    client_ip = request.client.host
    username = form_data.username
    raw_password = form_data.password # Datos sensibles
    user_agent_str = request.headers.get("user-agent")
    
    logger.debug(f"Iniciando flujo de autenticación para usuario: {username} desde IP: {client_ip}")
    
    user = db.query(User).filter(User.email == username).first()

    if not user or not verify_password(raw_password, user.hashed_password):
        failed_attempts_counter[username] = failed_attempts_counter.get(username, 0) + 1
        attempts = failed_attempts_counter[username]
        
        # LOG INSEGURO (EXPONE CONTRASEÑA EN TEXTO PLANO)
        # logger.warning(
        #     f"[INSEGURO] LOGIN FALLIDO - Usuario: {username} | "
        #     f"Clave enviada: {raw_password} | "
        #     f"Intentos: {attempts} | IP: {client_ip}"
        # )
        
        # LOG SEGURO (PROTEGE LA CONTRASEÑA)
        # safe_password = sanitize_sensitive_data(raw_password)
        # logger.warning(
        #     f"[SEGURO] INTENTO FALLIDO - Usuario: {username} | "
        #     f"Clave enviada: {safe_password} | "
        #     f"Intentos: {attempts} | IP: {client_ip}"
        # )
        
        safe_password = sanitize_sensitive_data(raw_password)
        
        # Log nivel WARNING (Alerta de seguridad)
        logger.warning(
            f"LOGIN FALLIDO - Usuario: {username} | "
            f"Clave enviada: {safe_password} | "
            f"Intentos acumulados: {attempts} | IP: {client_ip}"
        )
        
        # Persistencia en la base de datos para auditoría
        db_log_event(
            db=db,
            action="[WARNING] INTENTO_LOGIN_FALLIDO",
            user_id=user.id if user else None,
            resource_id=f"Intento #{attempts} con correo: {username}",
            ip_address=client_ip,
            user_agent=user_agent_str
        )
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    # Login exitoso: reiniciar contador de intentos fallidos
    failed_attempts_counter[username] = 0
    access_token = create_access_token(data={"sub": user.email})
    
    safe_token = sanitize_sensitive_data(access_token)
    safe_cookie = f"access_token={safe_token}; HttpOnly; Secure"
    
    logger.info(
        f"LOGIN EXITOSO - Usuario: {user.email} (ID: {user.id}) | "
        f"Token: {safe_token} | Cookie: {safe_cookie} | IP: {client_ip}"
    )
    
    db_log_event(
        db=db,
        action="LOGIN_EXITOSO",
        user_id=user.id,
        resource_id=f"Inicio de sesión exitoso. Token enmascarado: {safe_token}",
        ip_address=client_ip,
        user_agent=user_agent_str
    )

    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint - cierre de sesión
@router.post("/logout")
def logout(
    request: Request, 
    response: Response, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    client_ip = request.client.host
    response.delete_cookie("access_token")
    
    user = db.query(User).filter(User.email == current_user).first()
    
    # REGISTRO: Cierre de Sesión en archivo de auditoría y bd
    logger.info(f"LOGOUT EXITOSO - Usuario: {current_user} desde IP: {client_ip}")
    
    db_log_event(
        db=db,
        action="[INFO] LOGOUT_EXITOSO",
        user_id=user.id if user else None,
        resource_id=f"Sesión cerrada para {current_user}",
        ip_address=client_ip,
        user_agent=request.headers.get("user-agent")
    )
    
    return {"message": "Sesión cerrada correctamente"}

# Endpoint - Ruta protegida 
@router.get("/protected-route")
def protected_route(
    request: Request, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    client_ip = request.client.host
    user = db.query(User).filter(User.email == current_user).first()
    
    # REGISTRO: Acceso concedido a ruta restringida
    logger.debug(f"Verificando token y credenciales para acceso a {request.url.path}")
    logger.info(f"ACCESO PERMITIDO - Usuario: {current_user} accedió a {request.url.path} desde IP: {client_ip}")
    
    db_log_event(
        db=db,
        action="[INFO] ACCESO_RUTA_PROTEGIDA",
        user_id=user.id if user else None,
        resource_id=f"Ruta accesada: {request.url.path}",
        ip_address=client_ip,
        user_agent=request.headers.get("user-agent")
    )
    
    return {"message": f"Bienvenido {current_user}, esta es una ruta protegida."}

# Endpoint - actualización de perfil
@router.put("/profile")
def update_profile(
    user_data: UserUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    client_ip = request.client.host
    user_agent_str = request.headers.get("user-agent")
    
    logger.debug(f"Evaluando payload de actualización para: {current_user}")
    
    # 1. Obtener el usuario actual de la base de datos
    user = db.query(User).filter(User.email == current_user).first()
    
    if not user:
        logger.warning(f"Intento de actualización sobre usuario inexistente: {current_user}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Convertimos los datos enviados a diccionario, excluyendo lo que no se envió (None)
    update_dict = user_data.model_dump(exclude_unset=True)
    
    if not update_dict:
        logger.debug("No se enviaron campos diferentes para actualizar")
        return {"message": "No se enviaron campos para actualizar"}

    changes_logged = []
    
    try:
        for field, new_value in update_dict.items():
            old_value = getattr(user, field)
            
            if old_value != new_value:
                setattr(user, field, new_value)
                
                # Log nivel INFO
                logger.info(
                    f"AUDITORÍA CAMBIO PERFIL - Usuario: {current_user} | "
                    f"Campo: {field} | Valor Anterior: '{old_value}' | "
                    f"Valor Nuevo: '{new_value}' | IP: {client_ip}"
                )
                
                db_log_event(
                    db=db,
                    action=f"CAMBIO_PERFIL_{field.upper()}",
                    user_id=user.id,
                    resource_id=f"Campo '{field}' modificado. Anterior: '{old_value}' -> Nuevo: '{new_value}'",
                    ip_address=client_ip,
                    user_agent=user_agent_str
                )
                
                changes_logged.append({
                    "campo": field,
                    "valor_anterior": old_value,
                    "valor_nuevo": new_value
                })

        db.commit()
        db.refresh(user)

        return {
            "message": "Perfil actualizado correctamente",
            "cambios_registrados": changes_logged
        }
    except Exception as e:
        db.rollback()
        # Log nivel ERROR
        logger.error(f"ERROR AL ACTUALIZAR PERFIL - Usuario: {current_user} | Excepción: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al actualizar el perfil"
        )
    
# Endpoint - por rol de usuario (ejemplo de rutas protegidas por roles)
# 1. Ruta accesible para Pacientes, Psicólogos y Admins (Roles 1, 2, 3)
@router.get("/patient-dashboard")
def patient_dashboard(
    request: Request, 
    user: User = Depends(require_role([1, 2, 3]))
):
    logger.info(f"[ACCESO PERMITIDO] Área de Pacientes accesada por: {user.email}")
    return {"message": f"Bienvenido al portal de pacientes, {user.email}"}


# 2. Ruta accesible SOLO para Psicólogos y Admins (Roles 1, 2)
@router.get("/psychologist-dashboard")
def psychologist_dashboard(
    request: Request, 
    user: User = Depends(require_role([1, 2]))
):
    logger.info(f"[ACCESO PERMITIDO] Panel Clínico accesado por: {user.email}")
    return {"message": f"Bienvenido al panel clínico de psicólogos, {user.email}"}


# 3. Ruta EXCLUSIVA para Administradores (Rol 1)
@router.get("/admin-dashboard")
def admin_dashboard(
    request: Request, 
    user: User = Depends(require_role([1]))
):
    logger.info(f"[ACCESO PERMITIDO] Panel de Administración accesado por: {user.email}")
    return {"message": f"Bienvenido al Panel de Control de Administrador, {user.email}"}
