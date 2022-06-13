import string
import re
import statistics

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


def get_result_eval(path):
    scores = []
    with open(path, 'r', encoding='utf-8') as file:
        P = -1.0
        R = -1.0
        F = -1.0
        for line in file:
            line = line.strip()
            # print(line[-4:])
            if 'Precision' in line:
                P = float(line[-4:])
            if 'Recall' in line:
                R = float(line[-4:])
            if 'F-score' in line:
                F = float(line[-4:])
            if F != -1.0:
                scores.append([P, R, F])
                P = -1.0
                R = -1.0
                F = -1.0
    return scores

def get_sents_of_amrs(path):
    sents = []
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if '::snt' in line:
                sents.append(line[8:])

    return sents

def preprocess(sent):
    for w in string.punctuation:
        if w in sent:
            sent = sent.replace(w, ' ')

    sent = re.sub(' +', ' ', sent)

    return sent.strip()

def print_statistical(table):
    if len(table) > 0:
        scores_P = [i[2][0] for i in table]
        scores_R = [i[2][1] for i in table]
        scores_F = [i[2][2] for i in table]
        # print(scores)
        print('Tổng số câu:', len(table))
        p = statistics.mean(scores_P)
        r = statistics.mean(scores_R)
        f = statistics.mean(scores_F)

        print('%s P=%.2f R=%.2f F1=%.2f' %('Smatch trung bình:',p, r, f))
        return p, r, f
    else:
        print('Tổng số câu:', 0)
        return 0.0, 0.0, 0.0

def statistic_all_score(sents):
    lt_10 = []
    gt_10_to_20 = []
    gt_20 = []

    for i in range(len(sents)):
        sent = preprocess(sents[i])
        lo_sent = len(sent.split())
        if lo_sent <= 10:
            lt_10.append([sents[i], lo_sent])
        if lo_sent > 10 and lo_sent < 20:
            gt_10_to_20.append([sents[i], lo_sent])
        if lo_sent >= 20:
            gt_20.append([sents[i], lo_sent])
        # print(sent)
        # print(scores[i])
        # print()
    return lt_10, gt_10_to_20, gt_20

def get_scores_by_amr(scores, snts):
    amrs = []
    for score in scores:
        for snt in snts:
            if snt == score[0]:
                amrs.append(score)
                break
    # p, r, f = print_statistical(amrs)
    return len(amrs)


def statistic_complete(amrs):
    complete = []
    incomplete = []
    for amr in amrs:
        snt = amr['snt']
        graph = ' '.join(amr["graph"])
        # print(graph)
        if ':?' in graph:
            incomplete.append(snt)
        else:
            complete.append(snt)

    return complete, incomplete


if __name__ == '__main__':

    # path_amrs= '/home/dao/PycharmProjects/ViAMR/ViAMR_rule/data/result_AMR_format.txt'
    path_amrs= 'test_500.amr'
    sents = get_sents_of_amrs(path_amrs)
    # print(len(sents))

    lt_10, gt_10_to_20, gt_20 = statistic_all_score(sents)
    print('AMR có âm tiết <=10: ', len(lt_10))
    # print_statistical(lt_10)

    print('AMR có âm tiết >10 và <20: ', len(gt_10_to_20))
    # print_statistical(gt_10_to_20)

    print('AMR có âm tiết >=20: ', len(gt_20))
    # print_statistical(gt_20)
    print()
    print('_'*50)
    print()


    amrs = load_amr(path_amrs)
    complete, incomplete = statistic_complete(amrs)
    print('tổng số AMR gán hoàn thiện là:', len(complete))
    print('tổng số AMR gán chưa hoàn thiện là:', len(incomplete))

    print()
    print('_'*50)
    print()

    print('Bộ AMR hoàn thiện bao gồm:')

    print('AMR có âm tiết <=10:', get_scores_by_amr(lt_10, complete))

    print()
    print('AMR có âm tiết >10 và <20:', get_scores_by_amr(gt_10_to_20, complete))
    print()
    print('AMR có âm tiết >=20:', get_scores_by_amr(gt_20, complete))

    print()
    print('_'*50)
    print()


    print('Bộ AMR chưa hoàn thiện bao gồm:')
    print('AMR có âm tiết <=10:',get_scores_by_amr(lt_10, incomplete))

    print()
    print('AMR có âm tiết >10 và <=20:', get_scores_by_amr(gt_10_to_20, incomplete))

    print()
    print('AMR có âm tiết >20:', get_scores_by_amr(gt_20, incomplete))
