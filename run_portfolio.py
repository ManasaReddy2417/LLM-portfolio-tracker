import sys
import subprocess
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'yfinance', 'pandas', '-q'])

# Cell 2: Imports & Constants
import yfinance as yf
from datetime import datetime, timedelta
import json

INITIAL_INVESTMENT = 1000
MONTH_START = datetime(2026, 2, 2)
MONTH_END   = datetime(2026, 2, 28)

print(f'💰 Initial Investment: ${INITIAL_INVESTMENT}')
print(f'📅 Tracking: {MONTH_START.strftime("%b %d, %Y")} → {MONTH_END.strftime("%b %d, %Y")}')

# Cell 3: Portfolio Definitions
WEEKS_DATA = [
    {
        'week_num': 1,
        'start_date': datetime(2026, 2, 2),
        'end_date': datetime(2026, 2, 6),
        'portfolios': {
            'ChatGPT':  [{"stock": "NVDA", "weight": 30},{"stock": "TSLA", "weight": 25},{"stock": "META", "weight": 20},{"stock": "AMD",  "weight": 15},{"stock": "COIN", "weight": 10}],
            'Grok':     [{"stock": "NVDA",  "weight": 35},{"stock": "AMD",   "weight": 25},{"stock": "MU",    "weight": 20},{"stock": "PLTR",  "weight": 10},{"stock": "GOOGL", "weight": 10}],
            'DeepSeek': [{"stock": "TQQQ", "weight": 50},{"stock": "SPXL", "weight": 30},{"stock": "TSLA", "weight": 20}],
            'Claude AI':[{"stock": "NVDA",  "weight": 25},{"stock": "MSFT",  "weight": 20},{"stock": "AVGO",  "weight": 20},{"stock": "GOOGL", "weight": 15},{"stock": "META",  "weight": 10},{"stock": "AMD",   "weight": 10}]
        }
    },
    {
        'week_num': 2,
        'start_date': datetime(2026, 2, 9),
        'end_date': datetime(2026, 2, 13),
        'portfolios': {
            'ChatGPT':  [{"stock": "NVDA", "weight": 25},{"stock": "AAPL", "weight": 20},{"stock": "MSFT", "weight": 20},{"stock": "TSLA", "weight": 20},{"stock": "AMD",  "weight": 15}],
            'Grok':     [{"stock": "NVDA", "weight": 25},{"stock": "AMD",  "weight": 20},{"stock": "PLTR", "weight": 15},{"stock": "MU",   "weight": 15},{"stock": "HOOD", "weight": 10},{"stock": "BTDR", "weight": 10},{"stock": "AMZN", "weight": 5}],
            'DeepSeek': [{"stock": "SPXL", "weight": 40},{"stock": "NVDA", "weight": 35},{"stock": "IWM",  "weight": 25}],
            'Claude AI':[{"stock": "NVDA",  "weight": 25},{"stock": "TSM",   "weight": 20},{"stock": "GOOGL", "weight": 15},{"stock": "META",  "weight": 15},{"stock": "STX",   "weight": 10},{"stock": "ULTA",  "weight": 10},{"stock": "CDE",   "weight": 5}]
        }
    },
    {
        'week_num': 3,
        'start_date': datetime(2026, 2, 16),
        'end_date': datetime(2026, 2, 20),
        'portfolios': {
            'ChatGPT':  [{"stock": "NVDA",  "weight": 25},{"stock": "TSLA",  "weight": 20},{"stock": "AMD",   "weight": 15},{"stock": "PLTR",  "weight": 15},{"stock": "AMZN",  "weight": 15},{"stock": "COIN",  "weight": 10}],
            'Grok':     [{"stock": "CVNA", "weight": 30},{"stock": "PANW", "weight": 25},{"stock": "WMT",  "weight": 20},{"stock": "PLTR", "weight": 15},{"stock": "FSLY", "weight": 10}],
            'DeepSeek': [{"stock": "PANW", "weight": 50},{"stock": "CDNS", "weight": 30},{"stock": "WMT",  "weight": 20}],
            'Claude AI':[{"stock": "NVDA",  "weight": 25},{"stock": "TSM",   "weight": 20},{"stock": "META",  "weight": 15},{"stock": "GOOGL", "weight": 15},{"stock": "TTD",   "weight": 10},{"stock": "MELI",  "weight": 10},{"stock": "SPY",   "weight": 5}]
        }
    },
    {
        'week_num': 4,
        'start_date': datetime(2026, 2, 23),
        'end_date': datetime(2026, 2, 27),
        'portfolios': {
             'ChatGPT':  [{"stock": "FSLY", "weight": 20}, {"stock": "VAL", "weight": 20}, {"stock": "DHX", "weight": 20}, {"stock": "MU", "weight": 20}, {"stock": "GOOGL", "weight": 20}],
             'Claude AI': [{"stock": "NVDA", "weight": 25}, {"stock": "MSFT", "weight": 20}, {"stock": "AVGO", "weight": 20}, {"stock": "GOOGL", "weight": 15}, {"stock": "META", "weight": 10}, {"stock": "AMD", "weight": 10}],
             'DeepSeek':  [{"stock": "NVDA", "weight": 40}, {"stock": "CRM", "weight": 15}, {"stock": "INTU", "weight": 15}, {"stock": "CAVA", "weight": 10}, {"stock": "HIMS", "weight": 10}, {"stock": "RKLB", "weight": 10}],
             'Grok':      [{"stock": "NVDA", "weight": 40}, {"stock": "HD", "weight": 15}, {"stock": "LOW", "weight": 15},{"stock": "IONQ", "weight": 10},{"stock": "CRM", "weight": 10},{"stock": "WDAY", "weight": 10}]
        }
    }
]
print(f' {len(WEEKS_DATA)} weeks defined')

