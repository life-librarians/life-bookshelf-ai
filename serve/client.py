import requests


def stream_autobiography(url, data):
    with requests.post(url, json=data, stream=True) as response:
        # 서버가 정상적으로 응답했는지 확인
        response.raise_for_status()

        # 스트리밍된 데이터를 한 줄씩 읽어들이기
        for line in response.iter_lines():
            if line:
                # 스트리밍된 한 줄의 텍스트를 출력
                print(line.decode("utf-8"))


# 서버에 요청을 보낼 URL
url = "http://localhost:3000/api/v1/autobiographies/generate"

# 요청에 필요한 데이터
data = {
    "user_info": {
        "name": "최시원",
        "date_of_birth": "2000-02-21",
        "gender": "FEMALE",
        "occupation": "프로그래머",
        "education_level": "대학교 재학",
        "marital_status": "미혼",
    },
    "chapter_info": {"title": "20대", "description": "대학 생활과 첫 직장 경험"},
    "sub_chapter_info": {
        "title": "첫 직장 생활",
        "description": "소프트웨어 회사에서의 첫 직장 경험과 적응 과정",
    },
    "interviews": [
        {
            "content": "회사에서 맡은 첫 프로젝트는 무엇이었고, 어떤 도전이 있었나요?",
            "conversationType": "BOT",
        },
        {
            "content": "제가 맡은 첫 프로젝트는 온라인 쇼핑몰 구축 프로젝트였습니다. 처음으로 프로젝트를 맡아서 설계부터 개발까지 전반적인 업무를 담당했는데, 기존에 경험이 부족했기 때문에 많은 어려움을 겪었습니다. 특히, 프로젝트 일정이 타이트했기 때문에 개발 과정에서 많은 야근을 했었죠.",
            "conversationType": "HUMAN",
        },
    ],
}

# 스트리밍 요청 실행
stream_autobiography(url, data)
