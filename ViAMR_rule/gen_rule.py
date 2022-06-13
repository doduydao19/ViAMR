import csv


def read_sentences_origin(file_sentences_origin_path):
    with open(file_sentences_origin_path, "r", encoding="utf-8", newline='') as file:
        sentences = []
        for sentence in file:
            sentences.append(sentence)
    return sentences


def read_rule_file(file_rule_path):
    filename = open(file_rule_path, "r", encoding="utf-8")
    rule_labels = csv.reader(filename, delimiter='\t')
    rules = []
    for i in rule_labels:

        if len(i) > 0:
            rule = []
            # print(i)
            for j in i:
                if j != "|":
                    if j == "":
                        j = []
                    else:
                        j = j.split(", ")
                    rule.append(j)
            # print(rule)
            rules.append(rule)
    return rules


def read_data_file(file_data_path):
    data_file = open(file_data_path, "r", encoding="utf-8")
    data = csv.reader(data_file, delimiter='\t')

    sentences = []
    sentence = []
    for d in data:
        row = []
        for w in d:
            if "]" in w:
                w = w.strip('][').replace("'", "").split(', ')
            row.append(w)
        # print(row)
        if len(d) != 0:
            sentence.append(row)
        else:
            sentences.append(sentence)

            sentence = []

    return sentences


def find_index_word_head(sentence, index_current):
    for word_current in sentence:
        if word_current[6][0] == index_current:
            index_word_head = word_current[6][1]
            return index_word_head


def find_properties_head(sentence, index_word_head):
    for word_current in sentence:
        if index_word_head == word_current[6][0]:
            return word_current[1], word_current[3], word_current[4]
    return None, None, None


def find_word_behind_true_label(sentence, index_word_current, label_true):
    for word_current in sentence:
        if index_word_current == word_current[6][1]:
            word, label_POS, label_DP = word_current[1], word_current[3], word_current[4]
            if label_DP in label_true:
                return word, label_POS, label_DP
    return None, None, None


# trường hơp 1 chỉ có 1 nhãn DP trong luật thì không cần xét head:
def check_rule_label_case_1(label_DP_word_current, label_DP_rule, label_POS_word_current, label_POS_rule, word,
                            words_rule):
    weight_case_1 = 0

    # 3 trọng số cho trường hợp 1:
    # bằng 1 là đúng nhãn DP
    # bằng 2 là đúng nhãn DP và đúng nhãn POS OR đúng nhãn DP và đúng từ
    # băng 3 là đúng nhãn DP và đúng nhãn POS và đúng từ

    if (label_DP_word_current in label_DP_rule) and (label_POS_word_current in label_POS_rule):
        weight_case_1 += 1

    if weight_case_1 == 1:
        if label_POS_word_current in label_POS_rule:
            weight_case_1 += 1

        if word in words_rule:
            weight_case_1 += 1

    return weight_case_1


def check_rule_label_case_2_1(sentence, index_word_head, label_DP_word_current, labels_DP_rule, label_POS_word_current,
                              labels_POS_rule, word, words_rule):
    weight_case_2 = 0
    # 5 trọng số cho trường hợp 2:
    # bằng 2 là đúng nhãn DP và Head
    # bằng 3 là đđúng nhãn DP và Head và 1 nhãn POS đúng OR 1 từ đúng từ
    # bằng 4 là đúng nhãn DP và Head và đúng nhãn 2 POS OR 2 từ đúng từ
    # bằng 5 là đúng nhãn DP và Head và (đúng nhãn 2 POS và 1 từ đúng từ) OR (đúng nhãn 1 POS và 2 từ đúng từ)
    # băng 6 là đúng tất cả

    # tìm từ, nhãn POS, nhãn DP của từ head của từ đang xét:
    word_head, label_POS_head, label_DP_head = find_properties_head(sentence, index_word_head)

    if (label_DP_word_current in labels_DP_rule[0]) and (label_DP_head in labels_DP_rule[1]) and (
            label_POS_word_current in labels_POS_rule[0]):
        weight_case_2 += 2

    if weight_case_2 == 2:
        if label_POS_word_current in labels_POS_rule[0]:
            weight_case_2 += 1

        if label_POS_head in labels_POS_rule[1]:
            weight_case_2 += 1

        if word in words_rule[0]:
            weight_case_2 += 1

        if word_head in words_rule[1]:
            weight_case_2 += 1

    return weight_case_2


