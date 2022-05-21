from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # The main home poge of the web app is called
    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)