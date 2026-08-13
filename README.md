# Chat com Documentos (RAG)

Envie um PDF ou arquivo de texto, faça perguntas sobre o conteúdo e receba
respostas geradas por IA (Claude), baseadas apenas no que está no documento
— com autenticação de usuários via JWT.

É um exemplo de **RAG (Retrieval-Augmented Generation)**: em vez de mandar
o documento inteiro pra IA a cada pergunta, o texto é quebrado em pedaços,
cada pedaço vira um vetor (embedding), e só os pedaços mais relevantes para
a pergunta feita são enviados como contexto pro modelo.

## 📋 Como funciona

```
1. Upload do documento (PDF, .txt ou .md)
2. Backend extrai o texto e quebra em trechos (chunks)
3. Cada trecho vira um vetor numérico (embedding), gerado localmente
   — sem custo de API externa
4. Trechos e vetores ficam guardados no banco (SQLite)
5. Ao perguntar algo, o backend busca os trechos mais parecidos com a
   pergunta (similaridade de cosseno) e manda só eles pra API da Claude
6. A resposta vem baseada apenas nesse contexto — se a informação não
   estiver no documento, a IA diz isso em vez de inventar
```

## 📋 Estrutura do Projeto

```
chat-com-documentos/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py          # Configurações da aplicação
│   │   │   └── security.py        # Autenticação JWT e segurança
│   │   ├── database/
│   │   │   └── database.py        # Configuração do banco de dados
│   │   ├── models/
│   │   │   ├── user.py            # Modelo de usuário
│   │   │   ├── document.py        # Modelo de documento e trecho (chunk)
│   │   │   └── chat.py            # Modelo de sessão de chat e mensagem
│   │   ├── schemas/                # Schemas de validação (Pydantic)
│   │   ├── services/
│   │   │   ├── user_service.py     # Lógica de negócio de usuário
│   │   │   ├── embedding_service.py # Geração de embeddings locais
│   │   │   ├── document_service.py  # Extração de texto, chunking, indexação
│   │   │   └── rag_service.py       # Busca por similaridade + chamada à Claude
│   │   ├── routes/
│   │   │   ├── auth.py             # Rotas de autenticação
│   │   │   ├── documents.py        # Rotas de documentos
│   │   │   └── chat.py             # Rotas de chat
│   │   └── main.py                 # Aplicação FastAPI (fonte da verdade)
│   ├── tests/                      # Testes automatizados (pytest)
│   ├── main.py                     # `python main.py` sobe o servidor de dev
│   ├── requirements.txt            # Dependências Python
│   ├── Dockerfile
│   └── .env                        # Variáveis de ambiente (local, fora do git)
│
└── frontend/
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── components/
    │   │   ├── DocumentUpload.js   # Upload e lista de documentos
    │   │   └── ChatInterface.js    # Interface de chat
    │   ├── pages/
    │   │   ├── Login.js
    │   │   ├── Register.js
    │   │   └── Dashboard.js
    │   ├── context/
    │   │   └── AuthContext.js      # Context de autenticação
    │   ├── services/
    │   │   └── api.js              # Serviço de API
    │   ├── utils/
    │   │   └── ProtectedRoute.js   # Rota protegida
    │   ├── index.js
    │   └── index.css
    ├── Dockerfile
    └── package.json
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10+
- Node.js 18+
- Uma chave de API da Anthropic ([console.anthropic.com](https://console.anthropic.com/settings/keys)) — sem ela o chat não responde
- **Recomendado:** rode o backend dentro de um ambiente virtual (`venv`). O
  projeto instala `sentence-transformers` (que traz o PyTorch), uma
  dependência relativamente pesada — isolar evita conflito com outros
  projetos Python que você tenha na máquina.

### Backend

1. **Criar e ativar um ambiente virtual (recomendado)**
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

2. **Configurar variáveis de ambiente**
```bash
cp .env.example .env
```
Edite o `.env` e preencha `ANTHROPIC_API_KEY` com sua chave. O resto dos
valores padrão já funciona localmente.

3. **Instalar dependências**
```bash
pip install -r requirements.txt
```
> A primeira instalação baixa o PyTorch e demora alguns minutos. Na
> primeira vez que um documento for enviado, o modelo de embeddings
> (`all-MiniLM-L6-v2`, ~90MB) também é baixado automaticamente.

4. **Executar servidor FastAPI**
```bash
python main.py
```

O servidor estará disponível em: `http://localhost:8000`

Documentação da API: `http://localhost:8000/docs`

### Frontend

1. **Instalar dependências**
```bash
cd frontend
npm install
```

2. **Iniciar aplicação React**
```bash
npm start
```

A aplicação estará disponível em: `http://localhost:3000`

### 🐳 Ou com Docker (backend + frontend juntos)

```bash
cp backend/.env.example backend/.env
# edite backend/.env e preencha ANTHROPIC_API_KEY antes de subir
docker compose up --build
```

