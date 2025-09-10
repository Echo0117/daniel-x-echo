import os, re, glob
from datetime import datetime
from typing import List, Dict, Optional
from pywebio.output import put_html, put_markdown, clear, use_scope, put_text
from pywebio.session import run_js, register_thread, hold
from pywebio.input import actions
from app.ui import back_home

# ------------- Robust letters directory resolution -------------
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# allow override from env on Koyeb/Render if needed
ENV_DIR = os.getenv("LETTERS_DIR")
CANDIDATES = [
    ENV_DIR,
    os.path.join(ROOT_DIR, "letters")
]
print("Letter path candidates:", CANDIDATES)
CANDIDATES = [p for p in CANDIDATES if p]

def resolve_letters_dir() -> str:
    for p in CANDIDATES:
        if p and os.path.isdir(p):
            print("Using letters dir:", p)
            return p
    # default: create root/letters
    fallback = os.path.join(ROOT_DIR, "letters")
    os.makedirs(fallback, exist_ok=True)
    return fallback

LETTERS_DIR = resolve_letters_dir()
PATTERNS = ("*.md","*.MD","*.markdown","*.MARKDOWN")

def iter_letter_paths() -> List[str]:
    files = []
    for pat in PATTERNS:
        files.extend(glob.glob(os.path.join(LETTERS_DIR, pat)))
    # de-duplicate preserve order
    seen, uniq = set(), []
    print("Found letter files:", files)
    for f in files:
        if f not in seen:
            seen.add(f); uniq.append(f)
    return uniq

