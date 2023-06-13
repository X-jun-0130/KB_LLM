# KB_LLM
知识库、大语言模型、医疗知识库构建、基于大语言模型的知识库

### 向量库
Chroma [https://docs.trychroma.com/]

pip install chroma

### Embedding
chroma内部自带的sentence-transformers里的几个向量算法，测试下来不咋样

使用了text2vec-base-chinese
还有一个同款 text2vec-large-chinese

### 创建知识库
```
# create_kb.py
1.创建数据库，并将库文件置于自定义位置
2.利用text2ve将文本转为向量，文本与向量导入知识库中
```

### 构建搜索
```
同样利用text2vec将待匹配文本转为向量与库中向量进行匹配
```

### 大模型
```
搜索结果与问题转为特定的prompt，输入大语言模型进行答案生成
```

### 知识库设计范式
之前老的思路，不合适多轮的形式。如何将知识库设计成可以多轮的形式，可以参考如下的范式，当然搜索引擎插件的范式，也可以按照这种来设计。
```
模型角色信息： System、User、Assistant、Search、Thought

指令：
System:你是一名知识库助手。Thought是你在思考是否需要调用知识库API,Search是查询结果,你需要结合所有的查询结果来回答User的问题,不允许添加额外信息。</s>
turn 1:
    User:输入问题1</s>
    Thought:当前信息无法回答这个问题，需要调用知识库API。</s>           [模型第一次输出,隐藏步骤]
    Search:'\n\n'.join(查询结果拼接)</s>
    Assistant:xxx</s>                                               [模型第二次输出，最终输出]
    
turn 2:
    User:输入问题2</s>
    Thought:这个问题可以直接回答，无需调用知识库API。</s> 
    Search:None</s>
    Assistant:xxx</s>
```
