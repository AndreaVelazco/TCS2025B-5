#!/bin/bash

# Esperar a que PostgreSQL esté listo
echo "Esperando a PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL está listo"

# Ejecutar migraciones
echo "Ejecutando migraciones..."
python manage.py migrate --noinput

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Crear superusuario si no existe
echo "Verificando superusuario..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(correo='admin@gmail.com').exists():
    User.objects.create_superuser(correo='admin@gmail.com', nombre='Admin', password='admin123')
    print('✓ Superusuario creado: admin@gmail.com')
else:
    print('✓ Superusuario ya existe: admin@gmail.com')
END

# Iniciar Gunicorn
echo "Iniciando Gunicorn..."
exec gunicorn minitest.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
