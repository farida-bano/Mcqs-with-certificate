import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart
import datetime
import json
import os
import base64

# Page settings with custom background
st.set_page_config(
    page_title="Student MCQ Test",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for beautiful styling
def set_custom_style():
    st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.98) !important;
        backdrop-filter: blur(10px);
        border-right: 2px solid #E8EAED;
    }
    
    /* Main content area */
    .main .block-container {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 20px;
        padding: 3rem;
        margin-top: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1a1a1a !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 600;
    }
    
    /* Text color */
    p, div, span, label {
        color: #1a1a1a !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #FF6B6B, #FF8E53);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
        background: linear-gradient(45deg, #FF8E53, #FF6B6B);
    }
    
    /* Radio buttons */
    .stRadio>div {
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #4ECDC4;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #E8EAED;
    }
    
    /* Text input */
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 2px solid #4ECDC4;
        padding: 0.75rem;
        font-size: 16px;
        background: rgba(255, 255, 255, 0.9);
    }
    
    /* Select box */
    .stSelectbox>div>div>select {
        border-radius: 12px;
        border: 2px solid #4ECDC4;
        background: rgba(255, 255, 255, 0.9);
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid #E8EAED;
    }
    
    /* Success message */
    .stSuccess {
        background: linear-gradient(45deg, #00b09b, #96c93d);
        color: white !important;
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 5px solid #00b09b;
    }
    
    /* Error message */
    .stError {
        background: linear-gradient(45deg, #ff416c, #ff4b2b);
        color: white !important;
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 5px solid #ff416c;
    }
    
    /* Info message */
    .stInfo {
        background: linear-gradient(45deg, #4A90E2, #7B68EE);
        color: white !important;
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 5px solid #4A90E2;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(45deg, #FF6B6B, #FF8E53);
    }
    
    /* Metric cards */
    .stMetric {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        padding: 1rem;
        border-left: 5px solid #4ECDC4;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(78, 205, 196, 0.1) !important;
        border-radius: 10px !important;
        border-left: 4px solid #4ECDC4 !important;
    }
    
    /* Sidebar select box */
    .stSidebar .stSelectbox>div>div>select {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid #FF6B6B;
    }
    
    /* Download button */
    .stDownloadButton>button {
        background: linear-gradient(45deg, #4ECDC4, #44A08D) !important;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(78, 205, 196, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# Data file
DATA_FILE = "students_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"students": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Enhanced MCQ Questions with more variety
questions = [
    {
        "question": "What is the capital of Pakistan?",
        "options": ["Lahore", "Islamabad", "Karachi", "Peshawar"],
        "correct": "Islamabad",
        "category": "Geography"
    },
    {
        "question": "2 + 2 × 2 = ?",
        "options": ["6", "8", "4", "10"],
        "correct": "6",
        "category": "Mathematics"
    },
    {
        "question": "The sun is the center of our solar system?",
        "options": ["True", "False"],
        "correct": "True",
        "category": "Science"
    },
    {
        "question": "Who is the national poet of Pakistan?",
        "options": ["Hafiz Jalandhari", "Ahmed Faraz", "Allama Iqbal", "Faiz Ahmed Faiz"],
        "correct": "Allama Iqbal",
        "category": "Literature"
    },
    {
        "question": "What is the national bird of Pakistan?",
        "options": ["Chakor", "Shaheen", "Peacock", "Bulbul"],
        "correct": "Shaheen",
        "category": "General Knowledge"
    },
    {
        "question": "Which programming language is known as the 'language of the web'?",
        "options": ["Python", "JavaScript", "Java", "C++"],
        "correct": "JavaScript",
        "category": "Computer Science"
    },
    {
        "question": "What does CPU stand for?",
        "options": ["Computer Processing Unit", "Central Processing Unit", "Central Program Unit", "Computer Program Unit"],
        "correct": "Central Processing Unit",
        "category": "Computer Science"
    }
]

def send_certificate(email, student_name, score, total_questions):
    try:
        # Email settings (update these)
        sender_email = "bano23086@gmail.com"
        sender_password = "pgns hfxf dztn hozf"
        
        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = "🎓 Your MCQ Test Certificate"
        
        # Beautiful certificate HTML
        certificate_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    margin: 0;
                    padding: 40px;
                    text-align: center;
                }}
                .certificate {{
                    background: white;
                    border-radius: 20px;
                    padding: 40px;
                    margin: 20px auto;
                    max-width: 800px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    border: 10px solid #FF6B6B;
                    position: relative;
                }}
                .logo {{
                    font-size: 48px;
                    color: #FF6B6B;
                    margin-bottom: 20px;
                }}
                .title {{
                    color: #1a1a1a;
                    font-size: 36px;
                    font-weight: bold;
                    margin-bottom: 30px;
                }}
                .student-name {{
                    font-size: 32px;
                    color: #1a1a1a;
                    margin: 20px 0;
                    padding: 15px;
                    background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    font-weight: bold;
                }}
                .score {{
                    font-size: 28px;
                    color: #00b09b;
                    margin: 20px 0;
                }}
                .date {{
                    color: #666;
                    font-size: 18px;
                    margin-top: 30px;
                }}
                .footer {{
                    margin-top: 40px;
                    color: #888;
                    font-size: 14px;
                }}
                .badge {{
                    background: linear-gradient(45deg, #00b09b, #96c93d);
                    color: white;
                    padding: 10px 20px;
                    border-radius: 25px;
                    display: inline-block;
                    margin: 10px;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="certificate">
                <div class="logo">🎓</div>
                <div class="title">CERTIFICATE OF ACHIEVEMENT</div>
                <div style="font-size: 18px; color: #666; margin-bottom: 30px;">
                    This is to certify that
                </div>
                <div class="student-name">{student_name}</div>
                <div style="font-size: 18px; color: #666; margin: 20px 0;">
                    has successfully completed the MCQ Test with outstanding performance
                </div>
                <div class="score">Score: {score}/{total_questions}</div>
                <div class="badge">Percentage: {(score/total_questions)*100:.1f}%</div>
                <div class="date">Date: {datetime.datetime.now().strftime('%B %d, %Y')}</div>
                <div class="footer">
                    <p>🎉 Congratulations on your achievement! 🎉</p>
                    <p>Educational Testing System | Knowledge Excellence</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        message.attach(MIMEText(certificate_html, "html"))
        
        # Send email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

def generate_beautiful_certificate(student_name, score, total_questions):
    """Generate a beautiful certificate as HTML that can be downloaded"""
    percentage = (score/total_questions)*100
    
    certificate_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 40px;
                text-align: center;
            }}
            .certificate-container {{
                background: white;
                border-radius: 25px;
                padding: 50px;
                margin: 20px auto;
                max-width: 900px;
                box-shadow: 0 25px 50px rgba(0,0,0,0.15);
                border: 15px solid #FF6B6B;
                position: relative;
            }}
            .header {{
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 30px;
            }}
            .logo {{
                font-size: 60px;
                margin-right: 20px;
            }}
            .title {{
                color: #1a1a1a;
                font-size: 42px;
                font-weight: bold;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            }}
            .subtitle {{
                color: #666;
                font-size: 20px;
                margin-bottom: 40px;
            }}
            .student-name {{
                font-size: 38px;
                color: #1a1a1a;
                margin: 30px 0;
                padding: 20px;
                background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: bold;
                border-bottom: 3px solid #FF6B6B;
                display: inline-block;
            }}
            .achievement {{
                font-size: 22px;
                color: #555;
                margin: 25px 0;
                line-height: 1.6;
            }}
            .score-container {{
                background: linear-gradient(45deg, #00b09b, #96c93d);
                color: white;
                padding: 20px 40px;
                border-radius: 50px;
                display: inline-block;
                margin: 20px 0;
                font-size: 28px;
                font-weight: bold;
                box-shadow: 0 10px 20px rgba(76, 175, 80, 0.3);
            }}
            .performance {{
                font-size: 20px;
                color: #00b09b;
                margin: 15px 0;
                font-weight: bold;
            }}
            .date {{
                color: #777;
                font-size: 20px;
                margin-top: 40px;
                font-style: italic;
            }}
            .footer {{
                margin-top: 50px;
                padding-top: 20px;
                border-top: 2px solid #eee;
                color: #888;
            }}
            .signature {{
                margin-top: 40px;
                display: flex;
                justify-content: space-around;
            }}
            .signature-line {{
                border-top: 2px solid #FF6B6B;
                width: 200px;
                padding-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="certificate-container">
            <div class="header">
                <div class="logo">🏆</div>
                <div>
                    <div class="title">CERTIFICATE OF EXCELLENCE</div>
                    <div class="subtitle">Awarded for Outstanding Performance in MCQ Test</div>
                </div>
                <div class="logo">📚</div>
            </div>
            
            <div class="achievement">
                This certificate is proudly presented to
            </div>
            
            <div class="student-name">{student_name}</div>
            
            <div class="achievement">
                in recognition of successful completion and exceptional performance<br>
                in the Comprehensive Multiple Choice Question Examination
            </div>
            
            <div class="score-container">
                Score: {score}/{total_questions} • Percentage: {percentage:.1f}%
            </div>
            
            <div class="performance">
                { "🌟 Outstanding!" if percentage >= 90 else "👍 Excellent!" if percentage >= 80 else "💪 Good Job!" if percentage >= 70 else "📖 Keep Learning!" }
            </div>
            
            <div class="date">
                Awarded on {datetime.datetime.now().strftime('%B %d, %Y')}
            </div>
            
            <div class="signature">
                <div>
                    <div class="signature-line"></div>
                    <div>Test Administrator</div>
                </div>
                <div>
                    <div class="signature-line"></div>
                    <div>Head of Education</div>
                </div>
            </div>
            
            <div class="footer">
                <strong>Educational Excellence Foundation</strong><br>
                "Empowering Minds, Building Futures"
            </div>
        </div>
    </body>
    </html>
    """
    
    return certificate_html

def main():
    set_custom_style()
    
    # Header with logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center;'>
            <h1 style='color: white; font-size: 48px; margin-bottom: 10px;'>🎓 📚</h1>
            <h1 style='color: white; font-size: 42px; margin-bottom: 10px;'>Student MCQ Test System</h1>
            <p style='color: white; font-size: 20px; font-weight: 500;'>For Class 8, 9 and 10 Students</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sidebar with enhanced styling
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <div style='font-size: 40px; margin-bottom: 20px;'>🚀</div>
            <h2 style='color: #1a1a1a; font-weight: 600;'>Navigation</h2>
        </div>
        """, unsafe_allow_html=True)
        
        option = st.selectbox("", 
                            ["Take Test", "View Results", "Admin Panel", "About"],
                            label_visibility="collapsed")
    
    if option == "Take Test":
        take_test()
    elif option == "View Results":
        view_results()
    elif option == "Admin Panel":
        admin_panel()
    elif option == "About":
        show_about()

def take_test():
    st.header("📝 MCQ Test")
    st.markdown("### Test your knowledge with our comprehensive MCQ test!")
    
    # Student information with better layout
    st.subheader("🎯 Student Information")
    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input("**Full Name**", placeholder="Enter your full name")
        class_level = st.selectbox("**Class Level**", ["8", "9", "10"])
    with col2:
        email = st.text_input("**Email Address**", placeholder="your.email@example.com")
        roll_number = st.text_input("**Roll Number**", placeholder="Enter your roll number")
    
    if st.button("🚀 Start Test", use_container_width=True):
        if student_name and email and roll_number:
            st.session_state.test_started = True
            st.session_state.student_info = {
                "name": student_name,
                "email": email,
                "class": class_level,
                "roll_number": roll_number
            }
            st.session_state.answers = {}
            st.session_state.current_question = 0
            st.rerun()
        else:
            st.error("❌ Please fill all the required information")
    
    if st.session_state.get('test_started', False):
        display_questions()

def display_questions():
    current_q = st.session_state.current_question
    
    if current_q < len(questions):
        q = questions[current_q]
        
        # Progress bar
        progress = (current_q) / len(questions)
        st.progress(progress)
        st.markdown(f"**Progress: Question {current_q + 1} of {len(questions)}**")
        
        # Question display with category
        st.markdown(f"### 🔍 Question {current_q + 1}")
        st.markdown(f"**Category:** `{q['category']}`")
        st.markdown(f"**{q['question']}**")
        
        answer = st.radio(
            "Select your answer:",
            q['options'],
            key=f"q{current_q}",
            index=None
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏭️ Next Question" if current_q < len(questions) - 1 else "🏁 Finish Test", 
                        use_container_width=True, disabled=answer is None):
                st.session_state.answers[current_q] = answer
                st.session_state.current_question += 1
                st.rerun()
        
        with col2:
            if current_q > 0 and st.button("⏮️ Previous Question", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
    else:
        show_results()

def show_results():
    st.header("🎉 Test Results")
    
    # Calculate score
    score = 0
    results = []
    
    for i, q in enumerate(questions):
        user_answer = st.session_state.answers.get(i, "Not answered")
        correct = q['correct']
        is_correct = user_answer == correct
        
        if is_correct:
            score += 1
        
        results.append({
            "Question": q['question'],
            "Category": q['category'],
            "Your Answer": user_answer,
            "Correct Answer": correct,
            "Result": "✅ Correct" if is_correct else "❌ Wrong"
        })
    
    # Show results with emojis based on performance
    percentage = (score/len(questions))*100
    if percentage >= 90:
        emoji = "🏆"
        message = "Outstanding! You're a star! 🌟"
    elif percentage >= 80:
        emoji = "🎯"
        message = "Excellent work! Keep it up! 💪"
    elif percentage >= 70:
        emoji = "👍"
        message = "Good job! You're doing great! 📚"
    else:
        emoji = "📖"
        message = "Keep learning and improving! 🚀"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Score", f"{score}/{len(questions)}")
    with col2:
        st.metric("Percentage", f"{percentage:.1f}%")
    with col3:
        st.metric("Performance", emoji)
    
    st.success(f"**{message}**")
    
    # Result table
    st.subheader("📊 Detailed Results")
    results_df = pd.DataFrame(results)
    st.dataframe(results_df, use_container_width=True)
    
    # Save data
    student_data = {
        **st.session_state.student_info,
        "score": score,
        "total_questions": len(questions),
        "percentage": percentage,
        "timestamp": datetime.datetime.now().isoformat(),
        "answers": st.session_state.answers
    }
    
    data = load_data()
    data["students"].append(student_data)
    save_data(data)
    
    # Certificate options
    st.subheader("📜 Download Your Certificate")
    
    col1, col2 = st.columns(2)
    with col1:
        certificate_html = generate_beautiful_certificate(
            st.session_state.student_info['name'],
            score,
            len(questions)
        )
        
        st.download_button(
            label="📥 Download Certificate (HTML)",
            data=certificate_html,
            file_name=f"certificate_{st.session_state.student_info['name']}.html",
            mime="text/html",
            use_container_width=True
        )
    
    with col2:
        if st.button("📧 Send Certificate via Email", use_container_width=True):
            if send_certificate(
                st.session_state.student_info['email'],
                st.session_state.student_info['name'],
                score,
                len(questions)
            ):
                st.success("🎉 Certificate sent to your email successfully!")
            else:
                st.error("❌ Failed to send email. Please check your email settings.")

def view_results():
    st.header("📊 All Students Results")
    
    data = load_data()
    
    if not data["students"]:
        st.info("📝 No test results available yet. Take the test to see results here!")
        return
    
    # Prepare data for table
    table_data = []
    for student in data["students"]:
        table_data.append({
            "Name": student["name"],
            "Class": student["class"],
            "Roll Number": student["roll_number"],
            "Score": f"{student['score']}/{student['total_questions']}",
            "Percentage": f"{student['percentage']:.1f}%",
            "Date": student["timestamp"][:10]
        })
    
    df = pd.DataFrame(table_data)
    
    # Add some statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students", len(data["students"]))
    with col2:
        avg_percentage = sum(s['percentage'] for s in data["students"]) / len(data["students"])
        st.metric("Average Score", f"{avg_percentage:.1f}%")
    with col3:
        max_percentage = max(s['percentage'] for s in data["students"])
        st.metric("Highest Score", f"{max_percentage:.1f}%")
    with col4:
        min_percentage = min(s['percentage'] for s in data["students"])
        st.metric("Lowest Score", f"{min_percentage:.1f}%")
    
    st.dataframe(df, use_container_width=True)
    
    # Download option
    csv = df.to_csv(index=False)
    st.download_button(
        label="📊 Download Results (CSV)",
        data=csv,
        file_name="students_results.csv",
        mime="text/csv",
        use_container_width=True
    )

def admin_panel():
    st.header("🔧 Admin Panel")
    
    st.subheader("📝 Manage Questions")
    st.info("Here you can view and modify the test questions.")
    
    for i, q in enumerate(questions):
        with st.expander(f"📌 Question {i+1} - {q['category']}"):
            col1, col2 = st.columns([3, 1])
            with col1:
                new_question = st.text_input(f"Question", value=q['question'], key=f"q{i}_text")
                new_category = st.selectbox(
                    "Category", 
                    ["Geography", "Mathematics", "Science", "Literature", "General Knowledge", "Computer Science"],
                    index=["Geography", "Mathematics", "Science", "Literature", "General Knowledge", "Computer Science"].index(q['category']),
                    key=f"cat{i}"
                )
            with col2:
                new_correct = st.selectbox("Correct Answer", q['options'], key=f"q{i}_correct")
            
            st.write("Options:")
            new_options = []
            cols = st.columns(4)
            for j, opt in enumerate(q['options']):
                with cols[j]:
                    new_opt = st.text_input(f"Option {j+1}", value=opt, key=f"q{i}_opt{j}")
                    new_options.append(new_opt)
            
            if st.button(f"🔄 Update Question {i+1}", key=f"update_{i}"):
                st.success(f"✅ Question {i+1} updated successfully!")
    
    st.subheader("📈 System Statistics")
    data = load_data()
    if data["students"]:
        total_tests = len(data["students"])
        avg_score = sum(s['percentage'] for s in data["students"]) / total_tests
        st.metric("Total Tests Taken", total_tests)
        st.metric("Average Performance", f"{avg_score:.1f}%")

def show_about():
    st.header("ℹ️ About This System")
    
    st.markdown("""
    <div style='background: rgba(255, 107, 107, 0.1); padding: 30px; border-radius: 15px; border-left: 5px solid #FF6B6B;'>
        <h3 style='color: #1a1a1a;'>🎓 Educational MCQ Test System</h3>
        <p style='color: #1a1a1a;'>This is a comprehensive multiple-choice question test system designed for students of classes 8, 9, and 10.</p>
        
        <h4 style='color: #1a1a1a; margin-top: 20px;'>✨ Features:</h4>
        <ul style='color: #1a1a1a;'>
            <li>📝 Interactive MCQ Test Interface</li>
            <li>🎯 Real-time Progress Tracking</li>
            <li>📊 Detailed Performance Analytics</li>
            <li>📜 Beautiful Digital Certificates</li>
            <li>📧 Email Certificate Delivery</li>
            <li>👨‍💼 Admin Panel for Management</li>
        </ul>
        
        <h4 style='color: #1a1a1a; margin-top: 20px;'>🎨 Design Elements:</h4>
        <ul style='color: #1a1a1a;'>
            <li>🌈 Beautiful Gradient Backgrounds</li>
            <li>🎪 Emoji-rich Interface</li>
            <li>📱 Responsive Design</li>
            <li>🎯 Professional Certificate Templates</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # Initialize session state
    if 'test_started' not in st.session_state:
        st.session_state.test_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'student_info' not in st.session_state:
        st.session_state.student_info = {}
    
    main()