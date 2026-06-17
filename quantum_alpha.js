/* ═══════════════════════════════════════════════════════════════════
   QUANTUM ALPHA AI — SIMPLIFIED INDIAN MARKET JS
   Currency: ₹ INR | Markets: NSE / BSE
═══════════════════════════════════════════════════════════════════ */

/* ── TICKER DATA ── */
let TICKER_DATA = [
  {sym:'RELIANCE',price:'₹1,329.00',chg:'+1.24%',up:true},
  {sym:'TCS',price:'₹3,503.45',chg:'+0.87%',up:true},
  {sym:'INFY',price:'₹1,578.60',chg:'-0.43%',up:false},
  {sym:'HDFCBANK',price:'₹1,921.75',chg:'+0.96%',up:true},
  {sym:'ICICIBANK',price:'₹1,434.20',chg:'+1.52%',up:true},
  {sym:'BHARTIARTL',price:'₹1,874.90',chg:'+2.14%',up:true},
  {sym:'HINDUNILVR',price:'₹2,369.50',chg:'-0.28%',up:false},
  {sym:'ITC',price:'₹417.85',chg:'+0.66%',up:true},
  {sym:'SBIN',price:'₹823.15',chg:'+1.83%',up:true},
  {sym:'WIPRO',price:'₹245.60',chg:'-0.51%',up:false},
  {sym:'BAJFINANCE',price:'₹8,842.70',chg:'+2.87%',up:true},
  {sym:'SUNPHARMA',price:'₹1,695.30',chg:'+1.37%',up:true},
  {sym:'ONGC',price:'₹256.45',chg:'-0.62%',up:false},
  {sym:'NIFTY 50',price:'24,512.35',chg:'+0.72%',up:true},
  {sym:'SENSEX',price:'80,824.60',chg:'+0.68%',up:true},
];

/* ── WATCHLIST DATA (default, updated from API) ── */
let WATCHLIST_DATA = [
  {sym:'RELIANCE.NS',name:'Reliance Industries',price:'₹1,329.00',chg:'+1.24%',up:true,pred:'₹1,354.20',conf:'87.3%',sent:'Bullish',rec:'BUY'},
  {sym:'TCS.NS',name:'Tata Consultancy Services',price:'₹3,503.45',chg:'+0.87%',up:true,pred:'₹3,598.70',conf:'91.2%',sent:'Very Bullish',rec:'BUY'},
  {sym:'HDFCBANK.NS',name:'HDFC Bank Ltd.',price:'₹1,921.75',chg:'+0.96%',up:true,pred:'₹1,968.90',conf:'85.7%',sent:'Bullish',rec:'BUY'},
  {sym:'ICICIBANK.NS',name:'ICICI Bank Ltd.',price:'₹1,434.20',chg:'+1.52%',up:true,pred:'₹1,478.60',conf:'83.4%',sent:'Bullish',rec:'BUY'},
  {sym:'INFY.NS',name:'Infosys Ltd.',price:'₹1,578.60',chg:'-0.43%',up:false,pred:'₹1,569.30',conf:'74.8%',sent:'Neutral',rec:'HOLD'},
  {sym:'BHARTIARTL.NS',name:'Bharti Airtel Ltd.',price:'₹1,874.90',chg:'+2.14%',up:true,pred:'₹1,934.80',conf:'82.1%',sent:'Bullish',rec:'BUY'},
  {sym:'BAJFINANCE.NS',name:'Bajaj Finance Ltd.',price:'₹8,842.70',chg:'+2.87%',up:true,pred:'₹9,102.40',conf:'88.6%',sent:'Bullish',rec:'BUY'},
];

/* ── NEWS DATA (default, updated from API) ── */
let NEWS_DATA = [
  {title:'Reliance Jio Announces 5G Expansion Across 500 Indian Cities',source:'Economic Times',time:'12 min ago',sent:'pos',score:'+0.84'},
  {title:'RBI Holds Repo Rate at 6.5%, Signals Positive Growth Outlook',source:'Business Standard',time:'28 min ago',sent:'pos',score:'+0.67'},
  {title:'TCS Wins ₹15,000 Cr AI Transformation Deal from Indian Govt.',source:'Mint',time:'45 min ago',sent:'pos',score:'+0.91'},
  {title:'HDFC Bank Reports Record Q4 Profit on Strong Retail Lending',source:'Moneycontrol',time:'1 hr ago',sent:'pos',score:'+0.79'},
  {title:'Tata Motors EV Sales Surge 48% — Leads Indian EV Market',source:'LiveMint',time:'2 hr ago',sent:'pos',score:'+0.88'},
  {title:'Adani Group Faces Regulatory Scrutiny Over Port Expansion Plans',source:'NDTV Profit',time:'3 hr ago',sent:'neg',score:'-0.52'},
];