# -------------------- THEME (envelopes + letter paper) --------------------
def inject_theme():
    # Envelope + Stationery styles (fonts included)
    put_html("""
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600&family=Playfair+Display:wght@600;700&family=Great+Vibes&display=swap" rel="stylesheet">
    <style>
      :root{
        --bg:#0b0f1a; --bg2:#09122a; --line:#2a345f; --ring:#80ffdb;
        --paper:#fbfaf7; --ink:#2c2a28; --rule:#e8e4dc; --edge:#efece4;
      }
      body{margin:0;background:linear-gradient(160deg,var(--bg),var(--bg2));color:#eaf0ff;}

      .wrap{max-width:1040px;margin:24px auto;padding:0 16px}
      .titlebar{display:flex;align-items:center;gap:10px;margin:8px 0 18px}
      .titlebar h2{margin:0;font-size:24px;font-weight:800}

      /* —— Envelopes (unchanged from your working version but a little crisper) —— */
      .grid{display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
      a.env{
        position:relative; display:block; min-height:170px; border-radius:18px;
        background:linear-gradient(180deg,#1c2652,#0f1635);
        border:1px solid var(--line); box-shadow:0 20px 48px #000a, inset 0 -22px 40px rgba(0,0,0,.25);
        text-decoration:none; color:#eaf0ff; overflow:hidden; padding:18px 18px 22px;
        transition: transform .18s ease, box-shadow .18s ease, filter .18s ease;
      }
      a.env:hover{ transform:translateY(-2px); box-shadow:0 28px 64px #000c; filter:saturate(1.06) }
      a.env .flap{
        pointer-events:none; position:absolute; left:0; right:0; top:0; height:84px;
        background:linear-gradient(180deg,#25346f,#16214b);
        clip-path:polygon(0 0,100% 0,50% 100%); border-bottom:1px solid #2c3563;
      }
      a.env .stamp{
        position:absolute; right:16px; top:16px; width:50px; height:50px; border-radius:50%;
        background:radial-gradient(circle at 30% 30%, #ffd1dc 0%, #ff7eb3 50%, #ff4d6d 100%);
        border:2px solid rgba(255,255,255,.25); box-shadow:0 0 18px #ff7eb366;
      }
      a.env .title{
        position:relative; margin-top:64px; font:700 18px "Playfair Display",serif; letter-spacing:.2px;
        white-space:nowrap; overflow:hidden; text-overflow:ellipsis; text-shadow:0 2px 10px #0009;
      }
      a.env .date{ position:relative; margin-top:8px; opacity:.85; font-size:12px; color:#c6ceff }

      /* —— LETTER STATIONERY —— */
      .letter-wrap{max-width:900px;margin:28px auto;padding:0 14px}

      /* Ancient letter style: parchment border + ruled paper + soft shading */
.paper-airmail {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  color: #3b2f2f;
  padding: 56px 48px 46px 88px;

  background:
    /* faint ruled lines */
    repeating-linear-gradient(to bottom, transparent 0 28px, #e8e2d2 29px, transparent 30px),
    /* base parchment */
    linear-gradient(#fcf9ed, #f7f2df);
  
  /* ✨ border: parchment-yellow, no more red/blue chevrons */
  border: 12px solid #e3d4a5;

  box-shadow: 0 24px 68px rgba(0,0,0,.4), inset 0 1px 4px rgba(0,0,0,.15);
  font-family: "Noto Serif SC", serif;
}

/* margin line, now a soft brown-red */
.paper-airmail::before {
  content: "";
  position: absolute;
  left: 64px;
  top: 32px;
  bottom: 32px;
  width: 2px;
  background: #c9a068;   /* soft golden-brown margin */
  opacity: .9;
  border-radius: 2px;
}

/* subtle highlight overlay */
.paper-airmail::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  border-radius: 20px;
  background: linear-gradient(to bottom right, rgba(255,255,255,.5), transparent 45%);
  mix-blend-mode: overlay;
}

      /* glossy overlay */
      .paper-airmail::before{
        content:""; position:absolute; inset:0; pointer-events:none; border-radius:20px;
        background:linear-gradient(to bottom right, rgba(255,255,255,.55), rgba(255,255,255,0) 45%);
        mix-blend-mode:overlay;
      }
      /* faint heart/floral watermark */
      .paper-airmail::after{
        content:""; position:absolute; inset:0; pointer-events:none; opacity:.07;
        background:
          radial-gradient(120px 90px at 78% 22%, #ffb3c1 0 60%, transparent 61%),
          radial-gradient(140px 110px at 82% 25%, #ffd6e0 0 55%, transparent 56%),
          radial-gradient(circle at 78% 24%, #ff8fab 0 6px, transparent 7px),
          radial-gradient(circle at 86% 18%, #ff8fab 0 7px, transparent 8px);
        filter:blur(1px);
      }

      .ltitle{
        font-family:"Playfair Display",serif; color:#1d1b19; font-size:36px; font-weight:700; margin:0 0 8px; letter-spacing:.2px;
      }
      .ldate{ color:#6b6a68; font-size:14px; margin:0 0 18px }
      .letterhead{ font-family:"Great Vibes",cursive; color:#9b7d6b; font-size:20px; margin-bottom:6px }

      /* Drop cap on first paragraph */
      .paper-airmail .content p:first-of-type::first-letter{
        float:left; font-family:"Playfair Display",serif; font-weight:700;
        font-size:3.1rem; line-height:3rem; padding:6px 10px 0 0; color:#6b5247;
      }

      .btnbar{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0 6px}
      .pbtn{padding:10px 14px;border-radius:12px;border:1px solid #d6d0c6;background:#fff7ec;color:#2c2a28;font-weight:700}
      .pbtn:hover{box-shadow:0 0 0 3px rgba(179,136,255,.25)}
    </style>
    """)


# -------------------- Parsing helpers --------------------
def read_text(path:str)->str:
    with open(path,"r",encoding="utf-8") as f: return f.read()

def split_md(md:str)->Dict[str, Optional[str]]:
    """Return {title, date(str), tags(str), body} and strip those header lines from body."""
    lines = md.splitlines()
    title = date_s = tags_s = None
    drop = set()

    for i, ln in enumerate(lines):
        m = re.match(r'^\s*#\s+(.+?)\s*$', ln)
        if m: title = m.group(1).strip(); drop.add(i); break

    for i, ln in enumerate(lines):
        m = re.match(r'^\s*_date:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})\s*_\s*$', ln, flags=re.I)
        if m: date_s = m.group(1).strip(); drop.add(i); break

    for i, ln in enumerate(lines):
        m = re.match(r'^\s*tags:\s*(.+?)\s*$', ln, flags=re.I)
        if m: tags_s = m.group(1).strip(); drop.add(i); break

    body = "\n".join(ln for i, ln in enumerate(lines) if i not in drop).strip()
    return {"title": title, "date": date_s, "tags": tags_s, "body": body}

