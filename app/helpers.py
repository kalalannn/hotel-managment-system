class Helper(object):
    # [] -> [ ( id_0, '{} {} ... {}'.format(_obj.arg1, _obj.arg2 ..., ] ), (id_1, '...'), ... ]
    # _list -> list of objects _obj
    # *args     -> ['first_name', 'second_name', ... ]
    @staticmethod
    # VASIA EBAT UDALI ETI METODY!
    # каждый раз ебать открываю ее и удивляюсь. зачем? Карл, зачем вообще такое писать?))
    # невозможно же понять, что она делает. только выписав принтом могу догадаться
    def listObjToListOfTuples(_list, delimiter, *args):
        return [tuple for tuple in                                 \
            map(lambda _obj:                                       \
                ( getattr(_obj, "id"),                             \
                '{}'.format(delimiter)                             \
                    .join(['{}' for k in range(0, len(args))])     \
                    .format(*[getattr(_obj, arg) for arg in args]) \
                )
            , _list) ]
    
    # VASIA EBAT UDALI ETI METODY!
    @staticmethod
    def dictToListOfTuples(_dict, only_keys=False, only_values=False):
        # print(_dict, _dict.keys(), _dict.values())
        if only_keys:
            return [(key, key) for key in _dict.keys()]
        elif only_values:
            return [(val, val) for val in _dict.values()]
        else:
            return [(key, _dict[key]) for key in _dict.keys()]
    
    # VASIA EBAT UDALI ETI METODY!
    @staticmethod
    def sqlIN(field_name, _list):
        return '{} IN ('.format(field_name)+ \
            ','.join(map(lambda x: '\'{}\''.format(x), _list)) \
        +')'
