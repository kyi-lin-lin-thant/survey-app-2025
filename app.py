from flask import Flask, render_template, request, redirect, Response as FlaskResponse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv
from io import StringIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # change in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///responses.db'

db = SQLAlchemy(app)

# Define response model
class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Demographics & Background
    status = db.Column(db.String(50))
    status_other = db.Column(db.String(100))
    experience = db.Column(db.String(50))
    region = db.Column(db.String(50))
    region_other = db.Column(db.String(100))
    # Cloud Skills & Usage
    cloud_platforms = db.Column(db.String(200))
    cloud_skills = db.Column(db.String(200))
    cloud_learning = db.Column(db.String(200))
    # Industry Trends & Impact
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
    # Skill Gaps & Education
    edu_adequacy = db.Column(db.String(20))
    edu_adequacy_reason = db.Column(db.Text)
    edu_improvements = db.Column(db.String(500))
    edu_improvements_reason = db.Column(db.Text)
    # Open Feedback
    valuable_cloud_skills = db.Column(db.Text)
    university_suggestions = db.Column(db.Text)
    
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize database (run once)
with app.app_context():
    db.create_all()

# Home page
@app.route('/')
def index():
    return render_template('survey.html')

# Survey form submission
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = request.form
    
    # Helper to get list from checkboxes
    def get_list(name):
        return request.form.getlist(name)
    
    # Gather open-text answers into a dictionary for storage
    open_responses = {
        'importance_reason': form.get('importance_reason', ''),
        'agreement_reason': form.get('job_prospect_reason', ''),
        'impact_reason': form.get('cloud_career_reason', ''),
        'usage_reason': form.get('cloud_usage_reason', ''),
        'mandatory_reason': form.get('cloud_mandatory_reason', ''),
        'edu_adequacy_reason': form.get('edu_adequacy_reason', ''),
        'edu_improvements_reason': form.get('edu_improvements_reason', ''),
        'valuable_cloud_skills': form.get('valuable_cloud_skills', ''),
        'university_suggestions': form.get('university_suggestions', ''),
    }
    
    # Create Response object with all data
    response = Response(
        # Demographics & Background
        status=form.get('status'),
        status_other=form.get('status_other'),
        experience=form.get('experience'),
        region=form.get('country'),
        region_other=form.get('country_other'),
        # Cloud Skills & Usage
        cloud_platforms=','.join(get_list('cloud_platforms[]')),
        cloud_skills=','.join(get_list('cloud_skills[]')),
        cloud_learning=','.join(get_list('cloud_learning[]')),
        importance=form.get('cloud_importance'),
        importance_reason=open_responses['importance_reason'],
        agreement=form.get('job_prospect_agreement'),
        agreement_reason=open_responses['agreement_reason'],
        impact=form.get('cloud_career_impact'),
        impact_reason=open_responses['impact_reason'],
        usage_frequency=form.get('cloud_usage_frequency'),
        usage_reason=open_responses['usage_reason'],
        mandatory=form.get('cloud_mandatory'),
        mandatory_reason=open_responses['mandatory_reason'],
        edu_adequacy=form.get('edu_adequacy'),
        edu_adequacy_reason=open_responses['edu_adequacy_reason'],
        edu_improvements=','.join(get_list('edu_improvements[]')),
        edu_improvements_reason=open_responses['edu_improvements_reason'],
        valuable_cloud_skills=open_responses['valuable_cloud_skills'],
        university_suggestions=open_responses['university_suggestions']
    )
    
    # Save to database
    db.session.add(response)
    db.session.commit()
    
    return redirect('/thankyou')

@app.route('/thankyou')
def thankyou():
    return "Thank you for your participation!"

# Download and review data
@app.route('/download')
def download():
    responses = Response.query.all()

    # Create a CSV in memory
    output = StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow([column.name for column in Response.__table__.columns])

    # Write data rows
    for r in responses:
        writer.writerow([getattr(r, column.name) for column in Response.__table__.columns])

    output.seek(0)

    return FlaskResponse(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=responses.csv"}
    )

# Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

