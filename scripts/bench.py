#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SYNOPSIS

    bench [-b,--base] [-h,--help] [-k,--rank] [-r,--ratio] [-s,--size]
          [-t,--threshold]

DESCRIPTION

    Benchmark the RecommendationBolt class from ../storm/src/py/resources.

    -b int, --base int
        Configure the size of the user base to influence the underlying SVD.
        Defaults to 2500.

    -p float, --proximity float
        Configure the minimum proximity of the neighbors to consider.
        Defaults to 1.0.

    -h, --help
        Show this message.

    -k int, --rank int
        Configure the rank of the matrix approximation. Defaults to 100.

    -r float, --ratio float
        Configure the how many percent of the testing data to use for
        verification. Defaults to 0.5.

    -s int, --size int
        Configure how many users to generate recommendations for. The actual
        size may vary depending on threshold setting. Defaults to 5000.

    -t float, --threshold float
        Set the minimum ammount of observations must be on record for a user
        to be considered for testing. Defaults to 0.0.

AUTHOR

    Nicolas Drebenstedt <nicolas.drebenstedt@zeit.de>

LICENSE

    This script is BSD licenced, see LICENSE file for more info.

VERSION

    0.1
"""

import datetime
import numpy as np
import optparse
import os
import sys
import time
import traceback


def header(caption):
    return ' %s '.ljust(20, '-').rjust(30, '-') % caption


def report(description, verbose):
    if verbose:
        print '[%s] %s' % (datetime.datetime.now().ctime(), description)


def main(base, proximity, rank, ratio, size, threshold, verbose):
    if verbose:
        print header('Report')
    else:
        np.seterr(all='ignore')

    report('Configure mock recommendation bolt.', verbose)
    script_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(script_path + '/../storm/src/py/resources')
    from recommendation import RecommendationBolt

    t0 = time.time()
    rb = RecommendationBolt()
    conf = {
        'zeit.recommend.svd.base': base,
        'zeit.recommend.svd.rank': rank,
        'zeit.recommend.elasticsearch.host': '217.13.68.236'
        }
    rb.initialize(conf, None)
    initializing = (time.time() - t0) / base

    report('Generate test users with a minimum observation count.', verbose)
    goal = dict(
        rb.generate_seed(from_=base, size=size, threshold=threshold)
        ).items()

    report('Expand goal and prediction dicts to matrices.', verbose)
    goal_matrix = np.array(list(rb.expand(g[1]) for g in goal))

    report('Omit observations from user base according to ratio.', verbose)
    test = goal[:]
    for i in range(len(test)):
        test[i] = test[i][0], list(test[i][1])[:-int(len(test[i][1]) * ratio)]

    report('Generate numerical predictions for each item-user pair.', verbose)
    prediction_matrix = np.zeros_like(goal_matrix)
    t0 = time.time()
    for i in range(len(test)):
        vector = rb.expand(test[i][1])
        prediction_matrix[i, :] = rb.predict(vector, neighbors=10)
    predicting = (time.time() - t0) / len(test)

    report('Calculate mean absolute error.', verbose)
    error_aggregate = 0.0
    for i in range(goal_matrix.shape[0]):
        for j in range(goal_matrix.shape[1]):
            error_aggregate += abs(prediction_matrix[i, j] - goal_matrix[i, j])
    mae = error_aggregate / np.multiply(*goal_matrix.shape)

    report('Generate recommendations for incomplete test dict.', verbose)
    prediction = dict()
    t0 = time.time()
    for user, paths in test:
        vector = rb.expand(paths)
        prediction[user] = rb.recommend(vector)
    recommending = (time.time() - t0) / len(test)

    report('Calculate average recall, precisions and f1 metrics.', verbose)
    precision_aggregate = 0.0
    recall_aggregate = 0.0
    f1_aggregate = 0.0
    top_n_aggregate = 0.0
    len_goal = len(goal)

    for user, paths in goal:
        hits = set(paths).intersection(set(prediction[user]))

        recall = float(len(hits)) / len_goal
        recall_aggregate += recall

        if len(prediction[user]):
            precision = float(len(hits)) / len(prediction[user])
        else:
            precision = 0.0
        precision_aggregate += precision

        if (recall + precision):
            f1 = float(2 * recall * precision) / (recall + precision)
        else:
            f1 = 0.0
        f1_aggregate += f1

        top_n_aggregate += len(prediction[user])

    recall = recall_aggregate / len_goal
    precision = precision_aggregate / len_goal
    f1 = f1_aggregate / len_goal
    top_n = top_n_aggregate / len_goal

    print header('Options')
    print 'Base:\t\t', base
    print 'Proximity:\t', proximity
    print 'Rank:\t\t', rank
    print 'Ratio:\t\t', ratio
    print 'Size:\t\t', len_goal
    print 'Threshold:\t', threshold
    print header('Averages')
    print 'Recommending:\t%.8fs' % recommending
    print 'Predicting:\t%.8fs' % predicting
    print 'Initializing:\t%.8fs' % initializing
    print 'MAE:\t\t%.16f' % mae
    print 'Recall:\t\t%.16f' % recall
    print 'Precision:\t%.16f' % precision
    print 'F1 Score:\t%.16f' % f1
    print 'Top N:\t\t%.16f' % top_n

if __name__ == '__main__':
    try:
        parser = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version='0.1'
            )
        parser.add_option(
            '-b',
            '--base',
            default=2500,
            help='size of original user base',
            type='int'
            )
        parser.add_option(
            '-p',
            '--proximity',
            default=1.0,
            help='proximity of neighborhood',
            type='float'
            )
        parser.add_option(
            '-k',
            '--rank',
            default=100,
            help='rank of matrix approximation',
            type='int'
            )
        parser.add_option(
            '-r',
            '--ratio',
            default=0.5,
            help='ratio of testing to verification data',
            type='float'
            )
        parser.add_option(
            '-s',
            '--size',
            default=5000,
            help='size of test user base',
            type='int'
            )
        parser.add_option(
            '-t',
            '--threshold',
            default=0.0,
            help='minimum test user ranking',
            type='float'
            )
        parser.add_option(
            '-v',
            '--verbose',
            action='store_true',
            help='turn on verbose output'
            )
        (options, args) = parser.parse_args()
        main(
            options.base,
            options.proximity,
            options.rank,
            options.ratio,
            options.size,
            options.threshold,
            options.verbose
            )
    except SystemExit, e:
        raise e
    except UserWarning, e:
        print str(e)
        os._exit(1)
    except Exception, e:
        print str(e)
        traceback.print_exc()
        os._exit(1)
