import csv
import streamlit as st
import os
# pip安装命令

install_command = "pip install streamlit-option-menu"
install_command2 = "pip install openai-whisper"
install_command1 = "pip install extra_streamlit_components"
install_command3 = "pip install --upgrade erniebot"
install_command4 = "pip install streamlit-audiorecorder"
install_command5 = "pip install poetry"
install_command6 = "pip install pygame"
install_command7 = "pip install audiorecorder"
#install_command = "pip install -r requirements.txt"
# 执行安装命令
os.system(install_command)
os.system(install_command1)
os.system(install_command2)
os.system(install_command3)
os.system(install_command4)
os.system(install_command5)
os.system(install_command6)
os.system(install_command7)


import json
import pandas as pd
from streamlit_option_menu import option_menu
import extra_streamlit_components as stx
import uuid
import pandas as pd
import erniebot
import requests
import re
#from voice import create_voise
#from openai import OpenAI
from vocie2 import process_text
from audiorecorder import audiorecorder
from LLM import is_right
import whisper



st.set_page_config(page_title='十万个为什么', page_icon=' ', layout='wide')

def get_is_win_value(username):
    csv_file_path = 'winners.csv'
    try:
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Username'] == username:
                    return row['is_win']
    except FileNotFoundError:
        print("CSV文件未找到。")
        return None
    # 如果没有找到匹配的用户名，返回None
    return None

# username = 'default_user'
# is_win_value = get_is_win_value(username)
# if is_win_value is not None:
#     print(f"{username}的is_win值为: {is_win_value}")
# else:
#     print(f"未找到用户名为{username}的记录。")

def add_winner_to_csv(username, is_win):
    csv_file_path = 'winners.csv'
    # 检查CSV文件是否存在，如果不存在，则创建并添加表头
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Username', 'is_win'])  # 添加表头

    # 向CSV文件中添加赢家信息
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, is_win])
def get_question(n):
    # 假设我们有一个包含问题及其答案的列表
    questions_with_answers = [
        {"question": "有种动物似鹿非鹿、似马非马、似驴非驴、似牛非牛，请说出它的名字?", "answer": "四不像"},
        {"question": "现代最大的动物，其个体长度可达33米，体重超过150吨。它叫什么?", "answer": "蓝鲸"},
        {"question": "蝴蝶的生命周期包括四个阶段，卵、幼虫、蛹，还有一个阶段是什么?", "answer": "成虫"},
        {"question": "一种生活在青藏高原的鱼类，其鳞片严重退化，呈现出‘赤身裸体’的状态，它是什么?", "answer": "湟鱼"},
        {"question": "冬虫夏草并非虫或草，而是一种什么物质?", "answer": "真菌"},
        {"question": "马铃薯在发绿变青或长出嫩芽时，会产生一种剧毒物质，食用后可能导致中毒，这种物质的名称?", "answer": "龙葵素"},
        {"question": "发现海王星的人天文学家亚当斯是哪个国家的人", "answer": "英国"},
        {"question": "月球距离地球约多少千米?", "answer": "38万千米"},
        {"question": "DNA结构的发现1953年，论文发表在什么杂志上?", "answer": "英国《自然》杂志"},
        {"question": "人的染色体有多少对?", "answer": "23对"}
    ]
    # 根据 `n` 的值返回相应的问题和答案
    # 注意: 这里假设 `n` 的值不会超过问题列表的长度
    return questions_with_answers[n]

def STT(audio):
    # 파일 저장
    # filename='input.mp3'
    # wav_file = open(filename, "wb")
    # wav_file.write(audio.tobytes())
    # wav_file.close()
    filename = 'output1.wav'  # 或者保持为 'input.mp3'，取决于您的需求
    audio.export(filename, format="wav")  # 根据文件扩展名更改 format 参数 
    model = whisper.load_model("small")
    text = model.transcribe("output1.wav",initial_prompt="请识别语言，并翻译成对应的文字，如果是中文请翻译成简体中文，并添加标点符号")
    print(text['text'])
    return text['text']


def logout():
    # 使用 JavaScript 删除 cookie
    #html('<script>document.cookie = "login_status=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";</script>')
    
    st.write("You have been logged out.")


class Session:
    cookie_manager = None
    session_id = None
    #session_vars = None
    session_vars = {}  # 类变量，所有 Session 的实例都可以访问

    #@staticmethod
    def init(cookinit):
        #self.session_vars = {}
        Session.cookie_manager = cookinit
        cookies1 = Session.cookie_manager.get_all()
        #time.sleep(2)
        #print(cookies1)
        #print(cookies1['ajs_anonymous_id'])
        #print(0)
        #Session.session_vars = {}  # 初始化 session_vars 为一个空列表
        if 'ajs_anonymous_id' in cookies1:
            Session.session_id = cookies1['ajs_anonymous_id']
            Session.get_user_session()
            print("1")
            print(Session.session_id)
        else:
            Session.session_id = str(uuid.uuid4())  # 如果 cookies 中没有 ajs_anonymous_id，那么生成一个新的 UUID
            Session.set_value('count', 0)
            Session.set_value('session_id', Session.session_id)
            print("2")

        
    @staticmethod
    def get_user_session():
        session_file = os.getcwd() + '/sessions/' + Session.session_id + '.json'
        if os.path.exists(session_file) and os.path.getsize(session_file) > 0:
            with open(session_file) as json_file:
                data = json.loads(json_file.read())
                # for i in data:
                #     st.session_state[i] = data[i]
            # Session.session_vars = list(data.keys())
                Session.session_vars = data
        else:
            if not os.path.exists(os.getcwd() + '/sessions/'):
                os.makedirs(os.getcwd() + '/sessions/')
            with open(session_file, 'w') as json_file:
                json_file.write('{}')
            
    @staticmethod
    def save():
        data = {}
        # for i in Session.session_vars:
        #     if i not in st.session_state:
        #         continue
        #     data[i] = st.session_state[i]
        data = Session.session_vars

        # 将 data 字典写入到 session_file 中
        session_file = os.getcwd() + '/sessions/' + Session.session_id + '.json'
        with open(session_file, 'w') as json_file:
                data = json.dumps(data)
                json_file.write(data)

    @staticmethod
    def set_value(name, value):
        #st.session_state[name] = value
        Session.session_vars[name] = value  # 将变量名和值添加到 session_vars 中

    @staticmethod
    def get_value(key):
        if key in Session.session_vars:
            print(Session.session_vars[key])
            return Session.session_vars[key]
        else:
            return 0



