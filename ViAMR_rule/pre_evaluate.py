import penman

def load_amr(path):
    amrs = []
    with open(path, 'r', encoding='utf-8') as f:
        amr = dict()
        graph = []
        for line in f:
            line = line.strip()
            if line != '':
                if "# ::id" in line:
                    amr['id'] = line[7:].strip()
                    continue
                if "# ::snt" in line:
                    amr['snt'] = line[8:].strip()
                    continue
                graph.append(line)
            if line == '':
                amr['graph'] = graph
                amrs.append(amr)
                amr = dict()
                graph = []
        if len(graph) > 0:
            amr['graph'] = graph
            amrs.append(amr)
    return amrs

gold_path = 'gold_500.amr'
test_path_fit_gold = "test_500.amr"
test_path = '/home/dao/PycharmProjects/ViAMR/ViAMR_rule/data/result_AMR_format.txt'
gold_amrs = load_amr(gold_path)

test_amrs = load_amr(test_path)

pair_amrs = []
for amr in gold_amrs:
    id_gold = amr['id']
    snt_gold = amr['snt']
    for a in test_amrs:
        id_test = a['id']
        snt_test = a['snt']

        if id_gold == id_test:
            if snt_gold != snt_test:
                print(amr)
                print(a)
                break
            else:
                pair_amrs.append(a)



with open(test_path_fit_gold,'w', encoding='utf-8') as file:
    for amr in pair_amrs:
        graph = amr['graph']
        for i in range(len(graph)):
            if '/' in graph[i]:
                graph[i] = graph[i].replace(' (', '__(')
                graph[i] = graph[i].replace(' / ', '_/_')
                graph[i] = graph[i].replace(' ', '_')
                graph[i] = graph[i].replace('_/_', ' / ')
                graph[i] = graph[i].replace('__(', ' (')
        graph = ' '.join(graph)
        amr_graph = penman.encode(penman.decode(graph))
        amr_graph = amr_graph.replace('_', ' ')

        file.write("# ::id " + str(amr['id']) + "\n")
        file.write("# ::snt " + amr['snt'] + "\n")
        file.write(amr_graph+'\n')
        file.write("\n")

# print(len(amrs))
# id = 1
# for amr in amrs:
#     # print(amr)
#     if id != int(amr['id']):
#         print(amr)
#         break
#     id += 1