def check_rule_label_case_2_2(sentence, index_word_current, label_DP_word_current, labels_DP_rule,
                              label_POS_word_current, labels_POS_rule, word,
                              words_rule):
    weight_case_2 = 0
    # từ bị phụ thuộc == Behind

    # tìm từ, nhãn POS, nhãn DP của từ Behind đúng nhãn của từ đang xét:
    label_true = labels_DP_rule[0]
    word_behind, label_POS_behind, label_DP_behind = find_word_behind_true_label(sentence, index_word_current,
                                                                                 label_true)

    if (label_DP_behind in labels_DP_rule[0]) and (label_DP_word_current in labels_DP_rule[1]) and (
            label_POS_word_current in labels_POS_rule[1]):
        weight_case_2 += 2

    if weight_case_2 == 2:
        if label_POS_word_current in labels_POS_rule[1]:
            weight_case_2 += 1

        if label_POS_behind in labels_POS_rule[0]:
            weight_case_2 += 1

        if word in words_rule[1]:
            weight_case_2 += 1

        if word_behind in words_rule[0]:
            weight_case_2 += 1

    return weight_case_2


def check_rule_label_case_3_1(sentence, index_word_head, label_DP_word_current, labels_DP_rule,
                              label_POS_word_current, labels_POS_rule, word,
                              words_rule):
    weight_case_3 = 0
    # từ bị phụ thuộc == Behind
    # 7 trọng số cho trường hợp 3: (3,4,5,6,7,8,9)

    # tìm từ, nhãn POS, nhãn DP của từ Head_1 (cột 2) đúng nhãn của từ đang xét:
    word_head_1, label_POS_head_1, label_DP_head_1 = find_properties_head(sentence, index_word_head)

    # tìm từ, nhãn POS, nhãn DP của từ Head_2 (cột 3) đúng nhãn của từ đang xét:
    index_word_head = find_index_word_head(sentence, index_word_head)
    word_head_2, label_POS_head_2, label_DP_head_2 = find_properties_head(sentence, index_word_head)

    if (label_DP_word_current in labels_DP_rule[0]) and (label_DP_head_1 in labels_DP_rule[1]) and (
            label_DP_head_2 in labels_DP_rule[2]) and (label_POS_word_current in labels_POS_rule[0]):
        weight_case_3 += 3

    if weight_case_3 == 3:
        if label_POS_word_current in labels_POS_rule[0]:
            weight_case_3 += 1

        if label_POS_head_1 in labels_POS_rule[1]:
            weight_case_3 += 1

        if label_POS_head_2 in labels_POS_rule[2]:
            weight_case_3 += 1

        if word in words_rule[0]:
            weight_case_3 += 1

        if word_head_1 in words_rule[1]:
            weight_case_3 += 1

        if word_head_2 in words_rule[1]:
            weight_case_3 += 1

    return weight_case_3


def check_rule_label_case_3_2(sentence, index_word_current, index_word_head, label_DP_word_current, labels_DP_rule,
                              label_POS_word_current, labels_POS_rule, word,
                              words_rule):
    weight_case_3 = 0
    # từ bị phụ thuộc == Behind
    # 7 trọng số cho trường hợp 3: (3,4,5,6,7,8,9)

    # tìm từ, nhãn POS, nhãn DP của từ behind (cột 1) đúng nhãn của từ đang xét:
    label_true = labels_DP_rule[0]
    word_behind, label_POS_behind, label_DP_behind = find_word_behind_true_label(sentence, index_word_current,
                                                                                 label_true)

    # tìm từ, nhãn POS, nhãn DP của từ Head (cột 3) đúng nhãn của từ đang xét:

    word_head, label_POS_head, label_DP_head = find_properties_head(sentence, index_word_current)

    if (label_DP_behind in labels_DP_rule[2]) and (label_DP_word_current in labels_DP_rule[1]) and (
            label_DP_head in labels_DP_rule[2]) and (label_POS_word_current in labels_POS_rule[1]):
        weight_case_3 += 3

    if weight_case_3 == 3:
        if label_POS_behind in labels_POS_rule[0]:
            weight_case_3 += 1

        if label_POS_word_current in labels_POS_rule[1]:
            weight_case_3 += 1

        if label_POS_head in labels_POS_rule[2]:
            weight_case_3 += 1

        if word_behind in words_rule[0]:
            weight_case_3 += 1

        if word in words_rule[1]:
            weight_case_3 += 1

        if word_head in words_rule[2]:
            weight_case_3 += 1

    return weight_case_3


