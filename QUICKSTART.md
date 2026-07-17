# ⚡ Quick Start

## 🚀 Iniciar em 5 Minutos

### Windows
```bash
# Duplo-clique em start.bat
# ou
start.bat
```

### Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

---

## 📋 Setup Manual

### 1️⃣ Backend

```bash
cd backend

# Instalar dependências
pip install -r requirements.txt

# Iniciar servidor
python main.py
```

✅ Backend em: http://localhost:8000  
📖 Docs em: http://localhost:8000/docs

---

### 2️⃣ Frontend (nova janela de terminal)

```bash
cd frontend

# Instalar dependências
npm install

# Iniciar app
npm start
```

✅ Frontend em: http://localhost:3000

---

## 🔐 Testar

1. Abra http://localhost:3000
2. Clique em "Cadastre-se aqui"
3. Preencha o formulário:
   - Nome: Seu nome
   - Usuário: seu_usuario
   - Email: seu@email.com
   - Senha: senha123
4. Clique em "Cadastrar"
5. Faça login com suas credenciais
6. Explore as 3 abas! 🎉

---

## 📂 Estrutura

```
Calculadora/
├── backend/          ← API FastAPI
│   └── app/
│       ├── models/   ← Modelos BD
│       ├── routes/   ← Endpoints
│       └── services/ ← Lógica
├── frontend/         ← App React
│   └── src/
│       ├── pages/    ← Telas
│       └── components/ ← Componentes
└── README.md         ← Documentação
```

---

## 🛠️ Tecnologias

| Parte | Tecnologia | Versão |
|-------|-----------|--------|
| Backend | FastAPI | 0.104+ |
| Frontend | React | 18.2+ |
| Auth | JWT | |
| DB | SQLite | 3 |
| UI | Material UI | 5.14+ |

---

## 🎯 Funcionalidades

### 1. 🧮 Calculadora
- Operações: +, -, ×, ÷
- Suporta decimais
- Interface limpa

### 2. 📝 Bloco de Notas
- Criar notas
- Editar notas
- Deletar notas
- Persistência em BD

### 3. 🐍 Jogo da Cobrinha
- Clássico dos celulares
- Controle: setas ou WASD
- Sistema de pontos

---

## 🐛 Se der erro

| Erro | Solução |
|------|---------|
| `Port already in use` | Mude a porta: `PORT=3001 npm start` |
| `Python not found` | Instale Python 3.8+ |
| `npm not found` | Instale Node.js 14+ |
| `Module not found` | Rode `pip install -r requirements.txt` |
| `CORS Error` | Verifique `.env` backend |

---

## 📖 Documentação Completa

- [README.md](README.md) - Overview do projeto
- [DEVELOPMENT.md](DEVELOPMENT.md) - Guia técnico
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - FAQ e debugging

---

## 🎓 Próximos Passos

1. ✅ Entender a arquitetura
2. ✅ Testar as funcionalidades
3. ✅ Explorar o código
4. ✅ Adicionar novas features
5. ✅ Fazer deploy

---

**Bem-vindo! 🎉**

Qualquer dúvida, veja [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
