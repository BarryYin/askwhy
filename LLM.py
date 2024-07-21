import erniebot
import json
import requests
import re
 
erniebot.api_type = 'aistudio'
erniebot.access_token = 'a2a30f75102adf4d00eaefe013e32ad4cb9e4857'


def is_right(inputtext,answer):
            response = erniebot.ChatCompletion.create(
                model='ernie-3.5',
                messages=[{'role': 'user', 'content': f'''
                           请匹配用户输入的内容和答案之间是否匹配\n
                           用户输入： {inputtext} \n
                           答案： {answer}
                           请给出答案，如果匹配或者接近，请回复为1，如果不匹配，请回复为0.
                           输出格式如下：
                           ‘’‘json
                           [
                                {{
                                    'answer' : '1' ,
                                    'reason' : '判断的理由'
                                }}
                            ]
                           ’‘’
                           '''}],
            )
            response=response.get_result()
            # 移除非JSON的部分
            json_str = response.strip("```json\n").strip("```\n")

            data = json.loads(json_str)

            # 提取"answer"的值
            answer = data[0]["answer"]
            reason = data[0]["reason"]

            print(answer)  # 输出: 1
            print(reason)
            return answer

# response = is_right("乔布斯","苹果的创办者是乔布斯")
# print(response)


# response = erniebot.ChatCompletion.create(
#     model='ernie-3.5',
#     messages=[{'role': 'user', 'content': "请对我说“你好，世界！”"}],
# )
# print(response.get_result())


# model = 'ernie-3.5'
# messages = [{'role': 'user', 'content': "请问你能以《你好，世界》为题，写一首现代诗吗？"}]
# first_response = erniebot.ChatCompletion.create(
#     model=model,
#     messages=messages,
    
# )
# print(first_response.get_result())

# messages.append(first_response.to_message())
# messages.append({'role': 'user', 'content': "谢谢你！请问你能把这首诗改写成七言绝句吗？"})

# second_response = erniebot.ChatCompletion.create(
#     model=model,
#     messages=messages,
# )
# print(second_response.get_result())


# response_stream = erniebot.ChatCompletion.create(
#     model='ernie-3.5',
#     messages=[{'role': 'user', 'content': "请写一篇200字的文案，介绍文心一言"}],
#     stream=True,
# )
# for response in response_stream:
#     print(response.get_result(), end='', flush=True)
# print("")

# response = erniebot.ChatCompletion.create(
#     model='ernie-3.5',
#     messages=[{'role': 'user', 'content': "你好呀，和我打个招呼吧"}],
#     system="你是一个爱笑的智能助手，请在每个回答之后添加“哈哈哈”",
# )
# print(response.get_result())

# def get_current_temperature(location, unit):
#     return {"temperature": 25, "unit": "摄氏度"}


# functions = [
#     {
#         'name': 'get_current_temperature',
#         'description': "获取指定城市的气温",
#         'parameters': {
#             'type': 'object',
#             'properties': {
#                 'location': {
#                     'type': 'string',
#                     'description': "城市名称",
#                 },
#                 'unit': {
#                     'type': 'string',
#                     'enum': [
#                         '摄氏度',
#                         '华氏度',
#                     ],
#                 },
#             },
#             'required': [
#                 'location',
#                 'unit',
#             ],
#         },
#         'responses': {
#             'type': 'object',
#             'properties': {
#                 'temperature': {
#                     'type': 'integer',
#                     'description': "城市气温",
#                 },
#                 'unit': {
#                     'type': 'string',
#                     'enum': [
#                         '摄氏度',
#                         '华氏度',
#                     ],
#                 },
#             },
#         },
#     },
# ]

# messages = [
#     {
#         'role': 'user',
#         'content': "深圳市今天气温如何？",
#     },
# ]
 
# response = erniebot.ChatCompletion.create(
#     model='ernie-3.5',
#     messages=messages,
#     functions=functions,
# )
# assert response.is_function_response
# function_call = response.get_result()
# print(function_call)


# import json
 
# name2function = {'get_current_temperature': get_current_temperature}
# func = name2function[function_call['name']]
# args = json.loads(function_call['arguments'])
# res = func(location=args['location'], unit=args['unit'])
# print(res)

# messages.append(response.to_message())
# print(messages)

# messages.append(
#     {
#         'role': 'function',
#         'name': function_call['name'],
#         'content': json.dumps(res, ensure_ascii=False),
#     }
# )
# print(messages)


# response = erniebot.ChatCompletion.create(
#     model='ernie-3.5',
#     messages=messages,
# )
# print(response.get_result())


#  AiYXTFoUfpaotDAxUuiAakdK

# Jl0Rf1po0wBZyaVx0pGPdMsl1eqCg4XM

#import erniebot
 
# erniebot.api_type = 'yinian'
# erniebot.access_token = 'a2a30f75102adf4d00eaefe013e32ad4cb9e4857'
 
