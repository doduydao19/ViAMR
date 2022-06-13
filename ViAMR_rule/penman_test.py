import penman
from penman.graph import Graph
# g = penman.decode('(b / bark-01 :ARG0 (d / dog) :quant 3)')
# print(penman.encode(g))
#
# graph = Graph([('x1', ':instance', 'bark-01'), ('x2', ':instance', 'dog'),('x1', ':ARG0', 'x2')])
# amr = penman.encode(graph)
# print(amr)
#




# concepts = [('x1',':instance', 'bản_sao'), \
#            ('x2',':instance', 'đây'), \
#            ('x3',':instance', 'tranh'), \
#            ('x4',':instance', 'bức'), \
#            ('x5',':instance', 'đó')]
#
# variables = {3: 'x1', 1:'x2', 6:'x3', 5:'x4', 7:'x5'}
#
# relations = [(0,'root', 3), \
#             (3,':domain', 1), \
#            (3,':poss', 6), \
#            (6,':classifier', 5), \
#            (6,':domain', 7)]
# for rel in relations[1:]:
#     head = rel[0]
#     val_head = variables[head]
#     index = rel[2]
#     val_index = variables[index]
#
#     rel_type = rel[1]
#     concepts.append((val_head, rel_type, val_index))
#
# graph = Graph(concepts)
# amr = penman.encode(graph)
# print(amr)
#
#
#

a = [('x1', ':instance', 'đi'),
   ('x2', ':instance', 'em'),
   ('x3', ':instance', 'cậu'),
   ('x4', ':instance', 'đã'),
   ('x5', ':instance', 'qua'),
   ('x6', ':instance', 'vùng'),
   ('x7', ':instance', 'có'),
   ('x8', ':instance', 'tiểu tinh cầu'),
   ('x16', ':instance', 'và'),
   ('x1', ':ARG0', 'x2'),
   ('x2', ':classifier', 'x3'),
   ('x1', ':tense', 'x4'),
   ('x1', ':ARG1', 'x5'),
   ('x1', ':ARG1', 'x6'),
   ('x6', ':ARG0-of', 'x7'),
   ('x7', ':ARG1', 'x8'),
   ('x8', ':quant', '325'),
   ('325', ':?', '326'),
   ('325', ':?', '327'),
   ('325', ':?', '328'),
   ('325', ':?', '329'),
   ('325', ':mod', '330')]

graph = Graph(a)
print(graph)
amr = penman.encode(graph)
print(amr)
