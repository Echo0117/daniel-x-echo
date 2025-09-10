from flask import Flask
from pywebio.platform.flask import webio_view

# import your PyWebIO pages (each exposes app_main())
from app.pages import two_weeks_v1, two_weeks_menu, open_box, three_weeks, perseids_app

app = Flask(__name__, static_folder="static")

HOME_HTML = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Echo × Daniel</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='64' height='64'%3E%3Ctext y='52' x='6' font-size='54'%3E%F0%9F%92%95%3C/text%3E%3C/svg%3E">
<style>
:root{
  --bg:#0b0f1a; --bg2:#071024; --card:#11162a; --ink:#eaf0ff; --muted:#b6c6ff;
  --ring:#80ffdb; --accent:#ff85b3; --accent2:#b388ff; --line:#2a345f;
}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0; color:var(--ink); font-family: ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto;
  background:
    radial-gradient(1200px 600px at -10% -20%, #1b2a5522 0%, transparent 60%),
    radial-gradient(1200px 600px at 110% 0%, #1b2a5522 0%, transparent 60%),
    linear-gradient(160deg, var(--bg), var(--bg2));
}

/* Floating hearts (subtle) */
.floating{position:fixed; inset:0; pointer-events:none; overflow:hidden}
.heart{position:absolute; width:16px; height:16px; transform:rotate(45deg);
  background: radial-gradient(circle at 30% 30%, #ffd1dc 0%, #ff7eb3 50%, #ff4d6d 100%);
  opacity:.6; animation:float 12s linear infinite}
.heart:before,.heart:after{content:""; position:absolute; width:16px; height:16px; background:inherit; border-radius:50%}
.heart:before{left:-8px} .heart:after{top:-8px}
@keyframes float { 0%{ transform:translateY(100vh) rotate(45deg)} 100%{ transform:translateY(-20vh) rotate(45deg)} }

.wrap{max-width:1100px; margin:0 auto; padding:28px}
.header{
  margin:52px 0 22px; text-align:center;
}
.tag{display:inline-block; border:1px solid var(--line); color:var(--muted);
  padding:6px 10px; border-radius:999px; font-size:12px; letter-spacing:.12em}
.h1{font-size:44px; font-weight:900; letter-spacing:.2px; margin:12px 0}
.p{opacity:.92; max-width:780px; margin:0 auto}
.kiss{
  margin:10px auto 0; width:72px; height:72px; border-radius:50%;
  background: radial-gradient(circle at 30% 30%, #ffd1dc 0%, #ff7eb3 50%, #ff4d6d 100%);
  box-shadow:0 0 30px #ff7eb355; animation:pulse 3s ease-in-out infinite
}
@keyframes pulse { 0%,100%{ transform:scale(1)} 50%{ transform:scale(1.08)} }

.grid{
  display:grid; gap:18px; margin:28px 0 60px;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}
.card{
  background:linear-gradient(180deg, var(--card), #0e1430);
  border:1px solid var(--line); border-radius:18px; padding:18px;
  box-shadow:0 20px 60px #0007; position:relative; overflow:hidden
}
.card:before{
  content:""; position:absolute; inset:-1px; z-index:0;
  background: radial-gradient(400px 120px at -10% -10%, #80ffdb22, transparent 60%);
}
.card h3{margin:0 0 6px; font-size:18px; position:relative; z-index:1}
.card p{margin:6px 0 14px; opacity:.9; min-height:48px; position:relative; z-index:1}
.btn{
  position:relative; z-index:1;
  display:inline-flex; align-items:center; gap:8px; padding:10px 14px;
  border-radius:12px; border:1px solid var(--line); background:#151c35;
  color:var(--ink); text-decoration:none; font-weight:700;
  transition: box-shadow .2s, transform .08s, border-color .2s;
}
.btn:hover{border-color:var(--ring); box-shadow:0 0 0 4px #80ffdb33}
.btn:active{transform:translateY(1px)}
.emoji{font-size:18px}

.footer{
  text-align:center; opacity:.8; font-size:13px; margin:0 0 40px
}
.hr{height:1px; background:var(--line); border:none; margin:28px 0}
.small{opacity:.75}
</style>
</head>
<body>
  <div class="floating">
    <!-- a few floating hearts -->
    <div class="heart" style="left:12vw; animation-delay:.2s"></div>
    <div class="heart" style="left:28vw; animation-delay:1.1s; width:14px; height:14px"></div>
    <div class="heart" style="left:63vw; animation-delay:.6s"></div>
    <div class="heart" style="left:82vw; animation-delay:1.8s; width:18px; height:18px"></div>
  </div>

  <div class="wrap">
    <header class="header">
      <div class="kiss"></div>
      <div class="tag">for Daniel · from Echo</div>
      <h1 class="h1">Echo × Daniel</h1>
      <p class="p">Tiny surprises, sweet notes, and starry plans. Choose a card and open a page ✨</p>
    </header>

    <main class="grid">
      <div class="card">
        <h3>🌠 Perseids Surprise</h3>
        <p>Dinner → ferris wheel → a meteor shower night. Bring a wish.</p>
        <a class="btn" href="/perseids"><span class="emoji">Open</span> /perseids</a>
      </div>
      <div class="card">
        <h3>💖 Two Weeks (v1)</h3>
        <p>Say your name, share your mood, get a tiny surprise.</p>
        <a class="btn" href="/two-weeks"><span class="emoji">Open</span> /two-weeks</a>
      </div>
      <div class="card">
        <h3>💗 Two Weeks (menu)</h3>
        <p>Nickname, day check-in, and a small surprise menu.</p>
        <a class="btn" href="/two-weeks2"><span class="emoji">Open</span> /two-weeks2</a>
      </div>
      <div class="card">
        <h3>🎁 Open-Box Gifts</h3>
        <p>Pick a box to reveal a photo, a message, or a secret.</p>
        <a class="btn" href="/open-box"><span class="emoji">Open</span> /open-box</a>
      </div>
      <div class="card">
        <h3>🎉 Three Weeks Surprise</h3>
        <p>One big reveal, wrapped in pink and lavender.</p>
        <a class="btn" href="/three-weeks"><span class="emoji">Open</span> /three-weeks</a>
      </div>
    </main>

    <div class="hr"></div>
    <footer class="footer">
      <p class="small">Static music & images live in <code>/static</code> · Made with 💙 PyWebIO</p>
    </footer>
  </div>
</body>
</html>
"""

@app.route("/")
def index():
    return HOME_HTML

# Map PyWebIO pages -> Flask routes
app.add_url_rule("/two-weeks",  "two_weeks_v1",  webio_view(two_weeks_v1.app_main),  methods=['GET','POST','OPTIONS'])
app.add_url_rule("/two-weeks2", "two_weeks_menu",webio_view(two_weeks_menu.app_main),methods=['GET','POST','OPTIONS'])
app.add_url_rule("/open-box",   "open_box",      webio_view(open_box.app_main),      methods=['GET','POST','OPTIONS'])
app.add_url_rule("/three-weeks","three_weeks",   webio_view(three_weeks.app_main),   methods=['GET','POST','OPTIONS'])
app.add_url_rule("/perseids",   "perseids",      webio_view(perseids_app.app_main),  methods=['GET','POST','OPTIONS'])

if __name__ == "__main__":
    # Local dev
    app.run(host="0.0.0.0", port=8000, debug=True)
