from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return redirect("/index", code=302)


@app.route('/<page>')
def base(page):
    return render_template(f'{page}.html')

if __name__ == '__main__':
    app.run()