/* ── HEATMAP DATA (default) ── */
let HEATMAP_DATA = [
  {sector:'IT Services',cls:'bull-str',stocks:[{s:'TCS',c:'+0.87%'},{s:'INFY',c:'-0.43%'},{s:'WIPRO',c:'-0.51%'}]},
  {sector:'Banking',cls:'bull',stocks:[{s:'HDFCBANK',c:'+0.96%'},{s:'ICICIBANK',c:'+1.52%'},{s:'SBIN',c:'+1.83%'}]},
  {sector:'FMCG',cls:'neutral',stocks:[{s:'HINDUNILVR',c:'-0.28%'},{s:'ITC',c:'+0.66%'},{s:'NESTLEIND',c:'+0.41%'}]},
  {sector:'Pharma',cls:'bull',stocks:[{s:'SUNPHARMA',c:'+1.37%'},{s:'DRREDDY',c:'+0.78%'},{s:'CIPLA',c:'+0.54%'}]},
  {sector:'Energy',cls:'neutral',stocks:[{s:'RELIANCE',c:'+1.24%'},{s:'ONGC',c:'-0.62%'},{s:'NTPC',c:'+0.33%'}]},
  {sector:'Automobile',cls:'bull-str',stocks:[{s:'TATAMOTORS',c:'+3.12%'},{s:'MARUTI',c:'+0.94%'},{s:'M&M',c:'+2.18%'}]},
  {sector:'Telecom',cls:'bull',stocks:[{s:'BHARTIARTL',c:'+2.14%'},{s:'IDEA',c:'-1.67%'},{s:'INDUSTOWER',c:'+0.44%'}]},
  {sector:'Metals',cls:'bear',stocks:[{s:'TATASTEEL',c:'-1.34%'},{s:'JSWSTEEL',c:'-0.88%'},{s:'HINDALCO',c:'-0.54%'}]},
  {sector:'Finance',cls:'bull',stocks:[{s:'BAJFINANCE',c:'+2.87%'},{s:'HDFCLIFE',c:'+1.14%'},{s:'AXISBANK',c:'+0.74%'}]},
];

/* ── GLOBAL STATE ── */
let currentAnalysis = null;
let aiResponding = false;

/* ════════════════════
   TICKER TAPE
════════════════════ */
function buildTicker() {
  const inner = document.getElementById('tickerInner');
  if (!inner) return;
  const items = [...TICKER_DATA, ...TICKER_DATA].map(t => `
    <div class="ticker-item">
      <span class="sym">${t.sym}</span>
      <span>${t.price}</span>
      <span class="${t.up ? 'up' : 'dn'}">${t.chg}</span>
    </div>
    <span class="ticker-sep">|</span>
  `).join('');
  inner.innerHTML = items;
}

/* ════════════════════
   NAVIGATION
════════════════════ */
function showPage(pageId, navEl) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(n => n.classList.remove('active'));
  const page = document.getElementById('page-' + pageId);
  if (page) page.classList.add('active');
  if (navEl) navEl.classList.add('active');

  // Always try to init charts when switching to each section
  if (pageId === 'technical') {
    if (currentAnalysis) {
      updateTechnicalText();
      // Use rAF so page is fully visible before Chart.js renders
      requestAnimationFrame(() => {
        const dates = currentAnalysis.dates || [];
        renderRSIChart(dates, currentAnalysis.indicators?.rsi || []);
        renderCandlestick(currentAnalysis.candles || []);
      });
    }
  }
  if (pageId === 'sentiment')      { renderSentiment(); }
  if (pageId === 'watchlist')      { renderWatchlist(); }
  if (pageId === 'heatmap')        { renderHeatmap(); }
  if (pageId === 'recommendation') { if (currentAnalysis) renderScoreRings('rec'); }
  if (pageId === 'prediction')     { if (currentAnalysis) { renderPredChart(); renderScoreRings('score'); } }
}


function quickAnalyze(sym) {
  const input = document.getElementById('stockSymbol');
  if (input) { input.value = ''; input.value = sym.toUpperCase(); }
  runAnalysis();
  // Stay on dashboard so user sees price immediately
  showPage('dashboard', document.querySelector('.nav-btn[onclick*="dashboard"]'));
}


