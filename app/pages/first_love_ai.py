# app/pages/first_love_ai.py
import os, random, re
from pywebio.output import put_html, put_row, put_column, put_markdown, put_image, use_scope
from pywebio.input import textarea, file_upload, actions, input_group
from app.ui import back_home

# ---- model (PEFT) ----
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
try:
    import torch; torch.set_num_threads(1)
except Exception:
    pass

from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from peft import PeftModel, PeftConfig

BASE_ID   = os.getenv("FIRST_LOVE_BASE", "distilbert-base-uncased")
ADAPTERID = os.getenv("FIRST_LOVE_ADAPTER", "first_love_you/deduction_classifier")

_classifier = None
def get_classifier():
    """Lazy-load once; tiny-instance friendly."""
    global _classifier
    if _classifier: return _classifier
    try:
        peft_cfg = PeftConfig.from_pretrained(ADAPTERID)
        base_id = peft_cfg.base_model_name_or_path or BASE_ID
    except Exception:
        base_id = BASE_ID
    base = AutoModelForSequenceClassification.from_pretrained(base_id, num_labels=10)
    try:
        model = PeftModel.from_pretrained(base, ADAPTERID)
    except Exception:
        model = base
    tok = AutoTokenizer.from_pretrained(base_id)
    _classifier = pipeline("text-classification", model=model, tokenizer=tok, return_all_scores=False)
    return _classifier

ROMANTIC = {
    "0":"Destiny","1":"Unspoken Love","2":"Serendipity","3":"Shared Dreams","4":"Forever Promises",
    "5":"Cozy Moments","6":"Endless Laughter","7":"Warm Hugs","8":"Moonlight Walks","9":"Coffee Kisses"
}
COMPS = [
    "Your smile is my favorite sunrise 🌅",
    "Every day with you feels like a fairytale 🏰",
    "You're the poetry my soul always sought 💖",
    "You're the melody in my silence 🎶",
    "You're the only person who can steal my heart with a glance 💘",
    "When I see you, I forget how to breathe 🫶",
    "You're my once in a lifetime, never again 💫",
    "Even time slows down when you hold my hand ⏳",
    "You're not my type — you're my soulmate ❤️",
    "My heart beats in your rhythm 🌹",
]
POEMS = [
    "Roses are red, violets are blue, every love story is beautiful, but ours is the truest of true 💕",
    "If love is a language, you're every word I've ever wanted to say 💌",
    "We are pages of a book, meant to be read hand in hand 📖",
    "My world began the moment you said 'I love you' 🌍",
    "You are the poem I never knew how to write, and this life is the story I always wanted to tell with you 📝",
    "In a sea of stars, your soul is my North 🌠",
    "Every second with you is a verse I never want to end ✍️",
    "We whispered under moons, but our hearts sang the loudest 💞",
    "Loving you is my favorite forever 🎀",
]

def _css():
    put_html("""
<link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600&family=Gloria+Hallelujah&display=swap" rel="stylesheet">
<style>
  :root{ --ink:#111; --edge:#1a1e2e; --panel:#ffffff; }
  .wrap{max-width:1040px;margin:20px auto;padding:0 16px;font-family:'Gloria Hallelujah', cursive;color:var(--ink)}
  .title{font-size:48px;text-align:center;margin:6px 0}
  .subtitle{font-size:24px;text-align:center;opacity:.9;margin:6px 0 16px}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
  @media (max-width:900px){ .grid{grid-template-columns:1fr} }
  .panel{background:var(--panel);border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.08);padding:12px;border:2px solid var(--edge)}
  .label{font-size:14px;opacity:.75;margin:6px 0}
  textarea{width:100%;min-height:130px;border-radius:12px;border:2px solid var(--edge);background:#f5f7ff;padding:12px;font-family:inherit;font-size:16px}
  .file{width:100%;padding:12px;border:2px dashed var(--edge);border-radius:12px;background:#fafbff}
  .btn{display:inline-block;background:#111a2e;color:#fff;font-weight:700;border:none;border-radius:12px;padding:10px 14px;margin-top:10px;cursor:pointer}
  .btn:hover{filter:brightness(1.05)}
  .gif{height:220px;display:flex;align-items:center;justify-content:center;background:#fff;border-radius:12px;overflow:hidden;border:2px solid var(--edge)}
  .gif img{max-width:100%;max-height:100%}
  .result{margin-top:18px}
  .result-box{font-family:'Dancing Script', cursive; font-size:28px; line-height:1.6; color:#8B0000;
              background:rgba(255,255,255,.88); border-radius:12px; padding:16px}
  .preview{margin-top:12px;text-align:center}
  .preview img{max-width:100%;border-radius:12px}
</style>
""")

