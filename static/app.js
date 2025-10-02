const form = document.getElementById('emailForm');
const results = document.getElementById('results');
const categoryEl = document.getElementById('category');
const confidenceEl = document.getElementById('confidence');
const strategyEl = document.getElementById('strategy');
const suggestedEl = document.getElementById('suggested');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const fd = new FormData(form);
  categoryEl.textContent = 'Processando...';
  confidenceEl.textContent = '...';
  strategyEl.textContent = '...';
  suggestedEl.textContent = '...';
  results.classList.remove('hidden');

  const resp = await fetch('/api/classify', {
    method: 'POST',
    body: fd
  });
  const data = await resp.json();

  categoryEl.textContent = data.category;
  confidenceEl.textContent = (data.confidence * 100).toFixed(0) + '%';
  strategyEl.textContent = data.strategy;
  suggestedEl.textContent = data.response;
});
