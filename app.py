from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email
import json
import requests
import smtplib
from email.mime.text import MIMEText
from functools import lru_cache

app = Flask(__name__)
app.config['SECRET_KEY'] = 'une_clé_secrète_forte_ici'  # Change ceci par une valeur sécurisée !

class ContactForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])

@lru_cache(maxsize=1)
def load_projects():
    with open('data/projects.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Charger les projets
    projects = load_projects()

    # Charger les stats GitHub
    lang_stats = {}
    try:
        response = requests.get('https://api.github.com/users/ton-compte/repos')  # Remplace 'ton-compte' par ton username GitHub
        repos = response.json()
        for repo in repos:
            langs = requests.get(repo['languages_url']).json()
            for lang, bytes in langs.items():
                lang_stats[lang] = lang_stats.get(lang, 0) + bytes
        total = sum(lang_stats.values())
        if total > 0:
            lang_stats = {lang: round((bytes / total) * 100, 2) for lang, bytes in lang_stats.items()}
        else:
            lang_stats = None
    except:
        lang_stats = None

    # Gérer le formulaire de contact
    form = ContactForm()
    if form.validate_on_submit():
        msg = MIMEText(form.message.data)
        msg['Subject'] = 'Nouveau message de portfolio'
        msg['From'] = form.email.data
        msg['To'] = 'ton_email@example.com'  # Ton email de réception
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('ton_email@example.com', 'ton_mot_de_passe')  # Remplace par tes infos
                server.send_message(msg)
            flash('Message envoyé avec succès !', 'success')
        except Exception as e:
            flash(f'Erreur lors de l’envoi du message : {str(e)}', 'danger')
        return redirect(url_for('index') + '#contact')

    return render_template('index.html', projects=projects, lang_stats=lang_stats, form=form)

if __name__ == '__main__':
    app.run(debug=True)