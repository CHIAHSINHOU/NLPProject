# all the imports
from __future__ import with_statement
from flask import Flask, request, redirect, url_for, render_template
import sys
sys.path.append('correct')
from adjCorrectApi import adjCorrect

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


iq = ""
score = []
adj = ""


@app.route('/')
def show_result():
    iq = request.args[
        'iq'] if 'iq' in request.args else ''
    if iq == "":
        score = []
        adj = ""
    else:
        adj, score = adjCorrect(iq)
        if score[0][0] == adj:
            score = []
    return render_template('show_result.html', output=score[:5], inputquery=iq, adj=adj)


@app.route('/search', methods=['POST'])
def search_entry():
    iq = request.form['text']
    return redirect(url_for('show_result', iq=iq))

if __name__ == '__main__':
    app.run()
