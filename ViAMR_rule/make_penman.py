import csv

import penman
from penman.graph import Graph


def readData(path):
    with open(path, "r", encoding="utf-8") as file:
        data_csv = csv.reader(file, delimiter='\t')
        amrs = []
        amr = dict()
        concepts = []
        relations = []
        variables = dict()
        count = 1

        for row in data_csv:
            if len(row) != 0:
                if "# ::id" in row[0]:
                    id = row[0][7:]
                    amr['id'] = int(id)
                    continue

                if "# ::snt" in row[0]:
                    snt = row[0][8:]
                    amr['snt'] = snt
                    continue

                if "#" not in row[0]:
                    rel_type = row[0]
                    concept_val = row[1]
                    dep = row[6][2:-2].split("', '")
                    head = int(dep[1])
                    index = int(dep[0])

                    variable = 'x' + str(count)
                    count += 1
                    if concept_val.isdigit():
                        variables[index] = concept_val
                    else:
                        concept = (variable, ':instance', concept_val)
                        variables[index] = variable
                        concepts.append(concept)

                    if index != 0 and head != 0:
                        relation = (head, rel_type, index)
                        relations.append(relation)
            else:
                nodes_and_edges = reduce_node_amr(concepts, relations, variables)
                graph = Graph(nodes_and_edges)
                print(amr['id'])
                print(amr['snt'])
                print(graph)
                amr['graph'] = penman.encode(graph).replace(':polarity (- ', ':polarity -\n')
                amrs.append(amr)

                amr = dict()
                concepts = []
                relations = []
                count = 1

        if len(concepts) > 0:
            nodes_and_edges = reduce_node_amr(concepts, relations, variables)
            graph = Graph(nodes_and_edges)
            amr['graph'] = penman.encode(graph)
            amrs.append(amr)

        return amrs


def reduce_node_amr(concepts, relations, variables):
    # print('concepts = ', concepts)
    # print('relations = ', relations)
    # print('variables = ', variables)
    # print()
    while True:
        index_removed = []
        for rel in relations:
            # print(rel)
            if rel[1] == '*':
                for i in range(len(relations)):
                    # print(relations[i],  rel[2])
                    if relations[i][0] == rel[2]:
                        relations[i] = list(relations[i])
                        relations[i][0] = rel[0]
                        relations[i] = tuple(relations[i])
                index_removed.append(rel[2])
                relations.remove(rel)
        if len(index_removed) > 0:
            variables_removed = []
            for index in index_removed:
                variables_removed.append(variables[index])
            # print(variables_removed)

            concept_removed = []
            for concept in concepts:
                for variable in variables_removed:
                    if concept[0] == variable:
                        print(concept)
                        concept_removed.append(concept)
            for c in concept_removed:
                concepts.remove(c)
        else:
            break

    concepts, relations, variables = logical_node_amr(concepts, relations, variables)

    for i in range(len(relations)):
        head = relations[i][0]
        rel_type = relations[i][1]
        index = relations[i][2]
        relations[i] = (variables[head], rel_type, variables[index])
    # print('concepts = ', concepts)
    # print('relations = ', relations)
    # print('variables = ', variables)
    # print()

    return concepts + relations


def logical_node_amr(concepts, relations, variables):
    variable_logical = []
    for rel in relations:
        if rel[1] == ':polarity':
            variable_logical.append(variables[rel[2]])
            variables[rel[2]] = '-'
    for concept in concepts:
        for variable in variable_logical:
            if concept[0] == variable:
                concepts.remove(concept)

    return concepts, relations, variables


def write_out(pathOut, amrs):
    with open(pathOut, "w", encoding="utf-8", newline='') as file:
        for amr in amrs:
            file.write("# ::id " + str(amr['id']) + "\n")
            file.write("# ::snt " + amr['snt'] + "\n")
            file.write(amr['graph']+'\n')
            file.write("\n")

    print("write done")


def main():
    path_in = "data/results_LP-DPN.txt"
    pathOut = "data/result_AMR_format.txt"

    amrs = readData(path_in)
    # for amr in amrs:
    #     graph = amr['graph']
    #     print('# ::snt', amr['snt'])
    #     print(graph)
    #     print()

    write_out(pathOut, amrs)


if __name__ == '__main__':
    main()
