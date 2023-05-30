from search_query import Search_Query
from transformers import AutoTokenizer, AutoModelForCausalLM,GenerationConfig

import os
os.environ['CUDA_VISIBLE_DEVICES'] = "6"

model_name = '/Nlp_2023/Dialogue_Bloom/Bloom_dialogue/'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).half().cuda()
model.eval()

def generate(input):
    inputs = tokenizer.encode(input, return_tensors="pt").to("cuda")

    generation_config = GenerationConfig(
        temperature=0.2,
        top_k=30,
        top_p=0.85,
        repetition_penalty=1.2,
        do_sample=True,
        min_new_tokens=32,
        max_new_tokens=1024,
        )
    outputs = model.generate(inputs=inputs, generation_config=generation_config)
    output = tokenizer.decode(outputs[0])
    return output.strip('</s>')

query_list = ['虚寒胃痛颗粒每次吃多少']

for payload in query_list:
    input_list = Search_Query(payload)
    pre_input = 'User:'+ query_list[0] + '</s>\n Assistant:'
    pre_out = generate(pre_input)
    pre_out = pre_out.replace(pre_input, '')
    print(f"模型原始输出: {pre_out}")
    print("="*70+" 模型输入输出 "+"="*70)

    if len(input_list) > 0:
        input_text = 'User:'+input_list[0][0] + '\n请仔细阅读上述文本，并回答下面的问题。\n'+ payload + '</s>\n Assistant:'
        print(input_text)
        out = generate(input_text )
        out = out.replace(input_text, '')
        print(f"模型知识库输出: {out}")
