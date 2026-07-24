import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="숫자 맞추기 게임",
    page_icon="🎯",
    layout="centered"
)

# 커스텀 CSS로 UI 스타일링
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1E88E5;
        font-weight: 700;
    }
    .welcome-card {
        background-color: #F0F2F6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if "target_number" not in st.session_state:
    st.session_state.target_number = random.randint(1, 100)
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "history" not in st.session_state:
    st.session_state.history = []
if "best_score" not in st.session_state:
    st.session_state.best_score = None
if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = None

def reset_game():
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.history = []
    st.session_state.last_feedback = None

# 헤더 및 웰컴 메시지
st.title("🎯 1부터 100 사이 숫자 맞추기 게임")

st.markdown("""
<div class="welcome-card">
    <h4>👋 환영합니다!</h4>
    <p>1부터 100 사이의 숫자를 맞혀보세요.<br>
    목표는 <b>최대한 적은 횟수</b>로 정답을 성공하는 것입니다!</p>
</div>
""", unsafe_allow_html=True)

# 메트릭 카드 (현재 시도 횟수 & 최고 기록)
col1, col2 = st.columns(2)
with col1:
    st.metric(label="현재 시도 횟수", value=f"{st.session_state.attempts} 회")
with col2:
    best_str = f"{st.session_state.best_score} 회" if st.session_state.best_score is not None else "기록 없음"
    st.metric(label="🏆 최고 기록 (최소 시도)", value=best_str)

st.divider()

# 게임 실행 / 입력 폼
if not st.session_state.game_over:
    with st.form(key="guess_form", clear_on_submit=True):
        guess = st.number_input(
            "숫자를 입력하세요 (1~100)",
            min_value=1,
            max_value=100,
            value=50,
            step=1
        )
        submit_button = st.form_submit_button(label="제출 🚀", use_container_width=True)

    if submit_button:
        st.session_state.attempts += 1
        target = st.session_state.target_number

        if guess < target:
            st.session_state.history.append((st.session_state.attempts, guess, "📈 UP"))
            st.session_state.last_feedback = ("warning", f"**{guess}** 은(는) 정답보다 작은 숫자입니다! **UP! 📈**")
        elif guess > target:
            st.session_state.history.append((st.session_state.attempts, guess, "📉 DOWN"))
            st.session_state.last_feedback = ("info", f"**{guess}** 은(는) 정답보다 큰 숫자입니다! **DOWN! 📉**")
        else:
            st.session_state.game_over = True
            st.session_state.history.append((st.session_state.attempts, guess, "🎉 정답"))
            
            # 최고 기록 갱신 확인
            if st.session_state.best_score is None or st.session_state.attempts < st.session_state.best_score:
                st.session_state.best_score = st.session_state.attempts
                st.session_state.last_feedback = ("success", f"🎉 **정답입니다! ({guess})**\n\n🏆 **축하합니다! 신기록 달성!** (총 시도: **{st.session_state.attempts}회**)")
            else:
                st.session_state.last_feedback = ("success", f"🎉 **정답입니다! ({guess})**\n\n총 시도 횟수: **{st.session_state.attempts}회**")
            st.balloons()
        st.rerun()

# 피드백 출력 (UP/DOWN/정답)
if st.session_state.last_feedback:
    msg_type, msg_text = st.session_state.last_feedback
    if msg_type == "warning":
        st.warning(msg_text)
    elif msg_type == "info":
        st.info(msg_text)
    elif msg_type == "success":
        st.success(msg_text)

# 게임 끝났을 때 다시 시도 또는 종료 안내
if st.session_state.game_over:
    st.markdown("---")
    st.subheader("🔄 게임을 다시 시작하시겠습니까?")
    col_reset, col_space = st.columns([1, 1])
    with col_reset:
        if st.button("🎮 다시 시도하기", type="primary", use_container_width=True):
            reset_game()
            st.rerun()

# 옵션: 중간 게임 리셋
if not st.session_state.game_over and st.session_state.attempts > 0:
    with st.expander("⚙️ 게임 다시 시작"):
        if st.button("새 게임으로 포기하고 리셋"):
            reset_game()
            st.rerun()

# 시도 기록 (히스토리)
if st.session_state.history:
    st.divider()
    st.subheader("📜 시도 기록")
    for attempts_cnt, h_guess, result in reversed(st.session_state.history):
        st.write(f"• **{attempts_cnt}회차 시도**: `{h_guess}` ➔ {result}")
