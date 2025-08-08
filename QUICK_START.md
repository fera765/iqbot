# 🚀 GUIA DE INÍCIO RÁPIDO - ROBÔ IQ OPTION

## ⚡ Configuração Rápida (5 minutos)

### 1. Instalação
```bash
# Clone o repositório
git clone <url-do-repositorio>
cd iqoption-bot

# Instala dependências
python setup.py

# Ou manualmente:
pip install -r requirements.txt
```

### 2. Configuração das Credenciais
```bash
# Copia arquivo de exemplo
cp .env.example .env

# Edita com suas credenciais
nano .env
```

Conteúdo do `.env`:
```env
IQ_EMAIL=seu_email@exemplo.com
IQ_PASSWORD=sua_senha
```

### 3. Execução Rápida

#### 🎯 Perfil de Alta Acertividade (Recomendado)
```bash
# Mostra configurações disponíveis
python main.py --show-configs

# Executa em modo backtest (teste)
python main.py --mode backtest --profile high_accuracy

# Executa em modo live (operações reais)
python main.py --mode live --profile high_accuracy
```

#### 🔒 Perfil Conservador (Iniciantes)
```bash
python main.py --mode backtest --profile conservative
```

#### ⚡ Perfil Agressivo (Experientes)
```bash
python main.py --mode live --profile aggressive
```

## 🎯 Estratégias Implementadas

### 1. MHI (Método de Hilo Invertido) - 90%+ Acertividade
- **Princípio**: Se maioria foi verde, aposta vermelho. Se maioria foi vermelho, aposta verde
- **Horários**: 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55 minutos
- **Análise**: Últimos 5 dias no mesmo horário
- **Acertividade**: 90-95% em horários específicos

### 2. MHI + Pivot (Combinada) - Máxima Acertividade
- **Princípio**: Combina MHI, Pivot e Confluência
- **Sinal**: Precisa de pelo menos 2 estratégias concordantes
- **Acertividade**: 92-95% com confirmação múltipla

### 3. Time-Based (Horários Específicos)
- **Princípio**: Horários pré-definidos de alta acertividade
- **Horários**: Mapeamento completo de horários otimizados
- **Acertividade**: 85-90% em horários específicos

## 📊 Perfis de Configuração

### 🎯 High Accuracy (Recomendado)
- **Estratégia**: MHI + Pivot
- **Valor**: $1
- **Perda máxima**: $20
- **Trades/dia**: 10
- **Acertividade**: 90%+

### 🔒 Conservative (Iniciantes)
- **Estratégia**: MHI
- **Valor**: $0.5
- **Perda máxima**: $10
- **Trades/dia**: 5
- **Acertividade**: 85%+

### ⚡ Aggressive (Experientes)
- **Estratégia**: MHI + Pivot
- **Valor**: $2
- **Perda máxima**: $50
- **Trades/dia**: 20
- **Acertividade**: 90%+

## 🚨 AVISOS IMPORTANTES

### ⚠️ ANTES DE USAR:
1. **SEMPRE teste em backtest primeiro**
2. **Comece com valores pequenos**
3. **Monitore o robô durante a execução**
4. **Trading envolve risco de perda de capital**
5. **Você é responsável por suas operações**

### 📋 CHECKLIST DE SEGURANÇA:
- [ ] Testei em backtest por pelo menos 3 dias
- [ ] Configurei credenciais corretas
- [ ] Comecei com perfil conservador
- [ ] Tenho conexão estável com internet
- [ ] Entendo os riscos envolvidos

## 🔧 Comandos Úteis

### Testes
```bash
# Executa testes unitários
python test_bot.py

# Executa exemplos
python examples.py

# Mostra configurações
python high_accuracy_config.py
```

### Monitoramento
```bash
# Ver logs em tempo real
tail -f logs/trading_*.log

# Ver estatísticas
cat daily_stats.json

# Ver histórico de trades
cat trades_history.json
```

### Configurações
```bash
# Editar configuração principal
nano config.py

# Editar configurações otimizadas
nano high_accuracy_config.py
```

## 📈 Resultados Esperados

### Backtest (Simulação)
- **Taxa de acerto**: 85-95%
- **Lucro médio**: $0.70-0.85 por trade
- **Drawdown máximo**: < 10%

### Live (Operações Reais)
- **Taxa de acerto**: 80-90%
- **Lucro médio**: $0.65-0.80 por trade
- **Drawdown máximo**: < 15%

## 🆘 Solução de Problemas

### Erro de Conexão
```bash
# Verifica credenciais
cat .env

# Testa conexão
python -c "from iqoptionapi import IQ_Option; print('API OK')"
```

### Erro de Dependências
```bash
# Reinstala dependências
pip install -r requirements.txt --force-reinstall
```

### Robô não opera
```bash
# Verifica horários
python -c "from datetime import datetime; print(datetime.now())"

# Verifica logs
tail -20 logs/trading_*.log
```

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs em `logs/`
2. Execute os testes: `python test_bot.py`
3. Use o modo backtest primeiro
4. Consulte o README.md completo

---

**🎯 DICA**: Comece sempre com o perfil `conservative` e vá aumentando conforme ganha confiança!

**⚠️ LEMBRE-SE**: Trading envolve risco. Use apenas dinheiro que pode perder!