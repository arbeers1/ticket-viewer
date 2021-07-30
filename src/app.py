from flask import Flask, render_template

#Start application
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')