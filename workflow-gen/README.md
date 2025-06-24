# Workflow Generator (CI/CD)

Ferramenta de linha de comando que automatize a geração de arquivos de configuração de workflow CI/CD para GitHub Actions, simplificando o processo de configuração para projetos novos e existentes.

## 1. Introdução

- **Público-Alvo:**

  - Desenvolvedores de software, engenheiros DevOps e qualquer pessoa que queira configurar rapidamente pipelines de CI/CD para seus projetos no GitHub.

- **Funcionalidades Principais:**
  - Detecção automática da linguagem do projeto, framework de teste e linter.
  - Geração de um arquivo .github/workflows/main.yml com etapas de CI/CD pré-definidas.
  - Arquitetura extensível baseada em plugins para suportar várias linguagens e frameworks.

## 2. Decições técnicas

- **Linguagem de Programação:** Python (devido à sua versatilidade, facilidade de uso e rico ecossistema de bibliotecas para criação de CLIs e manipulação de YAML).

- **Framework CLI:** Click (para criar uma interface de linha de comando amigável).

- **Biblioteca YAML:** PyYAML (para gerar arquivos de configuração YAML).

- **Arquitetura de Plugins:** A ferramenta usará uma arquitetura baseada em plugins para suportar várias linguagens e frameworks. Cada linguagem terá seu próprio plugin que implementa uma interface comum.

- **Testes:** pytest (para testes unitários).

**Links importantes**

- [Python](https://www.python.org/)
- [Click](https://click.palletsprojects.com/en/stable/)
- [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Pytest](https://docs.pytest.org/en/stable/)

## 3. Linguagens e Frameworks Suportados

- **Backend:**
  - Node.js (JavaScript)
  - Python
  - Java

- **Frontend:**
  - React (JavaScript)
  - Angular (TypeScript)
  - Vue.js (JavaScript)

## 4. Interface de Linha de Comando (CLI)

### 4.1 Instalação

Verifique se a versão de Python instalada é 3.7+:

  ```
  python3 --version
  ```

Clone o repositório:

  ```
   git clone <URL_DO_REPOSITORIO>
  ```

Navegue para o diretório do projeto:

  ```
  cd <NOME_DO_REPOSITORIO>
  ```

Instale as dependências:

  ```
  pip install -e .
  ```

Teste a instalação:

  ```
  workflow-gen --help
  ```

### 4.2 Especificação do comando

- **Nome do Comando:** workflow-gen (abreviação de "Workflow Generator")

- **Opções:**
  - `--project <caminho>`: Caminho para o diretório do projeto (para projetos existentes).
  - `--language <linguagem>`: Linguagem de programação do projeto (para projetos novos). Valores suportados: nodejs, python, java.
  - `--frontend <framework>`: Framework frontend do projeto (para projetos novos). Valores suportados: react, angular, vue.
  - `--test <framework>`: Framework de teste do projeto (para projetos novos). Valores suportados: jest, mocha, pytest, unittest, junit, karma, jasmine.
  - `--linter <linter>`: Linter do projeto (para projetos novos). Valores suportados: eslint, flake8, pylint, checkstyle.
  - `--output <caminho>`: Especifica um diretório diferente para armazenar o arquivo .github/workflows/main.yml.

- **Exemplos de Uso:**

  - Para um projeto existente:

  ```
    workflow-gen --project /caminho/para/meu/projeto
  ```

  - Para um novo projeto Python com pytest e flake8:

  ```
    workflow-gen --language python --test pytest --linter flake8
  ```

  - Para um novo projeto React com Jest e ESLint:

  ```
    workflow-gen --frontend react --test jest --linter eslint
  ```

- **Entrada Esperada:**

  - Projeto Existente: Caminho para um diretório de projeto válido com código-fonte.

  - Projeto Novo: Valores válidos para linguagem, framework de teste e linter.

- **Saída Esperada:**

  - Um arquivo `.github/workflows/main.yml` no diretório `.github/workflows` do projeto (ou no diretório especificado por `--output`).

  - Uma mensagem de sucesso indicando que o arquivo foi gerado.

  - Mensagens de erro se ocorrerem erros durante o processo (por exemplo, caminho de projeto inválido, linguagem não suportada).

## 5. Interface do Plugin

A interface do plugin definirá as seguintes funções:

- `detect_language(project_path)`: Detecta a linguagem de programação do projeto. Retorna o código da linguagem (por exemplo, "python", "nodejs", "java") ou `None` se a linguagem não puder ser detectada.

- `get_dependencies(project_path)`: Detecta o framework de teste e o linter usados no projeto. Retorna um dicionário com as chaves `test` e `linter` e os códigos correspondentes dos frameworks/linters (por exemplo, `{"test": "pytest", "linter": "flake8"}`).

- `generate_workflow(language, test, linter)`: Gera o conteúdo do arquivo `.github/workflows/main.yml`. Recebe a linguagem, o framework de teste e o linter como entrada e retorna uma string com o conteúdo YAML.

**Todos os plugins devem implementar esta interface!**

## 6. Estrutura do Projeto

```
workflow-gen/
├── src/              # Pacote Python
│   ├── __init__.py   # Inicialização do pacote e entrypoint da aplicação
│   ├── core.py       # Lógica principal da CLI
│   ├── plugins/      # Plugins para diferentes linguagens
│   │   ├── __init__.py  # Inicialização do pacote plugins
│   │   ├── java.py      # Plugin para Java
│   │   ├── nodejs.py    # Plugin para Node.js
│   │   └── python.py    # Plugin para Python
│   ├── exceptions/  # Exceções personalizadas
│   │── utils/      # Funções utilitárias
|   │── templates/  # Templates para os workflows
│       ├── java/
│       ├── nodejs/
│       └── python/
├── tests/              # Testes unitários
├── .gitignore          # Arquivos ignorados pelo Git
├── README.md           # Instruções e documentação do projeto
├── requirements.txt    # Dependências do projeto
├── install.sh        # Executável de instalação do comando
└── workflow-gen      # Script executável principal (gerado automaticamente pelo install.sh)
```

## 7. Estratégia de Testes

- Testes unitários para a lógica principal (detecção de linguagem, carregamento de plugins, etc.).
- Testes de integração para verificar a interação entre o núcleo e os plugins.
- Testes end-to-end para verificar o workflow completo, incluindo a execução dos workflows gerados no GitHub Actions.
- Testes manuais para garantir a usabilidade e a correção.
