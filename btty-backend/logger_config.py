# import logging
# import os

# os.makedirs(LOG_DIR, exist_ok=True)

# # Asegurar que exista la carpeta de logs
# LOG_DIR = "logs"
# if not os.path.exists(LOG_DIR):
#     os.makedirs(LOG_DIR)

# LOG_FILE = os.path.join(LOG_DIR, "security.log")

# # Configuración del logger de seguridad
# logger = logging.getLogger("security_logger")
# logger.setLevel(logging.INFO)

# file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")

# # Formato del log: Fecha/Hora - Nivel - Mensaje
# formatter = logging.Formatter(
#     "[%(asctime)s] %(levelname)s - %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S"
# )

# # Handler para escribir en archivo .log
# file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
# file_handler.setFormatter(formatter)

# # Handler para mostrar también en consola
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(formatter)

# # Evitar duplicados de handlers si se recarga la app
# if not logger.handlers:
#     logger.addHandler(file_handler)
#     logger.addHandler(console_handler)

import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("security_logger")
logger.setLevel(logging.DEBUG)  

formatter = logging.Formatter(
    "%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler = logging.FileHandler("logs/security_classified.log", encoding="utf-8")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

if not logger.handlers:
    logger.addHandler(file_handler)