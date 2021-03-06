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


# tr?????ng h??p 1 ch??? c?? 1 nh??n DP trong lu???t th?? kh??ng c???n x??t head:
def check_rule_label_case_1(label_DP_word_current, label_DP_rule, label_POS_word_current, label_POS_rule, word,
                            words_rule):
    weight_case_1 = 0

    # 3 tr???ng s??? cho tr?????ng h???p 1:
    # b???ng 1 l?? ????ng nh??n DP
    # b???ng 2 l?? ????ng nh??n DP v?? ????ng nh??n POS OR ????ng nh??n DP v?? ????ng t???
    # b??ng 3 l?? ????ng nh??n DP v?? ????ng nh??n POS v?? ????ng t???

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
    # 5 tr???ng s??? cho tr?????ng h???p 2:
    # b???ng 2 l?? ????ng nh??n DP v?? Head
    # b???ng 3 l?? ??????ng nh??n DP v?? Head v?? 1 nh??n POS ????ng OR 1 t??? ????ng t???
    # b???ng 4 l?? ????ng nh??n DP v?? Head v?? ????ng nh??n 2 POS OR 2 t??? ????ng t???
    # b???ng 5 l?? ????ng nh??n DP v?? Head v?? (????ng nh??n 2 POS v?? 1 t??? ????ng t???) OR (????ng nh??n 1 POS v?? 2 t??? ????ng t???)
    # b??ng 6 l?? ????ng t???t c???

    # t??m t???, nh??n POS, nh??n DP c???a t??? head c???a t??? ??ang x??t:
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
    # t??? b??? ph??? thu???c == Behind

    # t??m t???, nh??n POS, nh??n DP c???a t??? Behind ????ng nh??n c???a t??? ??ang x??t:
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
    # t??? b??? ph??? thu???c == Behind
    # 7 tr???ng s??? cho tr?????ng h???p 3: (3,4,5,6,7,8,9)

    # t??m t???, nh??n POS, nh??n DP c???a t??? Head_1 (c???t 2) ????ng nh??n c???a t??? ??ang x??t:
    word_head_1, label_POS_head_1, label_DP_head_1 = find_properties_head(sentence, index_word_head)

    # t??m t???, nh??n POS, nh??n DP c???a t??? Head_2 (c???t 3) ????ng nh??n c???a t??? ??ang x??t:
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
    # t??? b??? ph??? thu???c == Behind
    # 7 tr???ng s??? cho tr?????ng h???p 3: (3,4,5,6,7,8,9)

    # t??m t???, nh??n POS, nh??n DP c???a t??? behind (c???t 1) ????ng nh??n c???a t??? ??ang x??t:
    label_true = labels_DP_rule[0]
    word_behind, label_POS_behind, label_DP_behind = find_word_behind_true_label(sentence, index_word_current,
                                                                                 label_true)

    # t??m t???, nh??n POS, nh??n DP c???a t??? Head (c???t 3) ????ng nh??n c???a t??? ??ang x??t:

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
    # t??? b??? ph??? thu???c == Behind
    # 7 tr???ng s??? cho tr?????ng h???p 3: (3,4,5,6,7,8,9)
    # t??m t???, nh??n POS, nh??n DP c???a t??? behind (c???t 2) ????ng nh??n c???a t??? ??ang x??t:
    label_true = labels_DP_rule[1]
    word_behind_2, label_POS_behind_2, label_DP_behind_2 = find_word_behind_true_label(sentence, index_word_current,
                                                                                       label_true)

    # t??m t???, nh??n POS, nh??n DP c???a t??? behind (c???t 1) ????ng nh??n c???a t??? ??ang x??t:
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


