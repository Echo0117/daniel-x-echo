from datetime import date
from pywebio import start_server
from pywebio.output import (
    put_markdown, put_html, put_buttons, put_row, put_column,
    use_scope, popup, toast
)
from pywebio.session import set_env
from app.ui import back_home

# ----- Personalize these -----
MEETING_DATE = date(2025, 6, 23)           # The day you met
DATE_NIGHT   = date(2025, 8, 12)           # The Perseids date night
BOYFRIEND_NAME = "Honey"
YOUR_NAME = "Your favorite Echo"
RESTAURANT_NAME = "Dinner for Two"        # You can customize
FERRIS_PLACE = "Ferris Wheel Adventure"   # You can customize
OCEAN_SPOT = "Ocean View Point"           # You can customize

# Put your MP3 into ./static as 'brooklyn_baby.mp3' (recommended for reliability)
# You can use a hosted track instead (user-provided):
AUDIO_SRC = "https://audio.com/user--1783173244587049/audio/lana-del-rey-brooklyn-baby-official-audio"  # fallback to /static if needed

# --------------------------------

HEART_CSS = """
<style>
:root{
  --bg:#0b0f1a; --card:#11162a; --accent:#ffd166; --rose:#ff6b88; --mint:#80ffdb; --lav:#b388ff; --text:#eaf0ff;
}
html,body{height:100%;}
body{background:linear-gradient(160deg,#0b0f1a 0%,#051126 100%);font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Ubuntu;}
.container{max-width:880px;margin:0 auto;padding:28px;}
.header{display:flex;align-items:center;gap:12px;margin-bottom:14px;color:var(--text)}
.logo{width:38px;height:38px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#ffd1dc 0%,#ff7eb3 45%,#ff758c 100%);box-shadow:0 0 20px #ff7eb380}
.h1{font-size:28px;font-weight:800;letter-spacing:.3px}
.sub{opacity:.8}

.nav{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 22px}
.nav button{border:none;padding:10px 14px;border-radius:14px;background:#151c35;color:var(--text);cursor:pointer;font-weight:700}
.nav button:hover{transform:translateY(-1px);box-shadow:0 8px 24px #0006}

.card{background:linear-gradient(180deg,#11162a,#0e1430);color:var(--text);border:1px solid #2a345f;border-radius:20px;padding:18px;box-shadow:0 16px 40px #0007}
.card h2{margin:0 0 10px;font-size:22px}
.card p{opacity:.92}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-top:12px}
.kicker{color:var(--accent);font-weight:800;text-transform:uppercase;letter-spacing:.12em;font-size:11px}
.badge{display:inline-flex;align-items:center;gap:8px;border:1px dashed #39406c;padding:6px 10px;border-radius:999px;margin-top:8px}
.count{font-size:40px;font-weight:900;}

/* Floating hearts */
#heart-sky{position:fixed;inset:0;pointer-events:none;overflow:hidden}
.heart{position:absolute;width:18px;height:18px;background:radial-gradient(circle at 30% 30%,#ffd1dc 0%,#ff7eb3 45%,#ff4d6d 100%);transform:rotate(45deg);animation:float 6s linear infinite;opacity:.9}
.heart:before,.heart:after{content:"";position:absolute;width:18px;height:18px;background:inherit;border-radius:50%}
.heart:before{left:-9px}
.heart:after{top:-9px}
@keyframes float{0%{transform:translateY(100vh) rotate(45deg)}100%{transform:translateY(-20vh) rotate(45deg)}}

/* Meteor shower */
.sky{position:relative;isolation:isolate;height:240px;border-radius:18px;background:radial-gradient(1200px 400px at 20% -40%,#213150 0%,transparent 50%),linear-gradient(180deg,#0b1020,#040c1a)}
.meteor{position:absolute;top:-10px;width:2px;height:120px;background:linear-gradient(180deg,white,transparent);filter:drop-shadow(0 0 6px #fff);opacity:.9;transform:rotate(45deg);animation:shoot 2.5s linear infinite}
.meteor:nth-child(2){left:40% ;animation-delay:.6s}
.meteor:nth-child(3){left:70% ;animation-delay:1.2s}
.meteor:nth-child(4){left:85% ;animation-delay:1.8s}
@keyframes shoot{0%{transform:translate(-50vw,-30vh) rotate(45deg)}100%{transform:translate(20vw,40vh) rotate(45deg)}}

.footer{opacity:.75;font-size:12px;margin-top:18px}
  /* Make generic buttons larger/clearer */
  .btn{font-size:16px !important;padding:10px 16px !important;border-radius:12px !important}
  /* Improve body text contrast and size */
  .card p{opacity:1;font-size:16px;line-height:1.6}
  /* Notes badges styling */
  .badge{font-size:15px}
</style>
"""

