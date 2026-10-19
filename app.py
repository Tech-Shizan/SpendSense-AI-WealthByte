import streamlit as st
from logic import get_financial_advice, mask_sensitive_data
from database import create_session, get_sidebar_history, toggle_pin, delete_session, add_chat_message, get_session

# Page Configuration
st.set_page_config(
    page_title="SpendSense AI",
    page_icon="💸",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown('''
    <style>
    /* Hide only the right-side actions (settings, deploy, 3-dots) */
    [data-testid="stHeaderActionElements"],
    .stAppDeployButton,
    footer,
    #stDecoration,
    #MainMenu {
        display: none !important;
        visibility: hidden !important;
    }

    /* Ensure the expand arrow is always visible and clickable */
    [data-testid="stExpandSidebarButton"] {
        display: flex !important;
        visibility: visible !important;
        pointer-events: auto !important;
        color: white !important;
        z-index: 99999 !important;
        cursor: pointer !important;
    }

    [data-testid="stExpandSidebarButton"] * {
        visibility: visible !important;
        color: white !important;
        fill: white !important;
        pointer-events: auto !important;
    }

    /* Legacy expand and collapse button selectors */
    [data-testid="collapsedControl"],
    [data-testid="collapsedControl"] button,
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarHeader"] button {
        display: flex !important;
        visibility: visible !important;
        z-index: 99999 !important;
        color: white !important;
        pointer-events: auto !important;
        cursor: pointer !important;
    }

    /* Ensure the header itself is transparent and doesn't block clicks */
    [data-testid="stHeader"],
    header {
        background: transparent !important;
        pointer-events: none !important;
    }

    /* Hide any main area popover gear */
    .stMainBlockContainer div[data-testid="stPopover"],
    [data-testid="stMain"] div[data-testid="stPopover"] {
        display: none !important;
    }

    /* Keep sidebar popovers in natural document flow */
    [data-testid="stSidebar"] div[data-testid="stPopover"] {
        position: static !important;
        width: 100% !important;
        margin: 0 !important;
    }

    /* New Chat Button: ChatGPT-style clean button */
    div.st-key-new_chat_btn > button {
        background-color: #2B2D31 !important;
        border: 1px solid #444444 !important;
        border-radius: 8px !important;
        padding: 0.5rem 0.75rem !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        width: 100% !important;
        margin: 0.25rem 0 0.5rem 0 !important;
        color: #ffffff !important;
        box-shadow: none !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    div.st-key-new_chat_btn > button:hover {
        background-color: #383A40 !important;
        border-color: #555555 !important;
        color: #ffffff !important;
    }
    div.st-key-new_chat_btn > button p {
        color: #ffffff !important;
        font-weight: 500 !important;
    }

    /* Distinct scrollable box styling for history container */
    [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #3F4248 !important;
        border-radius: 8px !important;
        background-color: #1E1F22 !important;
        padding: 0.25rem !important;
    }

    /* Tighten vertical margins between history item rows */
    [data-testid="stSidebarUserContent"] div[data-testid="stHorizontalBlock"] {
        align-items: center !important;
        margin-bottom: 2px !important;
        padding: 0px !important;
        border-radius: 6px !important;
    }

    /* Target ONLY the sidebar history buttons to remove borders and backgrounds */
    [data-testid="stSidebarUserContent"] div[data-testid="stHorizontalBlock"] [data-testid="stButton"] > button {
        border: none !important;
        background-color: transparent !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 0.25rem 0.5rem !important;
        box-shadow: none !important;
        border-radius: 6px !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        color: inherit !important;
    }

    /* Add a subtle background on hover for the history item row */
    [data-testid="stSidebarUserContent"] div[data-testid="stHorizontalBlock"]:hover {
        background-color: rgba(150, 150, 150, 0.1) !important;
    }

    /* Hide the 3-dot popover button by default */
    [data-testid="stSidebarUserContent"] div[data-testid="stHorizontalBlock"] div[data-testid="stPopover"] {
        opacity: 0 !important;
        transition: opacity 0.2s ease-in-out !important;
        position: static !important;
        width: 100% !important;
        margin: 0 !important;
    }

    /* Show the 3-dot popover button ONLY when hovering or focused on that specific row */
    [data-testid="stSidebarUserContent"] div[data-testid="stHorizontalBlock"]:hover div[data-testid="stPopover"],
    [data-testid="stSidebarUserContent"] div[data-testid="stHorizontalBlock"] div[data-testid="stPopover"]:focus-within {
        opacity: 1 !important;
    }

    /* Make the 3-dot text larger and remove its native border */
    [data-testid="stSidebarUserContent"] div[data-testid="stHorizontalBlock"] div[data-testid="stPopover"] > button {
        font-size: 1.2rem !important;
        font-weight: bold !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0.1rem 0.3rem !important;
    }

    /* Hide the default dropdown caret arrow inside Streamlit popover buttons */
    [data-testid="stPopover"] button div[aria-hidden="true"],
    [data-testid="stPopover"] button [data-testid="stIconMaterial"] {
        display: none !important;
    }

    /* Style the outer alert box */
    [data-testid="stSidebarUserContent"] div[data-testid="stAlert"] {
        border-radius: 8px !important;
        padding: 0.8rem 1rem !important;
        margin-bottom: 1rem !important;
        width: 100% !important;
    }

    /* Success alert styling in sidebar */
    [data-testid="stSidebarUserContent"] div[data-testid="stAlert"]:not(:has([data-testid="stAlertContentError"])):not(:has(svg[data-testid="stAlertIconError"])) {
        background-color: #173829 !important;
        border: 1px solid #238551 !important;
    }
    [data-testid="stSidebarUserContent"] div[data-testid="stAlert"]:not(:has([data-testid="stAlertContentError"])):not(:has(svg[data-testid="stAlertIconError"])) p {
        color: #d1fae5 !important;
    }

    /* Error alert styling in sidebar */
    [data-testid="stSidebarUserContent"] div[data-testid="stAlert"]:has([data-testid="stAlertContentError"]),
    [data-testid="stSidebarUserContent"] div[data-testid="stAlert"]:has(svg[data-testid="stAlertIconError"]) {
        background-color: #3b1818 !important;
        border: 1px solid #991b1b !important;
    }
    [data-testid="stSidebarUserContent"] div[data-testid="stAlert"]:has([data-testid="stAlertContentError"]) p,
    [data-testid="stSidebarUserContent"] div[data-testid="stAlert"]:has(svg[data-testid="stAlertIconError"]) p {
        color: #fca5a5 !important;
    }

    /* Make the header a relative container */
    [data-testid="stSidebarHeader"] {
        position: relative !important;
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }

    /* Inject the logo text directly into the header box */
    [data-testid="stSidebarHeader"]::after {
        content: "💸 SpendSense AI";
        position: absolute;
        left: 20px; /* Positions it to the left side */
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.4rem;
        font-weight: 700;
        color: inherit;
        white-space: nowrap;
    }

    /* Push the rest of the sidebar down so it doesn't overlap */
    [data-testid="stSidebarUserContent"] {
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
    }

    /* Ensure the collapse arrow stays on the right and on top */
    [data-testid="stSidebarCollapseButton"] {
        position: absolute !important;
        right: 15px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        z-index: 99 !important;
    }

    /* Sidebar headings clean spacing (strictly positive margins, no overlap) */
    [data-testid="stSidebar"] h3 {
        margin-top: 0.25rem !important;
        margin-bottom: 0.5rem !important;
        font-weight: 700 !important;
    }

    .stMainBlockContainer {
        padding-top: 3rem !important;
    }

    /* Completely hide scrollbars across all browsers in the sidebar */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] *,
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarContent"] *,
    [data-testid="stSidebarUserContent"],
    [data-testid="stSidebarUserContent"] * {
        scrollbar-width: none !important; /* Firefox */
        -ms-overflow-style: none !important; /* IE and Edge */
    }

    [data-testid="stSidebar"]::-webkit-scrollbar,
    [data-testid="stSidebarContent"]::-webkit-scrollbar,
    [data-testid="stSidebarUserContent"]::-webkit-scrollbar,
    [data-testid="stSidebar"] *::-webkit-scrollbar,
    [data-testid="stSidebarContent"] *::-webkit-scrollbar,
    [data-testid="stSidebarUserContent"] *::-webkit-scrollbar {
        display: none !important;
        width: 0px !important;
        height: 0px !important;
        background: transparent !important;
    }
    </style>
''', unsafe_allow_html=True)

# Top Navigation Header
st.title("💸 SpendSense AI")
st.caption("Intelligent Personal Finance & Smart Budgeting Assistant")

# Locked Default Dark Theme
theme = "🌙 Dark Mode"

# Custom Theme CSS injection
if theme == "🌙 Dark Mode":
    st.markdown('''
        <style>
        .stApp { background-color: #0e1117 !important; }
        [data-testid="stSidebar"] { background-color: #1a1c23 !important; }
        h1, h2, h3, h4, h5, h6, p, span, label, li, .stMarkdown { color: #ffffff !important; }
        .stTextInput input, .stTextArea textarea { background-color: #262730 !important; color: #ffffff !important; }
        .stButton > button { background-color: #262730 !important; color: #ffffff !important; border: 1px solid #555 !important; }
        .stPopover > button { background-color: #262730 !important; color: #ffffff !important; border: 1px solid #555 !important; }
        [data-testid="stPopoverBody"] { background-color: #1a1c23 !important; border: 1px solid #333 !important; }
        div.st-key-new_chat_btn > button { background-color: #2B2D31 !important; color: #ffffff !important; border: 1px solid #444444 !important; }
        div.st-key-new_chat_btn > button:hover { background-color: #383A40 !important; border-color: #555555 !important; }
        div.st-key-new_chat_btn > button p { color: #ffffff !important; }
        </style>
    ''', unsafe_allow_html=True)
else:
    st.markdown('''
        <style>
        .stApp { background-color: #f8f9fa !important; }
        [data-testid="stSidebar"] { background-color: #e9ecef !important; }
        h1, h2, h3, h4, h5, h6, p, span, label, li, .stMarkdown { color: #111111 !important; }
        .stTextInput input, .stTextArea textarea { background-color: #ffffff !important; color: #111111 !important; border: 1px solid #cccccc !important; }
        .stButton > button, .stButton > button p { background-color: #111111 !important; color: #ffffff !important; border: none !important; }
        .stPopover > button, .stPopover > button p { background-color: #ffffff !important; color: #111111 !important; border: 1px solid #cccccc !important; }
        [data-testid="stPopoverBody"] { background-color: #ffffff !important; border: 1px solid #cccccc !important; }
        div.st-key-new_chat_btn > button { background-color: #ffffff !important; color: #111111 !important; border: 1px solid #cccccc !important; }
        div.st-key-new_chat_btn > button:hover { background-color: #f1f3f5 !important; border-color: #bbbbbb !important; }
        div.st-key-new_chat_btn > button p { color: #111111 !important; }
        </style>
    ''', unsafe_allow_html=True)

# Session State for Chat & Bill Context
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Welcome! I can analyze your bills, track spending insights, and provide actionable recommendations based on your income and expenses. How can I help you today?"}
    ]

