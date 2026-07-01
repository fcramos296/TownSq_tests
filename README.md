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
## Pré requisitos

- Python 3.11+
- Máquina Windows (caso queira utilizar o setup.bat)

## Instalacao

Clone ou baixe o repositório e execute o arquivo `setup.bat` na raiz do projeto.

O script realiza automaticamente as seguintes etapas:

- Solicita um e-mail válido para os testes.
- Solicita uma senha válida para os testes.
- Cria o arquivo `.env` na raiz do projeto.
- Cria a virtualenv `.venv`.
- Instala as dependências definidas no `requirements.txt`.
- Instala `pytest`, `playwright` e `pytest-playwright`, se necessário.
- Instala `Allure`.
- Instala os navegadores usados pelo Playwright.
- Executa os testes com `pytest`.
- Gera o report do Allure e o exibe ao final da execução.

Configuração manual (Linux, Mac)

Crie um arquivo .env na raíz do projeto e configure as credenciais de acesso

BASE_URL=https://townsq.octadesk.com/login
USERNAME=example@teste.com
PASSWORD=examplepassword

```bash
python -m venv .venv
.venv\Scripts\activate.bat
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m playwright install chromium
```

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

# Com relatorio do Allure
.venv\Scripts\python -m pytest allure generate allure-results -o allure-report --clean
```

## Variaveis de Ambiente

| Variavel    | Descricao                        |
|-------------|----------------------------------|
| BASE_URL    | URL da pagina de login            |
| USERNAME    | E-mail/usuario para testes        |
| PASSWORD    | Senha para testes                 |

## Observacoes

O arquivo setup.bat foi preparado para ambiente Windows.
O Python deve estar previamente instalado na máquina.
Caso o PowerShell bloqueie scripts, prefira executar o setup.bat pelo Prompt de Comando.
