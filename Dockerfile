# Usamos la versión de Python que tienes en local, en su variante 'slim' para que la imagen sea ligera.
FROM python:3.10.12-slim

# Evita que Python escriba archivos .pyc en el disco (ahorra espacio y mejora rendimiento)
ENV PYTHONDONTWRITEBYTECODE=1

# Evita que Python haga buffer en la salida estándar, permitiendo ver los logs en tiempo real en Docker
ENV PYTHONUNBUFFERED=1

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Actualizar repositorios e instalar dependencias del sistema para mysqlclient
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiamos el archivo de requerimientos primero para aprovechar la caché de Docker
COPY requirements.txt /app/

# Instalamos las dependencias, agregando gunicorn explícitamente, y evitamos guardar la caché de pip
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copiamos el resto del código del proyecto al contenedor
COPY . /app/

# Exponemos el puerto internamente
EXPOSE 8000

# Ejecuta collectstatic para reunir los archivos antes de arrancar
RUN python manage.py collectstatic --noinput

# Comando para levantar la aplicación con Gunicorn
# IMPORTANTE: Cambia "nombre_de_tu_proyecto" por la carpeta donde está tu archivo wsgi.py
CMD ["gunicorn", "Inmunolife.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--access-logfile","-"] 
# Ajustar el nombre del proyecto antes de .wsgi y el puerto que este libre en el vps
