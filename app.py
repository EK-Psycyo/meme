import streamlit as st
from openai import OpenAI


MODEL = "gpt-4o-mini"
SYSTEM_PROMPT = "당신은 친절하고 정확한 한국어 AI 도우미입니다. 필요한 경우 단계별로 설명하세요."


st.set_page_config(
    page_title="OpenAI 챗봇",
    page_icon="💬",
    layout="centered",
)

st.title("💬 OpenAI 챗봇")
st.caption(f"Powered by {MODEL}")


def get_client() -> OpenAI | None:
    """Streamlit Community Cloud Secrets에서 API 키를 읽어 OpenAI 클라이언트를 생성합니다."""
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except (KeyError, FileNotFoundError):
        st.error(
            "OpenAI API 키가 설정되지 않았습니다. "
            "Streamlit Cloud의 App settings > Secrets에 OPENAI_API_KEY를 추가하세요."
        )
        return None

    return OpenAI(api_key=api_key)


if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("설정")
    st.write("모델")
    st.code(MODEL)
    if st.button("대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("API 키는 Streamlit Secrets에서만 읽습니다.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("메시지를 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    client = get_client()
    if client is not None:
        with st.chat_message("assistant"):
            try:
                request_messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *st.session_state.messages,
                ]
                stream = client.chat.completions.create(
                    model=MODEL,
                    messages=request_messages,
                    stream=True,
                )
                answer = st.write_stream(
                    chunk.choices[0].delta.content or ""
                    for chunk in stream
                )
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
            except Exception as exc:
                st.error(f"응답을 가져오는 중 오류가 발생했습니다: {exc}")
