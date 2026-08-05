# 📂 Estrutura do Projeto - Visão Completa

```
sistema-de-cadastro-e-jogos/
│
├── 📖 DOCUMENTAÇÃO
│   ├── README.md                 ← Começar aqui!
│   ├── QUICKSTART.md             ← Iniciar rápido
│   ├── DEVELOPMENT.md            ← Guia técnico detalhado
│   ├── DEPLOYMENT.md             ← Docker e deploy na nuvem
│   ├── TROUBLESHOOTING.md        ← FAQ e debugging
│   ├── ROADMAP.md                ← Futuro do projeto
│   └── STRUCTURE.md              ← Este arquivo
│
├── 🚀 SCRIPTS
│   ├── start.bat                 ← Iniciar (Windows)
│   ├── start.sh                  ← Iniciar (Linux/Mac)
│   └── docker-compose.yml        ← Iniciar tudo via Docker
│
├── 🔙 BACKEND (FastAPI + SQLite)
│   │
│   ├── main.py                   ← `python main.py` sobe o servidor de dev
│   ├── requirements.txt          ← Dependências Python (runtime)
│   ├── requirements-dev.txt      ← + pytest/httpx para testes
│   ├── Dockerfile
│   ├── .env                      ← Configurações (local)
│   ├── .env.example              ← Template .env
│   │
│   ├── tests/                    ← Testes automatizados (pytest)
│   │   ├── conftest.py           ← Fixtures (client, banco de testes)
│   │   ├── test_auth.py
│   │   └── test_notes.py
│   │
│   └── app/
│       │
│       ├── 🔐 core/
│       │   ├── __init__.py
│       │   ├── config.py         ← Configurações da app
│       │   └── security.py       ← JWT, hashing, auth
│       │
│       ├── 💾 database/
│       │   ├── __init__.py
│       │   └── database.py       ← SQLAlchemy setup
│       │
│       ├── 🗄️ models/
│       │   ├── __init__.py
│       │   ├── user.py           ← Modelo User ORM
│       │   └── note.py           ← Modelo Note ORM
│       │
│       ├── 📋 schemas/
│       │   ├── __init__.py
│       │   ├── user.py           ← Validação de User (Pydantic)
│       │   └── note.py           ← Validação de Note (Pydantic)
│       │
│       ├── ⚙️ services/
│       │   ├── __init__.py
│       │   ├── user_service.py   ← Lógica de User
│       │   └── note_service.py   ← Lógica de Note
│       │
│       ├── 🛣️ routes/
│       │   ├── __init__.py
│       │   ├── auth.py           ← Endpoints /auth/
│       │   └── notes.py          ← Endpoints /notes/
│       │
│       ├── 📊 main.py            ← FastAPI app principal (fonte da verdade)
│       └── __init__.py
│
├── 🎨 FRONTEND (React + Material UI)
│   │
│   ├── package.json              ← Dependências Node
│   ├── Dockerfile
│   ├── .env                      ← API URL (local)
│   ├── .env.example              ← Template .env
│   │
│   ├── public/
│   │   └── index.html            ← HTML principal
│   │
│   └── src/
│       │
│       ├── 📄 pages/
│       │   ├── Login.js           ← Página login
│       │   ├── Register.js        ← Página cadastro
│       │   └── Dashboard.js       ← Dashboard principal
│       │
│       ├── 🧩 components/
│       │   ├── Calculator.js      ← Componente Calculadora
│       │   ├── NoteBlock.js       ← Componente Notas
│       │   └── SnakeGame.js       ← Componente Jogo
│       │
│       ├── 🔐 context/
│       │   └── AuthContext.js     ← Estado de autenticação
│       │
│       ├── 🌐 services/
│       │   └── api.js             ← Cliente HTTP (axios)
│       │
│       ├── 🛠️ utils/
│       │   └── ProtectedRoute.js  ← Rota protegida
│       │
│       ├── index.js               ← Entrada React (main)
│       └── index.css              ← Estilos globais
│
└── 🔧 CONFIGURAÇÃO
    └── .gitignore                ← Arquivos ignorados git
```

---

## 📊 Fluxo de Dados

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Pages (Login, Register, Dashboard)                     │
│           ↓                        ↓                    │
│  Components (Calculator, Notes, Snake)                  │
│           ↓                        ↓                    │
│  Services/API (axios client)                            │
│           ↓                        ↓                    │
│  Context (AuthContext)            HTTP                  │
│           ↓                        ↓                    │
└─────────────────┬──────────────────┬────────────────────┘
                  │                  │
                  ↓ JWT Token        ↓
