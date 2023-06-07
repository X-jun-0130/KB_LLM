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

