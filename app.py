from flask import Flask, render_template

app = Flask(__name__)


@app.route('/<page>')
def base(page):
    return render_template(f'{page}.html')

if __name__ == '__main__':
    app.run()
