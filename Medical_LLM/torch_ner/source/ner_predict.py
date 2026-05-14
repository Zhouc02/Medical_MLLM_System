# coding:utf-8
import json
import os
import pickle
import torch
import sys

sys.path.append('/public/home/medical_2324/Medical_LLM/source/')
from source.predict import _check_entity_continuous, _merge_entity

from transformers import BertTokenizer
import source.addFeature as addFeature
from source.config import Config
from collections import OrderedDict


# 预先定义好要识别的实体种类
entity_map_dic = {"drug": "药品", "time": "时间", "body": "部位", "disease": "疾病",
                  "symptom": "症状", "treatment": "治疗", "department": "科室", "crowd": "人群",
                  "feature": "程度", "physiology": "生理", "test": "检查"}
label_list_dir = '/public/home/medical_2324/torch_ner/data/cMedQANER/label.txt'
radical_dict_path = '/public/home/medical_2324/torch_ner/data/featureData/radical_dict.txt'
terminology = "{'药品': '/public/home/medical_2324/torch_ner/data/cMedQANER/technology_data/drug.txt', " \
              "'时间': '/public/home/medical_2324/torch_ner/data/cMedQANER/technology_data/time.txt'," \
              "'部位': '/public/home/medical_2324/torch_ner/data/cMedQANER/technology_data/body.txt'," \
              "'疾病': '/public/home/medical_2324/torch_ner/data/cMedQANER/technology_data/disease.txt'," \
              "'症状': '/public/home/medical_2324/torch_ner/data/cMedQANER/technology_data/symptom.txt'," \
              "'治疗': '/public/home/medical_2324/torch_ner/data/cMedQANER/technology_data/treatment.txt'," \
              "'科室': '/public/home/medical_2324/torch_ner/data/cMedQANER/technology_data/department.txt'," \
              "'人群': '/public/home/medical_2324/torch_ner/data/cMedQANER/technology_data/crowd.txt'," \
              "'程度': '/public/home/medical_2324/torch_ner/data/cMedQANER/technology_data/feature.txt'," \
              "'生理': '/public/home/medical_2324/torch_ner/data/cMedQANER/technology_data/physiology.txt'," \
              "'检查': '/public/home/medical_2324/torch_ner/data/cMedQANER/technology_data/test.txt'}"


