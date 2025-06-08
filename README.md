# Sistema de Gestão de Hotel

Este é um projeto de um sistema de desktop para gestão de hotelaria, desenvolvido em Python com a biblioteca PyQt5 e um banco de dados relacional (MySQL/MariaDB). A aplicação permite gerenciar reservas, funcionários, serviços de quarto e status dos quartos.

---
## Configuração e Execução

Siga os passos abaixo para configurar e executar o projeto.

### 1. Configurar o Banco de Dados

É necessário ter um servidor MySQL ou MariaDB em execução.

* Primeiro, crie um novo banco de dados no seu servidor (ex: `hotel_db`).
* Em seguida, importe a estrutura e os dados para o banco que você criou usando o arquivo SQL gerado pelo programa. Use o seguinte comando no seu terminal, substituindo os valores necessários:
    ```bash
    mysql -u [seu_usuario] -p [nome_do_banco] < [nome_do_seu_arquivo].sql
    ```

### 2. Configurar Variáveis de Ambiente

Para a aplicação se conectar ao banco de dados, você precisa definir as credenciais em um arquivo `.env`.

* Na pasta raiz do projeto, crie um arquivo chamado `.env`.
* Adicione as seguintes variáveis a este arquivo, preenchendo com os seus dados:

    ```ini
    DB_HOST=localhost
    DB_USER=seu_usuario
    DB_PASSWORD=sua_senha
    DB_NAME=hotel_db
    ```

### 3. Preparar o Ambiente Python

O projeto utiliza um ambiente virtual para gerenciar suas dependências.

* **Crie o ambiente virtual:**
    ```bash
    python -m venv venv
    ```

* **Ative o ambiente:**
    * No Linux ou macOS:
        ```bash
        source venv/bin/activate
        ```
    * No Windows:
        ```bash
        venv\Scripts\activate
        ```

* **Instale as dependências:**
    *(Observação: Você precisa ter um arquivo `requirements.txt`. Se não tiver, gere-o com `pip freeze > requirements.txt`)*
    ```bash
    pip install -r requirements.txt
    ```

### 4. Executar o Projeto

Com o ambiente ativado e configurado, execute o arquivo principal para iniciar o sistema.
```bash
python main.py
