from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secret_key_for_session"

# 1. 데이터 설정 (실제 팀원 이름과 주제로 변경하세요)
TEAM_MEMBERS = ["김건동", "지혜민", "박진희", "이찬혜", "강신석"]
TOPICS = {
    "김건동": "교통약자(장애인, 유모차) 무장애 경로 안내 시스템",
    "지혜민": "실시간 대기질 기반 스마트 환기 가이드 및 에너지 효율 분석 시스템",
    "박진희": "공공도서관 대출 데이터 기반 수요 예측 및 AI 대기기간 안내 시스템",
    "이찬혜": "공동주택별 분리수거 대행 서비스 수익성 및 환경 비용 시뮬레이션 플랫폼",
    "강신석": "한국인들이 많이 가는 비수도권 관광지를 외국인에게 추천해주는 서비스"
}

# 투표 결과 저장 (누가, 어떤 주제에, 몇 점을 줬는지)
# 구조: { "투표자": { "주제명": 점수, ... } }
votes = {}

@app.route('/')
def index():
    return render_template('index.html', members=TEAM_MEMBERS)

@app.route('/vote/<voter_name>', methods=['GET', 'POST'])
def vote(voter_name):
    # 유효한 팀원인지 확인
    if voter_name not in TEAM_MEMBERS:
        flash(f"오류: '{voter_name}'은(는) 등록된 팀원이 아닙니다.")
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # 폼에서 데이터 가져오기
        selected_scores = {}
        assigned_scores = []

        for topic_owner, topic_name in TOPICS.items():
            score = request.form.get(topic_name)
            if score and score != "0":
                score_int = int(score)
                selected_scores[topic_name] = score_int
                assigned_scores.append(score_int)
        
        # 검증 로직: 1, 3, 5점이 중복 없이 선택되었는지 확인
        required_scores = [1, 3, 5]
        if sorted(assigned_scores) != required_scores:
            flash("오류: 반드시 1점, 3점, 5점을 각각 한 번씩 사용해야 합니다!")
            return redirect(url_for('vote', voter_name=voter_name))

        # 투표 저장
        votes[voter_name] = selected_scores
        flash(f"{voter_name}님, 투표가 성공적으로 완료되었습니다!")
        return redirect(url_for('results'))

    # 본인 주제 제외하고 렌더링
    available_topics = {owner: name for owner, name in TOPICS.items() if owner != voter_name}
    
    # 본인 주제가 없는 경우 (TOPICS에 본인 이름이 key로 없는 경우) 처리
    if len(available_topics) == len(TOPICS):
        flash(f"경고: {voter_name}님은 발제한 주제가 없습니다. 모든 주제에 투표 가능합니다.")
    
    # 투표 가능한 주제가 3개 미만인 경우
    if len(available_topics) < 3:
        flash(f"오류: 투표 가능한 주제가 {len(available_topics)}개뿐입니다. 최소 3개가 필요합니다.")
        return redirect(url_for('index'))
    
    return render_template('vote.html', voter=voter_name, topics=available_topics)

@app.route('/results')
def results():
    # 점수 합산 로직
    total_scores = {name: 0 for name in TOPICS.values()}
    for voter, choices in votes.items():
        for topic, score in choices.items():
            total_scores[topic] += score
    
    # 내림차순 정렬
    sorted_results = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)
    return render_template('results.html', results=sorted_results, detailed_votes=votes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)