from flask import Flask, render_template

app = Flask(__name__)

# import routes ***DON'T REMOVE***
import ChatFlow.src


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
