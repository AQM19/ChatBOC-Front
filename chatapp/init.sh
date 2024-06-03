#!/bin/bash

# Función para detectar el sistema operativo
detect_os() {
    case "$OSTYPE" in
        linux*)   echo "Linux" ;;
        msys*)    echo "Windows" ;;
        cygwin*)  echo "Windows" ;;
        *)        echo "unknown" ;;
    esac
}

OS=$(detect_os)

# Creación del entorno virtual y su gestión
echo '**************************************************************************************************'
echo Creando entorno virtual
echo '**************************************************************************************************'

if [ "$OS" = "Linux" ]; then
    python3 -m venv .venv
    source .venv/bin/activate
elif [ "$OS" = "Windows" ]; then
    python -m venv .venv
    source .venv/Scripts/activate
else
    echo "Sistema operativo no soportado."
    exit 1
fi

pip install -r requirements.txt

# Inicio de la api
echo '**************************************************************************************************'
echo Iniciando la aplicacion
echo '**************************************************************************************************'


reflex run