def app_main():
    _css()
    back_home()
    use_scope("content")

    # Header
    with use_scope("content", clear=True):
        put_html("<div class='wrap'>")
        put_html("<h1 class='title'>💘 First 'I love you' Dainiversary</h1>")
        put_html("<h2 class='subtitle'>✨ Let Echo AI uncover the romantic theme of your message!</h2>")

        # Right column (GIF + result holder) first, so it shows before submit
        def right_col():
            items = []
            # GIF from static or skip
            gif_path = os.path.join("static","first_love","kiss.gif")
            if os.path.exists(gif_path):
                items.append( put_html("<div class='gif'>") )
                items.append( put_image(open(gif_path,"rb").read()) )
                items.append( put_html("</div>") )
            else:
                items.append( put_html("<div class='gif' style='color:#666;display:flex;align-items:center;justify-content:center'>Add a GIF at <code>static/first_love/kiss.gif</code></div>") )
            items.append( put_html("<div id='py-result' class='result'></div>") )
            items.append( put_html("<div id='py-preview' class='preview'></div>") )
            return items

        # Build grid with PyWebIO layout (no JS)
        put_row([
            put_column([
                put_html("<div class='panel'>"),
                put_html("<div class='label'>Textbox</div>"),
            ]),
            put_column([
                put_html("<div class='panel'>"),
                *right_col(),
                put_html("</div>"),
            ])
        ])

        # The form lives after left panel open tags so it visually sits inside it
        vals = input_group("", [
            textarea(name="text", placeholder="Write something romantic..."),
            file_upload("Upload a Memory (Optional)", name="img", accept="image/*", multiple=False, max_size="25M"),
            actions("", name="do", buttons=[{"label":"Reveal the Romance 💌", "value":"go"}])
        ])

        # Only proceed if pressed the button
        if not vals or vals.get("do") != "go":
            put_html("</div></div>")  # close panel + wrap
            return

        text = (vals.get("text") or "").strip()
        img  = vals.get("img")  # {'filename','content','mime_type'} or None

        # Compute / render result
        if not text:
            put_html("<script>document.getElementById('py-result').innerHTML = `<div class='result-box'>Please write something romantic 🌹</div>`;</script>")
        else:
            clf = get_classifier()
            out = clf(text)[0]
            label = re.sub(r"^LABEL_","", out["label"])
            theme = ROMANTIC.get(label, "Mystery")
            comp  = random.choice(COMPS)
            poem  = random.choice(POEMS)
            res_html = f"""
            <div class='result-box'>
              💘 <b>Romantic Theme:</b> <u>{theme}</u><br>
              💌 <b>Confidence:</b> {out['score']:.2%}<br><br>
              💖 {comp}<br><br>
              <i>📖 {poem}</i>
            </div>
            """
            put_html(f"<script>document.getElementById('py-result').innerHTML = {res_html!r};</script>")

        # Show uploaded image below result (like Gradio)
        if img and img.get("content"):
            from base64 import b64encode
            b64 = b64encode(img["content"]).decode()
            mime = img.get("mime_type","image/png")
            put_html(f"<script>document.getElementById('py-preview').innerHTML = `<img src='data:{mime};base64,{b64}'/>`;</script>")
        else:
            put_html("<script>document.getElementById('py-preview').innerHTML = '';</script>")

        put_html("</div></div>")  # close left panel + wrap
