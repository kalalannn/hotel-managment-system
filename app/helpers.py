class Helper(object):
    # [] -> [ ( id_0, '{} {} ... {}'.format(_obj.arg1, _obj.arg2 ..., ] ), (id_1, '...'), ... ]
    # _list -> list of objects _obj
    # *args     -> ['first_name', 'second_name', ... ]
    @staticmethod
    def toArrayOfTuples(_list, delimiter, *args):
        return [tuple for tuple in                                 \
            map(lambda _obj:                                       \
                ( getattr(_obj, "id"),                             \
                '{}'.format(delimiter)                             \
                    .join(['{}' for k in range(0, len(args))])     \
                    .format(*[getattr(_obj, arg) for arg in args]) \
                )
            , _list) ]
    
    @staticmethod
    def dictToArrayOfTuples(_dict):
        # print(_dict, _dict.keys())
        return [(key, _dict[key]) for key in _dict.keys()]


