from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Charger les projets depuis un fichier JSON
def load_projects():
    with open('data/projects.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    projects = load_projects()
    return render_template('projects.html', projects=projects)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Ici tu peux traiter le formulaire (ex: envoyer un email)
        # Pour l’instant, juste rediriger vers la page d’accueil
        return redirect(url_for('index'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
