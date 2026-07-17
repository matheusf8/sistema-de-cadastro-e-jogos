# 📖 Guia Completo de Desenvolvimento

## 🎯 Visão Geral do Projeto

Este é um sistema completo de gerenciamento de usuários e funcionalidades, construído com:
- **Backend**: FastAPI com autenticação JWT e SQLite
- **Frontend**: React com Material UI
- **Autenticação**: JWT (JSON Web Tokens)
- **Banco de Dados**: SQLite3

## 🏗️ Arquitetura em Camadas

### Backend

```
┌─────────────────────────────────────────┐
│       Routes (auth.py, notes.py)        │  ← Endpoints da API
├─────────────────────────────────────────┤
│      Services (user_service, note)      │  ← Lógica de negócio
├─────────────────────────────────────────┤
│      Models (User, Note) + Database     │  ← Persistência de dados
├─────────────────────────────────────────┤
│  Core (Security, Config, Database)      │  ← Configurações e segurança
└─────────────────────────────────────────┘
```

### Frontend

```
┌──────────────────────────────────────────┐
│   Pages (Login, Register, Dashboard)     │  ← Telas principais
├──────────────────────────────────────────┤
│ Components (Calculator, NoteBlock, etc)  │  ← Componentes reutilizáveis
├──────────────────────────────────────────┤
│  Context (AuthContext) + Services (API)  │  ← Estado global e HTTP
├──────────────────────────────────────────┤
│      Utils (ProtectedRoute, etc)         │  ← Utilitários
└──────────────────────────────────────────┘
```

## 🔐 Fluxo de Autenticação

### 1. Registro
```
[Usuário preenche formulário] 
         ↓
[Frontend envia POST /auth/register]
         ↓
[Backend valida dados]
         ↓
[Backend cria usuário com senha criptografada]
         ↓
[Usuário é redirecionado para login]
```

### 2. Login
```
[Usuário entra username/senha]
         ↓
[Frontend envia POST /auth/login]
         ↓
[Backend verifica credenciais]
         ↓
[Backend gera JWT token]
         ↓
[Token é armazenado no localStorage]
         ↓
[Usuário é redirecionado para dashboard]
```

### 3. Acesso Protegido
```
[Usuário acessa rota protegida]
         ↓
[Frontend verifica se tem token]
         ↓
[Se não tem, redireciona para login]
         ↓
[Se tem, envia token no header Authorization]
         ↓
[Backend valida token]
         ↓
[Se válido, processa requisição]
```

## 📝 Fluxo de Dados - Notas

### Criar Nota
```
Frontend:
  1. Usuário preenche formulário (title, content)
  2. Clica em "Salvar"
  3. Frontend envia POST /notes/
  
Backend:
  1. Valida dados com schema NoteCreate
  2. Obtém user_id do token JWT
  3. NoteService.create_note() cria a nota
  4. Retorna NoteResponse
  
Frontend:
  1. Atualiza lista de notas
  2. Fecha dialog
```

### Listar Notas
```
Frontend:
  1. Componente carrega ao montar
  2. Envia GET /notes/?skip=0&limit=100
  
Backend:
  1. Obtém user_id do token
  2. NoteService.get_user_notes() filtra por user_id
  3. Retorna lista de NoteResponse
  
Frontend:
  1. Mapeia resposta e renderiza
```

### Atualizar Nota
```
Frontend:
  1. Usuário clica edit em uma nota
  2. Dialog abre com dados preenchidos
  3. Envia PUT /notes/{id}
  
Backend:
  1. Valida se nota pertence ao usuário
  2. NoteService.update_note() atualiza
  3. Retorna NoteResponse atualizada
```

### Deletar Nota
```
Frontend:
  1. Usuário clica delete
  2. Confirma em dialog
  3. Envia DELETE /notes/{id}
  
Backend:
  1. Valida se nota pertence ao usuário
  2. NoteService.delete_note() deleta
  3. Retorna 204 No Content
```

## 🛠️ Como Adicionar Uma Nova Funcionalidade

### Exemplo: Adicionar Feature de Tags nas Notas

#### 1. Backend - Adicionar modelo
```python
# backend/app/models/tag.py
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from app.database.database import Base

# Tabela de associação
note_tags = Table(
    'note_tags',
    Base.metadata,
    Column('note_id', Integer, ForeignKey('notes.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
```

