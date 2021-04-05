import flask
from . import create_session
from .models.jobs import Job

jobs_blueprint = flask.Blueprint('jobs_api', __name__)


@jobs_blueprint.route('/api/jobs')
def jobs():
    session = create_session()
    jobs = session.query(Job).all()
    return flask.jsonify({
        'jobs': [
            item.to_dict(only=('id', 'job', 'work_size',
                'collaborators', 'start_date', 'end_date',
                'is_finished', 'category', 'team_leader')) 
            for item in jobs
        ]
    })



@jobs_blueprint.route('/api/jobs/<int:job_id>')
def get_one_job(job_id):
    session = create_session()
    job = session.query(Job).get(job_id)
    if not job:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify({
        'jobs': \
            job.to_dict(only=('id', 'job', 'work_size',
                'collaborators', 'start_date', 'end_date',
                'is_finished', 'category', 'team_leader')) 
    })
