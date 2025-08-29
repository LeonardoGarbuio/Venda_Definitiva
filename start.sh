#!/bin/bash

echo "🚀 === INICIANDO SETUP DO RENDER ==="

# 1. Executa migrações
echo "📋 Executando migrações..."
python manage.py migrate

# 2. Executa setup personalizado
echo "🔧 Executando setup personalizado..."
python setup_render.py

# 3. Coleta arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# 4. Inicia o servidor
echo "🌐 Iniciando servidor..."
gunicorn delivery_system.wsgi:application --bind 0.0.0.0:$PORT