/* ════════════════════
   MAIN CHART (price history)
════════════════════ */
let mainChartInst = null;
function renderMainChart(labels, prices) {
  const ctx = document.getElementById('mainChart');
  if (!ctx) return;
  if (mainChartInst) { mainChartInst.destroy(); mainChartInst = null; }

  const cleanPrices = prices.map(v => (v === null || v === undefined || isNaN(v)) ? null : v);

  mainChartInst = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Price (₹)',
        data: cleanPrices,
        borderColor: '#00e5c3',
        borderWidth: 2,
        fill: true,
        backgroundColor: (ctx) => {
          const gradient = ctx.chart.ctx.createLinearGradient(0, 0, 0, 280);
          gradient.addColorStop(0, 'rgba(0,229,195,0.18)');
          gradient.addColorStop(1, 'rgba(0,229,195,0)');
          return gradient;
        },
        tension: 0.4, pointRadius: 0, spanGaps: true
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(10,18,40,0.95)',
          borderColor: 'rgba(0,229,195,0.3)', borderWidth: 1,
          bodyColor: '#00e5c3', bodyFont: { family: 'JetBrains Mono', size: 13 },
          titleColor: '#94a3b8',
          callbacks: { label: ctx => ` ₹${Number(ctx.raw).toLocaleString('en-IN', {minimumFractionDigits:2})}` }
        }
      },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#475569', font: { size: 10 }, maxTicksLimit: 8 }, border: { color: 'rgba(255,255,255,0.06)' } },
        y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#475569', font: { family: 'JetBrains Mono', size: 10 }, callback: v => '₹' + Number(v).toLocaleString('en-IN') }, border: { color: 'rgba(255,255,255,0.06)' } }
      },
      animation: { duration: 600 }
    }
  });
}

/* ════════════════════
   PREDICTION CHART
════════════════════ */
let predChartInst = null;
function renderPredChart() {
  const ctx = document.getElementById('predChart');
  if (!ctx || !currentAnalysis) return;
  if (predChartInst) { predChartInst.destroy(); predChartInst = null; }

  const data = currentAnalysis;
  const labels = data.dates || [];
  const actual = data.prices || [];
  const predicted = data.predicted || [];
  const forecast = data.forecast || [];

  // Build future labels
  const futureDates = [];
  const lastDate = labels[labels.length - 1] || 'Today';
  for (let i = 1; i <= forecast.length; i++) {
    futureDates.push(`+${i}d`);
  }

  const allLabels = [...labels.slice(-60), ...futureDates];
  const actualFull   = [...actual.slice(-60), ...new Array(futureDates.length).fill(null)];
  const predFull     = [...predicted.slice(-60), ...new Array(futureDates.length).fill(null)];
  const forecastFull = [...new Array(actual.slice(-60).length - 1).fill(null), actual.slice(-60)[actual.slice(-60).length - 1], ...forecast];

  const isIndian = data.symbol && (data.symbol.endsWith('.NS') || data.symbol.endsWith('.BO'));

  predChartInst = new Chart(ctx, {
    type: 'line',
    data: {
      labels: allLabels,
      datasets: [
        { label: 'Actual Price', data: actualFull, borderColor: '#00e5c3', borderWidth: 2, fill: false, tension: 0.4, pointRadius: 0, spanGaps: true },
        { label: 'LSTM Prediction', data: predFull, borderColor: '#a855f7', borderWidth: 1.5, borderDash: [4,3], fill: false, tension: 0.4, pointRadius: 0, spanGaps: true },
        { label: '10-Day Forecast', data: forecastFull, borderColor: '#22c55e', borderWidth: 2, fill: true, backgroundColor: 'rgba(34,197,94,0.08)', tension: 0.4, pointRadius: 3, pointBackgroundColor: '#22c55e', spanGaps: false }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 11 }, boxWidth: 16 } },
        tooltip: {
          backgroundColor: 'rgba(10,18,40,0.95)', borderColor: 'rgba(0,229,195,0.3)', borderWidth: 1,
          bodyColor: '#fff', titleColor: '#94a3b8', bodyFont: { family: 'JetBrains Mono', size: 12 },
          callbacks: { label: ctx => ` ${ctx.dataset.label}: ₹${ctx.raw ? Number(ctx.raw).toLocaleString('en-IN', {minimumFractionDigits:2}) : ''}` }
        }
      },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#475569', font: { size: 10 }, maxTicksLimit: 10 }, border: { color: 'rgba(255,255,255,0.06)' } },
        y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#475569', font: { family: 'JetBrains Mono', size: 10 }, callback: v => '₹' + Number(v).toLocaleString('en-IN') }, border: { color: 'rgba(255,255,255,0.06)' } }
      }
    }
  });
}

