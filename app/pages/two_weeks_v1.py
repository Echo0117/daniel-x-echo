# app/pages/two_weeks_v1.py
from pywebio.input import input, actions, TEXT
from pywebio.output import put_html, put_text, put_image, clear
from app.ui import back_home

def app_main():
    back_home()
    while True:
        name = input("Hi love! What's your name?", type=TEXT)
        clear()
        put_html(f"<h1 style='color: pink;'>Happy 2 Weeks, {name}! 💖</h1>")

        mood = actions("How are you feeling today?", buttons=[
            {'label': '😊 Happy', 'value': 'happy'},
            {'label': '😔 Sad', 'value': 'sad'},
            {'label': '😎 Excited', 'value': 'excited'}
        ])
        clear()
        if mood == 'happy':
            put_text("Your happiness lights up my world! 💛").style('font-size:30px')
        elif mood == 'sad':
            put_text("I'm here to cheer you up! 🍀").style('font-size:30px')
        else:
            put_text("Your excitement is contagious! 🎉").style('font-size:30px')

        cont = actions("Ready for a surprise?", buttons=[
            {'label': 'Yes, show me!', 'value': 'yes'},
            {'label': 'Maybe later', 'value': 'no'}
        ])
        clear()
        if cont == 'yes':
            put_html("<h2 style='color: purple;'>🎁 Here's your surprise! 🎁</h2>")
            put_image('https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif', width='400px')
        else:
            put_text("No worries! We can share it anytime. 🤗").style('font-size:30px')

        more = actions("Would you like to see more messages?", buttons=[
            {'label': 'Yes', 'value': 'yes'},
            {'label': 'No', 'value': 'no'}
        ])
        clear()
        if more == 'no':
            put_html("<h2>I will always be by your side! 💘</h2>")
            break

        put_html("<p style='font-size:24px;'>You're my sunshine, my love, my everything. 🥰</p>")
        put_image('https://media.giphy.com/media/xT0BKmtQGLbumr5RCM/giphy.gif', width='400px')

        again = input("Type 'exit' to end or press Enter to restart", type=TEXT)
        clear()
        if (again or "").lower() == 'exit':
            put_html("<h2>Until next time! 🌹</h2>")
            break