def check_rule_label_case_3_3(sentence, index_word_current, label_DP_word_current, labels_DP_rule,
                              label_POS_word_current, labels_POS_rule, word,
                              words_rule):
    weight_case_3 = 0
    # từ bị phụ thuộc == Behind
    # 7 trọng số cho trường hợp 3: (3,4,5,6,7,8,9)
    # tìm từ, nhãn POS, nhãn DP của từ behind (cột 2) đúng nhãn của từ đang xét:
    label_true = labels_DP_rule[1]
    word_behind_2, label_POS_behind_2, label_DP_behind_2 = find_word_behind_true_label(sentence, index_word_current,
                                                                                       label_true)

    # tìm từ, nhãn POS, nhãn DP của từ behind (cột 1) đúng nhãn của từ đang xét:
    label_true = labels_DP_rule[0]
    index_behind_2 = 0
    for row in sentence:
        if word_behind_2 in row:
            if label_POS_behind_2 in row:
                if label_DP_behind_2 in row:
                    index_behind_2 = row[6][0]
    word_behind_1, label_POS_behind_1, label_DP_behind_1 = find_word_behind_true_label(sentence, index_behind_2,
                                                                                       label_true)

    if (label_DP_behind_1 in labels_DP_rule[0]) and (label_DP_behind_2 in labels_DP_rule[1]) and (
            label_DP_word_current in labels_DP_rule[2]) and (label_POS_word_current in labels_POS_rule[2]):
        weight_case_3 += 3

    if weight_case_3 == 3:
        if word_behind_1 in labels_POS_rule[0]:
            weight_case_3 += 1

        if word_behind_2 in labels_POS_rule[1]:
            weight_case_3 += 1

        if label_POS_word_current in labels_POS_rule[2]:
            weight_case_3 += 1

        if word_behind_1 in words_rule[0]:
            weight_case_3 += 1

        if word_behind_2 in words_rule[1]:
            weight_case_3 += 1

        if word in words_rule[2]:
            weight_case_3 += 1

    return weight_case_3


# trường hợp đặc biệt có nhãn DP trong luật và là từ đúng từ sẽ được chấp nhận
def check_rule_label_case_4(label_DP_word_current, labels_DP_rule, label_POS_word_current, label_POS_rule, word,
                            words_rule):
    weight_case_4 = 0

    if word in words_rule:
        weight_case_4 += 7
    if weight_case_4 == 7:
        if label_DP_word_current in labels_DP_rule:
            weight_case_4 += 1
        if label_POS_word_current in label_POS_rule:
            weight_case_4 += 1

    return weight_case_4


def select_label_AMR_to_word_current(label_AMR_with_weight):
    w_max = 0
    label_max = ""
    for s in label_AMR_with_weight:
        # print(s)
        if s[2] > w_max:
            w_max = s[2]
            label_max = s[1][0]
    return label_max


def count_label_DP_in_rule(rule):
    count_lDP_in_rule = 0
    for j in range(1, 4):
        if len(rule[j]) != 0:
            count_lDP_in_rule += 1
    return count_lDP_in_rule