class NER(object):
    def get_entities_result(self, query, model_path):
        sentence_list, predict_labels = self.predict(query, model_path)  # 调用模型进行预测，然后返回预测结果

        if len(predict_labels) == 0:
            print("句子: {0}\t实体识别结果为空".format(query))
            return []

        entities = []
        if len(sentence_list) == len(predict_labels):
            result = self._bio_data_handler(sentence_list, predict_labels)
            if len(result) != 0:
                end = 0
                prefix_len = 0

                for word, label in result:
                    sen = query.lower()[end:]
                    begin = sen.find(word) + prefix_len
                    end = begin + len(word)
                    prefix_len = end
                    if begin != -1:
                        ent = dict(value=query[begin:end], type=label, begin=begin, end=end)
                        entities.append(ent)
        return entities

    def predict(self, sentence, model_path):
        config = Config()
        max_seq_length = 128  # 定义能够识别的最大句子长度
        if len(sentence) > max_seq_length:
            print("输入的句子过长，请少于 100 个字符！")
            return list(sentence), []

        tokenizer = BertTokenizer.from_pretrained(model_path)

        #################################################################
        # 新的 label2id
        label_list = addFeature.load_label_list(label_list_dir)
        tag2idx = OrderedDict({label: i for i, label in enumerate(label_list, 0)})

        # 载入词根 radical
        radical_dict, radical_lst = addFeature.load_radical_dict(radical_dict_path) if config.add_radical_or_not else (
            dict(), [])
        radical_lst = ['[PAD]', None, '[CLS]', '[SEP]'] + radical_lst
        radical2idx = OrderedDict({radical: i for i, radical in enumerate(radical_lst, 0)})

        # 载入医学专业词典
        terminology_dicts = addFeature.load_terminology_dict(eval(terminology))
        label_list_based_terminology = addFeature.label_sentence_based_terminology(sentence, terminology_dicts)
        #################################################################
        tokens, labels, ori_tokens, labels_based_terminology, radicals = [], [], [], [], []
        for i, word in enumerate(sentence):
            # 防止wordPiece情况出现，不过貌似不会
            token = tokenizer.tokenize(word)
            tokens.extend(token)

            label_based_terminology = label_list_based_terminology[i]

            ori_tokens.append(word)
            # 单个字符不会出现wordPiece
            if len(token) == 1:
                labels_based_terminology.append(label_based_terminology)
            else:
                print("出现了wordPiece！token是：{}".format(token))

            for t in token:
                radicals.append(radical_dict.get(t))  # 根据当前字找到他的偏旁部首，然后将偏旁部首加到词根 radicals 中

        ntokens = ["[CLS]"]
        segment_ids = [0]
        label_ids_based_terminology = [tag2idx["[CLS]"]]
        radical_ids = [radical2idx["[CLS]"]]

        tag2idx = OrderedDict([('[PAD]', 0), ('O', 1), ('B-药品', 2), ('I-药品', 3), ('B-时间', 4), ('I-时间', 5), ('B-部位', 6), ('I-部位', 7), ('B-疾病', 8), ('I-疾病', 9), ('B-症状', 10), ('I-症状', 11), ('B-治疗', 12), ('I-治疗', 13), ('B-科室', 14), ('I-科室', 15), ('B-人群', 16), ('I-人群', 17), ('B-程度', 18), ('I-程度', 19), ('B-生理', 20), ('I-生理', 21), ('B-检查', 22), ('I-检查', 23), ('[CLS]', 24), ('[SEP]', 25)])

        for i, token in enumerate(tokens):
            ntokens.append(token)
            segment_ids.append(0)
            label_ids_based_terminology.append(tag2idx[labels_based_terminology[i]])
            radical_ids.append(radical2idx[radicals[i]])

        ntokens.append("[SEP]")
        segment_ids.append(0)
        label_ids_based_terminology.append(tag2idx["[SEP]"])
        radical_ids.append(radical2idx["[SEP]"])

        input_ids = tokenizer.convert_tokens_to_ids(ntokens)
        input_mask = [1] * len(input_ids)

        # padding 填充
        input_ids = addFeature.padding(input_ids, max_seq_length, 0)
        input_mask = addFeature.padding(input_mask, max_seq_length, 0)
        segment_ids = addFeature.padding(segment_ids, max_seq_length, 0)
        label_ids_based_terminology = addFeature.padding(label_ids_based_terminology, max_seq_length, tag2idx['[PAD]'])
        radical_ids = addFeature.padding(radical_ids, max_seq_length, radical2idx['[PAD]'])

        assert len(input_ids) == max_seq_length
        assert len(input_mask) == max_seq_length  # input_mask 就是 attention_mask
        assert len(segment_ids) == max_seq_length  # segment_ids 就是 token_type_ids
        # assert len(token_type_ids) == max_seq_length
        # assert len(attention_mask) == max_seq_length
        assert len(label_ids_based_terminology) == max_seq_length
        assert len(radical_ids) == max_seq_length

        input_ids = torch.tensor(input_ids, dtype=torch.long)
        input_mask = torch.tensor(input_mask, dtype=torch.long)
        segment_ids = torch.tensor(segment_ids, dtype=torch.long)
        label_ids_based_terminology = torch.tensor(label_ids_based_terminology, dtype=torch.long)
        radical_ids = torch.tensor(radical_ids, dtype=torch.long)

        input_ids = input_ids.to("cpu").unsqueeze(0)
        input_mask = input_mask.to("cpu").unsqueeze(0)
        segment_ids = segment_ids.to("cpu").unsqueeze(0)
        label_ids_based_terminology = label_ids_based_terminology.to("cpu").unsqueeze(0)
        radical_ids = radical_ids.to("cpu").unsqueeze(0)

        # 加载模型
        model = torch.load(os.path.join(model_path, "ner_model.ckpt"), map_location="cpu")
        if isinstance(model, torch.nn.DataParallel):
            model = model.module
        model.eval()

        # 模型预测，不需要反向传播
        with torch.no_grad():
            predict_val = model.predict(input_ids, radical_ids, label_ids_based_terminology, segment_ids, input_mask)

        # with open(os.path.join(model_path, "label2id.pkl"), "rb") as f:
        #     label2id = pickle.load(f)
        # id2label = {value: key for key, value in label2id.items()}

        id2label = {i: label for i, label in enumerate(label_list)}

        predict_labels = []
        for i, label in enumerate(predict_val[0]):
            if i != 0 and i != len(predict_val[0]) - 1:
                predict_labels.append(id2label[label])

        return list(sentence), predict_labels

    def _bio_data_handler(self, sentence, predict_label):
        entities = []
        # 获取初始位置实体标签
        pre_label = predict_label[0]
        # 实体词初始化
        word = ""
        for i in range(len(sentence)):
            # 记录问句当前位置词的实体标签
            current_label = predict_label[i]
            # 若当前位置的实体标签是以B开头的，说明当前位置是实体开始位置
            if current_label.startswith('B'):
                # 当前位置所属标签类别与前一位置所属标签类别不相同且实体词不为空，则说明开始记录新实体，前面的实体需要加到实体结果中
                if pre_label[2:] is not current_label[2:] and word != "":
                    entities.append([word, entity_map_dic[pre_label[2:]]])
                    # 将当前实体词清空
                    word = ""
                # 记录当前位置标签为前一位置标签
                pre_label = current_label
                # 并将当前的词加入到实体词中
                word += sentence[i]
            # 若当前位置的实体标签是以I开头的，说明当前位置是实体中间位置，将当前词加入到实体词中
            elif current_label.startswith('I'):
                word += sentence[i]
                pre_label = current_label
            # 若当前位置的实体标签是以O开头的，说明当前位置不是实体，需要将实体词加入到实体结果中
            elif current_label.startswith('O'):
                # 当前位置所属标签类别与前一位置所属标签类别不相同且实体词不为空，则说明开始记录新实体，前面的实体需要加到实体结果中
                if pre_label[2:] is not current_label[2:] and word != "":
                    entities.append([word, entity_map_dic[pre_label[2:]]])
                # 记录当前位置标签为前一位置标签
                pre_label = current_label
                # 并将当前的词加入到实体词中
                word = ""
        # 收尾工作，遍历问句完成后，若实体刚好处于最末位置，将剩余的实体词加入到实体结果中
        if word != "":
            entities.append([word, entity_map_dic[pre_label[2:]]])
        return entities

    def _combine_person_entity(self, entity):
        person_types = ['first_name', 'last_name']
        sort_entity = sorted(entity, key=lambda x: x['begin'])
        person_type_node = [e for e in sort_entity if e["type"] in person_types]
        other_type_node = [e for e in sort_entity if e["type"] not in person_types]
        new_entity, res_entity = list(), list()
        if len(person_type_node) == 0:
            return entity

        e1 = person_type_node[0]
        for e2 in person_type_node[1:]:
            if _check_entity_continuous(e1, e2):
                ent = _merge_entity(e1, e2)
                e1 = ent
            else:
                new_entity.append(e1)
                e1 = e2
        new_entity.append(e1)

        for e in new_entity:
            if e["type"] in person_types:
                e_info = {'type': 'person', 'value': e["value"], 'begin': e["begin"],
                          'end': e["end"], 'detail': [e]}
                res_entity.append(e_info)
            else:
                res_entity.append(e)
        res_entity.extend(other_type_node)
        return res_entity

    def _check_entity_continuous(self, e1, e2):
        return True if e1['end'] == e2['begin'] else False

    def _merge_entity(self, e1, e2):
        r_entity = dict()
        person_types = ['first_name', 'last_name', 'person']
        r_entity['type'] = 'person' if e1['type'] in person_types else e1['type']
        r_entity['value'] = e1['value'] + e2['value']
        r_entity['begin'] = e1['begin']
        r_entity['end'] = e2['end']
        detail = e1.get('detail', None)
        if detail:
            detail.append(e2)
            r_entity['detail'] = detail
        else:
            r_entity['detail'] = [e1, e2]
        return r_entity


if __name__ == '__main__':
    # 定义将要预测的句子
    sent1 = "今天感冒了，身体不舒服，头疼加拉肚子，吃了阿莫西林。"
    # 将预测的句子送入模型中进行判断
    model_path = '/root/Medical_LLM/torch_ner/output/cMedQANER/Bert-IDCNN-Att2-BiLSTM-CRF-Final'
    ner = NER()
    sent3 = sys.argv[1]
    pre = ner.get_entities_result(sent3.replace(" ", ""), model_path)  # .replace(" ", "")
    if len(pre) != 0:
        data = [_ for _ in pre]
        print(json.dumps(data))
    else:
        print("未检测到实体！")
