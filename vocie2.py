import requests
import base64
import pygame
import streamlit as st
import time

def split_text(text, limit=60):
    """
    将文本分段，每段不超过指定的字符数。
    """
    # 使用 UTF-8 编码计算长度
    text_bytes = text.encode('utf-8')
    if len(text_bytes) <= limit:
        return [text]
    else:
        parts = []
        current_part = ""
        for char in text:
            # 尝试添加当前字符到段落
            if len((current_part + char).encode('utf-8')) <= limit:
                current_part += char
            else:
                # 当前段落已满，开始新的段落
                parts.append(current_part)
                current_part = char
        # 添加最后一个段落
        parts.append(current_part)
        return parts

def process_text(text):
    """
    处理文本，如果文本超过长度限制，则分段处理。
    """
    parts = split_text(text)
    for part in parts:
        # 假设 send_request 是发送请求的函数
        create_voise(part)
        time.sleep(4)
        # 可能需要等待或处理响应

    
def play_audio(file_name):
    # 初始化 pygame 混音器
    # pygame.mixer.init()
    # # 加载音频文件
    # pygame.mixer.music.load(file_name)
    # # 播放音频
    # pygame.mixer.music.play()
    # # 等待音频播放完成
    # while pygame.mixer.music.get_busy():
    #     pygame.time.Clock().tick(10)
    audio_file = open(file_name, 'rb')
    audio_bytes = audio_file.read()
    base64_audio = base64.b64encode(audio_bytes).decode('utf-8')

    # 检查是否收到了音频播放结束的事件
    if 'audio_ended' not in st.session_state:
        st.session_state.audio_ended = False
    
    # 创建一个自动播放的 HTML audio 标签
    audio_html = f'<audio autoplay><source src="data:audio/mp3;base64,{base64_audio}" type="audio/mp3"></audio>'
#     audio_html = f"""
# <audio id="audioPlayer" autoplay>
#   <source src="data:audio/mp3;base64,{base64_audio}" type="audio/mp3">
#   Your browser does not support the audio element.
# </audio>
# <script>
# document.getElementById('audioPlayer').onended = function() {{
#     // 音频播放结束时，通过Streamlit的客户端事件系统发送消息
#     window.parent.postMessage({{
#         'type': 'streamlit:customEvent',
#         'key': 'audioEnded',
#         'isStreamlitMessage': true,
#     }}, '*');
# }};
# </script>
# """
    
    # 使用 Streamlit 显示 HTML
    st.markdown(audio_html, unsafe_allow_html=True)
    # 根据音频播放结束的事件来执行特定的Python代码
    # if st.session_state.audio_ended:
    #     print("音频播放已结束，执行下一步操作。")

API_KEY = "IAINmGmzxZ9SyNeqfXkB4jeE"
SECRET_KEY = "F3ArFlkOHyBStDqoDuK4chy984VQWIdX"

def create_voise(text):
    
    
    url = "https://tsn.baidu.com/text2audio"
    
    #payload='tex=%E4%BD%A0%E5%A5%BD%E5%95%8A%EF%BC%8C%E6%88%91%E6%98%AF%E8%B1%86%E5%B0%8F%E9%B8%AD&tok='+ get_access_token() +'&cuid=NN5cQAij5yI9xcFBqCwnQyHYlVVk9nfp&ctp=1&lan=zh&spd=5&pit=5&vol=5&per=4&aue=3'
    payload = 'tex='+ text + '&tok=' + get_access_token() + '&cuid=NN5cQAij5yI9xcFBqCwnQyHYlVVk9nfp&ctp=1&lan=zh&spd=5&pit=5&vol=5&per=4&aue=3'
    encoded_payload = payload.encode('utf-8')
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',  # 明确指定字符集为 UTF-8
        'Accept': '*/*'
    }
    # headers = {
    #     'Content-Type': 'application/x-www-form-urlencoded',
    #     'Accept': '*/*'
    # }
    
    response = requests.request("POST", url, headers=headers, data=encoded_payload)
     # 检查响应状态码
    if response.status_code != 200:
        print(f"请求失败，状态码：{response.status_code}")
        return
    
        
    # 检查内容类型
    content_type = response.headers.get('Content-Type', '')
    if 'audio/mp3' in content_type:
        # 直接处理音频数据
        file_name = "output.mp3"
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"音频文件已保存为 {file_name}")
        play_audio(file_name)
    elif 'application/json' in content_type:
        try:
            response_data = response.json()
            binary_data = base64.b64decode(response_data['binary'])
            file_name = f"{response_data['name']}.{response_data['suffix']}"
            with open(file_name, 'wb') as file:
                file.write(binary_data)
            print(f"音频文件已保存为 {file_name}")
            # 保存文件后直接播放
            play_audio(file_name)
            #time.sleep(10)
        except Exception as e:
            print(f"解析 JSON 时出错：{e}")
    else:
        print(f"预期的 JSON 或 audio/mp3 响应，但收到的是：{content_type}")
    

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    #create_voise('他是谁呀，你认识吗')
    text = "聪明的一休哥也斗不过阿凡提的毛驴子"
    #text = "他是谁呀，汤面"
    process_text(text)