def matching_label(sentence, rule_labels):
    for word_current in sentence:

        word = word_current[1]
        # print("***: ", word)
        index_word_current = word_current[6][0]
        label_DP_word_current = word_current[4]
        index_word_head = word_current[6][1]
        label_POS_word_current = word_current[3]
        # label_AMR_word_current = word_current[0][0]

        # if nhãn phụ thuộc là root thì là gốc
        if label_DP_word_current == "root":
            word_current[0] = "root"
        else:
            # tìm các vị trí các từ phụ thuộc của từ đang xét:

            # case:
            # 1 nhãn: c1
            # 2 nhãn: (c1,c2)
            # 3 nhãn: (c1,c2,c3)
            label_AMR_with_weight = []
            for rule in rule_labels:

                # tìm tổng số nhãn có trong 1 luật:
                c_LDP = count_label_DP_in_rule(rule)

                # Case1: chỉ có 1 nhãn DP ở cột 1:
                # kết quả là 1 tập hợp gồm (nhãn, trọng số)

                if (c_LDP == 1):

                    label_DP_rule = rule[1]

                    # tìm nhãn POS của từ ở cột 4 tương ứng với nhãn ở cột 2
                    label_POS_rule = rule[4]

                    # tìm các từ có thể có của từ ở cột 7 tương ứng với nhãn ở cột 2
                    words_rule = rule[7]
                    weight_case_1 = check_rule_label_case_1(label_DP_word_current, label_DP_rule,
                                                            label_POS_word_current, label_POS_rule, word, words_rule)
                    # lấy trọng số
                    if weight_case_1 >= 1:
                        label_AMR_with_weight.append(("case_1", rule[0], weight_case_1))

                # Case2: chỉ có 2 nhãn DP ở cột 1 và 2:
                # kết quả là 1 tập hợp gồm (nhãn, trọng số)

                if (c_LDP == 2):
                    # có 2 nhãn, nhãn ở cột 1, cột 2
                    labels_DP_rule = [rule[1], rule[2]]

                    # tìm nhãn POS của từ ở cột 4, 5 tương ứng với nhãn ở cột 1, 2
                    labels_POS_rule = [rule[4], rule[5]]

                    # tìm các từ có thể có của từ ở cột 7, 8 tương ứng với nhãn ở cột 1, 2
                    words_rule = [rule[7], rule[8]]

                    # trong trường hợp 2 thì có thể xét thành 2 trường hợp:
                    # case2.1: từ đang xét (thuộc cột 1) phụ thuộc và từ cột 2
                    # case2.2: từ cột 1 phụ thuộc vào đang xét (thuộc cột 2)
                    # vì thế cần truyền vào cả câu và vị trí của từ đang xét hiện tại để tìm từ phụ thuộc hoặc bị phụ thuộc cho từ hiện tại
                    # 3 trọng số cho trường hợp 2:
                    # bằng 2 là đúng 2 nhãn DP
                    # bằng 3 là đúng 2 nhãn DP và (1 nhãn POS đúng OR 1 từ đúng từ)
                    # bằng 4 là đúng 2 nhãn DP và (đúng nhãn 2 POS OR 2 từ đúng từ)
                    # bằng 5 là đúng 2 nhãn DP và (đúng nhãn 2 POS và 1 từ đúng từ) OR (đúng nhãn 1 POS và 2 từ đúng từ)
                    # băng 6 là đúng tất cả
                    # case2.1:
                    weight_case_2_1 = check_rule_label_case_2_1(sentence,
                                                                index_word_head,
                                                                label_DP_word_current,
                                                                labels_DP_rule,
                                                                label_POS_word_current,
                                                                labels_POS_rule,
                                                                word,
                                                                words_rule)

                    # lấy trọng số
                    if weight_case_2_1 >= 2:
                        label_AMR_with_weight.append(("case_2.1", rule[0], weight_case_2_1))

                    # case2.2:
                    weight_case_2_2 = check_rule_label_case_2_2(sentence,
                                                                index_word_current,
                                                                label_DP_word_current,
                                                                labels_DP_rule,
                                                                label_POS_word_current,
                                                                labels_POS_rule,
                                                                word,
                                                                words_rule)
                    # lấy trọng số
                    if weight_case_2_2 >= 2:
                        label_AMR_with_weight.append(("case_2.2", rule[0], weight_case_2_2))

                # Case3: chỉ có 3 nhãn DP ở cột 1 ,2 và 3:
                # kết quả là 1 tập hợp gồm (nhãn, trọng số)
                if (c_LDP == 3):
                    # có 3 nhãn, nhãn ở cột 1, cột 2, cột3
                    labels_DP_rule = [rule[1], rule[2], rule[3]]

                    # tìm nhãn POS của từ ở cột 4, 5, 6 tương ứng với nhãn ở cột 1, 2, 3
                    labels_POS_rule = [rule[4], rule[5], rule[6]]

                    # tìm các từ có thể có của từ ở cột 7, 8, 9 tương ứng với nhãn ở cột 1, 2, 3
                    words_rule = [rule[7], rule[8], rule[9]]

                    # trong trường hợp 3 thì có thể xét thành 3 trường hợp:
                    # case3.1: từ đang xét (thuộc cột 1) phụ thuộc vào từ cột 2 và từ cột 2 phụ thuộc vào từ cột 3
                    # case3.2: từ cột 1 phụ thuộc vào từ đang xét (thuộc cột 2) và từ cột 2 phụ thuộc vào từ cột 3
                    # case3.3: từ cột 1 phụ thuộc vào từ cột 2 và từ cột 2 phụ thuộc vào từ đang xét (thuộc cột 3)

                    # case 3.1:
                    weight_case_3_1 = check_rule_label_case_3_1(sentence,

                                                                index_word_head,
                                                                label_DP_word_current,
                                                                labels_DP_rule,
                                                                label_POS_word_current,
                                                                labels_POS_rule,
                                                                word,
                                                                words_rule)
                    # lấy trọng số
                    if weight_case_3_1 >= 3:
                        label_AMR_with_weight.append(("case_3.1", rule[0], weight_case_3_1))

                    # case 3.2:
                    weight_case_3_2 = check_rule_label_case_3_2(sentence,
                                                                index_word_current,
                                                                index_word_head,
                                                                label_DP_word_current,
                                                                labels_DP_rule,
                                                                label_POS_word_current,
                                                                labels_POS_rule,
                                                                word,
                                                                words_rule)
                    # lấy trọng số
                    if weight_case_3_2 >= 3:
                        label_AMR_with_weight.append(("case_3.2", rule[0], weight_case_3_2))

                    # case 3.3:
                    weight_case_3_3 = check_rule_label_case_3_3(sentence,
                                                                index_word_current,
                                                                label_DP_word_current,
                                                                labels_DP_rule,
                                                                label_POS_word_current,
                                                                labels_POS_rule,
                                                                word,
                                                                words_rule)
                    # lấy trọng số
                    if weight_case_3_3 >= 3:
                        label_AMR_with_weight.append(("case_3.3", rule[0], weight_case_3_3))

                # tìm nhãn POS của từ ở cột 4 tương ứng với nhãn ở cột 2
                # Các trường hợp đặc biệt:
                # trường hợp đặc biệt 1: chỉ cần từ đúng từ là sẽ dc chọn nhãn
                if len(rule[7]) != 0:
                    labels_DP_rule = [1]
                    label_POS_rule = rule[4]
                    # tìm các từ có thể có của từ ở cột 7 tương ứng với nhãn ở cột 2
                    words_rule = rule[7]
                    # trường hợp này chỉ xét ở cột nhãn POS và cột từ đúng của từ
                    weight_case_4 = check_rule_label_case_4(label_DP_word_current, labels_DP_rule,
                                                            label_POS_word_current, label_POS_rule, word, words_rule)
                    # lấy trọng số
                    if weight_case_4 >= 4:
                        label_AMR_with_weight.append(("case_4", rule[0], weight_case_4))

            word_current[0] = select_label_AMR_to_word_current(label_AMR_with_weight)
            if word_current[0] == "":
                word_current[0] = ":?"
        # print(word_current)

    return sentence


