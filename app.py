
import streamlit as st
from cryptography.fernet import Fernet, InvalidToken
import hashlib
import base64

st.set_page_config(
    page_title="CipherBox",
    page_icon="🔐",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #080b18, #111a35);
    color: white;
}

.block-container {
    max-width: 1100px;
    padding-top: 35px;
}

.header {
    text-align: center;
    padding: 20px;
}

.logo {
    font-size: 55px;
}

.title {
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(90deg, #818cf8, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: #a5b4c8;
    font-size: 16px;
}

.card {
    background: rgba(25, 34, 60, 0.95);
    border: 1px solid #33446b;
    border-radius: 18px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.25);
}

.card h3 {
    color: #e0e7ff;
}

.stTextInput input,
.stTextArea textarea {
    background: #0b1224 !important;
    color: white !important;
    border: 1px solid #3b4d75 !important;
    border-radius: 10px !important;
}

.stButton button {
    width: 100%;
    height: 48px;
    border-radius: 10px;
    border: none;
    color: white;
    font-weight: bold;
    background: linear-gradient(90deg, #6366f1, #06b6d4);
}

.stDownloadButton button {
    width: 100%;
    border-radius: 10px;
    background: #17223d;
    color: #dbeafe;
    border: 1px solid #3b4d75;
}

[data-testid="stFileUploader"] {
    background: #0c1428;
    border-radius: 12px;
    border: 1px dashed #52658f;
}

.feature {
    background: #141d35;
    border: 1px solid #29395d;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
}

.feature-icon {
    font-size: 28px;
}

.feature-title {
    font-weight: bold;
    margin-top: 8px;
}

.feature-text {
    color: #8e9ab3;
    font-size: 13px;
}

.footer {
    text-align: center;
    color: #68738c;
    margin-top: 35px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


def generate_key(password):
    password_hash = hashlib.sha256(
        password.encode("utf-8")
    ).digest()

    return base64.urlsafe_b64encode(password_hash)


def encrypt_data(data, password):
    key = generate_key(password)
    cipher = Fernet(key)
    return cipher.encrypt(data)


def decrypt_data(data, password):
    key = generate_key(password)
    cipher = Fernet(key)
    return cipher.decrypt(data)


# HEADER

st.markdown("""
<div class="header">
    <div class="logo">🔐</div>
    <div class="title">CipherBox</div>
    <div class="subtitle">
        Securely encrypt and decrypt your text and files
    </div>
</div>
""", unsafe_allow_html=True)


# OPERATION

st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("Choose Operation")

mode = st.radio(
    "Operation",
    ["🔒 Encrypt", "🔓 Decrypt"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown('</div>', unsafe_allow_html=True)


# MAIN COLUMNS

left, right = st.columns([1.6, 1], gap="large")


with left:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    if mode == "🔒 Encrypt":

        st.markdown("### 🔒 Encrypt Data")

        st.caption(
            "Enter text or upload a file to encrypt."
        )

        text_input = st.text_area(
            "Text",
            placeholder="Type your secret message here...",
            height=180
        )

        uploaded_file = st.file_uploader(
            "Upload File"
        )

    else:

        st.markdown("### 🔓 Decrypt Data")

        st.caption(
            "Enter encrypted text or upload an encrypted file."
        )

        text_input = st.text_area(
            "Encrypted Text",
            placeholder="Paste encrypted text here...",
            height=180
        )

        uploaded_file = st.file_uploader(
            "Upload Encrypted File"
        )

    st.markdown('</div>', unsafe_allow_html=True)


with right:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("### 🔑 Security")

    st.caption(
        "Use the same password when decrypting your data."
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password"
    )

    st.info(
        "Keep your password safe. It cannot be recovered."
    )

    st.markdown('</div>', unsafe_allow_html=True)


# ACTION BUTTON

if mode == "🔒 Encrypt":

    action = st.button("🔐 Encrypt Now")

else:

    action = st.button("🔓 Decrypt Now")


# PROCESS

if action:

    if not password:

        st.error("Please enter a password.")

    elif not text_input and uploaded_file is None:

        st.warning(
            "Please enter text or upload a file."
        )

    else:

        try:

            # FILE

            if uploaded_file is not None:

                data = uploaded_file.read()

                if mode == "🔒 Encrypt":

                    result = encrypt_data(
                        data,
                        password
                    )

                    filename = (
                        uploaded_file.name +
                        ".encrypted"
                    )

                    st.success(
                        "File encrypted successfully! 🔐"
                    )

                else:

                    result = decrypt_data(
                        data,
                        password
                    )

                    filename = uploaded_file.name.replace(
                        ".encrypted",
                        ""
                    )

                    st.success(
                        "File decrypted successfully! 🔓"
                    )

                st.download_button(
                    "⬇️ Download File",
                    data=result,
                    file_name=filename,
                    mime="application/octet-stream"
                )

            # TEXT

            else:

                if mode == "🔒 Encrypt":

                    result = encrypt_data(
                        text_input.encode("utf-8"),
                        password
                    )

                    output = result.decode("utf-8")
                    filename = "encrypted.txt"

                    st.success(
                        "Text encrypted successfully! 🔐"
                    )

                else:

                    result = decrypt_data(
                        text_input.encode("utf-8"),
                        password
                    )

                    output = result.decode("utf-8")
                    filename = "decrypted.txt"

                    st.success(
                        "Text decrypted successfully! 🔓"
                    )

                st.text_area(
                    "Result",
                    value=output,
                    height=180
                )

                st.download_button(
                    "⬇️ Download Result",
                    data=output,
                    file_name=filename,
                    mime="text/plain"
                )

        except InvalidToken:

            st.error(
                "❌ Wrong password or invalid encrypted data."
            )

        except Exception:

            st.error(
                "❌ Unable to process this data."
            )


# FEATURES

st.write("")
st.write("")

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
    <div class="feature">
        <div class="feature-icon">🛡️</div>
        <div class="feature-title">Secure</div>
        <div class="feature-text">
            Fernet symmetric encryption
        </div>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="feature">
        <div class="feature-icon">📁</div>
        <div class="feature-title">File Support</div>
        <div class="feature-text">
            Encrypt and decrypt files
        </div>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="feature">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Fast & Simple</div>
        <div class="feature-text">
            Easy to use interface
        </div>
    </div>
    """, unsafe_allow_html=True)


# FOOTER

st.markdown("""
<div class="footer">
    🔐 CipherBox • Secure Encryption Utility
</div>
""", unsafe_allow_html=True)