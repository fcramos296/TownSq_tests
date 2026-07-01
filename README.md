# Townsq QA Automation

Projeto de testes automatizados E2E para a página de login do Townsq (Octadesk), utilizando Pytest, Playwright, Page Object Model e Allure.

## Tecnologias

- Python 3.11+
- Pytest
- Playwright
- pytest-playwright
- allure-pytest
- python-dotenv

## Estrutura do projeto

```text
townsq_qa_tests/
├── pages/
│   ├── base_page.py
│   └── login_page.py
├── tests/
│   └── e2e/
│       └── test_login_e2e.py
├── utils/
│   └── settings.py
├── conftest.py
├── pytest.ini
├── requirements.txt
├── .env.example
├── .gitignore
└── setup.bat
```

## Objetivo

Este projeto valida a experiência da tela de login com testes E2E cobrindo carregamento da página, visibilidade dos campos, validações negativas, fluxo de autenticação e verificação de erro global no primeiro acesso.

## Pré-requisitos

- Python 3.11 ou superior.
- Git opcional, caso queira clonar o repositório.
- Windows para execução automatizada com `setup.bat`.
- Linux ou macOS para configuração manual.
- Credenciais válidas de teste para executar o cenário de login positivo.

## Configuração de ambiente

O projeto usa arquivo `.env` para centralizar parâmetros de execução e credenciais locais.

Exemplo de `.env`:

```env
BASE_URL=https://townsq.octadesk.com/login
USERNAME=seu_email_de_teste@exemplo.com
PASSWORD=sua_senha_de_teste
BROWSER=chromium
HEADLESS=true
TIMEOUT=30000
```

### Variáveis de ambiente

| Variável | Descrição |
|---|---|
| BASE_URL | URL da página de login a ser testada |
| USERNAME | Usuário ou e-mail válido para o teste positivo |
| PASSWORD | Senha válida para o teste positivo |
| BROWSER | Navegador padrão usado pelo Playwright |
| HEADLESS | Define execução sem interface gráfica quando `true` |
| TIMEOUT | Timeout padrão dos testes em milissegundos |

## Fluxo no Windows

No Windows, a forma recomendada de preparar e executar o projeto é usar o `setup.bat`.

### O que o `setup.bat` faz

O script executa o fluxo abaixo automaticamente:

1. Entra na pasta do projeto.
2. Cria o arquivo `.env` a partir do `.env.example`, caso o `.env` ainda não exista.
3. Solicita `USERNAME` e `PASSWORD` válidos no terminal.
4. Salva as credenciais informadas no arquivo `.env` local.
5. Cria o ambiente virtual `.venv`, se necessário.
6. Detecta o tipo de terminal e ativa o ambiente virtual.
7. Atualiza o `pip`.
8. Instala as dependências do `requirements.txt`.
9. Instala o navegador Chromium do Playwright.
10. Verifica se o Allure CLI está disponível.
11. Instala o Scoop se ele não existir.
12. Instala o Allure CLI via Scoop, se necessário.
13. Remove resultados antigos de `allure-results` e `allure-report`.
14. Executa os testes com `pytest --alluredir=allure-results --headed`.
15. Gera o relatório Allure em `allure-report`.
16. Abre o relatório Allure automaticamente ao final.

### Como executar

```bat
setup.bat
```

### Observações do fluxo

- O script pede credenciais válidas sempre no início da execução.
- As credenciais ficam salvas somente no `.env` local.
- O fluxo usa Allure como único formato de relatório automatizado.
- A execução padrão do script está configurada com navegador visível (`--headed`).

## Configuração manual no Linux ou macOS

Para Linux ou macOS, a configuração deve ser feita manualmente.

### 1. Criar e ativar o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependências

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Instalar o navegador do Playwright

```bash
python -m playwright install chromium
```

### 4. Criar o `.env`

```bash
cp .env.example .env
```

Depois disso, ajuste `USERNAME`, `PASSWORD` e as demais variáveis conforme o ambiente.

### 5. Instalar o Allure CLI

Instale o Allure CLI usando o gerenciador de pacotes da sua distribuição ou a forma oficial compatível com o seu sistema operacional.

## Execução dos testes

### Todos os testes

```bash
python -m pytest
```

### Apenas testes E2E

```bash
python -m pytest -m e2e
```

### Apenas smoke tests

```bash
python -m pytest -m smoke
```

### Apenas testes negativos

```bash
python -m pytest -m negative
```

### Apenas testes de regressão

```bash
python -m pytest -m regression
```

### Execução com navegador visível

```bash
python -m pytest --headed
```

## Relatórios com Allure

### Gerar resultados

```bash
python -m pytest --alluredir=allure-results
```

### Gerar relatório

```bash
allure generate allure-results -o allure-report --clean
```

### Abrir relatório

```bash
allure open allure-report
```

## Cobertura da suite E2E

A suite atual cobre cenários de interface, validação e fluxo de autenticação da tela de login.

### Cenários cobertos

- Carregamento da página de login.
- Título da página.
- Visibilidade do campo de usuário.
- Visibilidade do campo de senha.
- Visibilidade do botão de envio.
- Ausência de erro global no primeiro acesso com contexto isolado.
- Validação de credenciais vazias.
- Validação de formato de e-mail inválido.
- Presença do link de recuperação de senha.
- Login com credenciais válidas, quando configuradas.
- Exibição de erro com credenciais inválidas.

## Organização dos testes

A suite usa marcações do Pytest para facilitar a execução segmentada.

- `@pytest.mark.e2e`: identifica os testes end-to-end.
- `@pytest.mark.smoke`: cobre verificações principais de carregamento e elementos críticos.
- `@pytest.mark.negative`: cobre cenários de validação e erro.
- `@pytest.mark.regression`: cobre fluxos mais amplos, como autenticação.

## Arquitetura

O projeto segue o padrão Page Object Model para separar regras de interação da camada de testes.

- `pages/`: contém os objetos de página e seletores.
- `tests/`: contém as suites e cenários automatizados.
- `utils/settings.py`: centraliza leitura de variáveis de ambiente.
- `conftest.py`: concentra fixtures compartilhadas.
- `pytest.ini`: concentra configurações e marcações do Pytest.

## Boas práticas adotadas

- Não versionar o arquivo `.env`.
- Usar `.env.example` como base para novos ambientes.
- Manter credenciais reais somente no ambiente local.
- Manter relatórios e artefatos gerados fora do Git.
- Centralizar parâmetros de execução em `settings.py`.
- Preferir seletores estáveis e alinhados ao DOM real da aplicação.

## Observações importantes

- O teste de login positivo depende de `USERNAME` e `PASSWORD` válidos.
- Sem credenciais válidas, o teste positivo pode ser ignorado pela suite.
- O teste de primeiro acesso usa contexto isolado para simular uma sessão limpa.
- O projeto gera relatório Allure, e não depende de report HTML adicional do Pytest.