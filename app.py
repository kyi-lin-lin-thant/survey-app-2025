import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, redirect, Response as FlaskResponse, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import csv
from io import StringIO

app = Flask(__name__)

# Secrets
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Database config
DATABASE_URL = os.environ.get("DATABASE_URL") or os.environ.get("EXTERNAL_DATABASE_URL") or "sqlite:///responses.db"

# Heroku can provide postgres:// — SQLAlchemy expects postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# If we're on a network Postgres, require SSL
if DATABASE_URL.startswith("postgresql://") and "localhost" not in DATABASE_URL:
    app.config.setdefault('SQLALCHEMY_ENGINE_OPTIONS', {})
    app.config['SQLALCHEMY_ENGINE_OPTIONS'].setdefault("connect_args", {})
    app.config['SQLALCHEMY_ENGINE_OPTIONS']["connect_args"].setdefault("sslmode", "require")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50))
    status_other = db.Column(db.String(100))
    experience = db.Column(db.String(50))
    region = db.Column(db.String(50))
    region_other = db.Column(db.String(100))
    cloud_platforms = db.Column(db.String(200))
    cloud_skills = db.Column(db.String(200))
    cloud_learning = db.Column(db.String(200))
    importance = db.Column(db.String(20))
    importance_reason = db.Column(db.Text)
    agreement = db.Column(db.String(20))
    agreement_reason = db.Column(db.Text)
    impact = db.Column(db.String(50))
    impact_reason = db.Column(db.Text)
    usage_frequency = db.Column(db.String(20))
    usage_reason = db.Column(db.Text)
    mandatory = db.Column(db.String(20))
    mandatory_reason = db.Column(db.Text)
    edu_adequacy = db.Column(db.String(20))
    edu_adequacy_reason = db.Column(db.Text)
    edu_improvements = db.Column(db.String(500))
    edu_improvements_reason = db.Column(db.Text)
    valuable_cloud_skills = db.Column(db.Text)
    university_suggestions = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def consent():
    return render_template('consent.html')

@app.route('/survey')
def index():
    return render_template('survey.html')

@app.route('/submit', methods=['POST'])
def submit():
    form = request.form

    def get_list(name):
        return request.form.getlist(name)

    response = Response(
        status=form.get('status'),
        status_other=form.get('status_other'),
        experience=form.get('experience'),
        region=form.get('country'),
        region_other=form.get('country_other'),

        cloud_platforms=','.join(get_list('cloud_platforms[]')),
        cloud_skills=','.join(get_list('cloud_skills[]')),
        cloud_learning=','.join(get_list('cloud_learning[]')),

        importance=form.get('cloud_importance'),
        importance_reason=form.get('importance_reason', ''),

        agreement=form.get('job_prospect_agreement'),
        agreement_reason=form.get('job_prospect_reason', ''),

        impact=form.get('cloud_career_impact'),
        impact_reason=form.get('cloud_career_reason', ''),

        usage_frequency=form.get('cloud_usage_frequency'),
        usage_reason=form.get('cloud_usage_reason', ''),

        mandatory=form.get('cloud_mandatory'),
        mandatory_reason=form.get('cloud_mandatory_reason', ''),

        edu_adequacy=form.get('edu_adequacy'),
        edu_adequacy_reason=form.get('edu_adequacy_reason', ''),
        edu_improvements=','.join(get_list('edu_improvements[]')),
        edu_improvements_reason=form.get('edu_improvements_reason', ''),

        valuable_cloud_skills=form.get('valuable_cloud_skills', ''),
        university_suggestions=form.get('university_suggestions', ''),
    )

    db.session.add(response)
    db.session.commit()
    return redirect('/thanks')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/download')
def download():
    responses = Response.query.order_by(Response.submitted_at.desc()).all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([c.name for c in Response.__table__.columns])
    for r in responses:
        writer.writerow([getattr(r, c.name) for c in Response.__table__.columns])
    output.seek(0)
    return FlaskResponse(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=responses.csv"}
    )

if __name__ == '__main__':
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=debug)
