# 🎰 Telegram Casino Simulator Bot (Conversion Focused)

Este é um bot de Telegram profissional, modular e focado em conversão de afiliados, simulando jogos de cassino populares para engajar usuários e redirecioná-los para casas reais.

## 🚀 Funcionalidades
- **Jogos Simulados:** Tigrinho (Slots), Aviator (Crash) e Roleta.
- **Sistema de Ganhos:** Taxa de vitória de 70-80% para manter o usuário engajado.
- **Limite de Conversão:** Ao atingir 200 SM (Simulated Money), o bot bloqueia os jogos e envia um CTA forte para a casa oficial.
- **Multilíngue:** Suporte completo para PT-BR e EN.
- **UX de Conversão:** Botões de "Depositar" e "Sacar" que levam diretamente ao link de afiliado.
- **Gamificação:** Sistema de bônus inicial, perfil e ranking global.

## 🛠️ Stack Técnica
| Componente | Tecnologia | Finalidade |
| :--- | :--- | :--- |
| **Linguagem** | Python 3.11+ | Core do bot |
| **Framework** | `aiogram 3.x` | Manipulação de API do Telegram (Assíncrono) |
| **Banco de Dados** | `SQLite` com `aiosqlite` | Persistência de dados de usuário |
| **Configuração** | `pydantic-settings` e `python-dotenv` | Gerenciamento seguro de variáveis de ambiente |

## 📂 Estrutura de Pastas
A estrutura modular facilita a manutenção e a adição de novos jogos ou funcionalidades:

```text
casino_bot/
├── src/
│   ├── database/    # Gerenciamento do SQLite (db.py)
│   ├── handlers/    # Lógica de comandos e mensagens (base.py, games.py, extra.py)
│   ├── utils/       # Textos e traduções (texts.py)
│   └── config.py    # Configurações globais
├── main.py          # Ponto de entrada do bot
├── requirements.txt # Dependências
├── .env.example     # Exemplo de variáveis de ambiente
└── README.md        # Documentação
```

## ⚙️ Configuração e Instalação
Para rodar o bot localmente, siga os passos:

1.  **Clone o projeto:**
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd casino_bot
    ```
2.  **Crie e ative o ambiente virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/Mac
    # venv\Scripts\activate   # Windows
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure as variáveis de ambiente:**
    Copie o arquivo de exemplo e preencha com seus dados:
    ```bash
    cp .env.example .env
    ```
    Edite o arquivo `.env` com:
    -   `TELEGRAM_TOKEN`: Token do seu bot (obtido no @BotFather).
    -   `LINK_BR_AFILIADO`: Seu link de afiliado para o público PT-BR.
    -   `LINK_EN_AFILIADO`: Seu link de afiliado para o público EN.

5.  **Execute o bot:**
    ```bash
    python main.py
    ```

## 🚢 Deploy (Pronto para Produção)

O bot é assíncrono e utiliza SQLite, o que o torna ideal para serviços de hospedagem gratuitos ou de baixo custo como Railway e Render.

### 1. Railway (Recomendado)
1.  Crie uma conta em [railway.app](https://railway.app/).
2.  Crie um novo projeto e conecte-o ao seu repositório GitHub.
3.  O Railway detectará o ambiente Python.
4.  Nas **Variables**, adicione as chaves do seu `.env` (`TELEGRAM_TOKEN`, `LINK_BR_AFILIADO`, `LINK_EN_AFILIADO`).
5.  O Railway irá construir e rodar o bot automaticamente.

### 2. Render (Free Tier)
1.  Crie uma conta em [render.com](https://render.com/).
2.  Crie um novo **Background Worker**.
3.  Conecte seu repositório.
4.  **Build Command:** `pip install -r requirements.txt`
5.  **Start Command:** `python main.py`
6.  Adicione as variáveis de ambiente nas configurações.

## 🎯 Estratégia de Conversão
O bot foi desenhado com uma alta taxa de vitória (70-80%) para criar um **viés de sorte** no usuário. Ao atingir o limite de R$ 200,00 SM, o jogo é bloqueado, e o usuário é confrontado com a mensagem de que precisa ir para a casa real para "sacar" ou "continuar jogando". Os botões de **Depositar** e **Sacar** no menu principal reforçam constantemente o CTA, transformando o bot em um funil de afiliação altamente otimizado.
