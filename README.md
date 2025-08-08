# 🤖 Robô de Trading IQ Option

Um robô automatizado para operações na IQ Option usando análise técnica e gerenciamento de risco.

## 📋 Características

- **Múltiplas Estratégias**: RSI, MACD, Bandas de Bollinger e Random
- **Gerenciamento de Risco**: Stop loss, take profit e limites diários
- **Logs Coloridos**: Interface visual com cores no terminal
- **Histórico de Operações**: Salva todas as operações em arquivos JSON
- **Modo Backtest**: Simula operações sem usar dinheiro real
- **Horários de Trading**: Configurável para operar em horários específicos

## 🚀 Instalação

1. **Clone o repositório**:
```bash
git clone <url-do-repositorio>
cd iqoption-bot
```

2. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

3. **Configure suas credenciais**:
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais da IQ Option
```

## ⚙️ Configuração

### Credenciais (.env)
```env
IQ_EMAIL=seu_email@exemplo.com
IQ_PASSWORD=sua_senha
```

### Configurações do Robô (config.py)
```python
# Ativo para operar
ASSET = 'EURUSD'

# Valor por operação (em dólares)
AMOUNT = 1

# Estratégia: RSI, MACD, BOLLINGER, RANDOM
STRATEGY = 'RSI'

# Tempo de expiração (1 ou 5 minutos)
EXPIRATION = 1

# Gerenciamento de risco
MAX_DAILY_LOSS = 50      # Perda máxima diária
MAX_DAILY_TRADES = 20    # Máximo de operações por dia
STOP_LOSS = 10           # Stop loss por operação
TAKE_PROFIT = 15         # Take profit por operação
```

## 🎯 Estratégias Disponíveis

### 1. RSI (Relative Strength Index)
- **Sinal de Compra**: RSI < 30 (oversold)
- **Sinal de Venda**: RSI > 70 (overbought)
- **Configuração**: Período 14, níveis 30/70

### 2. MACD (Moving Average Convergence Divergence)
- **Sinal de Compra**: MACD cruza acima da Signal Line
- **Sinal de Venda**: MACD cruza abaixo da Signal Line
- **Configuração**: EMA 12/26, Signal 9

### 3. Bandas de Bollinger
- **Sinal de Compra**: Preço toca banda inferior
- **Sinal de Venda**: Preço toca banda superior
- **Configuração**: Período 20, 2 desvios padrão

### 4. Random (Para Testes)
- Gera sinais aleatórios para testes

## 🏃‍♂️ Como Usar

### Modo Live (Operações Reais)
```bash
python main.py --mode live
```

### Modo Backtest (Simulação)
```bash
python main.py --mode backtest --days 7
```

### Parâmetros Disponíveis
- `--mode`: `live` ou `backtest`
- `--days`: Número de dias para backtest
- `--config`: Arquivo de configuração personalizado

## 📊 Monitoramento

### Logs
- **Console**: Logs coloridos em tempo real
- **Arquivo**: Logs salvos em `logs/trading_YYYYMMDD.log`

### Estatísticas
- **Diárias**: Salvas em `daily_stats.json`
- **Histórico**: Salvas em `trades_history.json`

### Exemplo de Log
```
2024-01-15 10:30:15 - INFO - Connected to IQ Option
2024-01-15 10:30:16 - INFO - Balance: $100.00
2024-01-15 10:31:00 - INFO - SIGNAL: CALL on EURUSD | Strategy: RSI Strategy
2024-01-15 10:31:01 - INFO - Order placed: CALL EURUSD | Amount: $1 | ID: 12345
2024-01-15 10:32:00 - INFO - TRADE: CALL EURUSD | Amount: $1 | Profit: $0.80 | Result: WIN
```

## ⚠️ Avisos Importantes

1. **Risco Financeiro**: Trading envolve risco de perda de capital
2. **Teste Primeiro**: Use o modo backtest antes do live
3. **Valores Pequenos**: Comece com valores baixos
4. **Monitoramento**: Sempre monitore o robô em execução
5. **Responsabilidade**: Você é responsável por suas operações

## 🔧 Personalização

### Adicionar Nova Estratégia
1. Crie uma classe que herda de `TradingStrategy`
2. Implemente o método `calculate_signal()`
3. Adicione à função `get_strategy()` em `strategies.py`

### Exemplo:
```python
class MinhaEstrategia(TradingStrategy):
    def calculate_signal(self, candles):
        # Sua lógica aqui
        return 'call'  # ou 'put' ou None
```

## 📁 Estrutura do Projeto

```
iqoption-bot/
├── main.py              # Arquivo principal
├── config.py            # Configurações
├── trading_bot.py       # Classe principal do robô
├── strategies.py        # Estratégias de trading
├── risk_manager.py      # Gerenciamento de risco
├── logger.py           # Sistema de logs
├── requirements.txt    # Dependências
├── .env.example       # Exemplo de credenciais
├── README.md          # Documentação
└── logs/              # Pasta de logs
    └── trading_*.log
```

## 🐛 Solução de Problemas

### Erro de Conexão
- Verifique suas credenciais no arquivo `.env`
- Confirme se a IQ Option está acessível
- Verifique sua conexão com a internet

### Erro de Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Erro de API
- A API da IQ Option pode ter mudanças
- Verifique a versão da `iqoptionapi`
- Consulte a documentação oficial

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs em `logs/`
2. Teste com valores pequenos
3. Use o modo backtest primeiro
4. Consulte a documentação da API

## 📄 Licença

Este projeto é para fins educacionais. Use por sua conta e risco.

---

**⚠️ DISCLAIMER**: Este robô é fornecido "como está" sem garantias. Trading envolve risco de perda de capital. Use por sua conta e risco.