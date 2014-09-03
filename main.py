#!/usr/bin/env python

import csv
import datetime
import codecs
import sys

from twitter_follow_bot import auto_follow


def job_valid_now(job):
    start = parse_date(job['start_date'])
    end = parse_date(job['end_date'])
    return start <= datetime.date.today() <= end


def parse_date(date_string):
    return datetime.datetime.strptime(
        date_string, '%Y-%m-%d').date()


def run_job(job):
    print("Running {}".format(job))

    auto_follow_query = job.get('auto_follow')
    if auto_follow_query is not None:
        auto_follow(auto_follow_query)


def main():
    with open('schedule.csv', 'r') as f:
        for row in csv.DictReader(f):
            if job_valid_now(row):
                run_job(row)

if __name__ == '__main__':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    main()
