from vncorenlp import VnCoreNLP

def get_dependency(sentence):
    annotator = VnCoreNLP("/home/dao/PycharmProjects/ViAMR/ViAMR_rule/VnCoreNLP/VnCoreNLP-1.1.1.jar", annotators="wseg,pos,ner,parse", max_heap_size='-Xmx2g')
    annotated_text = annotator.annotate(sentence)
    # print(annotated_text)
    annotator.close()
    sentences = annotated_text['sentences']
    dp = sentences[0]
    return dp

if __name__ == '__main__':
    text = "Ông Nguyễn Khắc Chúc  đang làm việc tại Đại học Quốc gia Hà Nội"
    dp = get_dependency(text)

    for d in dp:
        print(d)

    # print(dp)



