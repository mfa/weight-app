from flask import Flask, Response

app = Flask(__name__)

# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_Xxxxxxx'
)

@app.route('/')
def home():
    return Response("Hello World!")

if __name__ == "__main__":
    app.run()
