import boto3
import multiprocessing as mp

import datetime
from datetime import timezone

# kwargs = dict(jobQueue='arn:aws:batch:{region}{account_id}:job-queue/batch-training-job')

num_workers = mp.cpu_count()  
print(num_workers)

def get_sm_session(execution_role):
    session = boto3.Session()
    sts = session.client("sts")
    response = sts.assume_role(
        RoleArn=execution_role,
        RoleSessionName="preprocess-execution-session",
    )
    sm_session = boto3.Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
                                aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                                aws_session_token=response['Credentials']['SessionToken'])
    return sm_session


def cancel_jobs_on_batch(job_id):#, failed_job_id_list):
    response = batch_client.cancel_job(
            jobId=job_id,
            reason='Cancelling job.',
        )


time_filter = str(int(datetime.datetime(2023,8,22,0,0,0, tzinfo=timezone.utc).timestamp()*1000))
print(time_filter)

EXECUTION_ROLE = 'arn:aws:iam::811120793315:role/ai-ml-qa4-fm-batch-service'
JOB_QUEUE = 'ai-ml-qa4-lad'
NUM_OF_JOBS = 20000


for new_idx in range(NUM_OF_JOBS):
    print(f"Iteration {new_idx}")
    execution_role = EXECUTION_ROLE
    sm_session = get_sm_session(execution_role)
    batch_client = sm_session.client('batch')

    kwargs = dict(jobQueue=JOB_QUEUE, 
              # jobStatus='FAILED',
                 filters=[
                     {'name':'AFTER_CREATED_AT',
                      'values':[time_filter]
                     },
                       ]
                 )

    job_list = batch_client.list_jobs(**kwargs)

    job_id_list = [job_meta['jobId'] for job_meta in job_list['jobSummaryList'] if job_meta['status'] in ['SUBMITTED','PENDING','RUNNABLE']]

    # pool = mp.Pool(num_workers)
    with mp.Pool(num_workers) as pool:
        pool.map(cancel_jobs_on_batch,job_id_list)

    # pool.close()
    # pool.join()

    idx = 0
    print('Cancelled jobs in iteration', idx)

    while 'nextToken' in job_list:
        kwargs = dict(jobQueue=JOB_QUEUE,
                        filters=[
                 {'name':'AFTER_CREATED_AT',
                  'values':[time_filter]
                 },
                   ],
                       nextToken=job_list['nextToken']
                     )
        job_list = batch_client.list_jobs(**kwargs)

    
        job_id_list = [job_meta['jobId'] for job_meta in job_list['jobSummaryList'] if job_meta['status'] in ['SUBMITTED','PENDING','RUNNABLE']]
        
        # pool = mp.Pool(num_workers)
        with mp.Pool(num_workers) as pool:
            pool.map(cancel_jobs_on_batch,job_id_list)

        # pool.map(cancel_jobs_on_batch,job_id_list)

    #     for job_meta in job_list['jobSummaryList']:
    #         if job_meta['status'] in ['SUBMITTED','PENDING','RUNNABLE']:
    #             pool.apply_async(cancel_jobs_on_batch, args = (batch_client, job_meta['jobId']))

        # pool.close()
        # pool.join()

        idx = idx + 1
        print('Cancelled jobs in iteration', idx)