/* ════════════════════
   RSI CHART
════════════════════ */
let rsiChartInst = null;
function renderRSIChart(labels, rsiData) {
  const ctx = document.getElementById('rsiChart');
  if (!ctx) return;
  if (rsiChartInst) { rsiChartInst.destroy(); rsiChartInst = null; }

  const clean = rsiData.map(v => (v === null || v === undefined || isNaN(v)) ? null : v);

  rsiChartInst = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'RSI', data: clean,
        borderColor: '#f59e0b', borderWidth: 2, fill: false, tension: 0.4, pointRadius: 0, spanGaps: true
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { backgroundColor: 'rgba(10,18,40,0.95)', bodyFont: { family: 'JetBrains Mono' }, callbacks: { label: ctx => ` RSI: ${ctx.raw?.toFixed(1)}` } },
        annotation: {}
      },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#475569', font: { size: 10 }, maxTicksLimit: 8 }, border: { color: 'rgba(255,255,255,0.06)' } },
        y: {
          min: 0, max: 100,
          grid: { color: 'rgba(255,255,255,0.04)' },
          ticks: { color: '#475569', font: { family: 'JetBrains Mono', size: 10 } },
          border: { color: 'rgba(255,255,255,0.06)' }
        }
      }
    }
  });
}

/* ════════════════════
   CANDLESTICK (LightweightCharts)
════════════════════ */
let candleSeries = null;
function renderCandlestick(candles) {
  const container = document.getElementById('candlestickContainer');
  if (!container || !candles || !candles.length) return;

  container.innerHTML = '';
  const chart = LightweightCharts.createChart(container, {
    width: container.clientWidth,
    height: 280,
    layout: { background: { color: 'transparent' }, textColor: '#94a3b8' },
    grid: { vertLines: { color: 'rgba(255,255,255,0.04)' }, horzLines: { color: 'rgba(255,255,255,0.04)' } },
    crosshair: { mode: LightweightCharts.CrosshairMode.Normal },
    rightPriceScale: { borderColor: 'rgba(255,255,255,0.06)' },
    timeScale: { borderColor: 'rgba(255,255,255,0.06)', timeVisible: true }
  });

  candleSeries = chart.addCandlestickSeries({
    upColor: '#22c55e', downColor: '#ef4444',
    borderUpColor: '#22c55e', borderDownColor: '#ef4444',
    wickUpColor: '#22c55e', wickDownColor: '#ef4444'
  });

  const validCandles = candles.filter(c => c && c.time && !isNaN(c.open) && !isNaN(c.high) && !isNaN(c.low) && !isNaN(c.close));
  candleSeries.setData(validCandles);
  chart.timeScale().fitContent();
}

/* ════════════════════
   SCORE RINGS
════════════════════ */
let scoreRingInsts = {};
function drawRing(canvasId, numId, value, color) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  if (scoreRingInsts[canvasId]) {
    scoreRingInsts[canvasId].destroy();
  }
  const pct = Math.max(0, Math.min(100, value));
  scoreRingInsts[canvasId] = new Chart(canvas, {
    type: 'doughnut',
    data: {
      datasets: [{
        data: [pct, 100 - pct],
        backgroundColor: [color, 'rgba(255,255,255,0.06)'],
        borderWidth: 0
      }]
    },
    options: {
      responsive: false, cutout: '72%',
      plugins: { legend: { display: false }, tooltip: { enabled: false } },
      animation: { duration: 800 }
    }
  });
  const numEl = document.getElementById(numId);
  if (numEl) { numEl.textContent = Math.round(pct) + '%'; numEl.style.color = color; }
}

function renderScoreRings(prefix) {
  if (!currentAnalysis) return;
  const conf = parseFloat(currentAnalysis.kpis?.conf) || 75;
  const rsiScore = 100 - Math.abs(50 - (currentAnalysis.indicators?.rsi?.slice(-1)[0] || 50));
  const sentScore = (currentAnalysis.sentiment?.score || 0) * 50 + 50;
  const mktScore = currentAnalysis.kpis?.perf_val >= 0 ? 70 : 40;

  drawRing(`${prefix}Ring1`, `${prefix}Num1`, rsiScore,      '#4cc9f0');
  drawRing(`${prefix}Ring2`, `${prefix}Num2`, sentScore,     '#a855f7');
  drawRing(`${prefix}Ring3`, `${prefix}Num3`, conf,          '#00e5c3');
  drawRing(`${prefix}Ring4`, `${prefix}Num4`, mktScore,      '#f59e0b');
}

