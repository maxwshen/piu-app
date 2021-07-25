from flask import Flask, redirect, render_template

app = Flask(__name__)


#what to serve for a given page.
@app.route('/')
def index():
# def index(page):
  # return render_template('/articles/' + page + '.html')
  return 'Hello world!'