# def parse_letter(path:str)->Dict:
#     slug = os.path.splitext(os.path.basename(path))[0]
#     parts = split_md(read_text(path))
#     title = parts["title"] or slug.replace("-", " ")
#     date = None
#     if parts["date"]:
#         try: date = datetime.strptime(parts["date"], "%Y-%m-%d").date()
#         except: pass
#     return dict(slug=slug, title=title, date=date, body_md=parts["body"], path=path)
def parse_letter(path:str)->Dict:
    slug = os.path.splitext(os.path.basename(path))[0]

    # split into date + rest
    if "_" in slug:
        date_part, title_part = slug.split("_", 1)
        list_title = title_part.replace("-", " ").title()
    else:
        date_part, list_title = None, slug.replace("-", " ").title()

    # Default romantic title for inside the letter
    letter_title = "Love you"

    # Date: prefer from filename
    date = None
    try:
        if date_part:
            date = datetime.strptime(date_part, "%Y-%m-%d").date()
    except:
        pass

    return dict(
        slug=slug,
        list_title=list_title,     # shows on envelope list
        letter_title=letter_title, # shows inside the letter
        date=date,
        body_md=read_text(path),
        path=path
    )



def load_letters()->List[Dict]:
    paths = iter_letter_paths()
    return sorted(
        (parse_letter(p) for p in paths),
        key=lambda x:(x["date"] or datetime.min.date(), x["slug"]),
        reverse=True
    )

# -------------------- Views --------------------
def render_list(letters: List[Dict]):
    put_html("<div class='wrap'>")
    put_html("<div class='titlebar'><h2>📜 Love Letters</h2></div>")
    if not letters:
        # helpful empty state with path + quick sample generator
        put_html(f"""
        <div class="empty">
          <div style="font-weight:700;margin-bottom:6px">No letters found.</div>
          <div>Looked in: <span class="kbd">{LETTERS_DIR}</span></div>
          <div style="margin-top:8px">Add some <span class="kbd">.md</span> files there, or click “Create sample letter”.</div>
        </div>
        """)
        return
    put_html("<div class='grid'>")
    for it in letters:
        date_str = it["date"].strftime("%Y-%m-%d") if it["date"] else "—"
        put_html(f"""
        <a class="env" href="?open={it['slug']}">
            <div class="flap"></div>
            <div class="stamp"></div>
            <div class="title">{it['list_title']}</div>
            <div class="date">Date: {date_str}</div>
        </a>
        """)
    put_html("</div></div>")

def render_letter(letter: Dict):
    # 1) Convert markdown -> HTML so we can inject everything in one put_html
    try:
        import markdown as md
        body_html = md.markdown(letter["body_md"])
    except Exception:
        # Fallback: very simple paragraphs/linebreaks if markdown pkg missing
        import html
        t = html.escape(letter["body_md"])
        body_html = "<p>" + t.replace("\n\n", "</p><p>").replace("\n", "<br/>") + "</p>"

    date_str = letter["date"].strftime("%Y-%m-%d") if letter["date"] else "—"

    # 2) Single put_html containing the entire stationery + content
    put_html(f"""
    <div class="letter-wrap">
      <div class="paper-airmail">
        <div class="letter-inner">
          <div class="letterhead">Dear Daniel,</div>
          <h1 class="ltitle">{letter['letter_title']}</h1>
          <p class="ldate">Date: {date_str}</p>
          <div class="content">
            {body_html}
          </div>
          <div class="btnbar">
            <button class="pbtn" onclick="window.history.replaceState({{}},'', window.location.pathname); window.location.href=window.location.pathname">← Back to list</button>
            <button class="pbtn" onclick="window.location.href='/'">🏠 Home</button>
          </div>
        </div>
      </div>
    </div>
    """)


# -------------------- Entry --------------------
from pywebio.output import use_scope
from pywebio.session import eval_js, run_js
from pywebio.input import actions

def app_main():
    inject_theme()
    back_home()

    # persistent content area; do NOT clear the root
    use_scope("content")

    letters = load_letters()

    # open via querystring
    slug = eval_js("new URLSearchParams(window.location.search).get('open')")
    if slug:
        letter = next((x for x in letters if x['slug'] == slug), None)
        if letter:
            with use_scope("content", clear=True):
                render_letter(letter)
            nav = actions("", buttons=[
                {"label":"← Back to list","value":"back"},
                {"label":"🏠 Home","value":"home"},
            ])
            if nav == "home":
                run_js("window.location.href='/'"); return
            run_js("window.location.href = window.location.pathname")
            return

    # list view
    with use_scope("content", clear=True):
        render_list(letters)
