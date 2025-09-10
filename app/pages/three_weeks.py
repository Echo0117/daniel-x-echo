# app/pages/three_weeks.py
from pywebio.input import actions
from pywebio.output import put_html, put_text, clear
from app.ui import back_home

def app_main():
    back_home()
    clear()
    put_html("""
        <h1 style='color: hotpink; font-size: 48px; text-align: center;'>🎁 Three Weeks Anniversary 🎁</h1>
        <p style='font-size: 24px; color: darkslateblue; text-align: center;'>
            Click the big gift box to discover what I’ve been planning for us...
        </p>
    """)
    box_clicked = actions(buttons=[{'label': '🎁 OPEN THE BOX 🎁', 'value': 'open'}])
    if box_clicked == 'open':
        clear()
        put_html("""
            <div style='background:linear-gradient(to bottom right, pink, lavender);
                        padding:30px;border-radius:20px;text-align:center;color:#333;'>
                <h2 style='font-size: 40px; color: crimson;'>💖 My Love, Happy Three Weeks 💖</h2>
                <p style='font-size: 22px;'>On <b>Friday, July 18th, 2025</b> at <b>9:00 PM</b> — we have a date at:</p>
                <h3 style='font-size: 30px; color: purple;'>🎭 The Setup Stand-Up Comedy Show 🎭</h3>
                <p style='font-size: 20px; color: #800000;'>2 tickets under your name at Will Call. Bring your ID. Doors open 30 minutes before showtime.</p>
                <p style='font-size: 24px; color: darkred; margin-top: 30px;'>I can’t wait to laugh the night away with you…</p>
            </div>
        """)
