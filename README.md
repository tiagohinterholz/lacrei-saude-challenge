# 🩺 Lacrei Saúde API

API desenvolvida para o **desafio técnico da Lacrei Saúde**, utilizando **Django REST Framework**, **JWT**, **PostgreSQL** e **Docker**.

---

## 🚀 Tecnologias

- **Python 3.12**
- **Django 5.2**
- **Django REST Framework**
- **SimpleJWT** (autenticação)
- **PostgreSQL**
- **Docker / Docker Compose**
- **DRF Spectacular** (documentação Swagger)
- **Pytest** (testes automatizados)

---

## ⚙️ Setup Local

### 1️⃣ Clone o repositório
```bash
git clone git@github.com:tiagohinterholz/lacrei-saude-challenge.git
cd lacrei-saude-challenge
```

### 2️⃣ Configure o ambiente
Crie um arquivo `.env` na raiz com:
```env
SECRET_KEY="sua_chave_aqui"
DEBUG=True
SSL_REDIRECT=False

ENGINE_DB=django.db.backends.postgresql
NAME_DB=lacrei
USER_DB=seu_user
PASSWORD_DB=seu_password
HOST_DB=localhost
PORT_DB=5432

SUPER_USER=admin
EMAIL=seu_email@gmail.com
SUPER_PASSWORD=seu_password
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
PORT=8000
```

### 3️⃣ Crie o banco
No PostgreSQL:
```sql
CREATE DATABASE lacrei;
CREATE USER seu_user WITH PASSWORD 'seu_user';
ALTER ROLE seu_user SET client_encoding TO 'utf8';
ALTER ROLE seu_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE seu_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE lacrei TO seu_user;
```

### 4️⃣ Configure o ambiente Poetry
```bash
poetry install
poetry shell
python manage.py migrate
python manage.py createsuperuser
```

### 5️⃣ Execute a aplicação
```bash
python manage.py runserver
```
Acesse:
- **API Docs:** http://127.0.0.1:8000/api/schema/swagger-ui/

---

## 🐳 Setup via Docker

### 1️⃣ Build e execução
```bash
docker-compose up --build
```

### 2️⃣ Acesse os serviços
- **API:** http://localhost:8000  
- **Swagger:** http://localhost:8000/api/schema/swagger-ui/  
- **Banco:** porta `5432` (usuario: `seu_user`, senha: `seu_password`)

---

## 🧪 Testes Automatizados

### Executar todos os testes
```bash
pytest -v
```

### Executar com cobertura
```bash
pytest --cov=apps --cov-report=term-missing
```

**Cobertura mínima:**
- CRUD de profissionais
- CRUD de consultas
- Validação de conflitos e erros (400)
- Requisições não autenticadas (401)

---

## 🧱 Estrutura do Projeto

```
apps/
 ├── appointments/   → CRUD de consultas
 ├── professionals/  → CRUD de profissionais
 ├── users/          → autenticação JWT
 └── common/         → base model, mixins, repos, utils
```

---

## 🔐 Segurança

- Sanitização e validação de dados (serializers DRF)
- Proteção contra SQL Injection (ORM do Django)
- **CORS** configurado corretamente (permitindo origens seguras)
- **JWT Authentication**
- Logs de acesso e erros via `TimedRotatingFileHandler`

---

## 🤖 CI/CD (Fluxo de Deploy)

Pipeline (GitHub Actions):
1. **Lint + Testes:** executa `pytest` a cada push/PR  
2. **Build Docker:** gera imagem da API  
3. **Deploy:** envia para ambiente remoto (Heroku ou Render)

```yaml
name: CI/CD

on: [push]

jobs:
  build-test-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.12
      - name: Install dependencies
        run: |
          pip install poetry
          poetry install
      - name: Run tests
        run: pytest -v
      - name: Deploy to Heroku
        if: github.ref == 'refs/heads/main'
        run: git push heroku main
```

---

## 💡 Justificativas Técnicas

| Tecnologia | Motivo |
|-------------|--------|
| **Django REST Framework** | Rápido desenvolvimento de APIs e serializers automáticos |
| **JWT (SimpleJWT)** | Autenticação stateless e segura |
| **PostgreSQL** | Consistência, integridade e suporte a JSON |
| **Docker** | Isolamento, portabilidade e fácil deploy |
| **DRF Spectacular** | Documentação Swagger automática |
| **Pytest** | Testes simples e cobertura clara |

---

## 🔄 Proposta de Rollback

**Estratégia Blue/Green Deploy:**
1. Mantenha dois ambientes: `blue` (ativo) e `green` (staging).  
2. Faça deploy no `green` → se tudo passar, troque o tráfego (`blue` → `green`).  
3. Em caso de falha:  
   ```bash
   git revert <commit_sha>
   git push origin main
   ```
   O pipeline do GitHub Actions reexecuta o deploy da versão anterior.

---

## 📄 Licença
Projeto desenvolvido para o desafio técnico **Lacrei Saúde** — uso educacional e demonstrativo.
