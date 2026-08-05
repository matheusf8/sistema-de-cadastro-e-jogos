# ❓ Troubleshooting e FAQ

## ❌ Problemas Comuns

### Backend não inicia

**Erro**: `ModuleNotFoundError: No module named 'fastapi'`

**Solução**:
```bash
cd backend
pip install -r requirements.txt
```

**Erro**: `Port 8000 is already in use`

**Solução**:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

---

### Frontend não inicia

**Erro**: `npm: command not found`

**Solução**: Instale Node.js de https://nodejs.org/

**Erro**: `Port 3000 is already in use`

**Solução**:
```bash
# Use outra porta
PORT=3001 npm start
```

---

### Erro 401 na API

**Erro**: `Credentials invalid`

**Solução**:
1. Verifique se fez login
2. Verifique se o token está no localStorage
3. Tente fazer logout e login novamente

---

### CORS Error

**Erro**: `Access to XMLHttpRequest... has been blocked by CORS policy`

**Solução**:
1. Adicione a origem em `ALLOWED_ORIGINS` no `backend/.env`
2. Reinicie o backend

---

### Banco de dados não persiste

**Problema**: Dados desaparecem ao reiniciar

**Solução**:
1. Verifique se o arquivo `app.db` foi criado
2. Verifique se tem permissão de escrita na pasta
3. Use caminho absoluto se necessário

---

## ❔ Perguntas Frequentes

### P: Como mudar a porta?

**R**: 
```bash
# Backend
python main.py --port 8001

# Frontend
PORT=3001 npm start
```

### P: Como resetar o banco de dados?

**R**:
```bash
cd backend
rm app.db  # Deleta o arquivo
python main.py  # Recria automaticamente
```

### P: Como adicionar um novo modelo?

**R**:
1. Crie em `app/models/`
2. Crie schema em `app/schemas/`
3. Crie service em `app/services/`
4. Crie rotas em `app/routes/`
5. Importe o modelo em `app/main.py`

### P: Como hospedar em produção?

**R**: Veja [DEPLOYMENT.md](DEPLOYMENT.md)

### P: Como fazer login automático ao registrar?

**R**: Modifique o `Register.js` para fazer login após registrar

### P: Posso usar PostgreSQL em vez de SQLite?

**R**: Sim! Mude o `DATABASE_URL`:
```python
# Instale: pip install psycopg2
DATABASE_URL = "postgresql://user:password@localhost/dbname"
```

### P: Como adicionar autenticação com Google?

**R**: Use `python-google-auth` e adicione rota OAuth2

### P: Como fazer backup das notas?

**R**: Faça backup do arquivo `app.db`

---

## ✅ Checklist de Desenvolvimento

### Antes de começar
- [ ] Python 3.8+ instalado
- [ ] Node.js 14+ instalado
- [ ] Clonou o repositório
- [ ] Criou ambiente virtual (opcional)

### Desenvolvimento Backend
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Backend inicia sem erros
- [ ] Swagger acessível em `/docs`
- [ ] Consegue fazer registro e login
- [ ] Tokens JWT funcionam

### Desenvolvimento Frontend
- [ ] Dependências instaladas (`npm install`)
- [ ] Frontend inicia sem erros
- [ ] Consegue acessar /login
- [ ] Consegue se registrar
- [ ] Consegue fazer login
- [ ] Dashboard carrega corretamente
- [ ] Abas funcionam

### Testes
- [ ] Calculadora realiza operações corretamente
- [ ] Notas: criar funciona
- [ ] Notas: ler funciona
- [ ] Notas: editar funciona
- [ ] Notas: deletar funciona
- [ ] Jogo da Cobrinha funciona
- [ ] Logout funciona

### Antes de Produção
- [ ] Mudar `SECRET_KEY` em `.env`
- [ ] Testar em navegadores diferentes
- [ ] Testar em dispositivos móveis
- [ ] Adicionar HTTPS
- [ ] Configurar CORS corretamente
- [ ] Adicionar rate limiting
- [ ] Adicionar logging
- [ ] Fazer backup do banco

---

## 🔍 Como Debugar

### Verificar requisições HTTP

**Frontend**:
```javascript
// DevTools → Network tab
// Veja requests e responses
```

**Backend**:
```python
from fastapi.logger import logger
logger.info(f"Request received: {request}")
```

### Verificar estado Redux/Context

**Frontend**:
```javascript
// console.log no seu componente
const { user, token } = useAuth();
console.log({ user, token });
```

### Verificar banco de dados

```bash
# Instale sqlite3
sqlite3 backend/app.db

# No prompt SQLite
.tables  # Ver tabelas
SELECT * FROM users;  # Ver usuários
SELECT * FROM notes;  # Ver notas
```

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique os erros no console
2. Consulte a seção de troubleshooting
3. Leia a documentação do projeto
4. Revise os arquivos de configuração

---

## 🔐 Segurança - Checklist

- [ ] Senhas criptografadas com bcrypt
- [ ] JWT com expiração
- [ ] CORS configurado
- [ ] HTTPS em produção
- [ ] Senhas fortes (mínimo 6 caracteres)
- [ ] Validação de entrada
- [ ] Rate limiting configurado
- [ ] Logs de auditoria

---

## 📈 Performance - Dicas

1. **Paginação**: Use `skip` e `limit` nas listagens
2. **Cache**: Implemente cache no frontend
3. **Compressão**: Comprima responses
4. **CDN**: Use CDN para assets estáticos
5. **Database**: Adicione índices nas colunas frequentes

---

## 🎓 Aprendizado

Este projeto demonstra:
- ✅ Arquitetura em camadas
- ✅ Autenticação JWT
- ✅ CRUD com banco de dados
- ✅ API RESTful
- ✅ Frontend React moderno
- ✅ Material UI
- ✅ Context API
- ✅ Componentes reutilizáveis
