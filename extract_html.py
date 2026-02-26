"""
extract_html.py — unchanged, still works the same way.
run_portfolio.py now writes directly to docs/index.html itself,
so this file is only needed if you run via nbconvert (notebook path).
"""
import json, os, shutil

os.makedirs('docs', exist_ok=True)

html_file = 'LLM_Portfolio_Dashboard_Feb2_Feb28.html'
if os.path.exists(html_file):
    shutil.copy(html_file, 'docs/index.html')
    print(f"✅ Copied {html_file} → docs/index.html")
else:
    for f in os.listdir('.'):
        if f.endswith('.html') and 'Portfolio' in f:
            shutil.copy(f, 'docs/index.html')
            print(f"✅ Copied {f} → docs/index.html")
            break
    else:
        print("❌ No HTML file found!")
        exit(1)
