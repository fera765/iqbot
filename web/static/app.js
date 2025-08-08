const statusEl = document.getElementById('status');
const assetEl = document.getElementById('asset');
const strategyEl = document.getElementById('strategy');
const accuracyEl = document.getElementById('accuracy');
const takenTradesEl = document.getElementById('taken_trades');
const pnlEl = document.getElementById('pnl');
const eventsEl = document.getElementById('events');

function addEvent(event) {
  const div = document.createElement('div');
  div.className = 'event';
  div.textContent = `[${new Date((event.ts || (Date.now()/1000)) * 1000).toLocaleTimeString()}] ${event.type}: ${JSON.stringify(event)}`;
  eventsEl.prepend(div);
}

function connectSSE() {
  const es = new EventSource('/stream');

  es.onopen = () => {
    statusEl.textContent = 'Conectado';
  };

  es.onmessage = (msg) => {
    if (!msg.data) return;
    let data = {};
    try { data = JSON.parse(msg.data); } catch (e) { return; }
    if (!data.type) return;
    addEvent(data);

    if (data.type === 'bot_status') {
      statusEl.textContent = 'Bot: ' + (data.status || 'desconhecido');
    }

    if (data.type === 'strategy_selected' || data.type === 'strategy_switched') {
      if (data.asset) assetEl.textContent = data.asset;
      if (data.strategy) strategyEl.textContent = data.strategy;
      if (data.accuracy !== undefined) accuracyEl.textContent = data.accuracy;
      if (data.taken_trades !== undefined) takenTradesEl.textContent = data.taken_trades;
    }

    if (data.type === 'order_result') {
      if (data.pnl !== undefined) pnlEl.textContent = Number(data.pnl).toFixed(2);
    }
  };

  es.onerror = () => {
    statusEl.textContent = 'Reconectando...';
    es.close();
    setTimeout(connectSSE, 2000);
  };
}

connectSSE();