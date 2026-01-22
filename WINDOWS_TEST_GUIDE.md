# 🪟 Guia de Teste no Windows

Siga estes passos para rodar o bot no seu computador:

### 1. Pré-requisitos
- **Python 3.11 ou superior:** Se não tiver, baixe em [python.org](https://www.python.org/downloads/). 
  - *Importante:* Marque a opção **"Add Python to PATH"** durante a instalação.
- **Token do Telegram:** Crie um bot no [@BotFather](https://t.me/BotFather) e copie o token.

### 2. Preparação da Pasta
1. Extraia o arquivo `casino_bot.zip` em uma pasta de sua preferência (ex: `C:\Projetos\casino_bot`).
2. Abra o **Prompt de Comando (CMD)** ou **PowerShell** nessa pasta.

### 3. Configuração do Ambiente
No terminal, execute os seguintes comandos:

```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 4. Configurar Variáveis
1. Na pasta do projeto, encontre o arquivo `.env.example`.
2. Renomeie-o para `.env`.
3. Abra-o com o Bloco de Notas e preencha:
   - `TELEGRAM_TOKEN=seu_token_aqui`
   - `LINK_BR_AFILIADO=https://seu_link.com`
   - `LINK_EN_AFILIADO=https://your_link.com`

### 5. Rodar o Bot
Com o ambiente virtual ativado, execute:
```powershell
python main.py
```

---

### 🛠️ Dicas de Teste
- **Comando /start:** Inicie o bot e escolha o idioma.
- **Simular Ganhos:** Jogue `/tigrinho` ou `/aviator`. Como a taxa está em 75%, você chegará rápido aos 200 SM.
- **Validar Bloqueio:** Assim que atingir 200 SM, tente jogar novamente. O bot deve exibir o link de afiliado.
- **Banco de Dados:** Um arquivo `casino.db` será criado na pasta. Se quiser resetar os testes, basta deletar esse arquivo.
