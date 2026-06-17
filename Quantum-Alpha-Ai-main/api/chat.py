from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

# Simple in-memory cache of last analysis (per Vercel instance)
_last_data = {}


class handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        query  = parse_qs(parsed.query)

        user_msg = query.get('message', [''])[0].lower().strip()
        symbol   = query.get('symbol',  ['RELIANCE.NS'])[0].upper().strip()

        data  = _last_data.get(symbol, {})
        reply = ""

        if not data:
            reply = (
                f"I'm ready to analyze **{symbol.replace('.NS','')}**. "
                f"Click **Analyze** at the top so I can load live market data and run the AI prediction!"
            )
        else:
            price    = data.get('kpis', {}).get('price', '—')
            pred     = data.get('kpis', {}).get('pred',  '—')
            decision = data.get('recommendation', {}).get('decision', 'HOLD')
            sent     = data.get('kpis', {}).get('sent', 'Neutral')
            perf     = data.get('kpis', {}).get('perf', '0.00%')
            risk     = data.get('kpis', {}).get('risk', 'Low')
            rsi_list = data.get('indicators', {}).get('rsi', [])
            rsi_last = next((v for v in reversed(rsi_list) if v is not None), None)
            conf     = data.get('kpis', {}).get('conf', '—')
            sym_clean = symbol.replace('.NS','').replace('.BO','')

            if any(k in user_msg for k in ['predict', 'forecast', 'future', 'price', 'target']):
                reply = (
                    f"My regression model forecasts **{sym_clean}** will reach **{pred}** "
                    f"over the next 10 days. Current price is **{price}**. "
                    f"Signal: **{decision}** with {conf} confidence."
                )
            elif any(k in user_msg for k in ['rsi', 'macd', 'indicator', 'technical', 'momentum']):
                rsi_str = f"{rsi_last:.1f}" if rsi_last is not None else "—"
                reply = (
                    f"Technical snapshot for **{sym_clean}**: RSI is **{rsi_str}** "
                    f"({'overbought ⚠️' if (rsi_last or 50) > 70 else 'oversold 🔋' if (rsi_last or 50) < 30 else 'neutral ✅'}). "
                    f"Risk zone: **{risk}**. Price trend: **{sent}**."
                )
            elif any(k in user_msg for k in ['sentiment', 'news', 'analyst', 'report']):
                reply = (
                    f"News sentiment for **{sym_clean}** is currently **{sent}**. "
                    f"Today's performance: **{perf}**. "
                    f"The AI recommendation is **{decision}** based on sentiment + technical signals."
                )
            elif any(k in user_msg for k in ['buy', 'sell', 'hold', 'invest', 'should i']):
                reply = (
                    f"Based on live data: **{sym_clean}** is rated **{decision}**. "
                    f"Current price: {price} → AI forecast: {pred}. "
                    f"Sentiment: {sent} | RSI risk: {risk}. "
                    f"Always do your own research before investing! 📊"
                )
            elif any(k in user_msg for k in ['risk', 'safe', 'volatile']):
                reply = (
                    f"**{sym_clean}** currently has **{risk}** risk. "
                    f"RSI: {f'{rsi_last:.1f}' if rsi_last else '—'} — "
                    f"{'above 70 means overbought (more risk)' if (rsi_last or 50) > 70 else 'below 30 means oversold (recovery possible)' if (rsi_last or 50) < 30 else 'in the neutral 30–70 zone (healthy)'}."
                )
            else:
                reply = (
                    f"Here's a quick summary for **{sym_clean}**: "
                    f"Price **{price}** | AI Forecast **{pred}** | Signal **{decision}** | "
                    f"Sentiment **{sent}** | Risk **{risk}**. "
                    f"Ask me about predictions, RSI/MACD, buy/sell signals, or news sentiment!"
                )

        body = json.dumps({'reply': reply}).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
