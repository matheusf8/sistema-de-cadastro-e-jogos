# Plano de Desenvolvimento — Chat com Documentos (RAG)

> Este documento é a fonte de verdade do projeto. Cada fase só começa depois
> que a anterior está marcada como concluída e revisada. Atualize o status
> aqui conforme o trabalho avança — é assim que qualquer pessoa (ou sessão
> futura) retoma o contexto sem precisar reconstruir tudo do zero.

## 1. Visão geral

**O que é:** uma aplicação web onde o usuário se cadastra, faz upload de um
documento (PDF ou texto) e conversa com ele — faz perguntas e recebe
respostas baseadas apenas no conteúdo daquele documento, com a IA (Claude)
citando o que encontrou.

**Por quê:** projeto de portfólio focado em algo que reflete o que está em
alta agora (integração real com LLM, não só CRUD), sem descartar o trabalho
de fundação que já existia (autenticação JWT, estrutura em camadas, testes,
Docker).

**Onde vive:** este mesmo repositório (antes "sistema-de-cadastro-e-jogos"),
na branch `rag-chat-docs`. O conteúdo antigo (calculadora, bloco de notas,
jogo da cobrinha) foi removido — histórico continua acessível via git caso
seja preciso consultar algo.

## 2. Arquitetura

```
┌─────────────┐      upload PDF/texto       ┌──────────────────────┐
│  Frontend   │ ───────────────────────────▶│       Backend         │
│  (React)    │                              │      (FastAPI)        │
│             │◀─────────────────────────────│                        │
└─────────────┘      pergunta / resposta     │  1. extrai texto       │
                                              │  2. quebra em chunks   │
                                              │  3. gera embeddings    │
                                              │     (local, sem custo) │
                                              │  4. guarda no SQLite   │
                                              └───────────┬────────────┘
                                                           │
                                              pergunta do usuário
                                                           │
                                                           ▼
                                              busca os chunks mais
                                              parecidos (cosseno)
                                                           │
                                                           ▼
                                              monta prompt + chama
                                              a API da Claude
                                                           │
                                                           ▼
                                              resposta grounded no
                                              documento
```

## 3. Stack e decisões técnicas

