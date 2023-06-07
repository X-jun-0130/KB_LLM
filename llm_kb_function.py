from search_query import Search_Query
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
import json
from fastapi.encoders import jsonable_encoder
import requests

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	# 允许跨域的源列表，例如 ["http://www.example.org"] 等等，["*"] 表示允许任何源
	allow_origins=["*"],

	# 跨域请求是否支持 cookie，默认是 False，如果为 True，allow_origins 必须为具体的源，不可以是 ["*"]
	allow_credentials=False,

	# 允许跨域请求的 HTTP 方法列表，默认是 ["GET"]
	allow_methods=["*"],
    
	# 允许跨域请求的 HTTP 请求头列表，默认是 []，可以使用 ["*"] 表示允许所有的请求头
	# 当然 Accept、Accept-Language、Content-Language 以及 Content-Type 总之被允许的
	allow_headers=["*"],
	# 可以被浏览器访问的响应头, 默认是 []，一般很少指定
	# expose_headers=["*"]
	# 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 600，一般也很少指定
	# max_age=1000
)


class Message(BaseModel):
    role: str = Field(regex='^(User)$')
    content: str = ''

class ChatRequest(BaseModel):
    messages: List[Message]
    stream: bool = False


def get_response(mes):
    Post_url = "http://127.0.0.1:5053/worker_generate"
    r_json = requests.post(Post_url, mes)
    text = json.loads(r_json.text)
    return text['message']


@app.post("/kb_example/", summary='知识库测试用例')
async def get_answer(item: ChatRequest):
    input_dict = jsonable_encoder(item)
    query = input_dict['messages'][0]['content']
    input_list = Search_Query(query)
    result={'prompt':'', 'answer':''}
    if len(input_list) > 0:
        input_text = '上下文:\n'+ '\n\n'.join(input_list[0]) + '\n\n'+ '根据上下文，来回答问题。如果无法从中得到答案，请说 “文本中未提及。”。' + '\n问题是:'+query
        input_dict['messages'][0]['content'] = input_text
        res = get_response(json.dumps(input_dict))

        result['prompt'] = input_text
        if res =='':
            result['answer'] = '文本过长无法处理'
        else:
            result['answer'] = res
    else:
        pass
    return result

if __name__ == "__main__":
    uvicorn.run("llm_kb_function:app", host="0.0.0.0", port=5052)
