import os
from hashlib import sha256
from struct import unpack


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
            for lelm in pyobj:
                yield from flatten_dict(lelm, keystring)
    else:
        yield keystring, pyobj
