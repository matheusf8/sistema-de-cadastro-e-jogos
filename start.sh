#!/bin/bash

# Iniciar aplicação (Linux/Mac)

echo "Iniciando Sistema de Cadastro e Funcionalidades..."

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Erro: Python não encontrado. Por favor, instale Python 3.8 ou superior."
    exit 1
fi

# Verificar se Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "Erro: Node.js não encontrado. Por favor, instale Node.js 14 ou superior."
    exit 1
fi

echo ""
echo "Instalando dependências do backend..."
cd backend
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Erro ao instalar dependências do backend"
    exit 1
fi

echo ""
echo "Iniciando backend em background..."
python main.py &
BACKEND_PID=$!

cd ..

echo ""
echo "Aguardando 3 segundos..."
sleep 3

echo "Instalando dependências do frontend..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "Erro ao instalar dependências do frontend"
    kill $BACKEND_PID
    exit 1
fi

echo ""
echo "Iniciando frontend..."
npm start

# Matar backend quando frontend encerrar
kill $BACKEND_PID 2>/dev/null

echo ""
echo "Aplicação encerrada."
