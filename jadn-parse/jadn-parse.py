from lark import Lark, Transformer
import json
import logging
import os
logging.basicConfig(level=logging.DEBUG)


class JADN(Transformer):
    def start(self, tree):
        return tree

    def typedef(self, tree):
        #desc = tree[2]['desc'] if len(tree) > 2 else ''
        #v = [str(tree[0])] + tree[1] + [desc]
        #return v
        return tree

    def items(self, tree):
        return tree

    def fields(self, tree):
        flist = []
        while tree:         # TODO: clean up this mess
            d = ''
            v = tree.pop()
            if isinstance(v, dict):
                d = v['desc']
                if not tree:
                    break
                v = tree.pop()
            assert isinstance(v, list)
            v.append(d)
            flist.append(v)
        flist.reverse()
        f = [d, flist]
        return f

    def item(self, tree):
        assert len(tree) == 2
        return [int(tree[0]), str(tree[1])]

    def field(self, tree):
        #assert len(tree) in (3, 4)
        #opts = [opt for opt in tree[3]] if len(tree) > 3 else []
        #return [int(tree[0]), str(tree[1]), tree[2], opts]
        return tree

    def desc(self, tree):
        return {'desc': str(tree[0]) if len(tree) > 0 else '.'}

    def typestring(self, tree):
        return tree

    def sub(self, tree):
        return tree

    def kvtype(self, tree):
        assert len(tree) == 2
        return ['+' + str(tree[0]), '*' + str(tree[1])]

    def vtype(self, tree):
        assert len(tree) == 1
        return ['*' + str(tree[0])]

    def efunc(self, tree):
        assert len(tree) == 1
        return ['$' + str(tree[0])]

    def pattern(self, tree):
        return tree

    def vrange(self, tree):
        return tree

    def format(self, tree):
        assert len(tree) == 1
        return ['/' + tree[0]]

    def fieldstr(self, tree):
        return tree

    def multi(self, tree, default=(0,0)):
        minc, maxc = (0, 1) if tree[0] == 'optional' else tree
        maxc = 0 if maxc == '*' else maxc
        d = [minc, maxc]
        return ['[]'[k] + str(d[k]) for k in [0,1] if d[k] != 1]

    def mrange(self, tree):
        return tree

    def tfield(self, tree):
        assert len(tree) == 1
        return ['&' + str(tree[0])]

if __name__ == '__main__':
    with open('jadn-idl.lark') as grammar:
        #p = Lark(grammar, parser='lalr', debug=True)       # may not work without %ignore WS
        p = Lark(grammar, debug=True)

    cdir = os.path.dirname(os.path.realpath('__file__'))    # Current directory
    idir = 'schema'
    odir = os.path.normpath(os.path.join(cdir, 'schema_gen'))
    print('Translating schemas from', os.path.realpath(idir), 'to', odir)
    for fn in (f[0] for f in (os.path.splitext(i) for i in os.listdir(idir)) if f[1] == '.jidl'):
        print('**', fn)
        with open(os.path.join(idir, fn) + '.jidl') as f:
            ptree = p.parse(f.read())
            print(ptree)
            print(ptree.pretty())
            JADN().transform(ptree)
