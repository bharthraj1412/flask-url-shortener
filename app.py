# app.py
import os
from flask import Flask, render_template, request, flash, redirect
from models import Urls, SessionLocal
import string, random

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        new_entry = Urls(short_url=short_url, original_url=original_url)
        with SessionLocal() as session:
            session.add(new_entry)
            session.commit()
            flash(f"{original_url} was saved successfully! Short URL: {short_url}\n")
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_short_url(short_url):
    with SessionLocal() as session:
        entry = session.query(Urls).filter_by(short_url=short_url).first()
        if entry:
            return redirect(entry.original_url)
        else:
            flash("Short URL not found.")
            return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
