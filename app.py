from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
import json
import os
from datetime import datetime

app = Flask(__name__,template_folder='templates')
app.secret_key = '5f8d7a4b3c6e90a12b45d78e1f2a3b4c7d9e0f1a2b3c4d5'

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visitors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Modèle de données
class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100))
    date = db.Column(db.String(20), nullable=False)
    number_visitors = db.Column(db.Integer, nullable=False)

# Initialisation de la base de données
with app.app_context():
    db.create_all()

# Fonctions JSON
def load_visitors():
    try:
        with open('visitors.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_to_json(data):
    visitors = load_visitors()
    visitors.append({
        'id': len(visitors) + 1,
        'name': data['name'],
        'surname': data['surname'],
        'email':data['email'],
        'date': data['date'],
        'number_visitors': data['number_visitors'],
        'timestamp': datetime.now().isoformat()
    })
    with open('visitors.json', 'w') as f:
        json.dump(visitors, f, indent=4)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record', methods=['GET', 'POST'])
def record():
    if request.method == 'POST':
        try:
            # Récupération des données
            visitor_data = {
                'name': request.form['name'],
                'surname': request.form['surname'],
                'email':request.form['email'],
                'date': request.form['date'],
                'number_visitors': int(request.form['number_visitors'])
            }

            # Enregistrement DB
            new_visitor = Visitor(**visitor_data)
            db.session.add(new_visitor)
            db.session.commit()

            # Sauvegarde JSON
            save_to_json(visitor_data)

            flash(' Enregistrement réussi !', 'success')
            return redirect(url_for('record'))

        except Exception as e:
            db.session.rollback()
            flash(f' Erreur : {str(e)}', 'error')
    
    return render_template('record.html')


# Gestion d'erreurs
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('record.html'), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
    app.run(debug=True)