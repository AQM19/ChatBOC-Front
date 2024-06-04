#!/bin/bash

detect_os() {
    case "$OSTYPE" in
        linux*)   echo "Linux" ;;
        msys*)    echo "Windows" ;;
        cygwin*)  echo "Windows" ;;
        *)        echo "unknown" ;;
    esac
}

OS=$(detect_os)

echo '**************************************************************************************************'
echo Iniciando la aplicacion
echo '**************************************************************************************************'

cd chatapp

if [ "$OS" = "Linux" ]; then
    source .venv/bin/activate
elif [ "$OS" = "Windows" ]; then
    source .venv/Scripts/activate
else
    echo "Sistema operativo no soportado."
    exit 1
fi

reflex run