import os # 引入 Python 标准库中的 os 模块，用于读取系统变量，如环境变量中的 API_KEY

from langchain.prompts import ChatPromptTemplate # 从 langchain 中导入 ChatPromptTemplate 模块，用于构建提示词模板
from langchain_openai import ChatOpenAI # 从 langchain_openai 模块中导入 ChatOpenAI，用于接入 OpenAI 或 DeepSeek 等 Chat API 模型
from langchain_community.utilities import WikipediaAPIWrapper # 从 langchain_community 中导入 WikipediaAPIWrapper，用于搜索维基百科内容

def generate_script(subject, video_length, creativity, api_key):
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "请为'{subject}'这个主题的视频想一个吸引人的标题")
        ]
    )
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human", """你是一位短视频频道博主，根据以下的标题和相关信息，为短视频频道生成标题：{title}, 视频时长：{duration}分钟，生成的脚本的长度
            尽可能遵循视频时长的要求。要求尽可能抓住眼球，中间提供干活内容，结尾有惊喜，脚本格式也请按照【开头，中间，结尾】分割。整体内同的表达形成要轻松有趣，
            吸引年轻人。脚本内容可以结合以下维基百科搜索出的信息，但仅仅作为从参考，只结合相关的即可，对不对成的进行忽略：
            ···{wikipedia_search}```""")
        ]
    )
    model = ChatOpenAI(
        model="deepseek-chat",
        openai_api_key= api_key,
        base_url="https://api.deepseek.com",
        temperature=creativity
    )

    title_chain = title_template | model
    script_chain = script_template | model

    title = title_chain.invoke({"subject": subject}).content

    search = WikipediaAPIWrapper(lang="zh")
    search_result = search.run(subject)

    script = script_chain.invoke({"title": title, "duration": video_length, "wikipedia_search": search_result}).content

    return  search_result, title, script