def matching_sentences_and_rule(sentences, rule_labels):
    sentences_labling = []
    for sentence in sentences:
        n_sentence = matching_label(sentence, rule_labels)
        # print(n_sentence)
        sentences_labling.append(n_sentence)
    return sentences_labling


def write_result(file_result_path, sentences_origin, sentences_labeled):
    with open(file_result_path, "w", encoding="utf-8", newline='') as file:
        data_writer = csv.writer(file, delimiter="\t")
        for s in range(len(sentences_labeled)):
            file.write("# ::id " +str(s+1)+"\n")
            file.write("# ::snt " +sentences_origin[s])
            data_writer.writerows(sentences_labeled[s])
            data_writer.writerow("")

    print("write done")


if __name__ == '__main__':

    file_rule_path = "rule/ruleV2.txt"
    rule_labels = read_rule_file(file_rule_path)

    file_data_path = "data/DP_reformat.txt"
    sentences = read_data_file(file_data_path)

    sentences_labeled = matching_sentences_and_rule(sentences, rule_labels)

    file_sentences_origin_path = "data/sentences_LP-DPN.txt"
    sentences_origin = read_sentences_origin(file_sentences_origin_path)

    file_result_path = "data/results_LP-DPN.txt"
    write_result(file_result_path, sentences_origin, sentences_labeled)