/* ════════════════════
   SENTIMENT TREND CHART
════════════════════ */
let sentTrendInst = null;
function renderSentTrend() {
  const ctx = document.getElementById('sentTrendChart');
  if (!ctx) return;
  if (sentTrendInst) { sentTrendInst.destroy(); sentTrendInst = null; }

  const labels = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
  const scores = [0.15, 0.32, 0.08, -0.12, 0.42, 0.55, 0.38];

  sentTrendInst = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Sentiment Score',
        data: scores,
        backgroundColor: scores.map(v => v >= 0 ? 'rgba(34,197,94,0.6)' : 'rgba(239,68,68,0.6)'),
        borderColor: scores.map(v => v >= 0 ? '#22c55e' : '#ef4444'),
        borderWidth: 1, borderRadius: 4
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#475569', font: { size: 10 } } },
        y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#475569', font: { family: 'JetBrains Mono', size: 10 } }, min: -1, max: 1 }
      }
    }
  });
}

/* ════════════════════
   SENTIMENT PAGE
════════════════════ */
function renderSentiment() {
  renderSentTrend();
  // Update bars from current analysis
  if (currentAnalysis && currentAnalysis.sentiment) {
    const s = currentAnalysis.sentiment;
    document.getElementById('bullBar').style.width = (s.bullish_pct || 0) + '%';
    document.getElementById('neuBar').style.width  = (s.neutral_pct || 0) + '%';
    document.getElementById('bearBar').style.width = (s.bearish_pct || 0) + '%';
    document.getElementById('bullPct').textContent = (s.bullish_pct || 0) + '%';
    document.getElementById('neuPct').textContent  = (s.neutral_pct || 0) + '%';
    document.getElementById('bearPct').textContent = (s.bearish_pct || 0) + '%';
    const sc = s.score || 0;
    const scoreEl = document.getElementById('sentScore');
    scoreEl.textContent = (sc > 0 ? '+' : '') + Number(sc).toFixed(3);
    scoreEl.style.color = sc > 0 ? 'var(--green)' : (sc < 0 ? 'var(--red)' : 'var(--muted)');
  }

  // News
  buildNewsFeed();
}

function buildNewsFeed() {
  const feed = document.getElementById('newsFeed');
  if (!feed) return;
  let news = NEWS_DATA;
  if (currentAnalysis?.sentiment?.news?.length) news = currentAnalysis.sentiment.news;

  if (!news.length) {
    feed.innerHTML = '<div style="color:var(--muted);font-size:13px;text-align:center;padding:24px">No news available</div>';
    return;
  }

  feed.innerHTML = news.slice(0,8).map(n => `
    <div class="news-card">
      <span class="news-tag ${n.sent}">${n.sent === 'pos' ? '📈 BULLISH' : n.sent === 'neg' ? '📉 BEARISH' : '➖ NEUTRAL'}</span>
      <div class="news-body">
        <div class="news-headline">${n.title}</div>
        <div class="news-meta">${n.source} · ${n.time}</div>
      </div>
      <div class="news-score" style="color:${n.sent === 'pos' ? 'var(--green)' : n.sent === 'neg' ? 'var(--red)' : 'var(--muted)'}">${n.score || ''}</div>
    </div>
  `).join('');
}

/* ════════════════════
   WATCHLIST
════════════════════ */
function renderWatchlist() {
  const tbody = document.getElementById('watchBody');
  if (!tbody) return;
  let data = WATCHLIST_DATA;
  if (currentAnalysis?.watchlist?.length) data = currentAnalysis.watchlist;

  tbody.innerHTML = data.map(r => `
    <tr>
      <td>
        <div class="sym-cell">
          <span class="sym-name" onclick="quickAnalyze('${r.sym.replace('.NS','').replace('.BO','')}')">${r.sym.replace('.NS','').replace('.BO','')}</span>
          <span class="sym-full">${r.name}</span>
        </div>
      </td>
      <td><span class="price-val">${r.price}</span></td>
      <td><span class="${r.up ? 'chg-up' : 'chg-dn'}">${r.up ? '▲' : '▼'} ${r.chg}</span></td>
      <td><span class="price-val" style="color:var(--cyan)">${r.pred}</span></td>
      <td><span style="font-family:'JetBrains Mono',monospace;font-size:12px">${r.conf}</span></td>
      <td><span style="font-size:12px;color:${r.up ? 'var(--green)' : 'var(--red)'}">${r.sent}</span></td>
      <td><span class="rec-badge ${r.rec}">${r.rec}</span></td>
    </tr>
  `).join('');
}

