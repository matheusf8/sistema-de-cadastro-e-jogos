# 🚀 Deploy

Duas formas de colocar o projeto no ar: **Docker** (mais simples para rodar
na sua própria máquina/servidor e compartilhar com amigos na mesma rede ou
via um túnel) ou **serviços gratuitos na nuvem** (para um link público fixo).

## 🐳 Opção 1 — Docker (recomendado para uso pessoal)

Pré-requisito: [Docker](https://www.docker.com/) instalado.

```bash
# 1. Configure o backend (só precisa fazer uma vez)
cp backend/.env.example backend/.env
# edite backend/.env e troque o SECRET_KEY por um valor aleatório seu

# 2. Suba tudo
docker compose up --build -d
```

- Frontend: http://localhost:3000
- Backend/API: http://localhost:8000
- Docs (Swagger): http://localhost:8000/docs

Os dados ficam salvos num volume Docker (`backend_data`), então sobrevivem a
`docker compose down` / `docker compose up` — só somem se você rodar com
`-v` explicitamente.

Para parar: `docker compose down`

### Compartilhar com amigos fora da sua rede

O jeito mais simples sem contratar servidor: rode `docker compose up` na sua
máquina e exponha a porta 3000 com um túnel, por exemplo:

```bash
# usando o Cloudflare Tunnel (gratuito, sem cadastro obrigatório)
cloudflared tunnel --url http://localhost:3000
```

Isso te dá uma URL pública temporária. Para algo permanente, veja a opção 2.

## ☁️ Opção 2 — Nuvem gratuita (link público fixo)

### Backend → [Render](https://render.com/)

1. Crie um "Web Service" novo apontando para este repositório, pasta raiz `backend/`
2. Build command: `pip install -r requirements.txt`
3. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Em "Environment", adicione as variáveis do `backend/.env.example`
   (principalmente `SECRET_KEY` com um valor único seu — **nunca** use o valor
   de exemplo em produção) e `ALLOWED_ORIGINS` com a URL que o frontend vai
   ter no Vercel/Netlify

> SQLite funciona, mas discos em serviços free tier costumam ser efêmeros
> (o `app.db` pode ser apagado a cada deploy). Se isso incomodar, troque
> `DATABASE_URL` por um Postgres gratuito (Render/Neon/Supabase oferecem) —
> o SQLAlchemy já está pronto pra isso, só muda a URL.

### Frontend → [Vercel](https://vercel.com/) ou [Netlify](https://netlify.com/)

1. Importe o repositório, pasta raiz `frontend/`
2. Build command: `npm run build` · Output dir: `build`
3. Variável de ambiente: `REACT_APP_API_URL` apontando para a URL do backend no Render

Depois disso é só compartilhar o link do frontend — cada amigo cria a própria
conta pela tela de cadastro.

## ✅ Checklist antes de expor pra alguém

- [ ] `SECRET_KEY` trocado por um valor aleatório (não o de exemplo)
- [ ] `ALLOWED_ORIGINS` contém só as URLs reais do seu frontend
- [ ] `backend/.env` e `frontend/.env` **não** foram commitados (o `.gitignore` já cuida disso)
- [ ] Testou registro + login + as 3 abas na URL pública antes de mandar o link
