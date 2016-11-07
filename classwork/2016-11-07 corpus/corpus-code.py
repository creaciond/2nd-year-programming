from flask import Flask
from flask import render_template, redirect, url_for, request
from urllib.parse import unquote

app = Flask(__name__)


def collect_corpus():
    with open('data/test.txt', 'r', encoding='utf-8') as f:
        sents = [line.strip() for line in f.readlines()
                if line.strip != '']
    return sents

def search(word):
    return [sent.replace(word, '<b>' + word + '</b>') for sent in corpus if word in sent]
    

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results')
def result():
    if request.args:
        word = unquote(request.args['word'])
        sentences = search(word)
        return render_template('results.html', sents=sentences)
    return redirect(url_for('index'))


if __name__ == '__main__':
    corpus = collect_corpus()
    app.run(debug=True)