AUDIO_HTML = f"""
<div class=\"card\">
  <h2>Now Playing: Brooklyn Baby</h2>
  <audio controls preload=\"auto\" style=\"width:100%\">
    <source src=\"{AUDIO_SRC}\" type=\"audio/mpeg\">
    Your browser does not support audio.
  </audio>
  <div class=\"footer\">If the player doesn't start, <a href=\"{AUDIO_SRC}\" target=\"_blank\" rel=\"noopener\">open the track</a> in a new tab.</div>
</div>
"""


# ------- Helpers -------

def days_since(d: date) -> int:
    return (date.today() - d).days


# ------- Sections -------

def header(days):
    put_html(HEART_CSS)
    set_env(title=f"{BOYFRIEND_NAME} ✦ Perseids Surprise")

    put_html('<div id="heart-sky"></div>')

    put_html(f"""
    <div class=\"container\"> 
      <div class=\"header\">
        <div class=\"logo\"></div>
        <div>
          <div class=\"h1\">Happy {days}<sup>th</sup> Day, {BOYFRIEND_NAME}! ✨</div>
          <div class=\"sub\">From {YOUR_NAME} · {date.today().strftime('%b %d, %Y')}</div>
        </div>
      </div>
    </div>
    """)

    # Navigation bar (now includes a real Home)
    put_row([
        put_buttons([
            dict(label='🏠 Home', value='home'),
            dict(label='💌 Open the Surprise', value='splash'),
            dict(label='📸 Little Moments', value='moments'),
            dict(label='📅 8/12 Date Plan', value='plan'),
            dict(label='🌠 Make a Wish', value='wish'),
            dict(label='🎵 Our song', value='song'),
        ], onclick=nav)
    ]).style('margin:0 28px')

    put_html('<div class="container">')
    use_scope('main', clear=True)


def nav(choice):
    with use_scope('main', clear=True):
        if choice == 'home':
            home()
        elif choice == 'splash':
            splash()
        elif choice == 'moments':
            moments()
        elif choice == 'plan':
            plan()
        elif choice == 'wish':
            wish()
        elif choice == 'song':
            put_html('<div class="card">'+AUDIO_HTML+'<div class="footer">Tip: press play and read the messages ♡</div></div>')


def sprinkle_hearts(n=22):
    # Create n floating hearts with random positions/timings (pure CSS/HTML; no JS needed)
    import random
    hearts = []
    for _ in range(n):
        left = random.randint(0, 100)
        delay = round(random.uniform(0, 3), 2)
        size = random.randint(12, 22)
        hearts.append(f'<div class="heart" style="left:{left}vw;animation-delay:{delay}s;width:{size}px;height:{size}px"></div>')
    put_html('<div id="heart-sky">' + ''.join(hearts) + '</div>')


def home():
    sprinkle_hearts()
    put_html(
        """
        <div class='card'>
          <h2>Welcome, my favorite person ♡</h2>
          <p>This is a tiny site I made for you. Ready to open the surprise?</p>
        </div>
        """
    )
    put_buttons([{'label':'Open the surprise ✨','value':'open'}], onclick=lambda _: splash())


def splash():
    sprinkle_hearts()
    put_html(f"""
    <div class="grid">
      <div class="card">
        <div class="kicker">Since we met</div>
        <div class="count">{days_since(MEETING_DATE)} days</div>
        <p>I still get butterflies every time I think of you.</p>
        <div class="badge">💖 Met on {MEETING_DATE.strftime('%b %d, %Y')}</div>
      </div>
      <div class="card">
        <h2>Three tiny reasons I adore you</h2>
        <ul>
          <li>Your laugh makes everything lighter.</li>
          <li>You notice the little things.</li>
          <li>You make ordinary moments feel like magic.</li>
        </ul>
      </div>
      <div class="card">
        <h2>A secret just for you</h2>
        <p>On <b>{DATE_NIGHT.strftime('%b %d')}</b>, meet me for dinner, then a ride on the ferris wheel, and finally—under the stars—to watch the Perseids together. 🌠</p>
      </div>
    </div>
    """)