if "latest_bill_context" not in st.session_state:
    st.session_state.latest_bill_context = None

if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None

# Sidebar Layout (ChatGPT Style: Top to Bottom)
with st.sidebar:
    # Top: PII Masking alert box (Logo injected into header via CSS)
    st.success("🔒 PII Masking Active: Your sensitive account numbers and emails are encrypted before processing.")

    # 1. New Chat Button
    if st.sidebar.button("➕ New chat", key="new_chat_btn", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome! I can analyze your bills, track spending insights, and provide actionable recommendations based on your income and expenses. How can I help you today?"}
        ]
        st.session_state.latest_bill_context = None
        st.session_state.current_session_id = None
        st.rerun()

    # 2. Add some vertical spacing
    st.sidebar.write("")
    st.sidebar.write("")

    # 3. History Header
    st.sidebar.markdown("### History")

    # 4. History List
    history_list = get_sidebar_history()

    if history_list is None:
        st.error("Database connection failed. Please check credentials.")
    elif not history_list:
        st.markdown("<p style='color: #888888; font-size: 0.85rem; padding: 0.25rem 0;'>No previous chats yet.</p>", unsafe_allow_html=True)
    else:
        for chat in history_list:
            chat_id = chat.get("session_id") or chat.get("id")
            # Use stHorizontalBlock for the row
            col1, col2 = st.columns([85, 15])
            
            with col1:
                pin_icon = "📌 " if chat.get("pinned") else "💬 "
                if st.button(f"{pin_icon} {chat.get('title', 'Chat')}", key=f"chat_{chat_id}", use_container_width=True):
                    st.session_state.current_session_id = chat_id
                    session_doc = get_session(chat_id)
                    if session_doc:
                        chat_msgs = session_doc.get("chat_messages", [])
                        msgs = [{"role": "assistant", "content": "Welcome! I can analyze your bills, track spending insights, and provide actionable recommendations based on your income and expenses. How can I help you today?"}]
                        for m in chat_msgs:
                            msgs.append({"role": m.get("role", "user"), "content": m.get("text", "")})
                        st.session_state.messages = msgs
                        st.session_state.latest_bill_context = session_doc.get("masked_bill_data")
                    st.rerun()
                
            with col2:
                with st.popover("⋮"):
                    if chat.get("pinned"):
                        if st.button("Unpin", key=f"unpin_{chat_id}", use_container_width=True):
                            toggle_pin(chat_id, True)
                            st.rerun()
                    else:
                        if st.button("Pin", key=f"pin_{chat_id}", use_container_width=True):
                            toggle_pin(chat_id, False)
                            st.rerun()
                    if st.button("Delete", key=f"del_{chat_id}", use_container_width=True):
                        delete_session(chat_id)
                        if st.session_state.get("current_session_id") == chat_id:
                            st.session_state.current_session_id = None
                            st.session_state.messages = [
                                {"role": "assistant", "content": "Welcome! I can analyze your bills, track spending insights, and provide actionable recommendations based on your income and expenses. How can I help you today?"}
                            ]
                            st.session_state.latest_bill_context = None
                        st.rerun()

