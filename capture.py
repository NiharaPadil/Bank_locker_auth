import streamlit as st
import cv2
import os
import subprocess

# Function to capture and save image
def capture_and_save_image(img_name):
    # Capture frame from webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    # Save the captured image with the specified name
    img_path = f"Images/{img_name}.jpg"
    cv2.imwrite(img_path, frame)
    st.success(f"Image '{img_name}' saved successfully!")

    # Run the encoder file
    #subprocess.run(["python", "EncodeGenerator.py"])

# Function to authenticate the user
def authenticate_user(username, password):
    # Hardcoded username and password (replace with your authentication logic)
    valid_username = "bank_officer"
    valid_password = "password"

    # Check if the entered credentials match
    if username == valid_username and password == valid_password:
        return True
    else:
        return False

# Function to display the login page
def login_page():
    st.title("Bank Officer Login")
    bank_officer_id = st.text_input("Bank Officer ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(bank_officer_id, password):
            st.success("Login successful!")
            st.session_state.is_logged_in = True
        else:
            st.error("Invalid username or password. Please try again.")

    if st.button("Proceed to bank locker"):
        subprocess.run(["python", "main.py"])

# Function to display the image capture and encoder page
def image_capture_page():
    st.title("Image Capture and Encoder")
    st.image("Resources/Banking.jpeg", use_column_width=True)
    # Display webcam feed
    st.header("Capture Image")
    img_name = st.text_input("Enter image name:")

    if not img_name.strip() == "":
        if st.button("Capture"):
            capture_and_save_image(img_name.strip())
            st.success("Image captured successfully!")

# Streamlit app
def main():
    # Check if the user is logged in
    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False

    # If not logged in, display login page
    if not st.session_state.is_logged_in:
        login_page()
    # If logged in, display image capture page
    else:
        st.button("Go Back to Login Page", on_click=lambda: st.session_state.pop("is_logged_in"))
        image_capture_page()


if __name__ == "__main__":
    main()