#### 2. Backend - Atualizar modelo de Note
```python
# Adicionar no modelo Note
tags = relationship("Tag", secondary=note_tags)
```

#### 3. Backend - Criar schema
```python
# backend/app/schemas/tag.py
from pydantic import BaseModel

class TagResponse(BaseModel):
    id: int
    name: str
```

#### 4. Backend - Criar service
```python
# backend/app/services/tag_service.py
class TagService:
    @staticmethod
    def create_tag(db, name, user_id):
        # implementar
        pass
```

#### 5. Backend - Criar rota
```python
# backend/app/routes/tags.py
@router.post("/tags/", response_model=TagResponse)
def create_tag(tag_data: TagCreate, ...):
    # implementar
    pass
```

#### 6. Frontend - Atualizar componente
```javascript
// frontend/src/components/NoteBlock.js
// Adicionar tag multi-select no formulário
```

#### 7. Frontend - Atualizar API
```javascript
// frontend/src/services/api.js
export const tagsAPI = {
    createTag: (name) => api.post('/tags/', { name }),
    // etc
}
```

## 📊 Banco de Dados - Schema

### Tabela: users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    hashed_password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT NOW,
    updated_at DATETIME DEFAULT NOW
);
```

### Tabela: notes
```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT NOW,
    updated_at DATETIME DEFAULT NOW,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## 🔒 Segurança

### Senhas
- Criptografadas com bcrypt
- Verificadas com `verify_password()`
- Nunca armazenadas em texto plano

### JWT
- Token expira em 30 minutos (configurável)
- Contém: sub (user_id), exp (expiração), iat (emissão)
- Verificado em `get_current_user()`
- Armazenado no localStorage (frontend)

### CORS
- Apenas origens permitidas podem acessar
- Configurável em `settings.ALLOWED_ORIGINS`

### Validação
- Pydantic valida entrada
- SQLAlchemy previne SQL injection
- Sanitização de dados

## 🧪 Testando a API

### Com cURL

```bash
# Registrar
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao",
    "email": "joao@example.com",
    "password": "senha123",
    "full_name": "João Silva"
  }'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao",
    "password": "senha123"
  }'

# Usar token (copiar access_token da resposta)
curl -X GET http://localhost:8000/notes/ \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### Com Swagger
Acesse: `http://localhost:8000/docs`

### Com Postman
1. Importe coleção
2. Configure variáveis: `{{base_url}}`, `{{token}}`
3. Use tests para extrair token do login

## 🐛 Debugging

### Backend
```python
# Adicione prints para debug
print(f"User created: {db_user.username}")

# Use logging
import logging
logger = logging.getLogger(__name__)
logger.info(f"User login: {username}")
```

### Frontend
```javascript
// Console do navegador
console.log('User:', user);
console.error('Error:', error);

// React DevTools
// Debugar componentes e props
```

## 📦 Dependências Principais

### Backend
- **fastapi**: Framework web
- **sqlalchemy**: ORM
- **pydantic**: Validação
- **python-jose**: JWT
- **passlib**: Hashing

### Frontend
- **react**: Biblioteca UI
- **react-router-dom**: Routing
- **axios**: HTTP client
- **@mui/material**: Design system

## 🚀 Deploy

### Backend (Heroku)
```bash
# Criar Procfile
echo "web: gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker" > Procfile

# Deploy
git push heroku main
```

### Frontend (Vercel)
```bash
cd frontend
npm install -g vercel
vercel
```

## 📝 Checklist de Boas Práticas

- ✅ Separação de concerns (models, services, routes)
- ✅ Type hints em Python
- ✅ Validação de entrada com Pydantic
- ✅ Tratamento de erros apropriado
- ✅ CORS configurado
- ✅ JWT para autenticação
- ✅ Senhas criptografadas
- ✅ Componentes reutilizáveis
- ✅ Context API para estado global
- ✅ Código comentado
- ✅ README documentado
- ✅ .gitignore configurado

## 💡 Dicas

1. **Performance**: Use paginação nas listas
2. **UX**: Adicione loading states
3. **Segurança**: Nunca confie em dados do cliente
4. **Testing**: Escreva testes para cada função
5. **Versionamento**: Versione suas APIs (`/api/v1/...`)

## 📚 Recursos Adicionais

- FastAPI Docs: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- React: https://react.dev/
- Material UI: https://mui.com/
- JWT: https://jwt.io/
