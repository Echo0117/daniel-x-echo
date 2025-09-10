# app/pages/two_weeks_menu.py
from pywebio.input import actions, input, TEXT
from pywebio.output import put_html, put_text, put_image, clear
from app.ui import back_home

def app_main():
    back_home()
    while True:
        clear()
        put_html("<h1 style='color: pink;'>💖 Happy 2 Weeks Anniversary! 💖</h1>")
        choice = actions("What would you like to ask or see?", buttons=[
            {"label": "What's my special nickname?", "value": "nickname"},
            {"label": "How was my day?", "value": "day"},
            {"label": "Show me a surprise!", "value": "surprise"},
            {"label": "Exit", "value": "exit"},
        ])

        clear()
        if choice == "nickname":
            his_nick = input("What sweet nickname do you call me?", type=TEXT)
            clear()
            put_text(f"Aww, you call me “{his_nick}” ❤️ — it melts my heart!") \
                .style('font-size:30px; color: purple;')

        elif choice == "day":
            mood = actions("How was your day today?", buttons=[
                {"label":"😊 Great!", "value":"great"},
                {"label":"😔 Not so good", "value":"bad"},
                {"label":"🤩 Amazing!", "value":"amazing"},
            ])
            clear()
            if mood == "great":
                put_text("So glad you had a great day! You deserve all the smiles. 😁") \
                    .style('font-size:30px; color: green;')
            elif mood == "bad":
                put_text("I'm sorry you had a bad day. I’m here whenever you need me. 🤗") \
                    .style('font-size:30px; color: orange;')
            else:
                put_text("Your amazing days light up my world! ✨") \
                    .style('font-size:30px; color: gold;')

        elif choice == "surprise":
            put_text("Loading image — be patient; or try the GIF!").style('color: orange; font-size:20px')
            sub = actions("Pick your surprise:", buttons=[
                {"label":"A cutie pie", "value":"photo"},
                {"label":"A fun vibe", "value":"gif"},
                {"label":"A secret message", "value":"message"},
            ])
            clear()
            if sub == "photo":
                put_html("<h2>A picture of a cutie pie 🥰</h2>")
                img = open('static/miss_you_compressed.JPG','rb').read()
                put_image(img, width='500px')
            elif sub == "gif":
                put_html("<h2>Enjoy this GIF! 🎉</h2>")
                put_image('https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif', width='400px')
            else:
                put_html("<h2>Your secret message 💌</h2>")
                put_text("“I am grateful every day now — thank God for sending you to my life!!”") \
                    .style('font-size:24px; color: teal;')

        else:
            put_html("<h2>I will always be by your side! 💘</h2>")
            break

        again = actions("", buttons=[
            {"label":"Back to main menu","value":"back"},
            {"label":"End here 💖","value":"exit"},
        ])
        if again == "exit":
            clear()
            put_html("<h2>See you soon, come homeeeee! 🌹</h2>")
            break
