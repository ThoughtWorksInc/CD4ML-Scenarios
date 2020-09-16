import os
import uuid
import json
from hashlib import sha256
from struct import unpack
from itertools import takewhile, islice, count
from collections import defaultdict
from time import time
import urllib
from random import Random
import urllib.request
import logging
logger = logging.getLogger(__name__)


def ensure_dir_exists(directory):
    """
    If a directory doesn't exists, create it
    :param directory:
    :return:
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def hash_string_obj(string):
    """
    Hash a string using sha256. Return a hash object
    To get an actual value, call .digest()
    or .hexdigest() on it.
    :param string: any string
    :return: sha256 hash object
    """
    x_bytes = string.encode()
    return sha256(x_bytes)


def hash_string(string, n_chars=16):
    """
    Hash a string using sha256. Return a hash object
    To get an actual value, call .digest()
    or .hexdigest() on it.
    :param string: any string
    :param n_chars: number of characters of hash
            to keep. From 0 to 64
    :return: sha256 hash object
    """
    hash_object = hash_string_obj(string)
    hash_val = hash_object.hexdigest()
    return hash_val[0:n_chars]


def hash_to_uniform_random(val, seed):
    """
    Hash any object to a uniform random number in [0,1]
    Objects will have the same hash if they have the same
    str(x) result and same class.
    :param val: any value that can be converted to string
    :param seed: any seed value that can be converted to string
    :return: psuedo-random number between 0 and 1
    """
    val_string = str(val) + str(val.__class__)
    seed_string = str(seed) + str(seed.__class__)
    string = val_string + seed_string
    return float(unpack('<Q', hash_string_obj(string).digest()[:8])[0]) / 2 ** 64


def flatten_dict(pyobj, keystring=''):
    if type(pyobj) is dict:
        if type(pyobj) is dict:
            keystring = keystring + "_" if keystring else keystring
            for k in pyobj:
                yield from flatten_dict(pyobj[k], keystring + k)

        elif type(pyobj) is list:
            for elem in pyobj:
                yield from flatten_dict(elem, keystring)
    else:
        yield keystring, pyobj


def mini_batch(stream, batch_size):
    return takewhile(bool, (list(islice(stream, batch_size)) for _ in count()))


def mini_batch_eval(stream, batch_size, multi_function):
    # for functions which are more efficient when running on
    # batches of data, e.g. large calling overhead
    mini_batch_stream = mini_batch(stream, batch_size)
    for batch in mini_batch_stream:
        evaluated_batch = multi_function(batch)
        for evaluated in evaluated_batch:
            yield evaluated


def float_or_zero(x):
    """
    :param x: any value
    :return: converted to float if possible, otherwise 0.0
    """
    if x is None:
        return 0

    try:
        return float(x)

    except ValueError:
        return 0.0


def average_by(stream, averaged_field, by_field, prior_num=0, prior_value=0.0, transform=None):
    """
    Average a value by some other field and return a dict of the averages
    Uses Laplace smoothing to deal with the noise from low numbers
    per group to reduce over-fitting
    :param stream: stream of data
    :param averaged_field: field to be averaged
    :param by_field: fields to be grouped by
    :param prior_num: Laplace smoothing, number of synthetic samples
    :param prior_value: Laplace smoothing, prior estimate of average
    :param transform: function or lambda to apply to by_field
        before aggregation
    :return: dict of (average, count) pairs
    """
    summation = defaultdict(float)
    number = defaultdict(int)

    for row in stream:
        by = row[by_field]

        if transform is not None:
            aggregate_key = transform(by)
        else:
            aggregate_key = by

        value = row[averaged_field]
        summation[aggregate_key] += value
        number[aggregate_key] += 1

    keys = summation.keys()
    prior_summation = prior_num * prior_value
    averages = {k: ((summation[k] + prior_summation)/(number[k] + prior_num), number[k]) for k in keys}

    return averages


def download_to_file_from_url(url, filename, use_cache=True):
    if not os.path.exists(filename) or not use_cache:
        logger.info('Data file download from url: %s' % url)
        start = time()
        urllib.request.urlretrieve(url, filename)
        runtime = time()-start
        logger.info('Download took %0.2f seconds' % runtime)
        return 1
    else:
        logger.info("Found a cached training file '{}'. Will use this for training.".format(filename))
        return 0


def create_lookup(stream, derived_fields, index_field):
    """
    Build a lookup table from an indexed field to a set of derived fields.
    Ensures that there is a unique relation, raises assertion if violated
    :param stream: stream of records
    :param derived_fields: list of derived fields assumed to be a function of the
        indexed field only
    :param index_field: the index field which determined the others
    :return: lookup table from index to dict of derived fields
    """
    lookup = {}
    for row in stream:
        index = row[index_field]
        if index not in lookup:
            # put info in lookup
            lookup[index] = {}
            for derived_field in derived_fields:
                value = row[derived_field]
                lookup[index][derived_field] = value
        else:
            # ensure there is a single unique derived field
            for derived_field in derived_fields:
                value = row[derived_field]
                assert lookup[index][derived_field] == value

    return lookup


def shuffle_csv_file(filename, filename_shuffled, seed=3623365):
    """
    Shuffle the rows of a csv file while keeping the header
    at the top. Deterministic unless you provide it with seed=None
    :param filename: a csv file
    :param filename_shuffled: a shuffled csv file to write to
    :param seed: a random seed, defaults to a particular one
    :return: None
    """
    rand = Random()
    rand.seed(seed)
    fp = open(filename, 'r')
    lines = fp.readlines()
    fp.close()

    fp = open(filename_shuffled, 'w')
    header = lines[0]
    fp.writelines([header])
    lines = lines[1:]
    rand.shuffle(lines)
    fp.writelines(lines)
    fp.close()


def get_uuid():
    return str(uuid.uuid1())


def get_json(filename):
    with open(filename, 'r') as fp:
        return json.load(fp)
