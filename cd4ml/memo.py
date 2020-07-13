def memo(f):
    """ Memoization decorator for a function taking a single argument """
    class MemoDict(dict):
        def __missing__(self, key):
            ret = self[key] = f(key)
            return ret
    return MemoDict().__getitem__
