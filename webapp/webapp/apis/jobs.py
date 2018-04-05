from flask import render_template, request, jsonify, Blueprint, url_for, send_file, make_response

from flask_security import login_required

from webapp import app

from redis import Redis
from rq import Queue, get_current_job
from rq.job import Job
from rq.registry import StartedJobRegistry

from webapp.apis import query

from datetime import datetime

jobs_api = Blueprint('jobs_api', __name__, url_prefix='/api/jobs')


redis_connection = Redis(host='redis', port=6379)
q = Queue('matching', connection=redis_connection)
registry = StartedJobRegistry('matching', connection=redis_connection)

@jobs_api.route('/get_jobs', methods=['GET'])
@login_required
def get_jobs():
    queued_job_ids = q.job_ids
    queued_jobs = q.jobs
    q_time = [job.enqueued_at for job in queued_jobs]
    q_event_type = [job.meta['event_type'] for job in queued_jobs]
    try:
        current_job_id = registry.get_job_ids()
        current_job_created_at = [Job.fetch(job_id, connection=redis_connection).created_at for job_id in current_job_id]
        current_job_event_type = [Job.fetch(job_id, connection=redis_connection).meta['event_type'] for job_id in current_job_id]
        current_job_file_name = [Job.fetch(job_id, connection=redis_connection).meta['filename'] for job_id in current_job_id]
        current_job = [
            {
                'job_id': job_id,
                'created_time': time.strftime('%Y-%m-%d %I:%M:%S %p'),
                'event_type': event,
                'runtime': str(datetime.now() - time).split('.', 2)[0],
                'filename': filename
            } for (job_id, time, event, filename) in zip(current_job_id, current_job_created_at, current_job_event_type, current_job_file_name)]
    except:
        current_job = []
    jobs_in_q = [{'job_id': job_id, 'created_time': time.strftime('%Y-%m-%d %I:%M:%S %p'), 'event_type': event} for (job_id, time, event) in zip(q.job_ids, q_time, q_event_type)]
    app.logger.info(f"current_job: {current_job}")
    return jsonify(current=current_job, q=jobs_in_q)


@jobs_api.route('/history', methods=['GET'])
@login_required
def get_match_hitory():
    df = query.get_history()
    df['upload_timestamp'] = df['upload_timestamp'].dt.strftime('%Y-%m-%d %I:%M:%S %p')
    df['match_start_timestamp'] = df['match_start_timestamp'].dt.strftime('%Y-%m-%d %I:%M:%S %p')
    df['match_complete_timestamp'] = df['match_complete_timestamp'].dt.strftime('%Y-%m-%d %I:%M:%S %p')
    try:
        output = df.to_dict('records')
        return jsonify(output)
    except:
        return "something is wrong", 500


@jobs_api.route('/upload_log/<upload_id>', methods=['GET'])
def get_upload_log(upload_id):
    df = query.get_upload_log(upload_id)
    try:
        output = df.to_dict('records')
        return jsonify(output)
    except:
        return "something is wrong", 500


@jobs_api.route('/merge_log/<upload_id>', methods=['GET'])
def get_merge_log(upload_id):
    df = query.get_merge_log(upload_id)
    print(df)
    try:
        output = df.to_dict('records')
        return jsonify(output)
    except:
        return "something is wrong", 500