/* ════════════════════
   HEATMAP
════════════════════ */
function renderHeatmap() {
  const grid = document.getElementById('heatmapGrid');
  if (!grid) return;
  let data = HEATMAP_DATA;
  if (currentAnalysis?.heatmap?.length) data = currentAnalysis.heatmap;

  grid.innerHTML = data.map(h => `
    <div class="heat-cell ${h.cls}">
      <div class="heat-sector">${h.sector}</div>
      <div class="heat-stocks">
        ${h.stocks.map(s => `
          <div class="heat-stock" onclick="quickAnalyze('${s.s}')">
            <span class="heat-sym">${s.s}</span>
            <span class="heat-chg">${s.c}</span>
          </div>
        `).join('')}
      </div>
    </div>
  `).join('');
}

/* ════════════════════
   TECHNICAL CHARTS
════════════════════ */
/* ════════════════════
   TECHNICAL — TEXT VALUES (always update, no canvas needed)
════════════════════ */
function updateTechnicalText() {
  if (!currentAnalysis) return;

  const rsi  = (currentAnalysis.indicators?.rsi  || []).filter(v => v !== null && !isNaN(v)).slice(-1)[0];
  const macd = (currentAnalysis.indicators?.macd || []).filter(v => v !== null && !isNaN(v)).slice(-1)[0];
  const ma50  = (currentAnalysis.indicators?.ma50  || []).filter(v => v !== null && !isNaN(v)).slice(-1)[0];
  const ma200 = (currentAnalysis.indicators?.ma200 || []).filter(v => v !== null && !isNaN(v)).slice(-1)[0];

  if (rsi !== undefined) {
    const rsiEl = document.getElementById('rsiVal');
    const rsiDescEl = document.getElementById('rsiDesc');
    if (rsiEl) { rsiEl.textContent = rsi.toFixed(1); rsiEl.style.color = rsi > 70 ? 'var(--red)' : rsi < 30 ? 'var(--green)' : 'var(--yellow)'; }
    if (rsiDescEl) rsiDescEl.textContent = rsi > 70 ? '⚠️ Overbought — price may drop soon' : rsi < 30 ? '✅ Oversold — possible buying opportunity' : '✅ Neutral zone — healthy momentum';
  }
  if (macd !== undefined) {
    const macdEl = document.getElementById('macdVal');
    const macdDescEl = document.getElementById('macdDesc');
    if (macdEl) { macdEl.textContent = macd.toFixed(2); macdEl.style.color = macd > 0 ? 'var(--green)' : 'var(--red)'; }
    if (macdDescEl) macdDescEl.textContent = macd > 0 ? '📈 Bullish momentum — uptrend signal' : '📉 Bearish momentum — downtrend signal';
  }
  if (ma50 !== undefined) {
    const el = document.getElementById('ma50Val');
    if (el) el.textContent = '₹' + Number(ma50).toLocaleString('en-IN', {minimumFractionDigits:2});
  }
  if (ma200 !== undefined) {
    const el = document.getElementById('ma200Val');
    if (el) el.textContent = '₹' + Number(ma200).toLocaleString('en-IN', {minimumFractionDigits:2});
  }
}

/* ════════════════════
   TECHNICAL CHARTS (canvas — needs page visible)
════════════════════ */
function renderTechnicalCharts() {
  if (!currentAnalysis) return;
  updateTechnicalText();
  // Only render canvas charts when page is actually visible
  const techPage = document.getElementById('page-technical');
  const isVisible = techPage && techPage.classList.contains('active');
  if (isVisible) {
    const dates = currentAnalysis.dates || [];
    renderRSIChart(dates, currentAnalysis.indicators?.rsi || []);
    renderCandlestick(currentAnalysis.candles || []);
  }
}



/* ════════════════════
   KPI UPDATE
════════════════════ */
function updateKPIs(data) {
  if (!data?.kpis) return;
  const k = data.kpis;

  setText('kpi-price', k.price || '—');
  setText('kpi-pred',  k.pred  || '—');
  setText('kpi-conf',  k.conf  || '—');
  setText('kpi-sent',  k.sent  || '—');

  const perfEl = document.getElementById('kpi-perf');
  if (perfEl) {
    perfEl.textContent = k.perf || '—';
    perfEl.style.color = (k.perf_val || 0) >= 0 ? 'var(--green)' : 'var(--red)';
  }

  const riskEl = document.getElementById('kpi-risk');
  if (riskEl) {
    riskEl.textContent = k.risk || '—';
    riskEl.style.color = k.risk === 'Low' ? 'var(--green)' : k.risk === 'Medium' ? 'var(--yellow)' : 'var(--red)';
  }

  // Update ticker tape with live price for this stock
  if (data.symbol && k.price) {
    const cleanSym = data.symbol.replace('.NS','').replace('.BO','');
    const isUp = (k.perf_val || 0) >= 0;
    // Update TICKER_DATA for this symbol
    const existing = TICKER_DATA.find(t => t.sym === cleanSym);
    if (existing) {
      existing.price = k.price;
      existing.chg   = k.perf || '+0.00%';
      existing.up    = isUp;
    } else {
      TICKER_DATA.unshift({ sym: cleanSym, price: k.price, chg: k.perf || '+0.00%', up: isUp });
    }
    buildTicker(); // rebuild ticker tape with updated price
  }
}


