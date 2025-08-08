# Robô de Trading Automatizado IQ Option (MHI)

## Descrição
Robô para operar na IQ Option usando a estratégia MHI, com CLI dinâmica, painel web Flask, gerenciamento de risco, logging e suporte a múltiplos pares.

## Estrutura de Pastas

```
trading_bot/
  __init__.py
  trading/
    __init__.py
    mhi.py
    iqapi.py
    risk.py
    manager.py
  cli/
    __init__.py
    main.py
  web/
    __init__.py
    app.py
    templates/
      dashboard.html
    static/
      style.css
  utils/
    __init__.py
    logger.py
    db.py
  config.py
logs/
  operations.log
bot.db
run.py
```

## Instalação

1. Clone o repositório
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure o arquivo `config.py` com seus dados de login demo IQ Option.

## Execução

- CLI:
  ```bash
  python run.py --cli
  ```
- Painel Web:
  ```bash
  python run.py --web
  ```

## Tecnologias
- iqoptionapi
- flask
- numpy, pandas
- click
- sqlite3

## Observações
- Apenas para conta de demonstração.
- Leia o código e configure os parâmetros de risco antes de operar.