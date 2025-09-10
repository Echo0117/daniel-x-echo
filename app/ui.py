# app/ui.py
from pywebio.output import put_buttons, put_html
from pywebio.session import run_js

def back_home(label="← Back to Home", sticky=True):
    """
    Renders a back-to-home button. If sticky=True, shows a top bar.
    Usage: from app.ui import back_home; back_home()
    """
    if sticky:
        put_html("""
        <div style="position:sticky;top:0;z-index:9999;backdrop-filter:saturate(1.2) blur(6px);
                    background:linear-gradient(180deg,rgba(17,22,42,.85),rgba(14,20,48,.6));
                    border-bottom:1px solid #2a345f;padding:8px 10px;margin:-10px -10px 10px -10px;">
          <button id="homebtn" style="all:unset;cursor:pointer;padding:8px 12px;border:1px solid #2a345f;border-radius:10px;">
            ← Back to Home
          </button>
        </div>
        <script>
          document.getElementById('homebtn').onclick = () => { window.location.href = '/' }
        </script>
        """)
    else:
        put_buttons(
            [{"label": label, "value": "home"}],
            onclick=lambda _: run_js("window.location.href='/'")
        ).style('margin:8px 0')
