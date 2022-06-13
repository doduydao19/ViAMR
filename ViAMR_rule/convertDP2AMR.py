import csv

def readData(dataPath):
    data = open(dataPath, "r", encoding="utf-8")
    data_csv = csv.reader(data, delimiter='\t')

    sentences = []
    sentence = []
    for row in data_csv:
        if (len(row) != 0):
            if row[1] == "\t":
                row[1] = "\""
                row.insert(2, "\"")
            sentence.append(row)
        else:
            sentences.append(sentence)
            sentence = []
    if len(sentence) > 0:
        sentences.append(sentence)
    return sentences
    pass
    # print (len(sentences))


def convert(sentences):
    sentences_converted = []

    for sentence in sentences:
        sentence_converted = []
        for row in sentence:
            order_number = int(row[0])
            word = row[1]
            word_NF = row[2]
            role = row[3]
            word_DP = int(row[6])
            label = row[7]

            if label != 'punct':

                if word_DP == 0:
                    word_DP_convert = [word_NF, "ROOT"]
                else:
                    word_DP_convert = [word_NF, sentence[word_DP - 1][2]]
                head_order_number = [order_number, word_DP]

                sentence_converted.append(['?', word, word_NF, role ,label, word_DP_convert, head_order_number])

        s = sort_rows_in_sentence(sentence_converted)
        # s = sentence_converted
        sentences_converted.append(s)

    return sentences_converted
    pass


def sort_rows_in_sentence(sentence):
    # for r in sentence:
    #     print(r)
    # print (len(sentence))
    sentence_sorted = []
    for row in sentence:
        if row[4] == "root":
            sentence_sorted.append(row)

    root = sentence_sorted[0]

    index_sentence_sorted = 0
    step = 1
    while (len(sentence_sorted) != len(sentence)):
        bootID = 1
        for row in sentence:
            if root != row:
                if row[6][1] == root[6][0]:
                    print(step)
                    next_index = index_sentence_sorted + bootID
                    sentence_sorted.insert(next_index, row)
                    bootID += 1

                    step += 1
                    # for r in sentence_sorted:
                    #     print(r)
        index_sentence_sorted += 1
        # print ("ID = ",index_sentence_sorted)
        root = sentence_sorted[index_sentence_sorted]

        # print("root = ")
        # print (root)
        # print()

    # for r in sentence_sorted:
    #     print(r)

    return sentence_sorted
    pass


def writeData(sentences_converted, outputPath):
    with open(outputPath, "w", encoding="utf-8", newline='') as data_converted:
        data_writer = csv.writer(data_converted, delimiter="\t")

        idSentence = 1
        for sentence in sentences_converted:
            print("câu:\n", idSentence)
            for row in sentence:
                if row[1] == '\"':
                    row[1] = '"'
                    row[2] = '"'

                print(row)

                data_writer.writerow(row)
            data_writer.writerow("")
            idSentence += 1

    pass

def main():
    dataPath = "data/LP-DPN.txt"
    outputPath = "data/DP_reformat.txt"
    data = readData(dataPath)
    sentences_converted = convert(data)
    writeData(sentences_converted, outputPath)

if __name__ == '__main__':
    main()