# tr?????ng h???p ?????c bi???t c?? nh??n DP trong lu???t v?? l?? t??? ????ng t??? s??? ???????c ch???p nh???n
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

        # if nh??n ph??? thu???c l?? root th?? l?? g???c
        if label_DP_word_current == "root":
            word_current[0] = "root"
        else:
            # t??m c??c v??? tr?? c??c t??? ph??? thu???c c???a t??? ??ang x??t:

            # case:
            # 1 nh??n: c1
            # 2 nh??n: (c1,c2)
            # 3 nh??n: (c1,c2,c3)
            label_AMR_with_weight = []
            for rule in rule_labels:

                # t??m t???ng s??? nh??n c?? trong 1 lu???t:
                c_LDP = count_label_DP_in_rule(rule)

                # Case1: ch??? c?? 1 nh??n DP ??? c???t 1:
                # k???t qu??? l?? 1 t???p h???p g???m (nh??n, tr???ng s???)

                if (c_LDP == 1):

                    label_DP_rule = rule[1]

                    # t??m nh??n POS c???a t??? ??? c???t 4 t????ng ???ng v???i nh??n ??? c???t 2
                    label_POS_rule = rule[4]

                    # t??m c??c t??? c?? th??? c?? c???a t??? ??? c???t 7 t????ng ???ng v???i nh??n ??? c???t 2
                    words_rule = rule[7]
                    weight_case_1 = check_rule_label_case_1(label_DP_word_current, label_DP_rule,
                                                            label_POS_word_current, label_POS_rule, word, words_rule)
                    # l???y tr???ng s???
                    if weight_case_1 >= 1:
                        label_AMR_with_weight.append(("case_1", rule[0], weight_case_1))

                # Case2: ch??? c?? 2 nh??n DP ??? c???t 1 v?? 2:
                # k???t qu??? l?? 1 t???p h???p g???m (nh??n, tr???ng s???)

                if (c_LDP == 2):
                    # c?? 2 nh??n, nh??n ??? c???t 1, c???t 2
                    labels_DP_rule = [rule[1], rule[2]]

                    # t??m nh??n POS c???a t??? ??? c???t 4, 5 t????ng ???ng v???i nh??n ??? c???t 1, 2
                    labels_POS_rule = [rule[4], rule[5]]

                    # t??m c??c t??? c?? th??? c?? c???a t??? ??? c???t 7, 8 t????ng ???ng v???i nh??n ??? c???t 1, 2
                    words_rule = [rule[7], rule[8]]

                    # trong tr?????ng h???p 2 th?? c?? th??? x??t th??nh 2 tr?????ng h???p:
                    # case2.1: t??? ??ang x??t (thu???c c???t 1) ph??? thu???c v?? t??? c???t 2
                    # case2.2: t??? c???t 1 ph??? thu???c v??o ??ang x??t (thu???c c???t 2)
                    # v?? th??? c???n truy???n v??o c??? c??u v?? v??? tr?? c???a t??? ??ang x??t hi???n t???i ????? t??m t??? ph??? thu???c ho???c b??? ph??? thu???c cho t??? hi???n t???i
                    # 3 tr???ng s??? cho tr?????ng h???p 2:
                    # b???ng 2 l?? ????ng 2 nh??n DP
                    # b???ng 3 l?? ????ng 2 nh??n DP v?? (1 nh??n POS ????ng OR 1 t??? ????ng t???)
                    # b???ng 4 l?? ????ng 2 nh??n DP v?? (????ng nh??n 2 POS OR 2 t??? ????ng t???)
                    # b???ng 5 l?? ????ng 2 nh??n DP v?? (????ng nh??n 2 POS v?? 1 t??? ????ng t???) OR (????ng nh??n 1 POS v?? 2 t??? ????ng t???)
                    # b??ng 6 l?? ????ng t???t c???
                    # case2.1:
                    weight_case_2_1 = check_rule_label_case_2_1(sentence,
                                                                index_word_head,
                                                                label_DP_word_current,
                                                                labels_DP_rule,
                                                                label_POS_word_current,
                                                                labels_POS_rule,
                                                                word,
                                                                words_rule)

                    # l???y tr???ng s???
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
                    # l???y tr???ng s???
                    if weight_case_2_2 >= 2:
                        label_AMR_with_weight.append(("case_2.2", rule[0], weight_case_2_2))

                # Case3: ch??? c?? 3 nh??n DP ??? c???t 1 ,2 v?? 3:
                # k???t qu??? l?? 1 t???p h???p g???m (nh??n, tr???ng s???)
                if (c_LDP == 3):
                    # c?? 3 nh??n, nh??n ??? c???t 1, c???t 2, c???t3
                    labels_DP_rule = [rule[1], rule[2], rule[3]]

                    # t??m nh??n POS c???a t??? ??? c???t 4, 5, 6 t????ng ???ng v???i nh??n ??? c???t 1, 2, 3
                    labels_POS_rule = [rule[4], rule[5], rule[6]]

                    # t??m c??c t??? c?? th??? c?? c???a t??? ??? c???t 7, 8, 9 t????ng ???ng v???i nh??n ??? c???t 1, 2, 3
                    words_rule = [rule[7], rule[8], rule[9]]

                    # trong tr?????ng h???p 3 th?? c?? th??? x??t th??nh 3 tr?????ng h???p:
                    # case3.1: t??? ??ang x??t (thu???c c???t 1) ph??? thu???c v??o t??? c???t 2 v?? t??? c???t 2 ph??? thu???c v??o t??? c???t 3
                    # case3.2: t??? c???t 1 ph??? thu???c v??o t??? ??ang x??t (thu???c c???t 2) v?? t??? c???t 2 ph??? thu???c v??o t??? c???t 3
                    # case3.3: t??? c???t 1 ph??? thu???c v??o t??? c???t 2 v?? t??? c???t 2 ph??? thu???c v??o t??? ??ang x??t (thu???c c???t 3)

                    # case 3.1:
                    weight_case_3_1 = check_rule_label_case_3_1(sentence,

                                                                index_word_head,
                                                                label_DP_word_current,
                                                                labels_DP_rule,
                                                                label_POS_word_current,
                                                                labels_POS_rule,
                                                                word,
                                                                words_rule)
                    # l???y tr???ng s???
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
                    # l???y tr???ng s???
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
                    # l???y tr???ng s???
                    if weight_case_3_3 >= 3:
                        label_AMR_with_weight.append(("case_3.3", rule[0], weight_case_3_3))

                # t??m nh??n POS c???a t??? ??? c???t 4 t????ng ???ng v???i nh??n ??? c???t 2
                # C??c tr?????ng h???p ?????c bi???t:
                # tr?????ng h???p ?????c bi???t 1: ch??? c???n t??? ????ng t??? l?? s??? dc ch???n nh??n
                if len(rule[7]) != 0:
                    labels_DP_rule = [1]
                    label_POS_rule = rule[4]
                    # t??m c??c t??? c?? th??? c?? c???a t??? ??? c???t 7 t????ng ???ng v???i nh??n ??? c???t 2
                    words_rule = rule[7]
                    # tr?????ng h???p n??y ch??? x??t ??? c???t nh??n POS v?? c???t t??? ????ng c???a t???
                    weight_case_4 = check_rule_label_case_4(label_DP_word_current, labels_DP_rule,
                                                            label_POS_word_current, label_POS_rule, word, words_rule)
                    # l???y tr???ng s???
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
