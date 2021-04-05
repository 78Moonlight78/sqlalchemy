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



@jobs_blueprint.route('/api/jobs', methods=['POST'])
def jobs_add():
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['job', 'work_size',
                  'collaborators', 'start_date', 'end_date',
                  'is_finished', 'category', 'team_leader']):
        return jsonify({'error': 'Bad request'})
    session = create_session()
    job = Job(
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        start_date=request.json['start_date'],
        end_date=request.json['end_date'],
        is_finished=request.json['is_finished'],
        category=request.json['category'],
        team_leader=request.json['team_leader']
    )
    session.add(job)
    session.commit()
    return flask.jsonify({'success': 'OK'})


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