┌─────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI)                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Routes (auth.py, notes.py) ← Endpoints HTTP            │
│        ↓                ↓                                │
│  Services ← Lógica de negócio                           │
│        ↓                ↓                                │
│  Models (User, Note) ← SQLAlchemy ORM                   │
│        ↓                ↓                                │
│  Database (SQLite)                                      │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🗂️ Hierarquia de Camadas - Backend

```
┌─────────────────────────────────┐
│  Routes (API Endpoints)         │  ← HTTP requests/responses
├─────────────────────────────────┤
│  Services (Business Logic)      │  ← Core da aplicação
├─────────────────────────────────┤
│  Models (Database Layer)        │  ← SQLAlchemy ORM
├─────────────────────────────────┤
│  Schemas (Validation)           │  ← Pydantic validation
├─────────────────────────────────┤
│  Core (Security/Config)         │  ← JWT, configs, DB setup
├─────────────────────────────────┤
│  Database (SQLite)              │  ← Storage final
└─────────────────────────────────┘
```

---

## 🎯 Matriz de Responsabilidades

| Camada | Responsável | Arquivo | O que faz |
|--------|-------------|---------|-----------|
| Route | auth.py | POST /auth/register | Recebe requisição HTTP |
| Schema | user.py | UserCreate | Valida dados de entrada |
| Service | user_service.py | create_user() | Implementa lógica |
| Model | user.py | User class | Define estrutura BD |
| Database | database.py | SessionLocal | Persiste dados |

---

## 📡 Fluxo de Autenticação

```
1. Registro:
   Usuário → Frontend (Register.js)
           → POST /auth/register
           → Backend (auth.py)
           → UserService.create_user()
           → Model User criado
           → Database persiste
           → Frontend → Login

2. Login:
   Usuário → Frontend (Login.js)
          → POST /auth/login
          → Backend valida credenciais
          → JWT gerado
          → Frontend armazena token
          → Redirect Dashboard

3. Acesso Protegido:
   Frontend → ProtectedRoute.js
           → Verifica se tem token
           → Se não, redirect Login
           → Se tem, envia em header
           → Backend valida JWT
           → get_current_user()
           → Request autorizado
```

---

## 🧭 Como Navegar no Projeto

### Para entender o fluxo de Login:
1. `frontend/src/pages/Login.js` - UI
2. `frontend/src/context/AuthContext.js` - chamada à API
3. `frontend/src/services/api.js` - HTTP request
4. `backend/app/routes/auth.py` - endpoint
5. `backend/app/services/user_service.py` - lógica

### Para adicionar nova funcionalidade:
1. `backend/app/models/` - criar modelo
2. `backend/app/schemas/` - criar schema de validação
3. `backend/app/services/` - criar lógica
4. `backend/app/routes/` - criar endpoints
5. `frontend/src/services/api.js` - adicionar chamada HTTP
6. `frontend/src/components/` - criar componente UI
7. `frontend/src/pages/Dashboard.js` - integrar aba

---

## 📚 Recursos por Funcionalidade

### Calculadora
- `frontend/src/components/Calculator.js` - Componente
- Lógica pura (sem backend)

### Notas
- Backend: `backend/app/routes/notes.py` + `services/note_service.py`
- Frontend: `frontend/src/components/NoteBlock.js` + `services/api.js`
- Database: `Note` model em `models/note.py`

### Jogo da Cobrinha
- `frontend/src/components/SnakeGame.js` - Componente
- Lógica pura (sem backend)

---

## 🔍 Localizar Informações

| Preciso de... | Vá para... |
|---|---|
| Entender fluxo geral | [README.md](README.md) |
| Começar rápido | [QUICKSTART.md](QUICKSTART.md) |
| Detalhes técnicos | [DEVELOPMENT.md](DEVELOPMENT.md) |
| Erro/problema | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |
| Planos futuros | [ROADMAP.md](ROADMAP.md) |
| Estrutura do projeto | Este arquivo |
| Configurar ambiente | `backend/.env` ou `frontend/.env` |
| Rodar projeto | `start.bat` ou `start.sh` |

---

**Última atualização**: 2024
