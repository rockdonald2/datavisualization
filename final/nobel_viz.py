# nobel_viz.py

from flask import Flask, send_from_directory, render_template

app = Flask(__name__)

@app.route('/')

def root():
    ''' return send_from_directory('.', './templates/index.html') '''
    return render_template('index.html', title='Nobel visualization')
# a metódus az első argumentumban meghatározott mappából, a második argumentumban
# meghatározott állományt szolgáltatja elérésre

if __name__ == '__main__':
    app.run(port=8000)