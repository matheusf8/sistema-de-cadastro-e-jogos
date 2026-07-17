# Iniciar aplicação (Windows)

echo Iniciando Sistema de Cadastro e Funcionalidades...

# Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Erro: Python não encontrado. Por favor, instale Python 3.8 ou superior.
    pause
    exit /b 1
)

# Verificar se Node.js está instalado
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Erro: Node.js não encontrado. Por favor, instale Node.js 14 ou superior.
    pause
    exit /b 1
)

echo.
echo Instalando dependências do backend...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Erro ao instalar dependências do backend
    pause
    exit /b 1
)

echo.
echo Iniciando backend em uma nova janela...
start cmd /k "python main.py"

cd ..

echo.
echo Aguardando 3 segundos...
timeout /t 3

echo Instalando dependências do frontend...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo Erro ao instalar dependências do frontend
    pause
    exit /b 1
)

echo.
echo Iniciando frontend em uma nova janela...
start cmd /k "npm start"

cd ..

echo.
echo Aplicação iniciada com sucesso!
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo Documentação API: http://localhost:8000/docs
echo.
echo Pressione Enter para fechar esta janela...
pause
