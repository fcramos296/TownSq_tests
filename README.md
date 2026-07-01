# Townsq QA Automation

Projeto de testes automatizados E2E e API para a pagina de login do Townsq (Octadesk), utilizando **Pytest**, **Playwright** e **Page Object Model (POM)**.

## Tecnologias

- Python 3.11+
- Pytest
- Playwright (chromium)
- pytest-html
- python-dotenv
- requests

## Estrutura

```
townsq_qa_tests/
├── pages/
│   ├── base_page.py
│   └── login_page.py
├── tests/
│   ├── e2e/
│   │   └── test_login_e2e.py
│   └── api/
│       └── test_login_api.py
├── utils/
│   └── settings.py
├── reports/
├── conftest.py
├── pytest.ini
├── requirements.txt
├── .env.example
└── setup.bat
```

## Instalacao

1. Clone ou baixe o projeto.
2. Execute o `setup.bat` (Windows) ou configure manualmente:

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m playwright install chromium
```

3. Configure as credenciais no arquivo `.env` (criado automaticamente pelo setup.bat).

## Execucao

```bash
# Todos os testes
.venv\Scripts\python -m pytest

# Apenas E2E
.venv\Scripts\python -m pytest -m e2e

# Apenas API
.venv\Scripts\python -m pytest -m api

# Smoke tests
.venv\Scripts\python -m pytest -m smoke

# Com relatorio HTML
.venv\Scripts\python -m pytest --html=reports/report.html --self-contained-html
```

## Variaveis de Ambiente

| Variavel    | Descricao                        |
|-------------|----------------------------------|
| BASE_URL    | URL da pagina de login            |
| USERNAME    | E-mail/usuario para testes        |
| PASSWORD    | Senha para testes                 |

## Observacoes

- Os seletores em `pages/login_page.py` utilizam estrategias multi-criterio (fallbacks) para campos de e-mail, senha e botao. Ajuste-os conforme o DOM real da pagina.
- Testes de login com credenciais validas sao pulados automaticamente se `.env` nao estiver preenchido.
- Screenshots de falha sao salvos automaticamente em `reports/screenshots/`.
