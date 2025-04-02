import streamlit as st
import pandas as pd
import random

# -----------------------------
# Generate Sample Employee Data
# -----------------------------
def generate_employee_data():
    names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Skylar"]
    data = []
    for name in names:
        weekly_steps = [random.randint(4000, 12000) for _ in range(7)]
        data.append({
            "Employee": name,
            "Steps": sum(weekly_steps),
            "Calories Burned": random.randint(1500, 3000),
            "Hours Exercised": round(random.uniform(0.5, 2.5), 1),
            "Water Intake (oz)": random.randint(40, 100),
            "Sleep (hrs)": round(random.uniform(5, 8.5), 1),
            "Wellness Score": random.randint(60, 100),
            "Weekly Steps": weekly_steps,
        })
    return pd.DataFrame(data)

df = generate_employee_data()

# -----------------------------
# Streamlit Layout
# -----------------------------
st.set_page_config("Corporate Fitness Dashboard", layout="wide")
st.sidebar.title("🏃‍♂️ Dashboard Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Employee Details", "Leaderboard", "Tips & Motivation"])

# -----------------------------
# Overview Page
# -----------------------------
if page == "Overview":
    st.title("🏢 Corporate Fitness & Wellness Overview")

    st.subheader("📊 Company-wide Averages")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Steps", f"{int(df['Steps'].mean()):,}")
    col2.metric("Avg Calories Burned", f"{int(df['Calories Burned'].mean())} kcal")
    col3.metric("Avg Sleep", f"{df['Sleep (hrs)'].mean():.1f} hrs")
    col4.metric("Avg Wellness Score", f"{df['Wellness Score'].mean():.0f}/100")

    st.subheader("📈 Wellness Trend")
    st.line_chart(df.set_index("Employee")[["Wellness Score"]])

    with st.expander("📋 Raw Data Table"):
        st.dataframe(df)

# -----------------------------
# Employee Details Page
# -----------------------------
elif page == "Employee Details":
    st.title("🧑‍💼 Employee Wellness Details")
    selected_employee = st.selectbox("Select Employee", df["Employee"])
    emp_data = df[df["Employee"] == selected_employee].iloc[0]

    st.subheader(f"📌 {selected_employee}'s Stats")
    st.write(f"**Steps This Week:** {emp_data['Steps']:,}")
    st.progress(min(emp_data['Steps'] / 70000, 1.0))  # 70k steps = goal

    st.write(f"**Calories Burned:** {emp_data['Calories Burned']} kcal")
    st.write(f"**Water Intake:** {emp_data['Water Intake (oz)']} oz")
    st.write(f"**Hours Exercised:** {emp_data['Hours Exercised']} hrs")
    st.write(f"**Sleep:** {emp_data['Sleep (hrs)']} hrs")
    st.write(f"**Wellness Score:** {emp_data['Wellness Score']}/100")
    st.progress(emp_data['Wellness Score'] / 100)

    st.subheader("📅 Daily Step Count")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    step_data = pd.DataFrame({
        "Day": days,
        "Steps": emp_data["Weekly Steps"]
    }).set_index("Day")
    st.bar_chart(step_data)

# -----------------------------
# Leaderboard Page
# -----------------------------
elif page == "Leaderboard":
    st.title("🏆 Wellness Leaderboard")

    top_steps = df.sort_values("Steps", ascending=False)[["Employee", "Steps"]].reset_index(drop=True)
    top_score = df.sort_values("Wellness Score", ascending=False)[["Employee", "Wellness Score"]].reset_index(drop=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🥇 Top by Steps")
        st.dataframe(top_steps.style.highlight_max(axis=0), use_container_width=True)
    with col2:
        st.subheader("🧘 Top by Wellness Score")
        st.dataframe(top_score.style.highlight_max(axis=0), use_container_width=True)

# -----------------------------
# Tips Page
# -----------------------------
elif page == "Tips & Motivation":
    st.title("💡 Wellness Tips & Daily Motivation")

    tips = [
        "💧 Drink a glass of water every hour.",
        "🚶 Take short walking breaks throughout your workday.",
        "🧘 Practice deep breathing for 5 minutes to reduce stress.",
        "🍎 Choose a healthy snack today—fruit, nuts, or yogurt.",
        "💤 Try to get 7–8 hours of sleep tonight.",
        "📅 Schedule your workout like a meeting.",
        "📈 Small progress is still progress—keep going!"
    ]

    st.subheader("✨ Today's Tip:")
    st.info(random.choice(tips))

    st.subheader("🌟 Motivational Quote")
    st.success("“The only bad workout is the one that didn’t happen.”")

# Footer
st.markdown("---")
st.caption("💻 Powered by Streamlit | Corporate Wellness Dashboard v1.1")
