"""
extract_html.py
Run after nbconvert executes the notebook.
Pulls the saved HTML file out of the notebook outputs and copies to docs/
"""
import json, os, shutil

os.makedirs('docs', exist_ok=True)

# The notebook Cell 8 saves the HTML file — just copy it
html_file = 'LLM_Portfolio_Dashboard_Feb2_Feb28.html'
if os.path.exists(html_file):
    shutil.copy(html_file, 'docs/index.html')
    print(f"✅ Copied {html_file} → docs/index.html")
else:
    # Try to find any .html file generated
    for f in os.listdir('.'):
        if f.endswith('.html') and 'Portfolio' in f:
            shutil.copy(f, 'docs/index.html')
            print(f"✅ Copied {f} → docs/index.html")
            break
    else:
        print("❌ No HTML file found!")
        exit(1)
