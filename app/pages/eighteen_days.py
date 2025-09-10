# app/pages/eighteen_days.py
from pywebio.input import actions
from pywebio.output import put_html, put_text, put_image, clear
from app.ui import back_home
from app.theme import inject_base

def app_main():
    back_home()
    inject_base()
    while True:
        clear()
        put_html("<h1 style='color: hotpink;'>🎁 18 days Anniversary 🎁</h1>")
        put_html("<p>Pick a gift box to open:</p>")

        box = actions(buttons=[
            {'label': '🎁 Box 1', 'value': 'box1'},
            {'label': '🎁 Box 2', 'value': 'box2'},
            {'label': '🎁 Box 3', 'value': 'box3'},
            {'label': '❌ I’m done', 'value': 'exit'},
        ])

        clear()
        if box == 'box1':
            put_html("<h2>Here’s a lovely photo of us! 📸</h2>")
            img = open('static/cartoon.jpg', 'rb').read()
            put_image(img, width='400px')

        elif box == 'box2':
            put_html("<h2>I have a question for you</h2>")
            put_text("“Мне ты очень, очень нравишься… Хочешь быть моим парнем?”") \
                .style('font-size: 28px; color: purple;')

        elif box == 'box3':
            put_html("<h2>My secret message… 'love' 🤫</h2>")
            put_text("“JCP LLJZ WFQC E NIOI MIOX, T KVR EC NUFSZDP WO”") \
                .style('font-size: 28px; color: teal;')

        elif box == 'exit':
            put_html("<h2>Will be with you always! 💖</h2>")
            break

        again = actions("Open another box?", buttons=[
            {'label': '🎁 Yes!', 'value': 'yes'},
            {'label': '❌ No, I’m good.', 'value': 'no'}
        ])
        if again == 'no':
            put_html("<h2>Aww such a non-greedy boy! 😘</h2>")
            break
