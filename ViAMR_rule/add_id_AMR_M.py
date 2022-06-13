import penman

def get_snt_amr(path):
    amrs = []
    with open(path, 'r', encoding='utf-8') as f:
        amr = dict()
        graph = []
        for line in f:
            line = line.strip()
            if line != '':
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


if __name__ == '__main__':

    gold_path = '/home/dao/PycharmProjects/ViAMR/ViAMR_rule/data/500M.txt'
    test_path = '/home/dao/PycharmProjects/ViAMR/ViAMR_rule/data/result_AMR_format.txt'
    gold_amrs = get_snt_amr(gold_path)
    test_amrs = load_amr(test_path)

    for amr in gold_amrs:
        # print(amr)
        snt_gold = amr['snt']
        for a in test_amrs:
            id_test = a['id']
            snt_test = a['snt']

            if snt_gold == snt_test:
                amr['id'] = id_test

    gold_500_amrs = "/home/dao/PycharmProjects/ViAMR/ViAMR_rule/gold_500.amr"
    with open(gold_500_amrs, 'w', encoding='utf-8') as file:
        for amr in gold_amrs:
            print(amr)
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
