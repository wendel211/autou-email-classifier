# AutoU – Classificador Inteligente de Emails

Este projeto foi desenvolvido como parte do case prático AutoU. A aplicação classifica emails em **Produtivo** ou **Improdutivo** e sugere uma resposta automática para cada caso, utilizando **técnicas de NLP** e **IA generativa (OpenAI GPT)**.

## Funcionalidades

* Upload de arquivos `.txt` ou `.pdf` e inserção direta de texto.
* **Classificação automática** em:
   * **Produtivo:** requer ação ou resposta.
   * **Improdutivo:** não exige ação imediata.
* **Respostas automáticas** sugeridas:
   * Por regras locais → sempre disponível.
   * Por **GPT-4o-mini** → se `OPENAI_API_KEY` estiver configurada.
* **Fallback inteligente:** se a API não estiver acessível, o sistema usa regras locais.
* Interface web simples e responsiva.

## Tecnologias Utilizadas

* **Backend:** Python, FastAPI, Uvicorn
* **Frontend:** HTML, JS, CSS (Tailwind base simplificada)
* **NLP:**
   * Normalização de texto (remoção de pontuação, URLs, emails).
   * Stopwords em português.
   * Tokenização.
   * **Stemming em PT-BR (NLTK SnowballStemmer)**.
* **IA Generativa:** OpenAI GPT-4o-mini (classificação + resposta).
* **Outros:** PyPDF2, Jinja2, pytest.

## Estrutura do Projeto

```
app/
  main.py                  # Entrada FastAPI
  services/
    classifier.py          # Classificação (Regras + OpenAI)
    extract.py             # Extração de texto (txt/pdf)
    nlp.py                 # Pré-processamento NLP
    responder.py           # Regras de resposta automática
templates/
  index.html               # Interface
static/
  app.js                   # Lógica frontend
  styles.css               # Estilos
tests/
  test_rules.py            # Testes unitários (pytest)
sample_emails/             # Exemplos
requirements.txt           # Dependências fixadas
Procfile                   # Deploy Heroku
Dockerfile                 # Deploy Render
README.md                  # Este documento
```

## Como Rodar Localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU-USUARIO/autou-email-classifier.git
cd autou-email-classifier
```

### 2. Criar ambiente virtual

```bash
python -m venv .venv
.\.venv\Scripts\Activate    # Windows
source .venv/bin/activate   # Linux/Mac
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. (Opcional) Configurar OpenAI GPT

```bash
$Env:OPENAI_API_KEY="sua_chave_aqui"   # PowerShell
export OPENAI_API_KEY="sua_chave_aqui" # Linux/Mac
```

### 5. Rodar servidor

```bash
uvicorn app.main:app --reload
```

Acesse http://127.0.0.1:8000

## Deploy

### Render (Docker)

1. Conectar repo no Render.
2. Ele detecta o `Dockerfile`.
3. Configurar variável `OPENAI_API_KEY` (opcional).

### Heroku

```bash
heroku create
git push heroku main
heroku config:set OPENAI_API_KEY=suachave
```

## Testes

Rodar testes unitários com `pytest`:

```bash
pytest -q
```

Saída esperada:

```
..                                                                   [100%]
2 passed in 0.04s
```


## Possíveis Melhorias

* Treinar modelo supervisionado (TF-IDF + Logistic Regression).
* Novas categorias além de Produtivo/Improdutivo.
* Integração com Gmail/Outlook para ingestão automática de emails.
* Dashboard de métricas de classificação.

## Licença

Projeto sob licença MIT.