st.markdown("---")

# Main Area: Universal Chat & Financial Analysis
# Display Chat Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Universal Chat Input (Bills and General Financial Queries)
if user_input := st.chat_input("Ask about your finances..."):
    # a) Run the input through the existing PII Masking function immediately
    masked_user_input = mask_sensitive_data(user_input.strip())

    # b) If there is no active session, create one (create_session) using the first few words of the masked text as the title
    if not st.session_state.get("current_session_id"):
        words = masked_user_input.split()
        first_few = " ".join(words[:5]) if words else "Financial Query"
        title = first_few[:30] + ("..." if len(first_few) > 30 else "")
        session_id = create_session(title, masked_user_input)
        if not session_id:
            st.sidebar.error("Database connection failed. Please check credentials.")
        else:
            st.session_state.current_session_id = session_id
            st.session_state.latest_bill_context = masked_user_input

    # c) Save the masked user message to MongoDB
    if st.session_state.get("current_session_id"):
        add_chat_message(st.session_state.current_session_id, "user", masked_user_input)

    # d) Display the user's message in the chat UI
    st.session_state.messages.append({"role": "user", "content": masked_user_input})
    with st.chat_message("user"):
        st.markdown(masked_user_input)

    # e) Pass the masked text to the AI model (logic.py) to generate the analysis or response
    with st.spinner("Analyzing your finances securely..."):
        try:
            bot_reply = get_financial_advice(
                masked_user_input,
                bill_context=st.session_state.get("latest_bill_context")
            )
        except Exception as e:
            bot_reply = f"Error connecting to AI: {str(e)}"

    # f) Display the AI response and save it to MongoDB
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    if st.session_state.get("current_session_id"):
        safe_bot_reply = mask_sensitive_data(bot_reply)
        add_chat_message(st.session_state.current_session_id, "assistant", safe_bot_reply)