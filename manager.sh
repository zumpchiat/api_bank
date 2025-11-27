#!/bin/bash

if [ -z "$1" ]; then
    echo "Uso: $0 informe o nome do App"
    exit 1
fi

echo -e "Criando app estrutural com nome: $1"
echo -e "Diretório base: ./src/$1"

mkdir -p "./src/$1"
touch "./src/$1/__init__.py"
touch "./src/$1/controller.py"
touch "./src/$1/models.py"
touch "./src/$1/schemas.py"





echo -e " Diretórios MVC/estruturais criados com sucesso em ./src/$1"
