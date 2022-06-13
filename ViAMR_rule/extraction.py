dataPath = "data/LP-DPN.txt"
outputPath = "data/sentences_LP-DPN.txt"

def readData(path):
    data = open(path, "r", encoding="utf-8")
    sentences = []
    sentence = ""
    for row in data:
        row = row.strip()

        if row != '':
            row = row.split('\t')
            sentence += row[1]+" "
        else:
            sentence = sentence.strip()
            sentences.append(sentence)
            sentence = ""

    if sentence != '':
        sentence = sentence.strip()
        sentences.append(sentence)
    return sentences
    pass

def writeOut(outputPath, sentences):
    with open(outputPath, "w", encoding="utf-8", newline='') as file:
        for sentence in sentences:
            # print(sentence[:-1])
            file.write(sentence)
            file.write("\n")

if __name__ == '__main__':
    sentences = readData(dataPath)
    print(len(sentences))
    writeOut(outputPath, sentences)
