import os, base64
from model import db, ConvertedStrings
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", 'jkljlkkj4l32j4k2lj432lj4')

@app.route('/')
def main_page():
    return render_template('main_page.jinja2') 

@app.route('/piglatinize/', methods=['POST'])
def pig_latinizer():
    original_text = request.form['input_text']
    original_text = original_text.split(' ')
    new_text = []
    for word in original_text:
        word = word[1:] + word[0] + 'ay'
        new_text.append(word)
    new_text = ' '.join(new_text)

    # Create the database (Heroku will automatically delete it later, which is convenient)
    db.connect()
    db.create_tables([ConvertedStrings])
    # Create a unique code for this conversion
    code = base64.b32encode(os.urandom(8)).decode().strip("=").lower()
    new_record = ConvertedStrings(value=new_text, code=code)
    new_record.save()
    db.close()
    return redirect(url_for('retrieve_conversion', code=code))

@app.route('/esultray/<code>/')
def retrieve_conversion(code):
    try:
        new_text = ConvertedStrings.get(ConvertedStrings.code == code).value
    except ConvertedStrings.DoesNotExist:
        new_text = "Invalid code"
    return render_template('piglatinize.jinja2', latinized_phrase=new_text)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)