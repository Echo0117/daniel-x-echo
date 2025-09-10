# app/theme.py
from pywebio.output import put_html

BASE_CSS = """
<style>
:root{
  --bg:#0b0f1a; --card:#11162a; --ink:#eaf0ff; --muted:#9fb3ff; --ring:#80ffdb; --accent:#ff85b3;
}
body{background:radial-gradient(1200px 600px at 0% -20%,#19264a22,transparent),var(--bg);color:var(--ink)}
.p-card{background:linear-gradient(180deg,#11162a,#0e1430);border:1px solid #2a345f;border-radius:18px;padding:18px;margin:10px 0;box-shadow:0 16px 44px #0007}
.p-title{font-size:22px;font-weight:800;margin:6px 0 10px}
.p-muted{opacity:.85}
.p-btn{display:inline-block;padding:10px 14px;border-radius:12px;border:1px solid #2a345f;background:#151c35;color:var(--ink);text-decoration:none;font-weight:700}
.p-btn:hover{border-color:var(--ring);box-shadow:0 0 0 3px #80ffdb33}
</style>
"""

def inject_base():
    put_html(BASE_CSS)