function setText(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}

/* ════════════════════
   DECISION BANNER UPDATE
════════════════════ */
function updateDecision(data) {
  if (!data?.recommendation) return;
  const rec = data.recommendation;
  const decision = rec.decision || 'HOLD';
  const reasoning = rec.reasoning || '';

  const isBuy  = decision.includes('BUY');
  const isSell = decision.includes('SELL');
  const cls    = isBuy ? 'buy' : isSell ? 'sell' : 'hold';
  const icon   = isBuy ? '🚀' : isSell ? '🔻' : '🤝';

  ['decisionBanner', 'recBanner'].forEach(id => {
    const el = document.getElementById(id);
    if (el) { el.className = `decision-banner ${cls}`; }
  });
  ['decisionVerdict', 'recVerdict'].forEach(id => setText(id, decision));
  ['decisionReason',  'recReason' ].forEach(id => setText(id, reasoning));
  ['decisionIcon',    'recIcon'   ].forEach(id => setText(id, icon));
}

/* ════════════════════
   ANALYSIS RUNNER
════════════════════ */
const STEPS = [
  'Connecting to NSE/BSE servers...',
  'Downloading price history...',
  'Calculating RSI & MACD...',
  'Training LSTM neural network...',
  'Analyzing news sentiment...',
  'Generating AI recommendation...',
  'Done! ✅'
];

function runAnalysis() {
  const input = document.getElementById('stockSymbol');
  let sym = (input?.value || '').trim();
  if (!sym) { showToast('⚠️ Please enter a stock symbol like RELIANCE or TCS'); return; }

  const overlay = document.getElementById('loadingOverlay');
  const stepEl  = document.getElementById('loadingStep');
  const barEl   = document.getElementById('loadingBar');
  const btn      = document.getElementById('analyzeBtn');

  overlay.classList.add('show');
  btn.disabled = true;
  btn.innerHTML = '<i class="bi bi-hourglass-split"></i> Analyzing...';

  let stepIdx = 0;
  const interval = setInterval(() => {
    if (stepIdx < STEPS.length - 1) {
      stepEl.textContent = STEPS[stepIdx];
      barEl.style.width = ((stepIdx + 1) / STEPS.length * 85) + '%';
      stepIdx++;
    }
  }, 350);

  fetch(`/api/analyze?symbol=${encodeURIComponent(sym)}`)
    .then(r => {
      if (!r.ok) throw new Error(`Stock "${sym}" not found. Try RELIANCE, TCS, INFY etc.`);
      return r.json();
    })
    .then(data => {
      clearInterval(interval);
      barEl.style.width = '100%';
      stepEl.textContent = '✅ Analysis complete!';

      currentAnalysis = data;

      // Update news and watchlist from server
      if (data.sentiment?.news?.length)  NEWS_DATA      = data.sentiment.news;
      if (data.watchlist?.length)        WATCHLIST_DATA = data.watchlist;
      if (data.heatmap?.length)          HEATMAP_DATA   = data.heatmap;

      setTimeout(() => {
        overlay.classList.remove('show');
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-cpu"></i> Analyze';

        const displaySym = data.symbol?.replace('.NS','').replace('.BO','') || sym;
        setText('chartStock', displaySym);
        setText('dashSubtitle', `Live AI analysis for ${data.companyName || displaySym} • ${new Date().toLocaleTimeString('en-IN')}`);

        // Update all widgets
        updateKPIs(data);
        updateDecision(data);

        // Render main chart
        renderMainChart(data.dates || [], data.prices || []);

        // Always pre-render ALL sections so navigating to them shows data immediately
        renderTechnicalCharts();
        renderSentiment();
        renderWatchlist();
        renderHeatmap();
        renderPredChart();
        renderScoreRings('score');
        renderScoreRings('rec');

        showToast(`✅ Analysis complete for ${displaySym}`);
      }, 400);
    })
    .catch(err => {
      clearInterval(interval);
      overlay.classList.remove('show');
      btn.disabled = false;
      btn.innerHTML = '<i class="bi bi-cpu"></i> Analyze';
      showToast('⚠️ ' + err.message);
    });
}