| Peça | Escolha | Por quê |
|---|---|---|
| Backend | FastAPI + SQLAlchemy (reaproveitado) | Já existia, funcionando e testado |
| Auth | JWT + bcrypt (reaproveitado, sem mudanças) | Não precisa reinventar |
| Banco | SQLite | Simples, roda sem infra extra — suficiente pra portfólio |
| Extração de texto | `pypdf` | Leve, sem dependências pesadas |
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`), **local** | Sem custo de API externa; primeira execução baixa o modelo (~90MB) |
| Busca de similaridade | Cosseno "na unha" com `numpy`, sem banco vetorial dedicado | Suficiente na escala de um portfólio; mostra que você entende o mecanismo, não só "plugou uma lib" |
| Geração da resposta | API da Claude (`claude-opus-5` por padrão, configurável) | Modelo atual recomendado; pode trocar por `claude-haiku-4-5` via `.env` pra reduzir custo em testes |
| Frontend | React + Material UI (reaproveitado) | Já existia, funcionando |

**Fora de escopo por enquanto (decisão consciente, não esquecimento):**
- Streaming da resposta da IA (fica como próxima melhoria — MVP responde de uma vez só)
- Banco vetorial dedicado (Chroma, pgvector) — só se a escala justificar
- App mobile (foi discutido como ideia separada, projeto futuro, sem relação com este)

## 4. Fases

### Fase 0 — Fundação ✅ concluída
- [x] Branch `rag-chat-docs` criada a partir da `main`
- [x] Conteúdo do projeto antigo removido (calculadora, bloco de notas, jogo da cobrinha, módulo `notes` do backend, docs antigas)
- [x] Auth (models, schemas, service, rotas, frontend) mantido — não precisa de mudanças, só de novos relacionamentos no model `User`

### Fase 1 — Backend: upload e processamento de documentos ✅ concluída
**Entregável:** endpoint que recebe um arquivo, extrai o texto, quebra em
pedaços, gera embeddings e salva tudo — e endpoints pra listar/remover
documentos.

- [x] `Settings` novo: `ANTHROPIC_API_KEY`, `CLAUDE_MODEL`, `UPLOAD_DIR`, `EMBEDDING_MODEL`, `CHUNK_SIZE`, `CHUNK_OVERLAP`, `TOP_K_CHUNKS`
- [x] Models `Document` e `DocumentChunk`
- [x] Serviço de embeddings locais (`embedding_service.py`)
- [x] Serviço de processamento (`document_service.py`): extração + chunking + geração de embeddings
- [x] Rotas `/documents` (upload, listar, deletar)
- [x] Testes do módulo (`tests/test_documents.py`, com embeddings mockados)

**Critério de pronto:** ✅ verificado — app sobe, tabelas são criadas, upload processa um `.txt` de teste e grava o documento com status `ready` e os chunks no banco.

### Fase 2 — Backend: RAG + chat ✅ concluída
**Entregável:** endpoint de chat que recebe uma pergunta, busca os trechos
mais relevantes do documento e responde usando a API da Claude.

- [x] Models `ChatSession` e `Message`
- [x] Serviço de RAG (`rag_service.py`): retrieval por similaridade + chamada à Claude
- [x] Rotas `/chat` (criar sessão, enviar mensagem, listar histórico)
- [x] Testes do módulo (`tests/test_chat.py`, com a chamada à Claude mockada — sem gastar créditos de verdade nos testes)

**Critério de pronto:** ✅ verificado nos testes automatizados (fluxo completo: criar sessão → enviar pergunta → receber resposta do "assistant" → histórico persistido). Teste manual ponta a ponta com uma chave real da Anthropic ainda não foi feito — ver seção 6.

### Fase 3 — Frontend: autenticação + upload ✅ concluída
- [x] Reaproveitar Login/Register/AuthContext/ProtectedRoute (sem mudanças)
- [x] Novo Dashboard: lista de documentos + upload
- [x] Serviço de API (`api.js`) atualizado pros novos endpoints (`documentsAPI`, `chatAPI`)

**Critério de pronto:** ✅ `npm run build` compila sem erros nem warnings.

### Fase 4 — Frontend: interface de chat ✅ concluída
- [x] Componente `ChatInterface`: seleção de documento (via `DocumentUpload`), histórico de mensagens, campo de pergunta
- [x] Estado de "carregando resposta" enquanto a IA processa, com UI otimista pra pergunta do usuário

**Critério de pronto:** ✅ build de produção passa; fluxo revisado por leitura (login → upload → conversar → perguntar → resposta). Falta validar clicando de verdade no navegador — ver seção 6.

### Fase 5 — Polimento e entrega 🔶 parcial
- [x] README novo (setup, variáveis de ambiente, como rodar, limitações conhecidas)
- [x] `.env.example` atualizado
- [x] Testes do backend passando (17/17)
- [ ] Screenshots do app funcionando
- [ ] Dockerfile/docker-compose — não testados de verdade (build Docker não foi executado; ficou só a atualização do `requirements.txt`, que o Dockerfile já usa)
- [ ] Deploy (opcional)

## 5. Status atual

**Projeto 100% funcional, testado de ponta a ponta no navegador com IA
real.** Fluxo completo confirmado: cadastro, login, upload de documento
real (extração + chunking + embeddings rodando de verdade), **duas
perguntas reais respondidas corretamente pela Claude** (`claude-haiku-4-5`)
com base apenas no conteúdo do documento — incluindo histórico de
conversa mantido entre perguntas —, exclusão de documento e logout.

Exemplo real de pergunta e resposta (documento de teste: manual fictício
do "Nébula X200"):

> **Pergunta:** Qual o tempo de garantia do produto?
> **Resposta:** De acordo com o documento, o Nébula X200 possui garantia
> de 24 meses a partir da data de compra. A garantia cobre defeitos de
> fabricação, mas não cobre danos causados por mau uso ou instalação fora
> das especificações recomendadas no Capítulo 1 do manual.

Só ficaram pendências opcionais/de polimento — ver seção 6.

**Bug real encontrado e corrigido durante o teste manual:** sem
`ANTHROPIC_API_KEY` configurada, a pergunta no chat **travava a interface
indefinidamente** em vez de mostrar um erro — o SDK da Anthropic usa um
timeout padrão de 10 minutos, e nada no código impunha um limite menor.
Corrigido em `rag_service.py`: (1) checagem explícita que falha na hora com
mensagem clara se a chave não estiver configurada, (2) timeout de 30s e
apenas 1 retry no cliente da Anthropic, para qualquer outra falha de rede
também falhar rápido em vez de travar. Testes de regressão adicionados em
`tests/test_rag_service.py` (19/19 passando).

**Última atualização:** 2026-08-11

## 6. Pendências / próximos passos

Coisas que foram deliberadamente deixadas para depois, ou que precisam de
uma pessoa (não dá pra verificar sozinho):

1. ~~**Chave da Anthropic**~~ ✅ resolvido — chave real configurada e
   testada com sucesso (duas perguntas reais, respostas corretas). Modelo
   em uso: `claude-haiku-4-5` (mais barato; trocar para `claude-opus-5` no
   `.env` quando quiser a qualidade padrão do projeto).
2. **Build Docker não testado de verdade** — tentei `docker compose build`
   e o Docker Desktop não estava rodando no momento (daemon inativo). Os
   Dockerfiles/compose não foram alterados na lógica, só o
   `requirements.txt` ganhou novas dependências — abrir o Docker Desktop e
   rodar `docker compose up --build` pra confirmar quando for conveniente.
3. **Screenshots** para o README — não capturadas ainda; o app está
   funcional e pode ser fotografado a qualquer momento.
4. **Nota de ambiente:** neste ambiente de desenvolvimento específico, o
   auto-reload do Uvicorn (`--reload`) não pegou uma alteração de código
   corretamente na primeira tentativa — foi preciso reiniciar o processo do
   zero. Se algo parecer "não aplicar" depois de uma edição, reiniciar o
   servidor manualmente antes de investigar mais fundo. Também notei uma
   extensão do navegador (autofill/gerenciador de senha) causando
   travamentos esporádicos de tela durante os testes manuais — não tem
   relação com a aplicação, é só ruído do ambiente de teste.
