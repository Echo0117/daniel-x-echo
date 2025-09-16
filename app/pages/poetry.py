import os, re, glob
from datetime import datetime
from typing import List, Dict
from pywebio.output import put_html, put_markdown, use_scope, clear
from pywebio.session import run_js
from app.ui import back_home
# top of file
from pywebio.session import eval_js  # <-- add this


# ---------- locations ----------
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
POEMS_ROOT = os.path.join(ROOT, "poems")
MINE_DIR   = os.path.join(POEMS_ROOT, "mine")
FOUND_DIR  = os.path.join(POEMS_ROOT, "found")
for d in (MINE_DIR, FOUND_DIR):
    print("Ensure dir:", d)
    os.makedirs(d, exist_ok=True)

# ---------- tiny theme (same vibe as Love Letters) ----------
def inject_css():
    put_html("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Noto+Serif+SC:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#0b0f1a; --bg2:#09122a; --text:#eaf0ff; --line:#293462;
    /* Mine (soft blush parchment) */
    --mine-paper:#fcf8f3; --mine-rule:#efe7dc; --mine-edge:#f0e6d6; --mine-accent:#e7b8c8;
    /* Found (aged parchment) */
    --found-paper:#fbf3df; --found-rule:#f0e5c5; --found-edge:#e1d4ae; --found-accent:#caa56b;
  }
  body{background:linear-gradient(160deg,var(--bg),var(--bg2));color:var(--text)}
  .wrap{max-width:1040px;margin:24px auto;padding:0 16px}
  .titlebar{display:flex;align-items:center;justify-content:space-between;margin:0 0 14px}
  .tabs{display:flex;gap:8px}
  .tab{padding:8px 12px;border:1px solid var(--line);border-radius:12px;background:#141b38;color:var(--text);text-decoration:none;font-weight:800}
  .tab.active{box-shadow:0 10px 26px #0007;background:#101737}
  .grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
  .env{position:relative;display:block;height:140px;border-radius:14px;overflow:hidden;border:1px solid var(--line);
       background:linear-gradient(180deg,#11162a,#0f1430);box-shadow:0 16px 40px #0008;text-decoration:none;color:var(--text)}
  .env .flap{position:absolute;left:0;right:0;top:0;height:70px;clip-path:polygon(0 0,100% 0,50% 100%);
             background:linear-gradient(180deg,#223066,#18224f);border-bottom:1px solid #2c3563}
  .env .title{position:absolute;left:16px;right:16px;bottom:42px;font:700 18px "Playfair Display",serif;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .env .meta{position:absolute;left:16px;bottom:14px;opacity:.85;font-size:12px}
  .env .badge{position:absolute;right:14px;top:14px;padding:4px 8px;border-radius:999px;background:#1b244d;border:1px solid #33407a;font-size:11px;opacity:.9}

  .letter-wrap{max-width:900px;margin:22px auto;padding:0 12px}

  /* Base paper */
  .paper{position:relative;border-radius:20px;box-shadow:0 20px 60px #0008;overflow:hidden}
  .paper .inner{position:relative;padding:52px 44px 40px 88px;font-family:"Noto Serif SC",serif;color:#2b2a28}
  .paper .inner:before{content:"";position:absolute;left:64px;top:28px;bottom:28px;width:2px;border-radius:2px}
  .ltitle{font-family:"Playfair Display",serif;font-size:34px;font-weight:700;margin:0 0 6px}
  .lmeta{color:#6a6056;font-size:14px;margin:0 0 16px}
  .md p{margin:0 0 10px}

  /* Mine style */
  .paper.mine{border:1px solid var(--mine-edge);
    background:repeating-linear-gradient(to bottom,var(--mine-paper) 0 28px,var(--mine-rule) 29px,var(--mine-paper) 56px);}
  .paper.mine .inner:before{background:linear-gradient(var(--mine-accent),var(--mine-edge))}
  /* Found style */
  .paper.found{border:1px solid var(--found-edge);
    background:repeating-linear-gradient(to bottom,var(--found-paper) 0 28px,var(--found-rule) 29px,var(--found-paper) 56px);}
  .paper.found .inner:before{background:linear-gradient(var(--found-accent),var(--found-edge))}

  .btns{display:flex;gap:10px;margin:16px 0}
  .pbtn{padding:10px 14px;border-radius:12px;border:1px solid #d6d0c6;background:#fff7ec;color:#2c2a28;font-weight:700;text-decoration:none}
</style>
""")


# ---------- helpers ----------
def read_text(p):
    with open(p,"r",encoding="utf-8") as f: return f.read()

def split_md(md:str):
    # grab optional "# Title", "_author: ..._", "_date: YYYY-MM-DD_"
    lines = md.splitlines()
    title = author = date_s = None
    drop = set()
    for i,ln in enumerate(lines):
        m = re.match(r'^\s*#\s+(.+?)\s*$', ln)
        if m: title=m.group(1).strip(); drop.add(i); break
    for i,ln in enumerate(lines):
        m = re.match(r'^\s*_author:\s*(.+?)\s*_\s*$', ln, flags=re.I)
        if m: author=m.group(1).strip(); drop.add(i); break
    for i,ln in enumerate(lines):
        m = re.match(r'^\s*_date:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})\s*_\s*$', ln, flags=re.I)
        if m: date_s=m.group(1).strip(); drop.add(i); break
    body = "\n".join(ln for i,ln in enumerate(lines) if i not in drop).strip()
    return dict(title=title, author=author, date=date_s, body=body)

def parse_file(path:str, kind:str)->Dict:
    slug = os.path.splitext(os.path.basename(path))[0]
    parts = split_md(read_text(path))

    # title from file header or prettified filename
    if "_" in slug:
        maybe_date, rest = slug.split("_",1)
        title_guess = rest.replace("-"," ").title()
        try:
            date_from_name = datetime.strptime(maybe_date,"%Y-%m-%d").date()
        except:
            date_from_name=None
    else:
        title_guess = slug.replace("-"," ").title()
        date_from_name=None

    title = parts["title"] or title_guess
    date = None
    if parts["date"]:
        try: date = datetime.strptime(parts["date"],"%Y-%m-%d").date()
        except: pass
    if not date and date_from_name: date = date_from_name

    return dict(kind=kind, slug=slug, title=title, author=parts["author"], date=date, body_md=parts["body"])

def load_list(folder:str, kind:str)->List[Dict]:
    files=[]
    for pat in ("*.md","*.markdown","*.MD","*.MARKDOWN"):
        files.extend(glob.glob(os.path.join(folder,pat)))
    items = [parse_file(p,kind) for p in files]
    items.sort(key=lambda x:(x["date"] or datetime.min.date(), x["slug"]), reverse=True)
    print(f"Loaded {len(items)} poems from {folder}")
    return items

# ---------- views ----------
def render_list(kind:str, items:List[Dict]):
    put_html("<div class='wrap'>")
    # tabs are pure links → always clickable
    put_html(f"""
      <div class='titlebar'>
        <h2 style="margin:0">📝 Poetry</h2>
        <div class='tabs'>
          <a class='tab {"active" if kind=="mine" else ""}'  href="/poetry?kind=mine">By Echo</a>
          <a class='tab {"active" if kind=="found" else ""}' href="/poetry?kind=found">Found Gems</a>
        </div>
      </div>
    """)
    put_html("<div class='grid'>")
    if not items:
        put_html("<div style='opacity:.7'>No poems yet. Add .md files under <code>poems/mine</code> or <code>poems/found</code>.</div>")
    for it in items:
        date_str = it["date"].strftime("%Y-%m-%d") if it["date"] else "—"
        badge = "Echo" if it["kind"]=="mine" else (it["author"] or "Author")
        # envelope is just a link → always works
        put_html(f"""
          <a class="env" href="/poetry?kind={it['kind']}&open={it['slug']}">
            <div class="flap"></div>
            <div class="badge">{badge}</div>
            <div class="title">{it['title']}</div>
            <div class="meta">Date: {date_str}</div>
          </a>
        """)
    put_html("</div></div>")

import html

def _poem_html(kind:str, title:str, author:str, date_str:str, body_md:str)->str:
    # very light “markdown to HTML”: keep lines, blank lines = paragraph breaks
    safe = html.escape(body_md).splitlines()
    html_lines=[]
    para=[]
    for ln in safe:
        if ln.strip()=="":
            if para:
                html_lines.append("<p>"+ "<br>".join(para) +"</p>")
                para=[]
        else:
            para.append(ln)
    if para:
        html_lines.append("<p>"+ "<br>".join(para) +"</p>")

    paper_class = "mine" if kind=="mine" else "found"
    return f"""
    <div class="letter-wrap">
      <div class="paper {paper_class}">
        <div class="inner">
          <h1 class="ltitle">{html.escape(title)}</h1>
          <p class="lmeta">Author: {html.escape(author)} · Date: {html.escape(date_str)}</p>
          <div class="md">
            {''.join(html_lines)}
          </div>
          <div class="btns">
            <a class="pbtn" href="/poetry?kind={kind}">← Back</a>
            <a class="pbtn" href="/">🏠 Home</a>
          </div>
        </div>
      </div>
    </div>
    """

def render_poem(kind:str, poem:Dict):
    date_str = poem["date"].strftime("%Y-%m-%d") if poem["date"] else "—"
    author = "Echo" if kind=="mine" else (poem["author"] or "—")
    put_html(_poem_html(kind, poem["title"], author, date_str, poem["body_md"]))



# ---------- entry ----------
def app_main():
    inject_css()
    back_home()
    use_scope("content", clear=True)

    # read query
    # run_js("window.__qs=(new URLSearchParams(location.search))")
    # kind = run_js("return window.__qs.get('kind')") or "mine"
    # if kind not in ("mine","found"): kind="mine"
    # open_slug = run_js("return window.__qs.get('open')")
    kind = eval_js("new URLSearchParams(window.location.search).get('kind')") or "mine"
    open_slug = eval_js("new URLSearchParams(window.location.search).get('open')")

    items = load_list(MINE_DIR if kind=="mine" else FOUND_DIR, kind)

    if open_slug:
        poem = next((x for x in items if x["slug"]==open_slug), None)
        if poem: render_poem(kind, poem)
        else:    render_list(kind, items)
    else:
        render_list(kind, items)
