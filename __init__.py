from flask import Flask
import requests
import admin
import main
app = Flask(__name__)
app.config.update(
    SECRET_KEY='dev'
)


if __name__ == "__main__":
    app.register_blueprint(main.mn)
    app.register_blueprint(admin.adm)
    app.add_url_rule('/', endpoint='main')  # ассоциирует первый объект со вторым
    app.run()
