from flask import render_template, request, jsonify, Blueprint, url_for, send_file, make_response

from flask_security import login_required


from redis import Redis
from rq import Queue
from rq.job import Job
from rq.registry import StartedJobRegistry

from webapp.apis import query

from datetime import datetime
from functools import partial
import pandas as pd


jobs_api = Blueprint('jobs_api', __name__, url_prefix='/api/jobs')


redis_connection = Redis(host='redis', port=6379)
q = Queue('matching', connection=redis_connection)
registry = StartedJobRegistry('matching', connection=redis_connection)

@jobs_api.route('/get_current_jobs', methods=['GET'])
@login_required
def get_current_jobs():
    queued_job_ids = q.job_ids
    queued_jobs = q.jobs
    q_time = [job.enqueued_at for job in queued_jobs]
    q_ids = [job.meta['upload_id'] for job in queued_jobs]
    try:
        current_job_id = registry.get_job_ids()
        current_job_created_at = [Job.fetch(job_id, connection=redis_connection).created_at for job_id in current_job_id]
        current_job_upload_id = [Job.fetch(job_id, connection=redis_connection).meta['upload_id'] for job_id in current_job_id]
        current_job = [
            {
                'job_id': job_id,
                'created_time': time.strftime('%Y-%m-%d %I:%M:%S %p'),
                'runtime': str(datetime.now() - time).split('.', 2)[0],
                'meta': query.get_metadata(upload_id).to_dict('records')[0]
            } for (job_id, time, upload_id) in zip(current_job_id, current_job_created_at, current_job_upload_id)]
    except:
        current_job = []

    jobs_in_q = [
        {
            'job_id': job_id,
            'created_time': time.strftime('%Y-%m-%d %I:%M:%S %p'),
            'meta': query.get_metadata(q_upload_id).to_dict('records')[0]
        } for (job_id, time, q_upload_id) in zip(q.job_ids, q_time, q_ids)]
    return jsonify(current=current_job, q=jobs_in_q)


@jobs_api.route('/history', methods=['GET'])
@login_required
def get_match_hitory():
    df = query.get_history()
    if df.empty:
        return jsonify([])

    df.index = df.index + 1
    df.sort_index(inplace=True, ascending=False)
    df.reset_index(level=0, inplace=True)
    try:
        output = df.to_dict('records')
        return jsonify(output)
    except:
        return "something is wrong", 500
