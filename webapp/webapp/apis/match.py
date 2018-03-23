from flask import render_template, request, jsonify, Blueprint, url_for, send_file, make_response

from flask_security import login_required

from webapp import app

from redis import Redis
from rq import Queue, get_current_job
from rq.job import Job
from rq.registry import StartedJobRegistry

from datetime import datetime

match_api = Blueprint('match_api', __name__, url_prefix='/api/match')


redis_connection = Redis(host='redis', port=6379)
q = Queue('matching', connection=redis_connection)
registry = StartedJobRegistry('matching', connection=redis_connection)

@match_api.route('/job_in_q', methods=['GET'])
@login_required
def get_jobs_in_q():
    queued_job_ids = q.job_ids
    queued_jobs = q.jobs
    q_time = [job.enqueued_at for job in queued_jobs]

    try:
        current_job_id = registry.get_job_ids()
        current_job_created_at = [Job.fetch(job_id, connection=redis_connection).created_at for job_id in current_job_id]
        current_job = [{'job_id': job_id, 'created_time': time.strftime('%Y-%m-%d %I:%M %p')} for (job_id, time) in zip(current_job_id, current_job_created_at)]
    except:
        current_job = []
    jobs_in_q = [{'job_id': job_id, 'created_time': time.strftime('%Y-%m-%d %I:%M %p')} for (job_id, time) in zip(q.job_ids, q_time)]
    app.logger.info(f"current_job: {current_job}")
    return jsonify(current=current_job, q=jobs_in_q)
