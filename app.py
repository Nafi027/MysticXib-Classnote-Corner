import streamlit as st
import os
import pickle
from datetime import datetime
import pandas as pd
import base64
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="MysticXib Classnote Corner",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for elegant styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main {
        padding: 0rem 1rem;
        background-color: #f5f7fa;
    }
    
    /* Custom header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Card styles */
    .custom-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Button styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Download button special style */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fb;
        padding: 2rem 1rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: white;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 2rem;
        background-color: transparent;
        border-radius: 10px;
        color: #666;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f8f9fb;
        border-radius: 10px;
        padding: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #e9ecef;
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 10px;
        padding: 1rem 1.5rem;
        border: none;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    /* File uploader */
    .uploadedFile {
        background-color: #f8f9fb;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 2px dashed #e0e0e0;
    }
    
    /* Custom animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Rotation button styles */
    .rotation-controls {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    
    .rotation-btn {
        background: #667eea;
        color: white;
        border: none;
        padding: 0.3rem 0.8rem;
        border-radius: 5px;
        cursor: pointer;
        font-size: 0.9rem;
    }
    
    .rotation-btn:hover {
        background: #764ba2;
    }
</style>
""", unsafe_allow_html=True)

# File paths for data persistence
DATA_FILE = "lectures_data.pkl"
USERS_FILE = "users_data.pkl"

# Subjects with emojis
SUBJECTS_WITH_ICONS = {
    "Solid State Devices": "💻",
    "Power Plant Engineering": "⚡",
    "Compound Semiconductor & Hetero Junction Devices": "🔬",
    "VLSI Design & Testing": "🖥️",
    "VLSI Design & Testing Lab": "🔧",
    "RF & Microwave Engineering": "📡",
    "RF & Microwave Engineering Lab": "📻",
    "Project/Thesis (Initial)": "📝",
    "Industrial Training": "🏭"
}

SUBJECTS = list(SUBJECTS_WITH_ICONS.keys())

# Initialize data structures if not exists
if not os.path.exists(DATA_FILE):
    lectures_data = []
    with open(DATA_FILE, "wb") as f:
        pickle.dump(lectures_data, f)

if not os.path.exists(USERS_FILE):
    users_data = {"eee20": "eee20"}  # Admin credentials
    with open(USERS_FILE, "wb") as f:
        pickle.dump(users_data, f)

# Helper functions
def load_data():
    with open(DATA_FILE, "rb") as f:
        return pickle.load(f)

def save_data(data):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(data, f)

def check_login(username, password):
    with open(USERS_FILE, "rb") as f:
        users = pickle.load(f)
    return username in users and users[username] == password

def file_to_base64(file):
    return base64.b64encode(file.getvalue()).decode()

def base64_to_image(base64_string):
    """Convert base64 string to PIL Image"""
    img_data = base64.b64decode(base64_string)
    img = Image.open(io.BytesIO(img_data))
    return img

def rotate_image(img, degrees):
    """Rotate PIL image by specified degrees"""
    return img.rotate(-degrees, expand=True)

def image_to_base64(img):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def create_metric_card(label, value, icon):
    return f"""
    <div class="metric-card">
        <div style="font-size: 2rem;">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if "rotation_states" not in st.session_state:
    st.session_state.rotation_states = {}

if "batch_lectures" not in st.session_state:
    st.session_state.batch_lectures = []

# Sidebar
with st.sidebar:
    st.markdown("## 🎓 **MysticXib Portal**")
    st.markdown("---")
    
    if not st.session_state.logged_in:
        st.markdown("### 🔐 **Admin Access**")
        st.markdown("Please login to manage content")
        
        with st.form("login_form", clear_on_submit=True):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("🚀 Login", use_container_width=True)
            with col2:
                st.form_submit_button("❓ Help", use_container_width=True)
            
            if submit:
                if check_login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("✅ Welcome back!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
    else:
        # User info card
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 1rem; border-radius: 10px; text-align: center;">
            <h3>👋 Welcome!</h3>
            <p style="margin: 0;">Logged in as <strong>{st.session_state.username}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick stats
        lectures = load_data()
        st.markdown("### 📊 Quick Statistics")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📚 Total Lectures", len(lectures))
        with col2:
            total_reads = sum(lec.get('reads', 0) for lec in lectures)
            st.metric("👀 Total Views", total_reads)
        
        # Recent activity
        st.markdown("### 🕒 Recent Activity")
        if lectures:
            recent = sorted(lectures, key=lambda x: x['date'], reverse=True)[:3]
            for lec in recent:
                st.markdown(f"• **{lec['title'][:30]}...**")
                st.caption(f"  {lec['date'].strftime('%d %b %Y')}")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
    
    # Footer info
    st.markdown("---")
    st.markdown("### ℹ️ **About**")
    st.info("📚 **Classnote Corner** v2.0\n\nA modern platform for sharing and accessing lecture notes efficiently.")
    st.caption("Made with ❤️ by MysticXib")

# Main content area
st.markdown("""
<div class="main-header fade-in">
    <h1>📚 MysticXib Classnote Corner</h1>
    <p>Your digital library for academic excellence</p>
</div>
""", unsafe_allow_html=True)

# Create tabs based on login status
if st.session_state.logged_in:
    tab1, tab2, tab3 = st.tabs(["📖 **Browse Notes**", "➕ **Admin Panel**", "📊 **Analytics**"])
else:
    tab1 = st.tabs(["📖 **Browse Notes**"])[0]

# Tab 1: Browse Notes
with tab1:
    # Search and filter section
    st.markdown("### 🔍 Find Your Notes")
    
    with st.container():
        col1, col2, col3, col4 = st.columns([3, 3, 2, 2])
        
        with col1:
            search_query = st.text_input(
                "Search", 
                placeholder="🔎 Search by title, description...",
                label_visibility="collapsed"
            )
        
        with col2:
            selected_subject = st.selectbox(
                "Subject",
                ["📚 All Subjects"] + [f"{SUBJECTS_WITH_ICONS[s]} {s}" for s in SUBJECTS],
                label_visibility="collapsed"
            )
        
        with col3:
            tag_search = st.text_input(
                "Tags",
                placeholder="🏷️ Filter by tags...",
                label_visibility="collapsed"
            )
        
        with col4:
            sort_by = st.selectbox(
                "Sort",
                ["🕒 Newest First", "📅 Oldest First", "🔥 Most Popular"],
                label_visibility="collapsed"
            )
    
    # Load and filter lectures
    all_lectures = load_data()
    filtered_lectures = all_lectures.copy()
    
    # Apply subject filter
    if selected_subject != "📚 All Subjects":
        subject_name = selected_subject.split(" ", 1)[1]  # Remove emoji
        filtered_lectures = [lec for lec in filtered_lectures if lec["subject"] == subject_name]
    
    # Apply search filter
    if search_query:
        filtered_lectures = [
            lec for lec in filtered_lectures 
            if search_query.lower() in lec["title"].lower() or 
               search_query.lower() in lec.get("description", "").lower()
        ]
    
    # Apply tag filter
    if tag_search:
        filtered_lectures = [
            lec for lec in filtered_lectures 
            if any(tag_search.lower() in tag.lower() for tag in lec.get("tags", []))
        ]
    
    # Apply sorting
    if "Newest" in sort_by:
        filtered_lectures.sort(key=lambda x: x["date"], reverse=True)
    elif "Oldest" in sort_by:
        filtered_lectures.sort(key=lambda x: x["date"])
    else:  # Most Popular
        filtered_lectures.sort(key=lambda x: x.get("reads", 0), reverse=True)
    
    # Display results summary
    st.markdown(f"### 📑 Found {len(filtered_lectures)} Lecture Notes")
    
    # Display lectures in a grid
    if filtered_lectures:
        for idx, lecture in enumerate(filtered_lectures):
            with st.container():
                # Create custom card
                st.markdown('<div class="custom-card fade-in">', unsafe_allow_html=True)
                
                # Header row
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    icon = SUBJECTS_WITH_ICONS.get(lecture["subject"], "📄")
                    st.markdown(f"### {icon} {lecture['title']}")
                    
                    # Metadata row
                    meta_cols = st.columns(4)
                    with meta_cols[0]:
                        st.caption(f"📚 {lecture['subject']}")
                    with meta_cols[1]:
                        st.caption(f"📝 Lecture {lecture['lecture_no']}")
                    with meta_cols[2]:
                        st.caption(f"📅 {lecture['date'].strftime('%d %b %Y')}")
                    with meta_cols[3]:
                        st.caption(f"👀 {lecture.get('reads', 0)} views")
                
                with col2:
                    # View count badge
                    st.markdown(f"""
                    <div style="text-align: center; padding: 0.5rem; 
                                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                                color: white; border-radius: 10px;">
                        <strong>{lecture.get('reads', 0)}</strong><br>
                        <small>Views</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Description
                if lecture.get("description"):
                    st.markdown(f"**Description:** {lecture['description']}")
                
                # Tags
                if lecture.get("tags"):
                    tag_html = " ".join([f'<span style="background: #e9ecef; padding: 0.2rem 0.6rem; border-radius: 15px; margin: 0.2rem; display: inline-block; font-size: 0.8rem;">#{tag}</span>' for tag in lecture["tags"]])
                    st.markdown(f"<div style='margin: 0.5rem 0;'>{tag_html}</div>", unsafe_allow_html=True)
                
                # Expandable content
                with st.expander("📂 View Files & Comments"):
                    # Files section
                    st.markdown("#### 📎 Attached Files")
                    
                    if lecture.get("files"):
                        file_cols = st.columns(3)
                        col_idx = 0
                        
                        for file_data in lecture["files"]:
                            with file_cols[col_idx % 3]:
                                if file_data["type"] == "pdf":
                                    pdf_bytes = base64.b64decode(file_data["content"])
                                    st.download_button(
                                        label=f"📄 {file_data['name']}",
                                        data=pdf_bytes,
                                        file_name=file_data['name'],
                                        mime="application/pdf",
                                        key=f"pdf_{lecture['id']}_{file_data['name']}"
                                    )
                                else:
                                    # Image with rotation
                                    img_key = f"{lecture['id']}_{file_data['name']}"
                                    
                                    # Initialize rotation state if not exists
                                    if img_key not in st.session_state.rotation_states:
                                        st.session_state.rotation_states[img_key] = 0
                                    
                                    # Get current rotation
                                    current_rotation = st.session_state.rotation_states[img_key]
                                    
                                    # Load and rotate image
                                    img = base64_to_image(file_data["content"])
                                    if current_rotation != 0:
                                        img = rotate_image(img, current_rotation)
                                    
                                    # Display image
                                    st.image(img, caption=f"🖼️ {file_data['name']}", use_column_width=True)
                                    
                                    # Rotation controls
                                    rot_col1, rot_col2, rot_col3 = st.columns(3)
                                    with rot_col1:
                                        if st.button("↶ 90°", key=f"rot_left_{img_key}"):
                                            st.session_state.rotation_states[img_key] = (current_rotation - 90) % 360
                                            st.rerun()
                                    with rot_col2:
                                        if st.button("↻ 90°", key=f"rot_right_{img_key}"):
                                            st.session_state.rotation_states[img_key] = (current_rotation + 90) % 360
                                            st.rerun()
                                    with rot_col3:
                                        if st.button("⟲ Reset", key=f"rot_reset_{img_key}"):
                                            st.session_state.rotation_states[img_key] = 0
                                            st.rerun()
                            
                            col_idx += 1
                    else:
                        st.info("No files attached to this lecture.")
                    
                    st.markdown("---")
                    
                    # Comments section
                    st.markdown("#### 💬 Comments")
                    
                    comments = lecture.get("comments", [])
                    if comments:
                        for comment in comments:
                            st.markdown(f"""
                            <div style="background: #f8f9fa; padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0; border-left: 3px solid #667eea;">
                                <strong>{comment['user']}</strong> • <small>{comment['date']}</small><br>
                                {comment['text']}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No comments yet. Be the first to comment!")
                    
                    # Add comment form
                    with st.form(f"comment_form_{lecture['id']}", clear_on_submit=True):
                        comment_text = st.text_area(
                            "Add your comment",
                            placeholder="Share your thoughts...",
                            key=f"comment_input_{lecture['id']}"
                        )
                        
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            submit_comment = st.form_submit_button("💬 Post", use_container_width=True)
                        
                        if submit_comment and comment_text:
                            # Add comment
                            if "comments" not in lecture:
                                lecture["comments"] = []
                            
                            lecture["comments"].append({
                                "user": st.session_state.username if st.session_state.logged_in else "Anonymous",
                                "text": comment_text,
                                "date": datetime.now().strftime("%d %b %Y, %I:%M %p")
                            })
                            
                            # Increment view count
                            lecture["reads"] = lecture.get("reads", 0) + 1
                            
                            # Save data
                            save_data(all_lectures)
                            st.success("✅ Comment posted successfully!")
                            st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        # No results found
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: #f8f9fa; border-radius: 15px;">
            <h2>🔍 No lectures found</h2>
            <p>Try adjusting your search filters or browse all lectures.</p>
        </div>
        """, unsafe_allow_html=True)

# Tab 2: Admin Panel (only for logged-in users)
if st.session_state.logged_in:
    with tab2:
        st.markdown("### ⚙️ Admin Dashboard")
        
        # Create sub-tabs for admin functions
        admin_tab1, admin_tab2, admin_tab3 = st.tabs(["📤 **Upload Lecture**", "📚 **Batch Upload**", "🗑️ **Manage Lectures**"])
        
        # Upload Lecture Tab
        with admin_tab1:
            st.markdown("#### 📤 Upload New Lecture Note")
            
            with st.form("upload_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    title = st.text_input("📝 Lecture Title*", placeholder="Enter lecture title...")
                    subject = st.selectbox("📚 Subject*", ["Select Subject"] + SUBJECTS)
                    lecture_no = st.number_input("🔢 Lecture Number*", min_value=1, value=1)
                
                with col2:
                    date = st.date_input("📅 Date", datetime.now())
                    tags = st.text_input("🏷️ Tags", placeholder="Separate with commas: tag1, tag2...")
                    description = st.text_area("📄 Description", placeholder="Brief description of the lecture...")
                
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("##### 📄 PDF Files (Max 3)")
                    pdf_files = st.file_uploader(
                        "Upload PDFs",
                        type="pdf",
                        accept_multiple_files=True,
                        key="pdf_upload",
                        label_visibility="collapsed"
                    )
                
                with col2:
                    st.markdown("##### 🖼️ Image Files (Max 30)")
                    img_files = st.file_uploader(
                        "Upload Images",
                        type=["jpg", "jpeg", "png"],
                        accept_multiple_files=True,
                        key="img_upload",
                        label_visibility="collapsed"
                    )
                
                st.markdown("---")
                
                col1, col2, col3 = st.columns([2, 1, 2])
                with col2:
                    submit_btn = st.form_submit_button("🚀 Upload Lecture", use_container_width=True)
                
                if submit_btn:
                    # Validation
                    if not title or subject == "Select Subject":
                        st.error("❌ Please fill in all required fields!")
                    elif len(pdf_files) > 3:
                        st.error("❌ Maximum 3 PDF files allowed!")
                    elif len(img_files) > 30:
                        st.error("❌ Maximum 30 image files allowed!")
                    else:
                        # Process files
                        files_data = []
                        
                        # Process PDFs
                        for pdf in pdf_files:
                            files_data.append({
                                "name": pdf.name,
                                "type": "pdf",
                                "content": file_to_base64(pdf)
                            })
                        
                        # Process images
                        for img in img_files:
                            files_data.append({
                                "name": img.name,
                                "type": "image",
                                "content": file_to_base64(img)
                            })
                        
                        # Create lecture object
                        lectures = load_data()
                        new_lecture = {
                            "id": len(lectures) + 1,
                            "title": title,
                            "lecture_no": lecture_no,
                            "subject": subject,
                            "description": description,
                            "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
                            "date": datetime.combine(date, datetime.min.time()),
                            "submitted_by": st.session_state.username,
                            "files": files_data,
                            "reads": 0,
                            "comments": []
                        }
                        
                        lectures.append(new_lecture)
                        save_data(lectures)
                        
                        st.success("✅ Lecture uploaded successfully!")
                        st.balloons()
        
        # Batch Upload Tab
        with admin_tab2:
            st.markdown("#### 📚 Batch Upload Multiple Lectures")
            st.info("📝 Upload multiple lectures at once. Each lecture will have the same subject and tags.")
            
            # Batch upload form
            with st.form("batch_upload_form"):
                # Common fields
                st.markdown("##### Common Information")
                col1, col2 = st.columns(2)
                
                with col1:
                    batch_subject = st.selectbox("📚 Subject*", ["Select Subject"] + SUBJECTS)
                    batch_tags = st.text_input("🏷️ Common Tags", placeholder="Separate with commas...")
                
                with col2:
                    batch_date = st.date_input("📅 Starting Date", datetime.now())
                    batch_description_prefix = st.text_input("📝 Description Prefix", placeholder="e.g., 'Lecture on'")
                
                st.markdown("---")
                
                # Number of lectures to add
                num_lectures = st.number_input("📊 Number of Lectures to Add", min_value=1, max_value=10, value=1)
                
                # Dynamic lecture fields
                st.markdown("##### Individual Lecture Details")
                
                if "batch_lectures" not in st.session_state:
                    st.session_state.batch_lectures = []
                
                # Create fields for each lecture
                for i in range(num_lectures):
                    with st.expander(f"📖 Lecture {i+1}", expanded=i==0):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            lec_title = st.text_input(f"Title*", key=f"batch_title_{i}", placeholder="Enter title...")
                            lec_no = st.number_input(f"Lecture Number*", key=f"batch_no_{i}", min_value=1, value=i+1)
                        
                        with col2:
                            lec_desc = st.text_area(f"Description", key=f"batch_desc_{i}", placeholder="Additional description...")
                        
                        st.markdown("**Files**")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            lec_pdfs = st.file_uploader(
                                f"PDFs (Max 3)",
                                type="pdf",
                                accept_multiple_files=True,
                                key=f"batch_pdf_{i}"
                            )
                        
                        with col2:
                            lec_imgs = st.file_uploader(
                                f"Images (Max 30)",
                                type=["jpg", "jpeg", "png"],
                                accept_multiple_files=True,
                                key=f"batch_img_{i}"
                            )
                
                st.markdown("---")
                
                col1, col2, col3 = st.columns([2, 1, 2])
                with col2:
                    batch_submit = st.form_submit_button("🚀 Upload All Lectures", use_container_width=True)
                
                if batch_submit:
                    if batch_subject == "Select Subject":
                        st.error("❌ Please select a subject!")
                    else:
                        lectures = load_data()
                        success_count = 0
                        
                        for i in range(num_lectures):
                            title = st.session_state.get(f"batch_title_{i}", "")
                            lec_no = st.session_state.get(f"batch_no_{i}", i+1)
                            
                            if title:  # Only process if title is provided
                                # Process files
                                files_data = []
                                
                                # PDFs
                                pdfs = st.session_state.get(f"batch_pdf_{i}", [])
                                if len(pdfs) <= 3:
                                    for pdf in pdfs:
                                        files_data.append({                                            "name": pdf.name,
                                            "type": "pdf",
                                            "content": file_to_base64(pdf)
                                        })
                                
                                # Images
                                imgs = st.session_state.get(f"batch_img_{i}", [])
                                if len(imgs) <= 30:
                                    for img in imgs:
                                        files_data.append({
                                            "name": img.name,
                                            "type": "image",
                                            "content": file_to_base64(img)
                                        })
                                
                                # Create lecture
                                desc = st.session_state.get(f"batch_desc_{i}", "")
                                full_desc = f"{batch_description_prefix} {desc}".strip() if batch_description_prefix else desc
                                
                                new_lecture = {
                                    "id": len(lectures) + success_count + 1,
                                    "title": title,
                                    "lecture_no": lec_no,
                                    "subject": batch_subject,
                                    "description": full_desc,
                                    "tags": [tag.strip() for tag in batch_tags.split(",") if tag.strip()],
                                    "date": datetime.combine(batch_date, datetime.min.time()),
                                    "submitted_by": st.session_state.username,
                                    "files": files_data,
                                    "reads": 0,
                                    "comments": []
                                }
                                
                                lectures.append(new_lecture)
                                success_count += 1
                        
                        if success_count > 0:
                            save_data(lectures)
                            st.success(f"✅ Successfully uploaded {success_count} lectures!")
                            st.balloons()
                        else:
                            st.warning("⚠️ No lectures were uploaded. Please provide titles for the lectures.")
        
        # Manage Lectures Tab
        with admin_tab3:
            st.markdown("#### 🗑️ Manage Existing Lectures")
            
            lectures = load_data()
            
            if lectures:
                # Search for lecture to delete
                search_delete = st.text_input("🔍 Search lecture to manage", placeholder="Enter title keywords...")
                
                # Filter lectures for deletion
                delete_candidates = lectures
                if search_delete:
                    delete_candidates = [
                        lec for lec in lectures 
                        if search_delete.lower() in lec["title"].lower()
                    ]
                
                if delete_candidates:
                    for lecture in delete_candidates:
                        with st.container():
                            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                            
                            col1, col2, col3 = st.columns([3, 1, 1])
                            
                            with col1:
                                st.markdown(f"**{lecture['title']}**")
                                st.caption(f"Subject: {lecture['subject']} | Lecture #{lecture['lecture_no']} | {lecture['date'].strftime('%d %b %Y')}")
                                st.caption(f"Uploaded by: {lecture['submitted_by']} | Views: {lecture.get('reads', 0)}")
                            
                            with col2:
                                if st.button("📝 Edit", key=f"edit_{lecture['id']}", use_container_width=True):
                                    st.session_state[f"edit_mode_{lecture['id']}"] = True
                            
                            with col3:
                                if st.button("🗑️ Delete", key=f"delete_{lecture['id']}", type="secondary", use_container_width=True):
                                    if f"confirm_delete_{lecture['id']}" not in st.session_state:
                                        st.session_state[f"confirm_delete_{lecture['id']}"] = False
                                    st.session_state[f"confirm_delete_{lecture['id']}"] = True
                            
                            # Edit mode
                            if st.session_state.get(f"edit_mode_{lecture['id']}", False):
                                st.markdown("---")
                                st.markdown("**📝 Edit Lecture**")
                                
                                with st.form(f"edit_form_{lecture['id']}"):
                                    col1, col2 = st.columns(2)
                                    
                                    with col1:
                                        new_title = st.text_input("Title", value=lecture['title'])
                                        new_subject = st.selectbox("Subject", SUBJECTS, index=SUBJECTS.index(lecture['subject']))
                                    
                                    with col2:
                                        new_lec_no = st.number_input("Lecture Number", value=lecture['lecture_no'], min_value=1)
                                        new_tags = st.text_input("Tags", value=", ".join(lecture.get('tags', [])))
                                    
                                    new_desc = st.text_area("Description", value=lecture.get('description', ''))
                                    
                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        if st.form_submit_button("💾 Save Changes", use_container_width=True):
                                            # Update lecture
                                            lecture['title'] = new_title
                                            lecture['subject'] = new_subject
                                            lecture['lecture_no'] = new_lec_no
                                            lecture['description'] = new_desc
                                            lecture['tags'] = [tag.strip() for tag in new_tags.split(",") if tag.strip()]
                                            
                                            save_data(lectures)
                                            st.success("✅ Lecture updated successfully!")
                                            del st.session_state[f"edit_mode_{lecture['id']}"]
                                            st.rerun()
                                    
                                    with col2:
                                        if st.form_submit_button("❌ Cancel", use_container_width=True):
                                            del st.session_state[f"edit_mode_{lecture['id']}"]
                                            st.rerun()
                            
                            # Show confirmation dialog for delete
                            if st.session_state.get(f"confirm_delete_{lecture['id']}", False):
                                st.warning(f"⚠️ Are you sure you want to delete '{lecture['title']}'?")
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    if st.button("✅ Yes, Delete", key=f"confirm_yes_{lecture['id']}", type="primary"):
                                        # Delete the lecture
                                        updated_lectures = [lec for lec in lectures if lec["id"] != lecture["id"]]
                                        save_data(updated_lectures)
                                        st.success(f"✅ Lecture '{lecture['title']}' deleted successfully!")
                                        del st.session_state[f"confirm_delete_{lecture['id']}"]
                                        st.rerun()
                                
                                with col2:
                                    if st.button("❌ Cancel", key=f"confirm_no_{lecture['id']}"):
                                        del st.session_state[f"confirm_delete_{lecture['id']}"]
                                        st.rerun()
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info("🔍 No lectures found matching your search.")
            else:
                st.info("📚 No lectures available to manage.")

# Tab 3: Analytics (only for logged-in users)
if st.session_state.logged_in:
    with tab3:
        st.markdown("### 📊 Analytics Dashboard")
        
        lectures = load_data()
        
        if lectures:
            # Convert to DataFrame for analysis
            df = pd.DataFrame(lectures)
            
            # Overview metrics
            st.markdown("#### 📈 Overview Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(create_metric_card("Total Lectures", len(lectures), "📚"), unsafe_allow_html=True)
            
            with col2:
                total_views = sum(lec.get('reads', 0) for lec in lectures)
                st.markdown(create_metric_card("Total Views", total_views, "👀"), unsafe_allow_html=True)
            
            with col3:
                total_comments = sum(len(lec.get('comments', [])) for lec in lectures)
                st.markdown(create_metric_card("Total Comments", total_comments, "💬"), unsafe_allow_html=True)
            
            with col4:
                avg_views = round(total_views / len(lectures), 1) if lectures else 0
                st.markdown(create_metric_card("Avg Views", avg_views, "📊"), unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Lectures by subject
                st.markdown("#### 📚 Lectures by Subject")
                subject_counts = df['subject'].value_counts()
                
                fig = px.pie(
                    values=subject_counts.values,
                    names=subject_counts.index,
                    color_discrete_sequence=px.colors.sequential.Purples
                )
                fig.update_layout(
                    showlegend=True,
                    height=300,
                    margin=dict(l=0, r=0, t=0, b=0)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Top viewed lectures
                st.markdown("#### 🔥 Most Popular Lectures")
                top_lectures = df.nlargest(5, 'reads')[['title', 'reads']]
                
                fig = px.bar(
                    top_lectures,
                    x='reads',
                    y='title',
                    orientation='h',
                    color='reads',
                    color_continuous_scale='Purples'
                )
                fig.update_layout(
                    showlegend=False,
                    height=300,
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis_title="Views",
                    yaxis_title=""
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Activity timeline
            st.markdown("#### 📅 Upload Timeline")
            
            # Prepare data for timeline
            df['date'] = pd.to_datetime(df['date'])
            df['month'] = df['date'].dt.to_period('M')
            monthly_uploads = df.groupby('month').size().reset_index(name='count')
            monthly_uploads['month'] = monthly_uploads['month'].dt.to_timestamp()
            
            fig = px.line(
                monthly_uploads,
                x='month',
                y='count',
                markers=True,
                line_shape='spline'
            )
            fig.update_traces(
                line_color='#667eea',
                line_width=3,
                marker_size=8,
                marker_color='#764ba2'
            )
            fig.update_layout(
                showlegend=False,
                height=250,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis_title="Month",
                yaxis_title="Number of Uploads",
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Additional analytics
            col1, col2 = st.columns(2)
            
            with col1:
                # Comments by lecture
                st.markdown("#### 💬 Most Discussed Lectures")
                df['comment_count'] = df['comments'].apply(lambda x: len(x) if x else 0)
                top_commented = df.nlargest(5, 'comment_count')[['title', 'comment_count']]
                
                if not top_commented.empty and top_commented['comment_count'].sum() > 0:
                    fig = px.bar(
                        top_commented,
                        x='comment_count',
                        y='title',
                        orientation='h',
                        color='comment_count',
                        color_continuous_scale='Blues'
                    )
                    fig.update_layout(
                        showlegend=False,
                        height=250,
                        margin=dict(l=0, r=0, t=0, b=0),
                        xaxis_title="Number of Comments",
                        yaxis_title=""
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No comments data available yet.")
            
            with col2:
                # Contributor stats
                st.markdown("#### 👥 Top Contributors")
                contributor_counts = df['submitted_by'].value_counts().head(5)
                
                fig = px.bar(
                    x=contributor_counts.values,
                    y=contributor_counts.index,
                    orientation='h',
                    color=contributor_counts.values,
                    color_continuous_scale='Greens'
                )
                fig.update_layout(
                    showlegend=False,
                    height=250,
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis_title="Number of Uploads",
                    yaxis_title="Contributor"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Recent activity table
            st.markdown("#### 🕒 Recent Activity")
            
            recent_df = df[['title', 'subject', 'date', 'submitted_by', 'reads']].copy()
            recent_df['date'] = recent_df['date'].dt.strftime('%d %b %Y')
            recent_df = recent_df.sort_values('date', ascending=False).head(10)
            recent_df.columns = ['Title', 'Subject', 'Date', 'Uploaded By', 'Views']
            
            st.dataframe(
                recent_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Title": st.column_config.TextColumn("Title", width="large"),
                    "Subject": st.column_config.TextColumn("Subject", width="medium"),
                    "Date": st.column_config.TextColumn("Date", width="small"),
                    "Uploaded By": st.column_config.TextColumn("Uploaded By", width="small"),
                    "Views": st.column_config.NumberColumn("Views", width="small", format="%d 👀")
                }
            )
            
            # Export data option
            st.markdown("---")
            st.markdown("#### 📥 Export Data")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Export as CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📊 Download as CSV",
                    data=csv,
                    file_name=f"lectures_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                # Export as JSON
                json_str = df.to_json(orient='records', indent=2)
                st.download_button(
                    label="📋 Download as JSON",                    data=json_str,
                    file_name=f"lectures_data_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col3:
                # Generate report
                if st.button("📄 Generate Report", use_container_width=True):
                    report = f"""
# MysticXib Classnote Corner - Analytics Report
Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

## Overview
- Total Lectures: {len(lectures)}
- Total Views: {total_views}
- Total Comments: {total_comments}
- Average Views per Lecture: {avg_views}

## Subject Distribution
{subject_counts.to_string()}

## Top 5 Most Viewed Lectures
{top_lectures.to_string()}

## Top Contributors
{contributor_counts.to_string()}

---
Report generated by MysticXib Classnote Corner v2.0
                    """
                    st.download_button(
                        label="💾 Download Report",
                        data=report,
                        file_name=f"analytics_report_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
        else:
            st.info("📊 No data available for analytics. Upload some lectures first!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>Made with ❤️ by <strong>MysticXib</strong> | © 2024 Classnote Corner</p>
    <p style="font-size: 0.8rem;">🔒 Your data is stored locally and securely</p>
</div>
""", unsafe_allow_html=True)

# Add floating help button
st.markdown("""
<style>
.help-button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    cursor: pointer;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
    z-index: 999;
}

.help-button:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
}
</style>

<div class="help-button" onclick="alert('Need help? Contact admin@mysticxib.com')">
    ?
</div>
""", unsafe_allow_html=True)

# Progress indicator for file uploads
def show_upload_progress():
    progress_bar = st.progress(0)
    for i in range(100):
        progress_bar.progress(i + 1)
        time.sleep(0.01)
    progress_bar.empty()

# Mobile responsiveness check
if st.session_state.get('check_mobile', True):
    st.markdown("""
    <script>
    if (window.innerWidth < 768) {
        alert('📱 For the best experience, please use this app on a desktop or tablet device.');
    }
    </script>
    """, unsafe_allow_html=True)
    st.session_state.check_mobile = False

# Add custom favicon and title
st.markdown("""
<script>
document.title = "MysticXib Classnote Corner - Your Academic Hub";
var link = document.querySelector("link[rel~='icon']");
if (!link) {
    link = document.createElement('link');
    link.rel = 'icon';
    document.getElementsByTagName('head')[0].appendChild(link);
}
link.href = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">📚</text></svg>';
</script>
""", unsafe_allow_html=True)

# Add keyboard shortcuts
st.markdown("""<script>
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + K for search focus
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        document.querySelector('input[type="text"]').focus();
    }
    
    // Ctrl/Cmd + U for upload (if logged in)
    if ((event.ctrlKey || event.metaKey) && event.key === 'u') {
        event.preventDefault();
        const uploadTab = document.querySelector('[data-baseweb="tab"]:nth-child(2)');
        if (uploadTab) uploadTab.click();
    }
    
    // Escape to close modals
    if (event.key === 'Escape') {
        const closeButtons = document.querySelectorAll('[aria-label="Close"]');
        closeButtons.forEach(button => button.click());
    }
});
</script>
""", unsafe_allow_html=True)

# Auto-save functionality for forms
if st.session_state.logged_in:
    # Auto-save draft every 30 seconds
    st.markdown("""
    <script>
    // Auto-save form data
    let autoSaveInterval;
    
    function autoSaveForm() {
        const formData = {};
        const inputs = document.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            if (input.id) {
                formData[input.id] = input.value;
            }
        });
        
        localStorage.setItem('formDraft', JSON.stringify(formData));
        console.log('Form data auto-saved');
    }
    
    // Start auto-save
    autoSaveInterval = setInterval(autoSaveForm, 30000);
    
    // Restore saved data on page load
    window.addEventListener('load', function() {
        const savedData = localStorage.getItem('formDraft');
        if (savedData) {
            const formData = JSON.parse(savedData);
            Object.keys(formData).forEach(key => {
                const input = document.getElementById(key);
                if (input) {
                    input.value = formData[key];
                }
            });
        }
    });
    
    // Clear saved data when form is submitted
    document.addEventListener('submit', function() {
        localStorage.removeItem('formDraft');
        clearInterval(autoSaveInterval);
    });
    </script>
    """, unsafe_allow_html=True)

# Performance monitoring
st.markdown("""
<script>
// Log performance metrics
window.addEventListener('load', function() {
    const perfData = window.performance.timing;
    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
    console.log(`Page load time: ${pageLoadTime}ms`);
    
    // Send analytics if needed
    if (window.gtag) {
        gtag('event', 'page_load_time', {
            'value': pageLoadTime,
            'page_location': window.location.href
        });
    }
});
</script>
""", unsafe_allow_html=True)

# Add print styles
st.markdown("""
<style>
@media print {
    .stButton, .stFileUploader, .stTextInput, .stSelectbox {
        display: none !important;
    }
    
    .custom-card {
        page-break-inside: avoid;
        border: 1px solid #ddd;
        margin-bottom: 1rem;
    }
    
    .main-header {
        background: none !important;
        color: black !important;
        border: 2px solid #333;
    }
    
    body {
        font-size: 12pt;
        line-height: 1.5;
    }
}
</style>
""", unsafe_allow_html=True)

# Accessibility features
st.markdown("""
<script>
// Add ARIA labels dynamically
document.addEventListener('DOMContentLoaded', function() {
    // Add labels to buttons
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        if (!button.getAttribute('aria-label')) {
            button.setAttribute('aria-label', button.innerText);
        }
    });
    
    // Add labels to inputs
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        const label = input.closest('div').querySelector('label');
        if (label && !input.getAttribute('aria-label')) {
            input.setAttribute('aria-label', label.innerText);
        }
    });
});

// Enable keyboard navigation for custom elements
document.addEventListener('keydown', function(event) {
    if (event.key === 'Tab') {
        // Custom tab handling if needed
    }
});
</script>
""", unsafe_allow_html=True)

# Session timeout warning
if st.session_state.logged_in:
    st.markdown("""
    <script>
    let warningTimer;
    let logoutTimer;
    
    function resetTimers() {
        clearTimeout(warningTimer);
        clearTimeout(logoutTimer);
        
        // Warn after 25 minutes of inactivity
        warningTimer = setTimeout(function() {
            if (confirm('Your session will expire in 5 minutes due to inactivity. Click OK to continue.')) {
                resetTimers();
            }
        }, 25 * 60 * 1000);
        
        // Auto logout after 30 minutes
        logoutTimer = setTimeout(function() {
            alert('Session expired due to inactivity.');
            window.location.reload();
        }, 30 * 60 * 1000);
    }
    
    // Reset timers on user activity
    ['mousedown', 'keypress', 'scroll', 'touchstart'].forEach(event => {
        document.addEventListener(event, resetTimers, true);
    });
    
    // Initialize timers
    resetTimers();
    </script>
    """, unsafe_allow_html=True)

# Final cleanup and optimization
st.markdown("""
<script>
// Clean up on page unload
window.addEventListener('beforeunload', function() {
    // Save any unsaved data
    if (typeof autoSaveForm === 'function') {
        autoSaveForm();
    }
});

// Optimize images loading
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.loading = 'lazy';
    });
});
</script>
""", unsafe_allow_html=True)
