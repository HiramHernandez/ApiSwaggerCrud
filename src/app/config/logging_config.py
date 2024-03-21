import logging

# Configurar el nivel de registro
logging.basicConfig(level=logging.INFO)

# Configurar el formato de registro
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Crear un manejador para escribir en un archivo
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)

# Añadir el manejador al registro
logging.getLogger().addHandler(file_handler)