def save_answered_questions_to_excel(username, answered_questions):
    # 尝试读取现有的Excel文件，如果不存在则创建一个新的DataFrame
    try:
        df = pd.read_excel('users.xlsx', sheet_name='Users', engine='openpyxl')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Username', 'AnsweredQuestions'])

    new_row = pd.DataFrame({'Username': [username], 'AnsweredQuestions': [','.join(map(str, answered_questions))]})

    # 检查用户是否已存在
    if username in df['Username'].values:
        # 更新已回答问题列表
        df.loc[df['Username'] == username, 'AnsweredQuestions'] = ','.join(map(str, answered_questions))
    else:
        # 如果用户不存在，添加新行
        df = pd.concat([df, new_row], ignore_index=True)

    # 保存更新后的DataFrame回Excel文件
    df.to_excel('users.xlsx', sheet_name='Users', index=False, engine='openpyxl')


def get_answered_questions_from_excel(username):
    try:
        # 读取Excel文件
        df = pd.read_excel('users.xlsx', sheet_name='Users', engine='openpyxl')
        # 查找用户
        user_row = df.loc[df['Username'] == username]
        if not user_row.empty:
            # 提取已回答问题列表
            answered_questions = user_row['AnsweredQuestions'].values[0]
            if answered_questions:
                #return list(map(int, answered_questions.split(',')))
                return answered_questions.split(',')
    except FileNotFoundError:
        pass
    return []


