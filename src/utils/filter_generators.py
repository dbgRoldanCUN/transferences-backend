# -*-coding: utf-8 -*-

def generateSQLFilter(filt, prefix, params):
    filter = ''
    for param in params:
        set_filter = filt.get(param)
        for f in set_filter:
            filter += ' and {}{}{}{}'.format(prefix,
             f.get('variable'),
             f.get('comparisson'),
             f.get('value'))
    return filter[len(params[0])+1:]