# Cell 4: Trading Days
def get_all_trading_days():
    dates, current = [], MONTH_START
    while current <= MONTH_END:
        if current.weekday() < 5:
            dates.append(current)
        current += timedelta(days=1)
    return dates

all_trading_days = get_all_trading_days()
print(f'📅 {len(all_trading_days)} trading days: {all_trading_days[0].strftime("%b %d")} → {all_trading_days[-1].strftime("%b %d")}')

# Cell 5: Fetch Stock Data
def fetch_stock_data():
    all_stocks = set()
    for w in WEEKS_DATA:
        for p in w['portfolios'].values():
            for h in p:
                all_stocks.add(h['stock'])
    all_stocks.add('^GSPC')
    stock_data = {}
    print(f'\n📊 Fetching {len(all_stocks)} symbols...')
    print('=' * 75)
    for symbol in sorted(all_stocks):
        try:
            hist = yf.Ticker(symbol).history(
                start=MONTH_START.strftime('%Y-%m-%d'),
                end=(MONTH_END + timedelta(days=3)).strftime('%Y-%m-%d')
            )
            prices, last_known = [], None
            for td in all_trading_days:
                ds = td.strftime('%Y-%m-%d')
                m  = [i for i, d in enumerate(hist.index.strftime('%Y-%m-%d')) if d == ds]
                if m:
                    p = round(hist['Close'].iloc[m[0]], 2)
                    last_known = p
                elif last_known is not None:
                    p = last_known
                elif not hist.empty:
                    p = round(hist['Close'].iloc[0], 2)
                else:
                    p = 100.0
                prices.append(p)
            chg = round(((prices[-1]-prices[0])/prices[0])*100, 2) if prices[0] > 0 else 0
            stock_data[symbol] = {'prices': prices, 'start_price': prices[0], 'end_price': prices[-1], 'change_pct': chg}
            icon  = '✅' if chg >= 0 else '❌'
            label = 'S&P 500' if symbol == '^GSPC' else symbol
            print(f'{icon} {label:8s} | ${prices[0]:8.2f} → ${prices[-1]:8.2f} | {chg:+7.2f}%')
        except Exception as e:
            print(f'❌ {symbol:8s} | Error: {str(e)[:50]}')
            stock_data[symbol] = {'prices': [100.0]*len(all_trading_days), 'start_price': 100.0, 'end_price': 100.0, 'change_pct': 0.0}
    print('=' * 75)
    return stock_data

stock_data = fetch_stock_data()

