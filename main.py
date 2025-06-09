import streamlit as st
from utils import generate_script

st.set_page_config(page_title="AI短视频脚本生成器", page_icon="📹")

st.title("📹 AI短视频脚本生成器")
st.markdown("输入一个主题，AI 将自动为你生成 **吸引人的标题 + 视频脚本**！")

# 输入栏
subject = st.text_input("🎯 视频主题", placeholder="例如：Sora、低碳建筑、元宇宙等")
video_length = st.slider("⏱️ 视频时长（分钟）", 1, 5, 1)
creativity = st.slider("🎨 创造力（temperature）", 0.1, 1.5, 0.7)
with st.sidebar:
    api_key = st.text_input("🔐 请输入API 密钥", type="password")
    st.markdown("[获取Deepseek API密钥](https://api.deepseek.com)")
submit = st.button("生成视频脚本")

# 按钮触发
if submit:
    if not api_key:
        st.error("请填写 API 密钥")
    elif not subject:
        st.error("请输入视频主题")
    else:
        with st.spinner("正在生成中，请稍候..."):
            wiki, title, script = generate_script(subject, video_length, creativity, api_key)
        st.success("生成完成！")

        st.subheader("🎬视频标题")
        st.write(title)
        st.subheader("📝视频脚本")
        st.write(script)
        with st.expander("📖 维基百科内容参考"):
                 st.write(wiki)