> A imagem do backend inclui PyTorch, então o build inicial é mais lento e
> a imagem final é maior do que um backend FastAPI comum — normal para um
> projeto com embeddings locais.

### 🧪 Rodando os testes do backend

```bash
cd backend
pip install -r requirements-dev.txt
pytest
```
Os testes usam funções fake no lugar do modelo de embeddings real e da API
da Claude — rodam rápido e não gastam créditos nem baixam modelos.

## 🔐 Autenticação JWT

- Login retorna um token JWT que deve ser enviado no header `Authorization: Bearer <token>`
- Token expira em 30 minutos (configurável)
- Todas as rotas de documentos e chat requerem autenticação

## 📚 Endpoints da API

### Autenticação
- `POST /auth/register` - Cadastrar novo usuário
- `POST /auth/login` - Fazer login
- `GET /auth/me` - Obter dados do usuário autenticado

### Documentos (requer autenticação)
- `POST /documents/upload` - Enviar um documento (PDF, .txt ou .md)
- `GET /documents/` - Listar os documentos do usuário
- `DELETE /documents/{id}` - Remover um documento

### Chat (requer autenticação)
- `POST /chat/sessions` - Criar uma sessão de chat associada a um documento
- `GET /chat/sessions` - Listar as sessões de chat do usuário
- `GET /chat/sessions/{id}/messages` - Listar o histórico de uma sessão
- `POST /chat/sessions/{id}/messages` - Enviar uma pergunta e receber a resposta da IA

## 🏗️ Arquitetura

### Backend
- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para banco de dados
- **JWT**: Autenticação e autorização
- **SQLite**: Banco de dados leve e portável (guarda também os embeddings, como JSON)
- **sentence-transformers**: Geração de embeddings localmente, sem custo de API
- **pypdf**: Extração de texto de arquivos PDF
- **Anthropic SDK**: Chamadas à API da Claude para gerar as respostas

### Frontend
- **React**: Biblioteca de UI
- **Material UI**: Componentes e design moderno
- **React Router**: Navegação entre páginas
- **Axios**: Cliente HTTP

## 💾 Banco de Dados

### Modelos

**User**
- id (PK), username (único), email (único), full_name, hashed_password, created_at, updated_at

**Document**
- id (PK), user_id (FK), filename, content_type, status (`processing`/`ready`/`error`), error_message, chunk_count, created_at

**DocumentChunk**
- id (PK), document_id (FK), chunk_index, content, embedding (vetor serializado em JSON), created_at

**ChatSession**
- id (PK), user_id (FK), document_id (FK), title, created_at

**Message**
- id (PK), session_id (FK), role (`user`/`assistant`), content, created_at

## ⚙️ Configurações

Edite o arquivo `.env` no backend para customizar:
- `SECRET_KEY`: Chave secreta para JWT (MUDE EM PRODUÇÃO)
- `ANTHROPIC_API_KEY`: Chave da API da Claude (**obrigatória** para o chat responder)
- `CLAUDE_MODEL`: Modelo usado nas respostas (padrão `claude-opus-5`; troque para `claude-haiku-4-5` para reduzir custo em testes)
- `DATABASE_URL`: URL do banco de dados
- `UPLOAD_DIR`, `MAX_UPLOAD_SIZE_MB`: onde e até que tamanho os documentos são salvos
- `EMBEDDING_MODEL`, `CHUNK_SIZE`, `CHUNK_OVERLAP`, `TOP_K_CHUNKS`: parâmetros do pipeline de RAG
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Tempo de expiração do token
- `ALLOWED_ORIGINS`: Origens permitidas para CORS

## 🎯 Limitações conhecidas (decisões conscientes de escopo)

- **Sem streaming**: a resposta da IA chega de uma vez, não token a token. Dá pra adicionar depois com Server-Sent Events.
- **Sem banco vetorial dedicado**: a busca por similaridade é feita "na unha" com numpy, carregando todos os chunks do documento a cada pergunta. Funciona bem na escala de um projeto de portfólio; para volumes grandes, um banco como Chroma ou pgvector seria o próximo passo.
- **Upload é síncrono**: o processamento (extração + chunking + embeddings) acontece dentro da própria requisição de upload, então arquivos grandes demoram alguns segundos para responder.

## 📝 Boas Práticas

- ✅ Separação de camadas (models, services, routes)
- ✅ Código bem comentado e organizado
- ✅ Validação de dados com Pydantic
- ✅ Tratamento de erros apropriado (inclusive falhas da API externa)
- ✅ Segurança com hashing de senhas e JWT
- ✅ CORS configurado
- ✅ Testes automatizados do backend (pytest), sem depender de API externa ou modelo real
- ✅ Pronto para rodar em Docker

## 📚 Documentação

- [PLANO_DESENVOLVIMENTO.md](PLANO_DESENVOLVIMENTO.md) — plano de desenvolvimento do projeto, por fases

## 📄 Licença

MIT — veja [LICENSE](./LICENSE).
