# app/flask_site.py
from flask import Flask
from pywebio.platform.flask import webio_view

# import your page functions (each is a callable: app_main())
from app.pages import eighteen_days, first_love_ai, love_letters, poetry, two_weeks_v1, two_weeks_menu, three_weeks, perseids_app

flask_app = Flask(__name__)

# Map each PyWebIO page to a Flask route
flask_app.add_url_rule(
    "/two-weeks", "two_weeks_v1",
    webio_view(two_weeks_v1.app_main),
    methods=['GET', 'POST', 'OPTIONS']
)
flask_app.add_url_rule(
    "/two-weeks2", "two_weeks_menu",
    webio_view(two_weeks_menu.app_main),
    methods=['GET', 'POST', 'OPTIONS']
)
flask_app.add_url_rule(
    "/eighteen-days", "eighteen-days",
    webio_view(eighteen_days.app_main),
    methods=['GET', 'POST', 'OPTIONS']
)
flask_app.add_url_rule(
    "/three-weeks", "three_weeks",
    webio_view(three_weeks.app_main),
    methods=['GET', 'POST', 'OPTIONS']
)
flask_app.add_url_rule(
    "/perseids", "perseids",
    webio_view(perseids_app.app_main),
    methods=['GET', 'POST', 'OPTIONS']
)
flask_app.add_url_rule(
    "/letters", "letters",
    webio_view(love_letters.app_main),
    methods=['GET', 'POST', 'OPTIONS']
)

flask_app.add_url_rule(
    "/first-love-you", "first_love_you",
    webio_view(first_love_ai.app_main),
    methods=['GET', 'POST', 'OPTIONS']
)

flask_app.add_url_rule(
    "/poetry", "poetry",
    webio_view(poetry.app_main),
    methods=['GET', 'POST', 'OPTIONS']
)