# response = erniebot.Image.create(
#     model='ernie-vilg-v2',
#     prompt="雨后的桃花，8k，辛烷值渲染",
#     width=512,
#     height=512
# )
 



# print(response.get_result())


# AppID 30680611
# API Key	 IAINmGmzxZ9SyNeqfXkB4jeE
# Secret Key	 F3ArFlkOHyBStDqoDuK4chy984VQWIdX



# def get_access_token(client_id, client_secret):
#     """
#     使用 AK，SK 生成鉴权签名（Access Token）
#     :return: access_token，或是None(如果错误)
#     """
#     url = "https://aip.baidubce.com/oauth/2.0/token"
#     params = {"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret}
#     return str(requests.post(url, params=params).json().get("access_token"))

# def get_access_token(API_KEY,SECRET_KEY):
#     """
#     使用 AK，SK 生成鉴权签名（Access Token）
#     :return: access_token，或是None(如果错误)
#     """
#     url = "https://aip.baidubce.com/oauth/2.0/token"
#     params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
#     return str(requests.post(url, params=params).json().get("access_token"))

# # 生成合成任务
# def create_task(text:str, client_id:str, client_secret:str):
#     url = "https://aip.baidubce.com/rpc/2.0/tts/v1/create?access_token=" + get_access_token(client_id, client_secret)
    
#     payload = json.dumps({
#         "text": text,
#         "format": "mp3-16k",
#         "voice": 111,
#         "lang": "zh",
#         "speed": 5,
#         "pitch": 5,
#         "volume": 5,
#         "enable_subtitle": 0
#     })
#     headers = {
#         'Content-Type': 'application/json',
#         'Accept': 'application/json'
#     }
    
#     response = requests.request("POST", url, headers=headers, data=payload)
#     return response.json()

# # 查询任务状态
# def get_voise_url(task_id:str, client_id, client_secret):
#     url = "https://aip.baidubce.com/rpc/2.0/tts/v1/query?access_token=" + get_access_token(client_id, client_secret)
#     payload = json.dumps({
#         "task_ids": [task_id]
#     })
#     headers = {
#         'Content-Type': 'application/json',
#         'Accept': 'application/json'
#     }
    
#     response = requests.request("POST", url, headers=headers, data=payload)
#     task = response.json()['tasks_info'][0]
#     task_status = task['task_status']
#     # 如果成功，返回语音地址；如果失败，抛出异常；如果进行中，返回空
#     if task_status == 'Success':
#         #print(task)
#         return task['task_result']['speech_url']
#     if task_status == 'Failure':
#         raise Exception("合成语音失败")
#     else:
#         return None

# # 用于递归语音任务的外部方法
# def create_voise(text:str, client_id:str, client_secret:str):
#     # 创建语音合成项目
#     task_resp = create_task(text, client_id, client_secret)
#     #print(task_resp)
#     task_id = task_resp['task_id']
#     # 获取语音文件,循环检测到地址
#     voice_url = None
#     while voice_url == None:
#         voice_url = get_voise_url(task_id, speak_client_id, speak_client_secret)
#     return voice_url

# answer = '喜鹊报喜、乌鸦报丧”有没有科学道理喜鹊是一种较为常见的鸟类，在中国，除内蒙古和青藏高原的部分地区外，都可以见到喜鹊的踪影。“喜上眉梢”是中国国画中常见的主题，其中的“喜”便是指喜鹊，这也从侧面说明了中国人对喜鹊的喜爱之情。'
# speak_client_id = 'IAINmGmzxZ9SyNeqfXkB4jeE'
# speak_client_secret ='F3ArFlkOHyBStDqoDuK4chy984VQWIdX'
# voice_url = create_voise(answer, speak_client_id, speak_client_secret)
#print(voice_url)
# voice_url = json.loads(voice_url)
# speech_url = voice_url['task_result']['speech_url']
# print(speech_url)
# 检查 voice_url 是否为空或者是否为有效的JSON字符串
# if voice_url:
#     try:
#         voice_url_dict = json.loads(voice_url)
#         # 确保返回的JSON中包含需要的数据
#         if 'task_result' in voice_url_dict and 'speech_url' in voice_url_dict['task_result']:
#             speech_url = voice_url_dict['task_result']['speech_url']
#             print(speech_url)
#         else:
#             print("返回的JSON格式不正确或缺少预期的数据")
#     except json.JSONDecodeError as e:
#         print("解析JSON时出错:", e)
# else:
#     print("voice_url 是空的或者返回了非法的JSON字符串")
# # 定义正则表达式来匹配 speech_url
# regex = r'"speech_url":\s*"([^"]+)"'

# # 使用 re.search() 查找匹配的URL
# match = re.search(regex, voice_url)

# if match:
#     # 提取匹配的URL
#     speech_url = match.group(1)
#     print(speech_url)
# else:
#     print("未找到 speech_url")

#token = get_access_token(speak_client_id,speak_client_secret)
#print(token)