# Note reveals without JS bridge
MESSAGES = [
    'You feel like home.',
    'I love the way you say my name.',
    'Thank you for being gentle with my heart.',
    'I’m proud of you — always.',
    'You make ordinary days sparkle.',
    'You’re my favorite “what are you doing?”',
    'I can’t wait for our ferris wheel wish.',
    'Under the Perseids, it’s you + me.'
]
_note_i = 0

def reveal_note():
    global _note_i
    with use_scope('notes', clear=False):
        if _note_i < len(MESSAGES):
            put_html(f"<div class='badge'>💗 · {MESSAGES[_note_i]}</div>")
            _note_i += 1
        else:
            toast('All notes revealed! 💞')


def moments():
    # Three-box layout like before: Notes reveal, Timeline, Extra message
    put_html("""
    <div class='grid'>
      <div class='card'>
        <h2>Tap for a memory</h2>
        <p>Every click reveals a little note.</p>
        <div id='notes_scope'></div>
      </div>
      <div class='card'>
        <h2>Our mini‑timeline</h2>
        <ul>
          <li>Jun 23: We met at 12:01 — a lucky time.</li>
           <li>Our inside joke: the ferris wheel wife/husband we still haven't ridden together 🎡</li>
          <li>Today: this little website made for you.</li>
        </ul>
      </div>
      <div class='card'>
        <h2>When you are in your mind, in your little world…</h2>
        <p>…please leave the door open, so Echo can walk in, and stay with you there. You never have to choose between your world and my world, coz we share the same drive! :3</p>
      </div>
    </div>
    """)
    # Add a dedicated scope right below the first card for notes
    use_scope('notes', clear=False)
    put_buttons([{'label':'Reveal one ✨','value':'reveal'}], onclick=lambda _: reveal_note())


def plan():
    put_html(f"""
    <div class='grid'>
      <div class='card'>
        <h2>📅 The Plan for {DATE_NIGHT.strftime('%b %d')}</h2>
        <p>Dress comfy, bring a light jacket. I’ll handle everything else.</p>
        <div class='grid'>
          <div class='card'>
            <div class='kicker'>Stop 1</div>
            <h3>🍽️ {RESTAURANT_NAME}</h3>
            <p>Cozy dinner to start the night. I booked us a table.</p>
          </div>
          <div class='card'>
            <div class='kicker'>Stop 2</div>
            <h3>🎡 {FERRIS_PLACE}</h3>
            <p>Finally take that ride we missed. One wish at the top.</p>
          </div>
          <div class='card'>
            <div class='kicker'>Stop 3</div>
            <h3>🌊 {OCEAN_SPOT}</h3>
            <p>Blanket, snacks, and a sky full of meteors — the Perseids.</p>
          </div>
        </div>
      </div>
      <div class='card'>
        <h2>Bring list</h2>
        <ul>
          <li>Light jacket / hoodie</li>
          <li>Comfy shoes</li>
          <li>Warm blanket</li>
          <li>A wish you’re ready to make</li>
        </ul>
      </div>
    </div>
    """)


def wish_popup():
    popup('Awww', put_column([
        put_html('<img src="https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif" style="width:100%;border-radius:12px">'),
        put_markdown("**Awww! Let's make it come true together.** 💖")
    ]))


def wish():
    put_html(
        """
        <div class='card'>
          <h2>Look up — make a wish together</h2>
          <div class='sky'>
            <div class='meteor'></div>
            <div class='meteor'></div>
            <div class='meteor'></div>
            <div class='meteor'></div>
          </div>
          <p>Close your eyes for three seconds and think of us. Then tell me your wish. 💫</p>
        </div>
        """
    )
    put_buttons([{'label':'I made my wish ✨','value':'wish'}], onclick=lambda _: wish_popup())


# # ------- App entry -------

# def main():
#     days = days_since(MEETING_DATE)
#     header(days)
#     with use_scope('main', clear=True):
#         home()  # real landing page now
def app_main():
    back_home()
    header(days_since(MEETING_DATE))
    with use_scope('main', clear=True):
        home()