/* ════════════════════
   AI CHAT
════════════════════ */
function sendChat() {
  if (aiResponding) return;
  const input = document.getElementById('chatInput');
  const msg = input.value.trim();
  if (!msg) return;
  input.value = '';

  const messages = document.getElementById('chatMessages');
  messages.innerHTML += `
    <div class="chat-msg user">
      <div class="chat-av">U</div>
      <div>
        <div class="chat-bubble">${msg}</div>
        <div class="chat-time">Just now</div>
      </div>
    </div>`;
  messages.scrollTop = messages.scrollHeight;
  aiResponding = true;

  messages.innerHTML += `
    <div class="chat-msg ai" id="typingMsg">
      <div class="chat-av">Q</div>
      <div>
        <div class="chat-bubble">
          <div class="typing"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div>
        </div>
      </div>
    </div>`;
  messages.scrollTop = messages.scrollHeight;

  const sym = currentAnalysis?.symbol || 'RELIANCE.NS';
  fetch(`/api/chat?message=${encodeURIComponent(msg)}&symbol=${sym}`)
    .then(r => r.json())
    .then(data => {
      document.getElementById('typingMsg')?.remove();
      messages.innerHTML += `
        <div class="chat-msg ai">
          <div class="chat-av">Q</div>
          <div>
            <div class="chat-bubble">${data.response || 'I could not get a response. Please try again.'}</div>
            <div class="chat-time">Just now</div>
          </div>
        </div>`;
      messages.scrollTop = messages.scrollHeight;
      aiResponding = false;
    })
    .catch(() => {
      document.getElementById('typingMsg')?.remove();
      messages.innerHTML += `
        <div class="chat-msg ai">
          <div class="chat-av">Q</div>
          <div>
            <div class="chat-bubble" style="color:var(--red)">⚠️ Could not connect to AI. Make sure the server is running.</div>
            <div class="chat-time">Just now</div>
          </div>
        </div>`;
      messages.scrollTop = messages.scrollHeight;
      aiResponding = false;
    });
}

function handleChatKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendChat(); }
}

/* ════════════════════
   TOAST NOTIFICATION
════════════════════ */
let toastTimer = null;
function showToast(msg) {
  const toast = document.getElementById('toast');
  const textEl = document.getElementById('toastMsg');
  if (!toast || !textEl) return;
  if (toastTimer) clearTimeout(toastTimer);
  textEl.textContent = msg;
  toast.classList.add('show');
  toastTimer = setTimeout(() => toast.classList.remove('show'), 3500);
}

/* ════════════════════
   INIT ON LOAD
════════════════════ */
window.addEventListener('DOMContentLoaded', () => {
  buildTicker();

  // Default main chart (mock Indian stock data)
  const now = new Date();
  const labels = [];
  const prices = [];
  let p = 2800;
  for (let i = 60; i >= 0; i--) {
    const d = new Date(now);
    d.setDate(d.getDate() - i);
    labels.push(d.toLocaleDateString('en-IN', {month:'short', day:'numeric'}));
    p += (Math.random() - 0.42) * 35;
    prices.push(+p.toFixed(2));
  }
  renderMainChart(labels, prices);

  // Default watchlist
  renderWatchlist();

  // Default heatmap
  renderHeatmap();

  // Init chat
  const messages = document.getElementById('chatMessages');
  if (messages) {
    messages.innerHTML = `
      <div class="chat-msg ai">
        <div class="chat-av">Q</div>
        <div>
          <div class="chat-bubble">
            🇮🇳 Namaste! I'm <strong>Quantum AI</strong> — your Indian stock market assistant.<br><br>
            Simply type a stock name above (like <strong>RELIANCE</strong> or <strong>TCS</strong>) and click <strong>Analyze</strong> to get AI-powered predictions in ₹ INR!
          </div>
          <div class="chat-time">Just now</div>
        </div>
      </div>`;
  }

  // Enter key for search
  const input = document.getElementById('stockSymbol');
  if (input) {
    input.addEventListener('keydown', e => {
      if (e.key === 'Enter') runAnalysis();
    });
  }

  renderSentTrend();
});

Chart.defaults.color = '#475569';
Chart.defaults.font.family = 'JetBrains Mono';