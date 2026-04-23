from flask import Flask, render_template, request, redirect, url_for, flash
from database import db, Patient
import uuid
import statistics
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'santetech2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///santetech.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/formulaire', methods=['GET', 'POST'])
def formulaire():
    if request.method == 'POST':
        poids = float(request.form['poids'])
        taille = float(request.form['taille']) / 100
        imc = round(poids / (taille ** 2), 2)
        antecedents = request.form.getlist('antecedents_medicaux')
        antecedents_str = ', '.join(antecedents)
        if request.form.get('antecedents_autre'):
            antecedents_str += ', ' + request.form.get('antecedents_autre')
        patient = Patient(
            code_patient=str(uuid.uuid4())[:8].upper(),
            nom=request.form['nom'],
            prenom=request.form['prenom'],
            age=request.form['age'],
            date_naissance=request.form['date_naissance'],
            sexe=request.form['sexe'],
            telephone=request.form['telephone'],
            poids=poids,
            taille=float(request.form['taille']),
            imc=imc,
            tension=request.form['tension'],
            frequence_cardiaque=request.form['frequence_cardiaque'],
            antecedents_medicaux=antecedents_str,
            antecedents_chirurgicaux=request.form['antecedents_chirurgicaux'],
            allergies=request.form['allergies'],
            tabagisme=request.form['tabagisme'],
            alcool=request.form['alcool'],
            motif_consultation=request.form['motif_consultation'],
            date_symptomes=request.form['date_symptomes'],
            douleur=request.form['douleur'],
            traitements_cours=request.form['traitements_cours'],
            examen_clinique=request.form['examen_clinique'],
            resultats_biologiques=request.form['resultats_biologiques']
        )
        db.session.add(patient)
        db.session.commit()
        flash('Données enregistrées avec succès !', 'success')
        return redirect(url_for('dashboard'))
    return render_template('formulaire.html')
@app.route('/dashboard')
def dashboard():
    patients = Patient.query.all()
    total = Patient.query.count()
    search = request.args.get('search', '')
    if search:
        patients = Patient.query.filter(
            Patient.nom.contains(search) |
            Patient.prenom.contains(search)
        ).all()
    # Calculs statistiques
    stats = {}
    if total > 0:
        ages = [p.age for p in Patient.query.all()]
        imcs = [p.imc for p in Patient.query.all() if p.imc]
        douleurs = [p.douleur for p in Patient.query.all() if p.douleur]
        poids = [p.poids for p in Patient.query.all() if p.poids]
        # Moyennes
        stats['age_moyen'] = round(statistics.mean(ages), 1)
        stats['imc_moyen'] = round(statistics.mean(imcs), 2) if imcs else 0
        stats['douleur_moyenne'] = round(statistics.mean(douleurs), 1) if douleurs else 0
        stats['poids_moyen'] = round(statistics.mean(poids), 1) if poids else 0
        # Quartiles ages
        ages_sorted = sorted(ages)
        n = len(ages_sorted)
        stats['q1_age'] = round(ages_sorted[n//4], 1)
        stats['q2_age'] = round(statistics.median(ages_sorted), 1)
        stats['q3_age'] = round(ages_sorted[(3*n)//4], 1)
        # Quartiles IMC
        if imcs:
            imcs_sorted = sorted(imcs)
            n2 = len(imcs_sorted)
            stats['q1_imc'] = round(imcs_sorted[n2//4], 2)
            stats['q2_imc'] = round(statistics.median(imcs_sorted), 2)
            stats['q3_imc'] = round(imcs_sorted[(3*n2)//4], 2)
        # Répartition sexe
        hommes = Patient.query.filter_by(sexe='Homme').count()
        femmes = Patient.query.filter_by(sexe='Femme').count()
        stats['hommes'] = hommes
        stats['femmes'] = femmes
        # Motifs
        motifs = {}
        for p in Patient.query.all():
            if p.motif_consultation:
                motifs[p.motif_consultation] = motifs.get(p.motif_consultation, 0) + 1
        stats['motifs'] = motifs
        # Tabagisme
        stats['fumeurs'] = Patient.query.filter_by(tabagisme='Fumeur').count()
        stats['non_fumeurs'] = Patient.query.filter_by(tabagisme='Non-fumeur').count()
        stats['ex_fumeurs'] = Patient.query.filter_by(tabagisme='Ancien fumeur').count()
    return render_template('dashboard.html',
                         patients=patients,
                         total=total,
                         stats=stats,
                         search=search)
@app.route('/recherche')
def recherche():
    return redirect(url_for('dashboard'))
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0', port=port)