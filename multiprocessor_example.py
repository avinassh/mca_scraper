import time
import multiprocessing
import random


def job(job_id):
    print('Starting job: {}'.format(job_id))
    # do job here
    sleep_time = random.uniform(5, 25)
    print('Sleeping job: {}, for {}'.format(job_id, sleep_time))
    time.sleep(sleep_time)
    print('Ending job: {}'.format(job_id))


if __name__ == '__main__':
    for i in range(10):
        p = multiprocessing.Process(target=job, args=(i, ))
        p.start()
