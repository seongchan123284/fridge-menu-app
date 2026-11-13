냉장고 파먹기 - 한국어 버전

[실행 방법]
1. 이 폴더에서 PowerShell을 엽니다.
2. 아래 명령어를 순서대로 실행합니다.

python -m pip install -r requirements.txt
python -m streamlit run app.py

3. 브라우저에서 http://localhost:8501 에 접속합니다.

[포함 기능]
- 식재료 등록 및 삭제
- 수량 및 유통기한 관리
- 유통기한 임박 재료 표시
- 보유 식재료 기반 메뉴 추천
- 상세 조리법 및 단계별 조리 안내

[주의]
이 프로젝트는 기존 프로젝트와 별도 폴더에서 실행하세요.
기존 프로젝트의 app.py 및 fridge_data.json은 수정하거나 삭제하지 않습니다.
새 프로젝트의 데이터는 이 폴더 안에 별도로 저장됩니다.
