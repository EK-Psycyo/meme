# OpenAI Streamlit 챗봇

`gpt-4o-mini`를 사용하는 간단한 한국어 챗봇입니다.

## Streamlit Community Cloud 배포

1. 이 폴더를 GitHub 저장소에 올립니다.
2. Streamlit Community Cloud에서 저장소와 `app.py`를 연결합니다.
3. 앱 설정의 **Secrets**에 아래 내용을 추가합니다.

```toml
OPENAI_API_KEY = "sk-..."
```

4. `requirements.txt`를 기준으로 의존성이 설치되면 앱을 실행합니다.

API 키는 소스 코드에 작성하지 말고 Secrets에만 저장하세요.

## 로컬 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

로컬에서는 `.streamlit/secrets.toml` 파일을 만들고 같은 형식으로 키를 넣을 수 있습니다. 이 파일은 `.gitignore`에 포함되어 있습니다.