# Cell 6: Calculate Performance
def calculate_performance():
    llm_results = {n: {'weeks': [], 'cumulative_values': [], 'current_capital': INITIAL_INVESTMENT, 'week_end_points': []}
                   for n in ['ChatGPT', 'Grok', 'DeepSeek', 'Claude AI']}

    for wd in WEEKS_DATA:
        wn, ws, we = wd['week_num'], wd['start_date'], wd['end_date']
        print(f'\n{"="*75}\n📅 WEEK {wn}: {ws.strftime("%b %d")} – {we.strftime("%b %d, %Y")}\n{"="*75}')
        week_days = [d for d in all_trading_days if ws <= d <= we]
        week_idx  = [all_trading_days.index(d) for d in week_days]
        if not week_idx:
            continue

        for llm_name, portfolio in wd['portfolios'].items():
            cap, stocks_detail = llm_results[llm_name]['current_capital'], []
            for h in portfolio:
                sym, wt   = h['stock'], h['weight']
                alloc     = (wt/100)*cap
                sp        = stock_data[sym]['prices'][week_idx[0]]
                shares    = alloc/sp if sp > 0 else 0
                ep        = stock_data[sym]['prices'][week_idx[-1]]
                ev        = shares*ep
                stocks_detail.append({'stock': sym, 'weight': wt, 'allocation': round(alloc,2),
                    'shares': round(shares,4), 'start_price': round(sp,2), 'end_price': round(ep,2),
                    'end_value': round(ev,2), 'return': round(ev-alloc,2),
                    'return_pct': round((ev-alloc)/alloc*100,2) if alloc > 0 else 0})

            ending  = sum(s['end_value'] for s in stocks_detail)
            ret     = ending - cap
            ret_pct = (ret/cap*100) if cap > 0 else 0
            llm_results[llm_name]['weeks'].append({'week_num': wn, 'start_date': ws, 'end_date': we,
                'starting_capital': round(cap,2), 'ending_value': round(ending,2),
                'return': round(ret,2), 'return_pct': round(ret_pct,2), 'stocks': stocks_detail})
            end_idx = all_trading_days.index(min(we, all_trading_days[-1]))
            llm_results[llm_name]['week_end_points'].append({'day_index': end_idx, 'value': round(ending,2), 'date': we.strftime('%b %d')})
            llm_results[llm_name]['current_capital'] = ending
            print(f'  {llm_name:12s} | ${cap:8.2f} → ${ending:8.2f} | {ret_pct:+6.2f}% | {"✅" if ret>=0 else "❌"}')

    for llm_name in llm_results:
        cum = []
        for day_idx, day in enumerate(all_trading_days):
            wfd = next((w for w in llm_results[llm_name]['weeks'] if w['start_date'] <= day <= w['end_date']), None)
            if wfd:
                val = sum(s['shares']*stock_data[s['stock']]['prices'][day_idx] for s in wfd['stocks'])
                cum.append(round(val,2))
            elif cum:
                cum.append(cum[-1])
            else:
                cum.append(INITIAL_INVESTMENT)
        llm_results[llm_name]['cumulative_values'] = cum
        llm_results[llm_name]['final_value']       = cum[-1]
        llm_results[llm_name]['total_return']      = round(cum[-1]-INITIAL_INVESTMENT, 2)
        llm_results[llm_name]['total_return_pct']  = round((cum[-1]-INITIAL_INVESTMENT)/INITIAL_INVESTMENT*100, 2)
    return llm_results

print('\n📈 CALCULATING PERFORMANCE...')
llm_results = calculate_performance()

ranked = sorted(llm_results.items(), key=lambda x: x[1]['total_return_pct'], reverse=True)
print(f'\n{"="*75}\n🏆 FINAL RANKINGS\n{"="*75}')
for i, (n, d) in enumerate(ranked):
    print(f'{["🥇","🥈","🥉","📊"][i]} #{i+1} {n:12s} | ${d["final_value"]:8.2f} | {d["total_return_pct"]:+6.2f}%')
print(f'\n📊 S&P 500: {stock_data["^GSPC"]["change_pct"]:+.2f}%')

