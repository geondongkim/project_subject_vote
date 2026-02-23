# 프로젝트 주제 투표 시스템

팀 프로젝트 주제에 대해 팀원들이 투표하는 웹 애플리케이션입니다.

## 기능

- ✅ 사용자 식별: 팀원 이름으로 로그인
- ✅ 본인 제외: 본인이 발제한 주제는 투표 대상에서 제외
- ✅ 점수 검증: 1점, 3점, 5점을 각각 한 번씩 배분하도록 강제
- ✅ 실시간 검증: JavaScript로 클라이언트 측 검증
- ✅ 결과 조회: 점수 순위 및 상세 투표 내역 확인

## 설치 및 실행

### 필수 요구사항
- Python 3.8 이상
- pip

### 설치
```bash
# 1. 저장소 클론
git clone https://github.com/your-username/project_subject_vote.git
cd project_subject_vote

# 2. 가상환경 생성
python3 -m venv .venv
# python -3.11 -m venv .venv

# 3. 가상환경 활성화
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. 의존성 설치
pip install -r requirements.txt