def get_score(username,password):
    if not os.path.exists('scores.csv'):
        with open('scores.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Username', 'Password','score'])

    # with open('scores.csv', 'r') as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         if row[0] == username and row[2] == password:
    #             return int(row[1])
    # #return 0  # Default score for new users
    # raise ValueError("Invalid username or password")  # Raise an exception if user does not exist or password is incorrect
    user_found = False
    with open('scores.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username:
                user_found = True
                if row[1] == password:
                    return row[2]  # 返回用户的分数
                else:
                    raise IncorrectPasswordError("密码不正确")
        if not user_found:
            raise UserNotFoundError("用户名不正确")
        
# def update_score(username, score):
#     with open('scores.csv', 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([username, score])

def update_score(username, score,password):
    rows = []
    with open('scores.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username:
                rows.append([username, password, score])
            else:
                rows.append(row)

    with open('scores.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


class UserNotFoundError(Exception):
    pass

class IncorrectPasswordError(Exception):
    pass

def register_user(username, password):
    # 检查用户是否已存在
    if user_exists(username):
        raise ValueError("用户名已存在。")
    
    # 检查文件是否存在且为空，如果是，则写入列标题
    file_exists = os.path.exists('scores.csv')
    should_write_header = not file_exists or os.stat('scores.csv').st_size == 0

    # 将新用户添加到 CSV 文件中
    with open('scores.csv', 'a', newline='') as file:
        fieldnames = ['Username', 'Password','score']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if should_write_header:
            writer.writeheader()

        writer.writerow({'Username': username, 'Password': password,'score': 0})

def user_exists(username):
    # 检查 CSV 文件中是否已有该用户名
    if not os.path.exists('scores.csv'):
        return False  # 文件不存在，意味着还没有用户注册
    with open('scores.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username:
                return True
    return False

def update_room_score(room_id, username, new_score):
    df = pd.read_csv('rooms.csv')

    for i in range(1, 3):
        if df.loc[df['room_id'] == int(room_id), f'user{i}'].values[0] == username:
            df.loc[df['room_id'] == int(room_id), f'score{i}'] = new_score
            break

    df.to_csv('rooms.csv', index=False)

def join_room(room_id, username):
    # Read the current rooms from the CSV file
    with open('rooms.csv', 'r') as f:
        reader = csv.reader(f)
        rooms = list(reader)

    # Find the room with the given room_id
    for room in rooms:
        if room[0] == room_id:
            # Check if the room is full
            if room[1] and room[2]:
                raise ValueError("Room is full")
            # Add the new user to the room
            elif not room[1]:
                room[1] = username
                room[3] = 0
            else:
                room[2] = username
                room[4] = 0
            break
    else:
        # If the room does not exist, create a new room
        rooms.append([room_id, username, ''])

    # Write the updated rooms back to the CSV file
    with open('rooms.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rooms)

def get_room_info(room_id):
    # Read the current rooms from the CSV file
    with open('rooms.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        rooms = list(reader)

    # Find the room with the given room_id
    for room in rooms:
        #print("房间号")
        #print(room[0])
        #print(room[0])
        #print(type(room[0]))
        # if room[0].isdigit() and int(float(room[0])) == room_id:
        if room[0] == room_id:
            # Return the room information
            return {
                'room_id': room_id,
                'users': [
                    {'username': room[1], 'score': room[3]},  # Convert string to float, then to int
                    {'username': room[2], 'score': room[4]}   # Convert string to float, then to int
                ]
            }

    # If the room does not exist, raise an error
    raise ValueError("Room does not exist")


def create_new_room(initial_user):
    # 读取现有的房间信息
    df = pd.read_csv('rooms.csv')
    # 生成新的房间ID，这里简单地使用当前最大的room_id加1
    new_room_id = df['room_id'].max() + 1
    # 新房间的用户数量初始为1
    #user_count = 1
    # 将新房间信息添加到DataFrame
    new_row = pd.DataFrame({'room_id': str(new_room_id), 'user1': initial_user,'score1':0}, index=[0])
    # 使用 pandas.concat 来添加新行
    df = pd.concat([df, new_row], ignore_index=True)
    # 保存更新后的DataFrame回CSV文件
    df.to_csv('rooms.csv', index=False)
    # 返回新房间的ID
    return new_room_id


def update_50_score(room_id, username, new_score,is_stand):
    df = pd.read_csv('rooms50.csv')
    print(is_stand)
    for i in range(1, 51):  # 假设最多有50个用户
        user_column = f'user{i}'
        score_column = f'score{i}'
        is_stand_column = f'id{i}_is_stand'
        # 检查房间ID匹配，并且确保返回的数组不为空
        matching_rows = df.loc[df['room_id'] == int(room_id), user_column]
        if not matching_rows.empty and matching_rows.values[0] == username:
            df.loc[df['room_id'] == int(room_id), score_column] = new_score
            df.loc[df['room_id'] == int(room_id), is_stand_column] = is_stand
            break  # 找到匹配后立即退出循环

    df.to_csv('rooms50.csv', index=False)

def join_50_room(room_id, username):
    # Read the current rooms from the CSV file
    with open('rooms50.csv', 'r') as f:
        reader = csv.reader(f)
        
        rooms = list(reader)
    # Find the room with the given room_id
    found_room = False
    room_full = True

    for room in rooms:
        if room[0] == room_id:  # 检查房间ID是否匹配
            found_room = True
            for i in range(1, 51):  # 用户从第2列到第51列，总共50个位置
                if username in room[1:]:  # 从第2列到第51列检查用户名是否存在
                    print(f"User {username} already exists in the room.")
                    room_full = False
                    break
                else:
                    if room[i] == '':  # 如果找到一个空位
                        room[i] = username  # 将新用户添加到这个位置
                        room[i + 50] = 0
                        room[i + 50 + 50] = 1
                        room_full = False
                        break  # 成功添加用户后退出循环
            if room_full:
                raise ValueError("Room is full")
            else:
                # 成功添加用户，写入CSV文件
                with open('rooms50.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(rooms)
                break  # 找到房间并处理完毕，退出循环
                    
        
         
    if not found_room:
        raise ValueError("Room does not exist")


def get_50_room_info(room_id,username):
    # Read the current rooms from the CSV file
    with open('rooms50.csv', 'r') as f:
        reader = csv.reader(f)
        #next(reader)  # Skip the header row
        rooms = list(reader)

    # Find the room with the given room_id
    for room in rooms:
        #print("房间号")
        #print(room[0])
        #print(room[0])
        #print(type(room[0]))
        # if room[0].isdigit() and int(float(room[0])) == room_id:
        if room[0] == room_id:
            users = []  # 初始化用户列表
            # 遍历房间中的用户位置，假设用户名从索引1开始，每个用户只占用一个位置
            for i in range(1, 51):  # 假设有50个用户位置
                if room[i] == username:  # 如果当前位置有用户名
                    score_index = i + 50  # 找到对应分数的位置
                    is_stand_key = i + 50 + 50
                    # 将用户名和对应的分数（转换为整数）添加到用户列表
                    users.append({'username': room[i], 'score': int(float(room[score_index])),'is_stand':int(float(room[is_stand_key]))})
            # 返回房间信息，包括房间ID和用户列表
            return {
                'room_id': room_id,
                'users': users
            }

    # If the room does not exist, raise an error
    raise ValueError("Room does not exist")

def show_50_room_info(room_id):
    # Read the current rooms from the CSV file
    with open('rooms50.csv', 'r') as f:
        reader = csv.reader(f)
        #next(reader)  # Skip the header row
        rooms = list(reader)

    # Find the room with the given room_id
    for room in rooms:
        if room[0] == room_id:
            users = []  # 初始化用户列表
            # 遍历房间中的用户位置，假设用户名从索引1开始，每个用户只占用一个位置
            for i in range(1, 51):  # 假设有50个用户位置
                if room[i]:
                    score_index = i + 50  # 找到对应分数的位置
                    is_stand_key = i + 50 + 50
                    # 将用户名和对应的分数（转换为整数）添加到用户列表
                    users.append({'username': room[i], 'score': room[score_index],'is_stand':room[is_stand_key]})
                    #users.append({'username': room[i], 'score': int(float(room[score_index])),'is_stand':int(float(room[is_stand_key]))})
                # 返回房间信息，包括房间ID和用户列表
            return {
                'room_id': room_id,
                'users': users
            }

    # If the room does not exist, raise an error
    raise ValueError("Room does not exist")


def create_50_new_room(initial_user):
    # 读取现有的房间信息
    df = pd.read_csv('rooms50.csv')
    # 生成新的房间ID，这里简单地使用当前最大的room_id加1
    new_room_id = int(df['room_id'].max()) + 1
    # 新房间的用户数量初始为1
    #user_count = 1 
    # 将新房间信息添加到DataFrame
    new_row = pd.DataFrame({'room_id': str(new_room_id), 'user1': initial_user,'score1':0,'id1_is_stand': 1}, index=[0])
    # 使用 pandas.concat 来添加新行
    df = pd.concat([df, new_row], ignore_index=True)
    # 保存更新后的DataFrame回CSV文件
    df.to_csv('rooms50.csv', index=False)
    # 返回新房间的ID
    return new_room_id

def main():
    cookinit = stx.CookieManager()
    #Session.init(cookinit)
    #Session.save()
    if 'score' not in st.session_state:
        st.session_state['score'] = '0'
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = ''
    if 'password' not in st.session_state:
            st.session_state['password'] = ''
    if 'question_index' not in st.session_state:
        st.session_state['question_index'] = 0
    if 'answer' not in st.session_state:
        st.session_state['answer'] = None
    
    if 'in_room' not in st.session_state:
        st.session_state['in_room'] = False
    if 'room_score' not in st.session_state:
        st.session_state['room_score'] = 0
    if 'room_id' not in st.session_state:
        st.session_state['room_id'] = 0

    if '50_in_room' not in st.session_state:
        st.session_state['50_in_room'] = False
    if '50_room_score' not in st.session_state:
        st.session_state['50_room_score'] = 0
    if '50_room_id' not in st.session_state:
        st.session_state['50_room_id'] = 0
    if '50_room_is_stand' not in st.session_state:
        st.session_state['50_room_is_stand'] = 1
    if 'flag_answer' not in st.session_state:
        st.session_state['flag_answer'] = ''
    # 检查 'voice_triggered' 是否在 session_state 中，且为 True
    if 'voice_triggered' not in st.session_state:
        st.session_state['voice_triggered'] = True
    # 在代码的开始部分初始化计数器
    if 'n' not in st.session_state:
        st.session_state['n'] = 0  # 初始化问题计数器
    if 'is_win' not in st.session_state:
        st.session_state['is_win'] = 0  # 初始化是否出局，0代表继续，1代表赢，2代表出局
    if 'start' not in st.session_state:
        st.session_state['start'] = 0

    with st.sidebar:
        selected = option_menu("一站到底", ["登录","十万个为什么","基础问答",'两人PK擂台','50选1','一站到底','排行榜','查看答案'], 
            icons=['piggy-bank','house', 'gear', 'clipboard-data','people',"flag","list-task","arrow-up-right-circle"], menu_icon="cast", default_index=0,
            styles={
                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                    "icon": {"color": "orange", "font-size": "25px"}, 
                    "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "green"},
    })
        #selected

    if selected == "登录":
        st.session_state.page = '登录'
        #st.write("Welcome to Page 1")
        if not st.session_state['logged_in']:  # User is not logged in
            st.session_state['username'] = st.text_input('Username')
            st.session_state['password'] = st.text_input('Password', type='password')
            st.write("liyi,haha")

            col1, col2 = st.columns(2)
            with col1:
                if st.button('登录'):
                    try:
                        if st.session_state['username'] and st.session_state['password']:  # User has entered username and password
                            try:
                                st.session_state['score'] = int(get_score(st.session_state['username'], st.session_state['password']))
                                st.session_state['logged_in'] = True  # User is now logged in
                                st.rerun()  # Force a rerun of the script
                            except UserNotFoundError:
                                st.error("用户名不正确，请重试。")
                                st.session_state['logged_in'] = False  # Ensure user is not marked as logged in
                            except IncorrectPasswordError:
                                st.error("密码不正确，请重试。")
                                st.session_state['logged_in'] = False  # Ensure user is not marked as logged in
                    except ValueError as e:
                        st.write(str(e))  # Print the error message

            with col2:
                if st.button('注册'):
                    try:
                        if st.session_state['username'] and st.session_state['password']:
                            if user_exists(st.session_state['username']):
                                st.error("用户名已存在，请尝试其他用户名。")
                            else:
                                # 如果用户名不存在，则保存新用户的信息
                                register_user(st.session_state['username'], st.session_state['password'])  # 假设这个函数处理用户注册
                                st.success("注册成功，请登录。")
                                st.session_state['logged_in'] = False  # Optionally, you could log the user in directly
                    except ValueError as e:
                        st.error(f"注册失败：{str(e)}")
            df = pd.read_csv('scores.csv')
            st.title('登录信息表')
            # 使用 st.dataframe 展示 DataFrame 的内容
            df = df.drop('score', axis=1)
            st.dataframe(df)
            # if st.button('Submit', key='button'):
            #     try:
            #         if st.session_state['username'] and st.session_state['password']:  # User has entered username and password
            #             st.session_state['score'] = get_score(st.session_state['username'], st.session_state['password'])
            #             st.session_state['logged_in'] = True  # User is now logged in
            #             st.experimental_rerun()  # Force a rerun of the script
            #     except ValueError as e:
            #         st.write(str(e))  # Print the error message
        else:  # User is logged in
            st.write(f" Welcome back, {st.session_state['username']}! Your score is {st.session_state['score']}.")
            # 根据登录状态显示不同的内容
           
            # 登出按钮
            if st.button('Logout'):
                # 用户登出
                st.session_state['logged_in'] = False
                st.write("You have been logged out.")
                # 使用 JavaScript 删除 cookie
                #st.markdown('<script>document.cookie = "login_status=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";</script>', unsafe_allow_html=True)
                # if cookinit:
                #     try:
                #         cookinit.delete(Session.session_id)
                #     except KeyError as e:
                #         print(f"Cookie {e} not found, might have been already deleted or never set.")

    elif selected == "基础问答":
        st.session_state.page = '基础问答'
        if not st.session_state['logged_in']:  # User is not logged in
            st.write("请先去登录")
        else:
            # ... rest of your code ...
            #st.session_state['score'] = st.session_state['score'] + 1
            #answer = st.text_input('What is the capital of France?')
            # if st.button('Check answer'):
            #     if answer.lower() == 'paris':
            #         st.write('Correct!')
            #         st.session_state['score'] += 1  # Increase the score
            #         update_score(st.session_state['username'], st.session_state['score'], st.session_state['password'])  # Update the score in the database
            #     else:
            #         st.write('Incorrect. The correct answer is Paris.')

            # questions = [
            #     {
            #         "question": "Who is the president of USA?",
            #         "options": ['Donald Trump', 'Joe Biden', 'Barack Obama', 'George Bush'],
            #         "answer": 'Joe Biden'
            #     },
            #     {
            #         "question": "What is the capital of Australia?",
            #         "options": ['Sydney', 'Melbourne', 'Canberra', 'Perth'],
            #         "answer": 'Canberra'
            #     }
            # ]
            # 手动指定的Excel文件列表
            excel_files = [
                "动物板块.xlsx",
                "植物板块.xlsx",
                #"another_file.xlsx",
                #"sample_data.xlsx",
                #"report_data.xlsx",
                #"analysis_results.xlsx"
            ]

            # 创建下拉框让用户选择Excel文件
            selected_excel_file = st.selectbox("请选择分学科", excel_files)

            # 根据选择的Excel文件进行操作
            # 例如，读取并展示Excel文件的内容
            # 这里需要根据你的具体需求来实现
            st.write(f"你选择了文件：{selected_excel_file}")

            #excel_path = 'data_dict_columns.xlsx'  # Excel文件的路径
            excel_path = selected_excel_file
            sheet_name = 'Sheet1'  # Excel工作表名称
            df = pd.read_excel(excel_path, sheet_name=sheet_name, engine='openpyxl')

            # 提取第一列数据
            first_column = df.iloc[:, 0]  # iloc[:, 0]表示选择所有行的第一列

            # 将第一列数据转换为列表
            questions_list = first_column.tolist()
            #print(questions_list)
            # for i, q in enumerate(questions_list):
            #     print(f"Element {i}: {q}")
            for i, q in enumerate(questions_list):
                try:
                    # 尝试将字符串替换单引号为双引号后解析为JSON
                    parsed = json.loads(q.replace("'", '"'))
                except json.JSONDecodeError as e:
                    print(f"解析元素 {i} 时出错: {q}")
                    print(f"错误信息: {e}")
            question_dicts = [json.loads(q.replace("'", '"')) for q in questions_list]
            questions = question_dicts
            
            st.markdown(f'<h1 style="color: black">Score: {st.session_state["score"]}</h1>', unsafe_allow_html=True)
            # 在程序开始时调用此函数
            if 'answered_questions' not in st.session_state:
                st.session_state['answered_questions'] = get_answered_questions_from_excel(st.session_state['username'])
            #print(st.session_state['answered_questions'])
            if st.session_state['question_index'] < len(questions):
                question = questions[st.session_state['question_index']]
                # 在展示问题前，检查当前问题是否已回答
                if question['question'] in st.session_state['answered_questions']:
                    # 如果当前问题已回答，可以选择跳过或直接展示下一个问题
                    st.session_state['question_index'] += 1  # 跳到下一个问题
                    st.rerun()  # 重新运行应用以更新状态
                else:
                    st.write(question['question'])
                    options_list = [f"{key}: {value}" for key, value in question['options'].items()]
                    st.session_state['answer'] = st.radio("Options", options_list, key='select')
                    st.session_state['answer'] = st.session_state['answer'][0]  # 取第一个字符
                    #st.session_state['answer'] = st.radio("Options", question['options'], key='select')
                    if st.button('Submit', key='button'):
                        #st.session_state['submitted'] = True
                        #if st.session_state['submitted']:
                            if st.session_state['answer'] == question['answer']:
                                st.session_state['score'] += 1
                                update_score(st.session_state['username'], st.session_state['score'], st.session_state['password'])
                                st.write('Correct')
                            else:
                                st.write('Incorrect')
                            if st.session_state['question_index'] not in st.session_state['answered_questions']:
                                    st.session_state['answered_questions'].append(question['question'])
                                    save_answered_questions_to_excel(st.session_state['username'],st.session_state['answered_questions'])
                            st.session_state['question_index'] += 1
                            st.rerun()

                    else:
                        #st.session_state['submitted'] = False
                        #st.session_state['answer'] = None
                        st.write('请选择你的答案')
            #st.button('下一题')
            else:
                st.write("你真棒")
    elif selected == "十万个为什么":
        st.session_state.page = '经典书籍'
        #image = Image.open("cover.jpg")
        #st.image(image, caption="十万个为什么")
        st.image("cover.jpg", caption="十万个为什么封面图片",width=150)
        st.subheader("十万个为什么——第六版")
        file_paths = ['天文.xlsx', '植物.xlsx','动物.xlsx', '古生物.xlsx','生命.xlsx', '航天与航空.xlsx','海洋.xlsx']
        #selected_file_path = st.sidebar.file_uploader("请选择一个文件", type=['csv', 'xlsx'])
        #selected_file_path = st.sidebar.selectbox("请选择一个文件", file_paths)
        selected_file_path = st.selectbox("请选择一个文件", file_paths)
        erniebot.api_type = 'aistudio'
        erniebot.access_token = 'a2a30f75102adf4d00eaefe013e32ad4cb9e4857'
        speak_client_id = 'IAINmGmzxZ9SyNeqfXkB4jeE'
        speak_client_secret ='F3ArFlkOHyBStDqoDuK4chy984VQWIdX'

        def LLM(text):
            response = erniebot.ChatCompletion.create(
                model='ernie-3.5',
                messages=[{'role': 'user', 'content': "请将下面的文字进行改写，50个字左右"+text }],
            )
            return response.get_result()


        # # 存储选定的文件路径到 session_state
        # if selected_file_path is not None:
        #     st.session_state['selected_file_path'] = selected_file_path

        # 当用户选择一个文件时，加载该文件
        if selected_file_path:
            try:
                # 尝试使用 UTF-8 编码读取
                df = pd.read_excel(selected_file_path)
            except UnicodeDecodeError:
                # 如果 UTF-8 失败，尝试使用另一个编码
                df = pd.read_excel(selected_file_path, encoding='ISO-8859-1')
            # 将加载的DataFrame存储在session_state中，以便在页面上显示
            st.session_state['df'] = df

        # 如果 session_state 中有 DataFrame，展示 DataFrame 的前5条
        if 'df' in st.session_state and not st.session_state['df'].empty:
            #st.dataframe(st.session_state['df'].head(5))  # 只展示前5条记录
            
            # 直接指定问题列和答案列的字段名
            question_column = 'knowledge_title'
            answer_column = 'knowledge_comment'
        
            # 展示用户选择的问题和答案列
            # st.write("问题列:", question_column)
            # st.write("答案列:", answer_column)

            # 如果用户已经选择了问题列和答案列
            if question_column and answer_column:
                # 使用问题列的值作为下一个下拉框的选项
                selected_question = st.selectbox('请选择一个问题', st.session_state['df'][question_column].unique(), key='selected_question')

                # 找到选中问题对应的答案并展示
                if selected_question:
                    answer = st.session_state['df'][st.session_state['df'][question_column] == selected_question][answer_column].iloc[0]
                    

                    summarize_text = LLM(answer)

                    # 展示答案并进行总结
                    summary = summarize_text
                    st.write("总结是:", summary)

                    # text_to_speech = create_voise(summary,speak_client_id, speak_client_secret)
                    process_text(summary)

                    # 将总结转换为语音并获取URL
                    # audio_url = text_to_speech
                    # # 假设`st.audio`可以播放音频URL
                    # #st.audio(audio_url, format='audio/mp3', start_time=0)
                    # # 使用JavaScript在客户端自动播放音频
                    # audio_html = f"""
                    # <audio id="audio" src="{audio_url}" autoplay="autoplay"></audio>
                    # <script>
                    # document.getElementById("audio").play();
                    # </script>
                    # """

                    #st.markdown(audio_html, unsafe_allow_html=True)
                    st.write(answer)

    elif selected == "两人PK擂台":
        st.session_state.page = '两人PK擂台'
        #st.write("Welcome to Page 2")
        if not st.session_state['logged_in']:  # User is not logged in
            st.write("请先去登录")
        else:
            if not st.session_state['in_room']:  # User is logged in
                #print(st.session_state['logged_in'])
                #print(st.session_state['username'])
                st.session_state['room_id'] = st.text_input('Enter room ID to join a room')
                if st.button('Join room'):
                    try:
                        #room_id_str = int(st.session_state['room_id'])  # 假设这是从某处获取的房间号码字符串
                        #room_id = int(float(room_id_str))  # 先转换为浮点数，再转换为整数
                        room_info = get_room_info(st.session_state['room_id'])
                        #print(type(st.session_state['room_id']))
                        for user in room_info['users']:
                            if user['username'] == st.session_state['username']:
                                st.session_state['room_score'] = user['score']
                                st.write("You are already in this room")
                                break
                        else:
                            try:
                                join_room(st.session_state['room_id'], st.session_state['username'])
                                st.write("Now, You join in this room")
                            except ValueError as e:
                                st.write(str(e))
                                return
                        #st.rerun()
                    except ValueError as e:
                        st.write(str(e))
                        return
                    st.session_state['in_room'] = True
                    st.rerun()
                else:
                    #st.session_state.page = 'PK情况'
                    #st.write("Welcome to Page 4")
                    # 读取 CSV 文件
                    if st.button('creat room'):
                        new_room_id = create_new_room(st.session_state['username'])
                        st.success(f"Room created successfully with ID {new_room_id}.")

                    df = pd.read_csv('rooms.csv')
                    st.title('PK房间情况')
                    # 使用 st.dataframe 展示 DataFrame 的内容
                    st.dataframe(df)



            else:
                #if st.session_state['in_room']:
                    try:

                        # 创建两列布局，比例为7:3
                        left, right = st.columns([7, 3])


                        # 在右侧列中显示内容
                        with right:
                            room_info = get_room_info(st.session_state['room_id'])
                            st.write("Room id:",st.session_state['room_id'])
                            for user in room_info['users']:
                                
                                st.write(f"{user['username']}: {user['score']}")                    
                        
                        with left:
                            if 'room_question_index' not in st.session_state:
                                st.session_state['room_question_index'] = 0
                            if 'room_submitted' not in st.session_state:
                                st.session_state['room_submitted'] = False
                            if 'room_answer' not in st.session_state:
                                st.session_state['room_answer'] = None
                            #excel_path = 'data_dict_columns.xlsx'  # Excel文件的路径
                            excel_path = "植物板块.xlsx"
                            sheet_name = 'Sheet1'  # Excel工作表名称
                            df = pd.read_excel(excel_path, sheet_name=sheet_name, engine='openpyxl')

                            # 提取第一列数据
                            first_column = df.iloc[:, 1]  # iloc[:, 0]表示选择所有行的第一列

                            # 将第一列数据转换为列表
                            questions_list = first_column.tolist()
                            #print(questions_list)
                            # for i, q in enumerate(questions_list):
                            #     print(f"Element {i}: {q}")
                            for i, q in enumerate(questions_list):
                                try:
                                    # 尝试将字符串替换单引号为双引号后解析为JSON
                                    parsed = json.loads(q.replace("'", '"'))
                                except json.JSONDecodeError as e:
                                    print(f"解析元素 {i} 时出错: {q}")
                                    print(f"错误信息: {e}")
                            question_dicts = [json.loads(q.replace("'", '"')) for q in questions_list]
                            questions = question_dicts
                            # questions = [
                            #     {
                            #         "question": "Who is the president of USA?",
                            #         "options": ['Donald Trump', 'Joe Biden', 'Barack Obama', 'George Bush'],
                            #         "answer": 'Joe Biden'
                            #     },
                            #     {
                            #         "question": "What is the capital of Australia?",
                            #         "options": ['Sydney', 'Melbourne', 'Canberra', 'Perth'],
                            #         "answer": 'Canberra'
                            #     }
                            # ]

                            st.markdown(f'<h1 style="color: black">Score: {st.session_state["room_score"]}</h1>', unsafe_allow_html=True)
                            # 在程序开始时调用此函数
                            if 'answered_questions' not in st.session_state:
                                st.session_state['answered_questions'] = get_answered_questions_from_excel(st.session_state['username'])
                            #print(st.session_state['answered_questions'])
                            if st.session_state['room_question_index'] < len(questions):
                                question = questions[st.session_state['room_question_index']]
                                if question['question'] in st.session_state['answered_questions']:
                                    # 如果当前问题已回答，可以选择跳过或直接展示下一个问题
                                    st.session_state['room_question_index'] += 1  # 跳到下一个问题
                                    st.rerun()  # 重新运行应用以更新状态
                                else:
                                    st.write(question['question'])
                                    options_list = [f"{key}: {value}" for key, value in question['options'].items()]
                                    st.session_state['room_answer'] = st.radio("Options", options_list, key='select')
                                    st.session_state['room_answer'] = st.session_state['room_answer'][0]  # 取第一个字符
                                    #st.session_state['answer'] = st.radio("Options", question['options'], key='select')
                                    if st.button('Submit', key='button'):
                                        #st.session_state['submitted'] = True
                                        #if st.session_state['submitted']:
                                            if st.session_state['room_answer'] == question['answer']:
                                                st.session_state['room_score'] = int(st.session_state['room_score']) + 1
                                                update_room_score(st.session_state['room_id'], st.session_state['username'], st.session_state['room_score'])
                                                st.write('Correct')
                                            else:
                                                st.write('Incorrect')
                                            
                                            #if st.session_state['question_index'] not in st.session_state['answered_questions']:
                                            st.session_state['answered_questions'].append(question['question'])
                                            save_answered_questions_to_excel(st.session_state['username'],st.session_state['answered_questions'])
                                            st.session_state['question_index'] += 1
                                            st.rerun()
                                    else:
                                        #st.session_state['submitted'] = False
                                        #st.session_state['answer'] = None
                                        st.write('请选择你的答案')
                            #st.button('下一题')
                            else:
                                st.write("你真棒")
                        #st.markdown(f'<h1 style="color: black">Score: {st.session_state["score"]}</h1>', unsafe_allow_html=True)




                    except ValueError as e:
                        st.write(str(e))
                        return
                        


    elif selected == "50选1":
        st.session_state.page = '50选1'
        #st.write("Welcome to Page 3")
        if not st.session_state['logged_in']:  # User is not logged in
            st.write("请先去登录")
        else:
            if not st.session_state['50_in_room']:  # User is logged in
                #print(st.session_state['logged_in'])
                #print(st.session_state['username'])
                st.session_state['50_room_id'] = st.text_input('Enter room ID to join a room')
                if st.button('Join room'):
                    try:
                        #room_id_str = int(st.session_state['room_id'])  # 假设这是从某处获取的房间号码字符串
                        #room_id = int(float(room_id_str))  # 先转换为浮点数，再转换为整数
                        room_info = get_50_room_info(st.session_state['50_room_id'],st.session_state['username'])
                        #print(type(st.session_state['room_id']))
                        for user in room_info['users']:
                            if user['username'] == st.session_state['username']:
                                st.session_state['50_room_score'] = user['score']
                                st.write("You are already in this room")
                                break
                        else:
                            try:
                                join_50_room(st.session_state['50_room_id'], st.session_state['username'])
                                st.write("Now, You join in this room")
                            except ValueError as e:
                                st.write(str(e))
                                return
                        #st.rerun()
                    except ValueError as e:
                        st.write(str(e))
                        return
                    st.session_state['50_in_room'] = True
                    st.rerun()
                else:
                    #st.session_state.page = 'PK情况'
                    #st.write("Welcome to Page 4")
                    # 读取 CSV 文件
                    if st.button('creat room'):
                        new_room_id = create_50_new_room(st.session_state['username'])
                        st.success(f"Room created successfully with ID {new_room_id}.")

                    df = pd.read_csv('rooms50.csv')
                    st.title('一站到底1/50房间情况')
                    # 使用 st.dataframe 展示 DataFrame 的内容
                    st.dataframe(df)



            else:
                #if st.session_state['in_room']:
                    try:
                        # 创建两列布局，比例为7:3
                        left, right = st.columns([7, 3])
                        # 在右侧列中显示内容
                        with right:
                            st.write("Room id:",st.session_state['50_room_id'])
                            #print('开始')
                            show_info = show_50_room_info(st.session_state['50_room_id'])
                            #print(show_info)
                            #st.write("Room id:",st.session_state['room_id'])
                            for user in show_info['users']:
                                is_stand = int(float(user['is_stand']))
                                st.write(f"{user['username']}是否站立:{is_stand}") 

                        with left:
                            room_info = get_50_room_info(st.session_state['50_room_id'],st.session_state['username'])
                            for user in room_info['users']:        
                                st.session_state['50_room_is_stand'] = user['is_stand']
                            if st.session_state['50_room_is_stand'] == 1:
                                if '50_room_question_index' not in st.session_state:
                                    st.session_state['50_room_question_index'] = 0
                                if '50_room_submitted' not in st.session_state:
                                    st.session_state['50_room_submitted'] = False
                                if '50_room_answer' not in st.session_state:
                                    st.session_state['50_room_answer'] = None
                                #excel_path = 'data_dict_columns.xlsx'  # Excel文件的路径
                                excel_path = "动物板块.xlsx"
                                sheet_name = 'Sheet1'  # Excel工作表名称
                                df = pd.read_excel(excel_path, sheet_name=sheet_name, engine='openpyxl')

                                # 提取第一列数据
                                first_column = df.iloc[:, 1]  # iloc[:, 0]表示选择所有行的第一列

                                # 将第一列数据转换为列表
                                questions_list = first_column.tolist()
                                #print(questions_list)
                                # for i, q in enumerate(questions_list):
                                #     print(f"Element {i}: {q}")
                                for i, q in enumerate(questions_list):
                                    try:
                                        # 尝试将字符串替换单引号为双引号后解析为JSON
                                        parsed = json.loads(q.replace("'", '"'))
                                    except json.JSONDecodeError as e:
                                        print(f"解析元素 {i} 时出错: {q}")
                                        print(f"错误信息: {e}")
                                question_dicts = [json.loads(q.replace("'", '"')) for q in questions_list]
                                questions = question_dicts
                                # questions = [
                                #     {
                                #         "question": "Who is the president of USA?",
                                #         "options": ['Donald Trump', 'Joe Biden', 'Barack Obama', 'George Bush'],
                                #         "answer": 'Joe Biden'
                                #     },
                                #     {
                                #         "question": "What is the capital of Australia?",
                                #         "options": ['Sydney', 'Melbourne', 'Canberra', 'Perth'],
                                #         "answer": 'Canberra'
                                #     }
                                # ]

                                st.markdown(f'<h1 style="color: black">Score: {st.session_state["50_room_score"]}</h1>', unsafe_allow_html=True)
                                # 在程序开始时调用此函数
                                if 'answered_questions' not in st.session_state:
                                    st.session_state['answered_questions'] = get_answered_questions_from_excel(st.session_state['username'])
                                #print(st.session_state['answered_questions'])
                                if st.session_state['50_room_question_index'] < len(questions):
                                    question = questions[st.session_state['50_room_question_index']]
                                    if question['question'] in st.session_state['answered_questions']:
                                        # 如果当前问题已回答，可以选择跳过或直接展示下一个问题
                                        st.session_state['50_room_question_index'] += 1  # 跳到下一个问题
                                        st.rerun()  # 重新运行应用以更新状态
                                    else:
                                        st.write(question['question'])
                                        options_list = [f"{key}: {value}" for key, value in question['options'].items()]
                                        st.session_state['50_room_answer'] = st.radio("Options", options_list, key='select')
                                        st.session_state['50_room_answer'] = st.session_state['50_room_answer'][0]  # 取第一个字符
                                        #st.session_state['answer'] = st.radio("Options", question['options'], key='select')
                                        if st.button('Submit', key='button'):
                                            #st.session_state['submitted'] = True
                                            #if st.session_state['submitted']:
                                                if st.session_state['50_room_answer'] == question['answer']:
                                                    st.session_state['50_room_score'] = int(st.session_state['50_room_score']) + 1
                                                    st.session_state['50_room_is_stand'] = 1
                                                    update_50_score(st.session_state['50_room_id'], st.session_state['username'], st.session_state['50_room_score'],st.session_state['50_room_is_stand'])
                                                    st.write('Correct')
                                                else:
                                                    st.session_state['50_room_is_stand'] = 0
                                                    update_50_score(st.session_state['50_room_id'], st.session_state['username'], st.session_state['50_room_score'],st.session_state['50_room_is_stand'])
                                                    st.write('Incorrect')
                                                
                                                #if st.session_state['question_index'] not in st.session_state['answered_questions']:
                                                st.session_state['answered_questions'].append(question['question'])
                                                save_answered_questions_to_excel(st.session_state['username'],st.session_state['answered_questions'])
                                                st.session_state['50_room_question_index'] += 1
                                                st.rerun()
                                        else:
                                            #st.session_state['submitted'] = False
                                            #st.session_state['answer'] = None
                                            st.write('请选择你的答案')
                                #st.button('下一题')
                                else:
                                    st.write("你真棒")
                            #st.markdown(f'<h1 style="color: black">Score: {st.session_state["score"]}</h1>', unsafe_allow_html=True)
                            else:
                                st.write('不好意思，因为你答错了提，你已躺下\n 请返回，选择其他房间比赛')
                                if st.button('返回房间', key='button'):
                                    st.session_state['50_in_room'] = False
                                    st.rerun()


                    except ValueError as e:
                        st.write(str(e))
                        return



    elif selected == "一站到底":
        st.session_state.page = '一站到底'
        if not st.session_state['logged_in']:  # User is not logged in
            st.write("请先去登录")
        else:
            is_win_value = get_is_win_value(st.session_state['username'])
            if is_win_value is not None:
                print(f"{st.session_state['username']}的is_win值为: {is_win_value}")
                st.session_state['is_win'] = is_win_value
            else:
                print(f"未找到用户名为{st.session_state['username']}的记录。")
                #st.session_state['is_win'] = 0
            st.markdown("""
                <div style="text-align: center;">
                    <h4>一站到底</h4>
                </div>
                        """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1,2,1])  # 调整比例以更好地居中

            # 在中间列显示图像
            with col2:
                #st.image("path/to/your/image.png")  # 替换为您的图像路径
                st.image("standing.png", caption="",width=350)
            
            if st.session_state['start'] == 1:
                if st.session_state['is_win'] == 2:
                    st.write("离成功已经很近了，建议再玩一次")
                    if st.button('再来一次'):
                        st.session_state['is_win'] = 0
                        add_winner_to_csv(st.session_state['username'],st.session_state['is_win'])
                        st.session_state['n'] = 0
                        st.rerun()
                    else:
                        pass
                elif st.session_state['is_win'] == 1:
                    st.write("你赢的了一站到底英雄的头衔")
                else:
                    if st.session_state['n'] < 10:
                        question_and_answer = get_question(st.session_state['n'])
                        question = question_and_answer["question"]
                        answer = question_and_answer["answer"]      
                        print(question)
                        st.markdown(f"""
                            <div style="text-align: center;">
                                <p>{question}</p>
                                <h4>语音答题请点击</h4>
                            </div>
                        """, unsafe_allow_html=True)

                        if st.session_state['voice_triggered']:
                            process_text(question)
                        #answer = "苹果的创办者是乔布斯" 
                        st.session_state['voice_triggered'] = False
                        # if not st.session_state['voice_triggered']:
                        #     # 这里放置触发语音输出的代码
                        #     # 例如：process_text("谁创办了苹果")
                        #     # 注意：确保这是触发语音输出的正确方式，这里仅为示例
                        #     #process_text("谁创办了苹果")
                        #     process_text(question)
                        #     # 假设这行代码触发了语音输出
                        #     # 更新 session_state 标志，表示语音已被触发
                        #     st.session_state['voice_triggered'] = True
                        # #process_text("谁创办了苹果")
                        # #answer = "苹果的创办者是乔布斯和沃伦"

                        # 使用 Streamlit 的 columns 方法创建三列
                        col1, col2, col3 = st.columns([2,1,2])  # 调整比例以更好地居中

                        # 在中间列添加 audiorecorder 组件
                        with col2:
                            audio = audiorecorder("点此开始答题", "点此结束答题")
                        if len(audio) > 0:
                            # To play audio in frontend:
                            st.audio(audio.export().read())
                            voice_answer = STT(audio)
                            st.write(voice_answer)
                            st.session_state['flag_answer'] = voice_answer


                        if input := st.chat_input("你也可以输入答案"):
                            st.session_state['flag_answer'] = input
                            print(st.session_state['flag_answer'])
                            print(answer)
                            #matches = difflib.get_close_matches(st.session_state['answer'], answer, n=1, cutoff=0.6)
                            matches = is_right(st.session_state['flag_answer'],answer)
                            if matches == '1':
                                st.write("答对了")
                                process_text("哦，答对了，加油哦，下一题")
                                st.session_state['voice_triggered'] = True
                                st.session_state['n'] += 1  # 答对了，计数器加1
                                if st.session_state['n'] >= 10:
                                    st.session_state['is_win'] = 1
                                    add_winner_to_csv(st.session_state['username'],st.session_state['is_win'])
                                st.rerun()
                            else:
                                st.write("出局")
                                process_text("哦，失败了，就差一点点了")
                                st.session_state['is_win'] = 2
                                add_winner_to_csv(st.session_state['username'],st.session_state['is_win'])
                                st.rerun()

                        if st.button('提交答案'):
                            print(st.session_state['flag_answer'])
                            print(answer)
                            matches = is_right(st.session_state['flag_answer'],answer)
                            if matches == '1':
                                st.write("答对了")
                                process_text("哦，答对了，加油哦，下一题")
                                st.session_state['voice_triggered'] = True
                                st.session_state['n'] += 1  # 答对了，计数器加1
                                if st.session_state['n'] >= 10:
                                    st.session_state['is_win'] = 1
                                    add_winner_to_csv(st.session_state['username'],st.session_state['is_win'])
                                st.rerun()
                            else:
                                st.write("出局")
                                process_text("哦，失败了，就差一点点了")
                                st.session_state['is_win'] = 2
                                add_winner_to_csv(st.session_state['username'],st.session_state['is_win'])
                                st.rerun()
                
            else:
                if st.button("开始吧"):
                    st.session_state['start'] = 1
                    st.rerun()
                else:
                    st.markdown("""
                        <div style="text-align: center;">
                            <p>我们将会持续给出10道题目，如果能全部答对，你将获得冠军头衔，准备好了吗？</p>
                        </div>
                    """, unsafe_allow_html=True)



    elif selected == "排行榜":
        st.session_state.page = '排行榜'
        #st.write("Welcome to Page 4")
        # 读取 CSV 文件
        df = pd.read_csv('scores.csv')
        # 删除 password 字段
        df = df.drop('Password', axis=1)
        # 根据分数降序排序并重置索引，不保留原索引
        df_sorted = df.sort_values(by='score', ascending=False).reset_index(drop=True)

        # 将 DataFrame 转换为 HTML，不显示索引
        html = df_sorted.to_html(index=False)

        # 显示排行榜，不显示索引
        st.subheader('基础问答排行榜')
        st.markdown(html, unsafe_allow_html=True)



        
        #print(st.session_state['score'])
    
    elif selected == "查看答案":
        st.session_state.page = '查看答案'
        if not st.session_state['logged_in']:  # User is not logged in
            st.write("请先去登录")
        else:
            if "messages" not in st.session_state:
                st.session_state["messages"] = []
                #st.session_state["messages"] = [{"role": "user", "content": "hello"}]
                #st.session_state["messages"].append({"role": "assistant", "content": "How can I help you?"})
            #st.write("搭建中")
            st.subheader("💬 十万个为什么·答疑小助手")
            st.caption("🚀 A 请将你的问题告诉我吧")

            # 调用函数获取下拉框的选项
            options = get_answered_questions_from_excel(st.session_state['username'])
            # 创建一个新的选项列表，首项为提示文本
            options_with_prompt = ["请选择..."] + options
            # 创建下拉框
            selected_option = st.selectbox("请查看你挑战过的题目：", options_with_prompt,index=0)
            
            # 检查用户是否选择了一个非提示选项
            if selected_option != "请选择...":
                st.session_state.messages.append({"role": "user", "content": selected_option})
                #st.chat_message("user").write(selected_option)
                response = llm(st.session_state.messages)
                #msg = response.choices[0].message.content
                msg = response.get_result()
                st.session_state.messages.append({"role": "assistant", "content": msg})
                #st.chat_message("assistant").write(msg)
                # 显示用户选择的选项
                #st.write(f"您选择的是：{selected_option}")
            else:
                st.write("")
            for msg in st.session_state.messages:
                    st.chat_message(msg["role"]).write(msg["content"])
            if prompt := st.chat_input():
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.chat_message("user").write(prompt)
                #response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
                response = llm(st.session_state.messages)
                #msg = response.choices[0].message.content
                msg = response.get_result()
                st.session_state.messages.append({"role": "assistant", "content": msg})
                st.chat_message("assistant").write(msg)
            else:
                st.write("")
            
def llm(Messages):
    erniebot.api_type = 'aistudio'
    erniebot.access_token = 'a2a30f75102adf4d00eaefe013e32ad4cb9e4857'
    response = erniebot.ChatCompletion.create(
                    model='ernie-3.5',
                    messages = Messages,
                    #messages=[{'role': 'user', 'content': "你好呀，和我打个招呼吧"}],
                    
                    system="你是一个《十万个为什么》书籍智能助手，你可以基于《十万个为什么》回答用户的问题，请用通俗易懂的语言，类似对8岁小朋友沟通的语气，回答问题",
                )
    return response


if __name__ == '__main__':
    main()