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
  div.textContent = `[${new Date(event.ts * 1000).toLocaleTimeString()}] ${event.type}: ${JSON.stringify(event)}`;
  eventsEl.prepend(div);
}

function connectWs() {
  const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
  const url = `${protocol}://${window.location.host}/ws`;
  const ws = new WebSocket(url);

  ws.onopen = () => {
    statusEl.textContent = 'Conectado';
    ws.send('hello');
  };

  ws.onmessage = (msg) => {
    const event = JSON.parse(msg.data);
    addEvent(event);

    if (event.type === 'bot_status' && event.status === 'connected') {
      statusEl.textContent = 'Bot conectado (' + event.account_type + ')';
    }

    if (event.type === 'strategy_selected' || event.type === 'strategy_switched') {
      if (event.asset) assetEl.textContent = event.asset;
      if (event.strategy) strategyEl.textContent = event.strategy;
      if (event.accuracy !== undefined) accuracyEl.textContent = event.accuracy;
      if (event.taken_trades !== undefined) takenTradesEl.textContent = event.taken_trades;
    }

    if (event.type === 'order_result') {
      if (event.pnl !== undefined) pnlEl.textContent = Number(event.pnl).toFixed(2);
    }
  };

  ws.onclose = () => {
    statusEl.textContent = 'Reconectando...';
    setTimeout(connectWs, 2000);
  };

  ws.onerror = () => {
    statusEl.textContent = 'Erro no WebSocket';
  };
}

connectWs();