# Cell 7: Generate HTML Dashboard — v5
def generate_html(llm_results, stock_data, all_trading_days):
    import json as _json
    date_labels   = [d.strftime('%b %d') for d in all_trading_days]
    fetch_time    = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ranked        = sorted(llm_results.items(), key=lambda x: x[1]['total_return_pct'], reverse=True)
    colors        = ['#6366f1', '#10b981', '#f59e0b', '#ef4444']
    sp500_prices     = stock_data['^GSPC']['prices']
    sp500_normalized = [round((p/sp500_prices[0])*INITIAL_INVESTMENT, 2) for p in sp500_prices]
    sp500_ret_pct    = stock_data['^GSPC']['change_pct']
    bar_colors  = ['#6366f1','#10b981','#f59e0b','#ef4444']
    card_names  = {r[0]: bar_colors[i] for i,r in enumerate(ranked)}
    DS_B64 = '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'
    CL_B64 = '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'
    logos = {
        'ChatGPT':  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="32" height="32" fill="white"><path d="M474.123 209.816a134.974 134.974 0 0 0-11.613-110.558 136.546 136.546 0 0 0-147.025-65.425A134.98 134.98 0 0 0 213.863 3.37a136.547 136.547 0 0 0-130.19 94.506 134.98 134.98 0 0 0-90.054 65.424 136.549 136.549 0 0 0 16.774 160.06 134.977 134.977 0 0 0 11.614 110.558 136.546 136.546 0 0 0 147.024 65.426 134.98 134.98 0 0 0 101.622 50.464 136.549 136.549 0 0 0 130.191-94.508 134.978 134.978 0 0 0 90.054-65.424 136.546 136.546 0 0 0-16.775-160.06zM298.136 470.458a101.21 101.21 0 0 1-64.974-23.505c.822-.45 2.264-1.244 3.198-1.813l107.895-62.302a17.508 17.508 0 0 0 8.855-15.332V236.11l45.6 26.328a1.619 1.619 0 0 1 .886 1.25v125.97a101.44 101.44 0 0 1-101.46 80.8zM77.076 385.538a101.19 101.19 0 0 1-12.09-68.11c.806.483 2.215 1.336 3.198 1.813l107.895 62.302a17.511 17.511 0 0 0 17.708 0l131.735-76.07v52.657a1.618 1.618 0 0 1-.647 1.393L218.084 421.84a101.441 101.441 0 0 1-141.008-36.302zm-13.203-235.08a101.197 101.197 0 0 1 52.88-44.54c0 .924-.048 2.551-.048 3.699v124.604a17.506 17.506 0 0 0 8.854 15.332l131.735 76.07-45.601 26.329a1.618 1.618 0 0 1-1.534.145L100.271 289.7a101.441 101.441 0 0 1-36.398-139.242zm374.547 87.081-131.735-76.07 45.6-26.328a1.619 1.619 0 0 1 1.535-.145l111.888 64.598a101.43 101.43 0 0 1-15.715 182.955V256.977a17.506 17.506 0 0 0-11.573-15.438zm45.4-68.396c-.806-.484-2.215-1.337-3.198-1.813l-107.895-62.302a17.512 17.512 0 0 0-17.708 0l-131.735 76.069v-52.657a1.619 1.619 0 0 1 .647-1.393l111.839-64.568a101.44 101.44 0 0 1 148.05 66.664zm-284.974 93.7-45.601-26.328a1.619 1.619 0 0 1-.886-1.25V110.296a101.44 101.44 0 0 1 166.35-77.908c-.822.45-2.263 1.245-3.198 1.814L208.616 196.502a17.51 17.51 0 0 0-8.855 15.332zm24.76-53.387 58.704-33.894 58.705 33.894v67.703l-58.705 33.894-58.704-33.894z"/></svg>',
        'Grok':     '<svg viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="white"><path d="M178.57 127.15 290 0h-26.46l-97.03 110.38L89.34 0H0l117.13 166.93L0 300h26.46l102.4-116.59L208.66 300H298L178.57 127.15Zm-36.18 41.05-11.84-16.47-94.13-131.04h40.57l76.01 105.82 11.84 16.47 98.95 137.38h-40.55l-80.85-111.16Z"/></svg>',
        'DeepSeek': f'<img src="data:image/png;base64,{DS_B64}" style="width:32px;height:32px;object-fit:contain;display:block;border-radius:50%;" alt="DeepSeek">',
        'Claude AI':f'<img src="data:image/png;base64,{CL_B64}" style="width:32px;height:32px;object-fit:contain;display:block;border-radius:50%;" alt="Claude AI">',
    }
    html_open = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>LLM Portfolio Battle — February 2026</title>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
  *{margin:0;padding:0;box-sizing:border-box;}
  body{font-family:'Inter','Segoe UI',sans-serif;background:linear-gradient(135deg,#6366f1 0%,#818cf8 30%,#a78bfa 60%,#7c3aed 100%);min-height:100vh;padding:30px 80px;}
  .container{max-width:100%;margin:0 auto;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 8px 40px rgba(99,102,241,.3);}
  .header{background:radial-gradient(ellipse at center, #1a2f72 0%, #1e3a8a 50%, #4c1d95 100%);color:#fff;padding:44px 40px 36px;text-align:center;position:relative;overflow:hidden;border-bottom:3px solid rgba(99,102,241,.4);}
  .header::before{content:'';position:absolute;top:-80px;right:-80px;width:320px;height:320px;background:rgba(99,102,241,.18);border-radius:50%;}
  .header::after{content:'';position:absolute;bottom:-60px;left:-60px;width:240px;height:240px;background:rgba(139,92,246,.15);border-radius:50%;}
  .header h1{font-size:2.8em;font-weight:900;letter-spacing:-0.5px;color:#ffffff;text-shadow:0 2px 12px rgba(0,0,0,.3);}
  .header .subtitle{font-size:1.1em;color:#fbbf24;margin-top:12px;font-weight:700;}
  .header .meta{font-size:.82em;margin-top:8px;color:rgba(255,255,255,.55);}
  .section{padding:28px 28px 20px;background:#fff;width:100%;}
  .section.alt{background:#f5f6ff;}
  .section-title{display:flex;align-items:center;gap:10px;font-size:1.3em;font-weight:800;color:#1e3a8a;margin-bottom:20px;padding-bottom:12px;border-bottom:2.5px solid #e0e7ff;letter-spacing:-0.2px;}
  .chart-box{background:#fff;border:1px solid #e2e8f0;border-radius:16px;padding:8px 8px 16px 8px;box-shadow:0 2px 12px rgba(0,0,0,.05);width:100%;}
  .bar-stage{display:flex;align-items:flex-end;justify-content:center;gap:36px;padding:16px 40px 0;min-height:300px;}
  .bar-col{display:flex;flex-direction:column;align-items:center;flex:1;max-width:180px;}
  .bar-amount{font-size:1.25em;font-weight:900;color:#1e3a8a;margin-bottom:10px;}
  .bar-body{width:100%;border-radius:14px 14px 0 0;display:flex;align-items:flex-end;justify-content:center;padding-bottom:14px;transition:filter .2s;cursor:default;min-height:24px;}
  .bar-body:hover{filter:brightness(1.08);}
  .bar-footer{margin-top:14px;text-align:center;width:100%;}
  .bar-footer .bname{font-size:.9em;font-weight:700;color:#1e3a8a;text-transform:uppercase;letter-spacing:.8px;}
  .bar-footer .bret{font-size:.85em;font-weight:600;margin-top:3px;}
  .bret.pos{color:#059669;} .bret.neg{color:#dc2626;}
  .sp-pill{text-align:center;padding:20px 0 8px;}
  .sp-pill span{display:inline-flex;align-items:center;gap:8px;background:#f1f5f9;border:1px solid #e2e8f0;border-radius:999px;padding:9px 24px;color:#475569;font-size:.92em;font-weight:600;}
  .llm-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;padding:24px 28px;background:#f5f6ff;}
  .llm-card{background:#fff;border-radius:18px;overflow:hidden;border:1px solid #e2e8f0;box-shadow:0 4px 18px rgba(0,0,0,.09);}
  .llm-card-header{padding:20px 24px;font-size:1.15em;font-weight:900;color:#fff;display:flex;justify-content:space-between;align-items:center;letter-spacing:-0.3px;}
  .llm-card-header .ret-badge{background:rgba(255,255,255,.18);border-radius:999px;padding:5px 16px;font-size:.9em;font-weight:700;}
  table{width:100%;border-collapse:collapse;}
  .tbl-head-row th{background:linear-gradient(135deg,#3b3f9e,#6c40c9);color:#fff;padding:11px 8px;font-size:.72em;font-weight:800;text-transform:uppercase;letter-spacing:.7px;text-align:center;border-right:1px solid rgba(255,255,255,0.15);}
  .tbl-sub-row th{background:linear-gradient(90deg,#4f52b8,#7c4dcf);color:#fff;padding:8px 7px;font-size:.68em;font-weight:700;text-transform:uppercase;letter-spacing:.5px;text-align:center;border-bottom:3px solid rgba(255,255,255,0.3);border-right:1px solid rgba(255,255,255,0.15);}
  tbody tr:nth-child(even){background:#f5f6ff;}
  tbody tr:hover{background:#eef0ff;}
  tbody tr{border-bottom:1px solid #e8eaf6;}
  td{padding:8px 8px;font-size:0.78em;text-align:center;color:#374151;border-right:1px solid #ececf8;}
  .stock-col{text-align:left!important;font-weight:800;color:#1e3a8a;padding-left:14px!important;font-size:0.82em;}
  .pos{color:#059669!important;font-weight:700;} .neg{color:#dc2626!important;font-weight:700;}
  .price-section{padding:28px;background:#fff;border-top:1px solid #e2e8f0;}
  .price-table-wrap{overflow-x:auto;border-radius:12px;border:1px solid #e2e8f0;margin-top:12px;}
  .price-table-wrap table thead th{background:#1e3a8a;color:#fff;padding:7px 4px;font-size:0.60em;font-weight:700;text-transform:uppercase;letter-spacing:.4px;text-align:center;white-space:nowrap;}
  .price-table-wrap table tbody td{font-size:0.68em;padding:5px 4px;}
  @media(max-width:1100px){.llm-grid{grid-template-columns:1fr;}.bar-stage{flex-wrap:wrap;}}
</style>
</head>
<body>
<div class="container">
'''
    html = html_open
    html += f'''  <div class="header">
    <h1> LLM Portfolio Comparison — February 2026</h1>
    <p class="subtitle">Feb 2 – Feb 28, 2026 | $1,000 Initial Investment | Rolling Weekly Strategy</p>
    <p class="meta">Last Updated: {fetch_time}</p>
  </div>
  <div class="section">
    <div class="section-title">📈 Cumulative Portfolio Value vs S&amp;P 500 (Feb 2 – Feb 28)</div>
    <div class="chart-box"><div id="line-chart"></div></div>
  </div>
  <div class="section alt">
    <div class="section-title">📊 Total Return vs Starting $1,000 — Ranked Highest to Lowest</div>
    <div class="bar-stage">
'''
    max_val    = ranked[0][1]['final_value']
    max_bar_px = 240
    for i, (name, data) in enumerate(ranked):
        fv     = data['final_value']
        trp    = data['total_return_pct']
        clr    = bar_colors[i]
        height = max(int((fv / max_val) * max_bar_px), 30)
        ssym   = '+' if trp >= 0 else ''
        rcls   = 'pos' if trp >= 0 else 'neg'
        logo   = logos.get(name, f'<span style="color:white;font-size:1.4em;font-weight:900">{name[0]}</span>')
        html += f'''
      <div class="bar-col">
        <div class="bar-amount">${fv:,.2f}</div>
        <div class="bar-body" style="height:{height}px;background:linear-gradient(180deg,{clr}f0,{clr}99);display:flex;align-items:center;justify-content:center;padding:15px 0 14px;">
          <div style="width:52px;height:52px;background:rgba(255,255,255,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;">
            {logo}
          </div>
        </div>
        <div class="bar-footer">
          <div class="bname">{name}</div>
          <div class="bret {rcls}">{ssym}{trp:.2f}%</div>
        </div>
      </div>
'''
    sp_fv   = sp500_normalized[-1]
    sp_sign = '+' if sp500_ret_pct >= 0 else ''
    html += f'''
    </div>
    <div class="sp-pill">
      <span>📊 S&amp;P 500 Benchmark &nbsp;·&nbsp; ${sp_fv:,.2f} &nbsp;·&nbsp; {sp_sign}{sp500_ret_pct:.2f}%</span>
    </div>
  </div>
'''
    html += '  <div class="llm-grid">\n'
    for rank_i, (llm_name, data) in enumerate(ranked, 1):
        fv      = data['final_value']
        trp     = data['total_return_pct']
        ssym    = '+' if trp >= 0 else ''
        hdr_clr = card_names[llm_name]
        html += f'''
    <div class="llm-card">
      <div class="llm-card-header" style="background:linear-gradient(135deg,{hdr_clr},{hdr_clr}cc);">
        <span>#{rank_i} {llm_name}</span>
        <span class="ret-badge">${fv:.2f} ({ssym}{trp:.2f}%)</span>
      </div>
      <div><table>
          <thead><tr class="tbl-head-row">
              <th rowspan="2" style="vertical-align:middle;text-align:left;padding-left:12px;">Stock</th>
'''
        for w in data['weeks']:
            html += f'<th colspan="2" style="white-space:nowrap;font-size:0.72em;">{w["start_date"].strftime("%b %-d")} (${w["starting_capital"]:.0f}) &ndash; {w["end_date"].strftime("%b %-d")} (${w["ending_value"]:.0f})</th>\n'
        html += '          </tr><tr class="tbl-sub-row">\n'
        for _ in data['weeks']:
            html += '<th>Weight</th><th>Shares</th>\n'
        html += '          </tr></thead><tbody>\n'
        all_stocks_llm = sorted({s['stock'] for w in data['weeks'] for s in w['stocks']})
        for sym in all_stocks_llm:
            html += f'            <tr><td class="stock-col">{sym}</td>\n'
            for w in data['weeks']:
                s = next((x for x in w['stocks'] if x['stock'] == sym), None)
                if s:
                    html += f'              <td style="font-weight:600;">{s["weight"]}%</td><td style="color:#4b5563;">{s["shares"]:.4f}</td>\n'
                else:
                    html += '              <td style="color:#9ca3af;">-</td><td style="color:#9ca3af;">-</td>\n'
            html += '            </tr>\n'
        html += '          </tbody></table></div>\n    </div>\n'
    html += '  </div>\n'
    html += '''
  <div class="price-section">
    <div class="section-title">Yahoo Finance US Stock Close Prices — Feb 2–28, 2026</div>
    <div class="price-table-wrap"><table>
      <thead><tr><th style="text-align:left;padding-left:10px;">Stock</th>
'''
    for dl in date_labels:
        html += f'      <th>{dl}</th>\n'
    html += '      <th>Chg%</th></tr></thead><tbody>\n'
    for sym in sorted(stock_data.keys()):
        if sym == '^GSPC': continue
        prices = stock_data[sym]['prices']
        chg    = stock_data[sym]['change_pct']
        cc     = 'pos' if chg >= 0 else 'neg'
        html += f'      <tr><td class="stock-col">{sym}</td>'
        for p in prices:
            html += f'<td>${p:.2f}</td>'
        html += f'<td class="{cc}">{chg:+.2f}%</td></tr>\n'
    html += '    </tbody></table></div>\n'
    html += '''
    <div class="section-title" style="margin-top:36px;">S&amp;P 500 — Feb 2–28, 2026</div>
    <div class="price-table-wrap"><table>
      <thead><tr><th style="text-align:left;padding-left:10px;">Metric</th>
'''
    for dl in date_labels:
        html += f'      <th>{dl}</th>\n'
    html += '      <th>Chg%</th></tr></thead><tbody>\n'
    sp_chg = stock_data['^GSPC']['change_pct']
    cc = 'pos' if sp_chg >= 0 else 'neg'
    html += '      <tr><td class="stock-col">Actual Points</td>'
    for p in sp500_prices:
        html += f'<td>{p:.2f}</td>'
    html += f'<td class="{cc}">{sp_chg:+.2f}%</td></tr>\n'
    html += '      <tr><td class="stock-col">Normalized ($1,000)</td>'
    for p in sp500_normalized:
        html += f'<td>${p:.2f}</td>'
    html += f'<td class="{cc}">{sp_chg:+.2f}%</td></tr>\n'
    html += '    </tbody></table></div>\n  </div>\n'
    html += f'''
</div>
<script>
var dates  = {_json.dumps(date_labels)};
var colors = {_json.dumps(colors)};
var lineTraces = [];
'''
    for i, (llm_name, data) in enumerate(ranked):
        cv = data['cumulative_values']
        html += f'''
lineTraces.push({{
  x: dates, y: {_json.dumps(cv)},
  type: 'scatter', mode: 'lines',
  name: '{llm_name}',
  line: {{ color: colors[{i}], width: 3, shape: 'spline', smoothing: 0.7 }},
  hovertemplate: '{llm_name}: $%{{y:.2f}}<extra></extra>'
}});
'''
    html += f'''
lineTraces.push({{
  x: dates, y: {_json.dumps(sp500_normalized)},
  type: 'scatter', mode: 'lines',
  name: 'S&P 500',
  line: {{ color: '#1e293b', width: 2.5, dash: 'dashdot', shape: 'spline', smoothing: 0.7 }},
  hovertemplate: 'S&P 500: $%{{y:.2f}}<extra></extra>'
}});
var annotations = [];
var lastDate = dates[dates.length-1];
'''
    all_series = []
    for i, (llm_name, data) in enumerate(ranked):
        cv       = data['cumulative_values']
        last_val = cv[-1]
        trp      = data['total_return_pct']
        ssym     = '+' if trp >= 0 else ''
        label    = f'{llm_name}: ${last_val:.0f} ({ssym}{trp:.1f}%)'
        all_series.append((last_val, label, colors[i]))
    sp_last  = sp500_normalized[-1]
    sp_ssym  = '+' if sp500_ret_pct >= 0 else ''
    sp_label = f'S&P 500: ${sp_last:.0f} ({sp_ssym}{sp500_ret_pct:.1f}%)'
    all_series.append((sp_last, sp_label, '#1e293b'))
    all_series_sorted = sorted(all_series, key=lambda x: x[0], reverse=True)
    label_arr_js = _json.dumps([[s[0], s[1], s[2]] for s in all_series_sorted])
    html += f'''
var labelArr = {label_arr_js};
labelArr.sort(function(a,b){{ return b[0]-a[0]; }});
var adjY = [];
for (var li=0; li<labelArr.length; li++) {{
  var y = labelArr[li][0];
  for (var lj=0; lj<adjY.length; lj++) {{ if (Math.abs(adjY[lj]-y) < 18) y = adjY[lj]-18; }}
  adjY.push(y);
  annotations.push({{
    x: lastDate, y: adjY[li],
    xanchor: 'left', yanchor: 'middle', xshift: 10,
    text: '<b>'+labelArr[li][1]+'</b>',
    showarrow: false,
    font: {{ size: 13.5, color: labelArr[li][2], family: 'Inter,sans-serif' }},
    bgcolor: 'rgba(255,255,255,0.93)', borderpad: 4
  }});
}}
Plotly.newPlot('line-chart', lineTraces, {{
  paper_bgcolor: '#ffffff', plot_bgcolor: '#fafbff',
  xaxis: {{
    title: {{ text: 'Date', font: {{ size: 14, color: '#374151', family: 'Inter,sans-serif' }} }},
    showgrid: true, gridcolor: '#e8ecf4', gridwidth: 1,
    color: '#374151',
    tickfont: {{ size: 13, color: '#374151', family: 'Inter,sans-serif' }},
    zeroline: false, showline: true, linecolor: '#cbd5e1', tickcolor: '#94a3b8',
    automargin: true, tickangle: 0,
    range: [-0.8, dates.length - 0.8]
  }},
  yaxis: {{
    title: {{ text: 'Portfolio Value ($)', font: {{ size: 14, color: '#1e3a8a', family: 'Inter,sans-serif' }}, standoff: 25 }},
    showgrid: true, gridcolor: '#e8ecf4', gridwidth: 1,
    color: '#374151',
    tickfont: {{ size: 13, color: '#374151', family: 'Inter,sans-serif' }},
    tickprefix: '$', showline: true, linecolor: '#cbd5e1',
    tickcolor: '#94a3b8', automargin: true
  }},
  height: 680,
  hovermode: 'x unified',
  hoverlabel: {{
    bgcolor: 'rgba(255,255,255,0.97)', bordercolor: '#e2e8f0',
    font: {{ size: 12, family: 'Inter,sans-serif', color: '#1e3a8a' }},
    namelength: 0
  }},
  annotations: annotations,
  margin: {{ t: 60, b: 80, l: 155, r: 210 }},
  legend: {{
    orientation: 'h', yanchor: 'bottom', y: 1.02,
    xanchor: 'center', x: 0.5,
    font: {{ color: '#374151', size: 15, family: 'Inter,sans-serif' }},
    bgcolor: 'rgba(255,255,255,0)'
  }},
  font: {{ color: '#374151', family: 'Inter,sans-serif' }}
}}, {{ responsive: true, displayModeBar: false }});
</script>

</body>
</html>'''
    return html

print('✅ generate_html() ready')


# Cell 8: Save Dashboard
print('Generating dashboard...')
html_content = generate_html(llm_results, stock_data, all_trading_days)
import os
os.makedirs('docs', exist_ok=True)
with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f'SUCCESS: docs/index.html saved ({len(html_content)//1024} KB)')
