import time
import av
import cv2
import streamlit as st

from streamlit_webrtc import webrtc_streamer

from gesture.gesture_engine import GestureEngine
from gesture.shared_state import SharedState

from speech.speech_to_text import SpeechToText
from speech.speech_queue import SpeechQueue


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SignBridge",
    page_icon="🤝",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "gesture_engine" not in st.session_state:
    st.session_state["gesture_engine"] = GestureEngine()

if "shared_state" not in st.session_state:
    st.session_state["shared_state"] = SharedState()

if "stt" not in st.session_state:
    st.session_state["stt"] = SpeechToText()

if "speech_queue" not in st.session_state:
    st.session_state["speech_queue"] = SpeechQueue()

if "conversation" not in st.session_state:
    st.session_state["conversation"] = []

if "last_gesture" not in st.session_state:
    st.session_state["last_gesture"] = None


engine = st.session_state["gesture_engine"]
shared_state = st.session_state["shared_state"]
speech_queue = st.session_state["speech_queue"]


# ============================================================
# TITLE
# ============================================================

st.title("🤝 SignBridge")

st.subheader("Breaking communication barriers")

st.write(
    "Real-time communication between sign language "
    "and spoken language."
)

st.divider()


# ============================================================
# MAIN COLUMNS
# ============================================================

col1, col2 = st.columns(2)


# ============================================================
# SIGN → SPEECH
# ============================================================

with col1:

    st.header("🖐️ Sign → Speech")

    st.write(
        "Use your camera to communicate using hand gestures."
    )


    def video_frame_callback(frame):

        image = frame.to_ndarray(
            format="bgr24"
        )

        timestamp_ms = int(
            time.time() * 1000
        )

        detected = engine.process_frame(
            image,
            timestamp_ms
        )

        shared_state.update(detected)


        # ----------------------------------------------------
        # DISPLAY GESTURE ON CAMERA
        # ----------------------------------------------------

        if detected["gesture"]:

            cv2.putText(
                image,
                (
                    f"{detected['gesture']} "
                    f"({detected['confidence']:.0%})"
                ),
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )


        # ----------------------------------------------------
        # DISPLAY EMERGENCY ON CAMERA
        # ----------------------------------------------------

        if detected["emergency"]:

            cv2.putText(
                image,
                "!!! EMERGENCY !!!",
                (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3
            )


        return av.VideoFrame.from_ndarray(
            image,
            format="bgr24"
        )


    webrtc_streamer(
        key="signbridge-camera",
        video_frame_callback=video_frame_callback,
        media_stream_constraints={
            "video": True,
            "audio": False
        }
    )


# ============================================================
# SPEECH → TEXT
# ============================================================

with col2:

    st.header("🎤 Speech → Text")

    st.write(
        "Speak into the microphone and SignBridge "
        "will convert your speech into text."
    )


    if st.button("🎙️ Start Listening"):

        with st.spinner("Listening..."):

            text = st.session_state["stt"].listen()


        if text:

            st.success(
                f"📝 You said: {text}"
            )

            st.session_state["conversation"].append({
                "sender": "speech",
                "text": text
            })

        else:

            st.warning(
                "Sorry, I couldn't understand that."
            )


# ============================================================
# AUTOMATIC GESTURE PROCESSING
# ============================================================

@st.fragment(run_every="1s")
def process_gesture():

    current_result = shared_state.get()


    # --------------------------------------------------------
    # CURRENT STATUS
    # --------------------------------------------------------

    if current_result["emergency"]:

        st.error(
            f"🚨 EMERGENCY: {current_result['message']}"
        )

    elif current_result["gesture"]:

        st.success(
            f"🖐️ Detected: "
            f"{current_result['gesture']} "
            f"({current_result['confidence']:.0%})"
        )

    else:

        st.info(
            "🟢 Ready for communication"
        )


    # --------------------------------------------------------
    # PROCESS CONFIRMED GESTURE
    # --------------------------------------------------------

    if current_result["triggered"]:

        message = current_result["message"]


        if message:

            # ------------------------------------------------
            # Prevent duplicate messages
            # ------------------------------------------------

            if message != st.session_state["last_gesture"]:

                st.session_state["conversation"].append({
                    "sender": "sign",
                    "text": message
                })

                st.session_state["last_gesture"] = message


                # --------------------------------------------
                # SPEAK GESTURE
                # --------------------------------------------

                speech_queue.speak(
                    message
                )


                st.success(
                    f"🔊 Speaking: {message}"
                )


process_gesture()


# ============================================================
# COMMUNICATION HISTORY
# ============================================================

st.divider()

st.header("💬 Communication History")


conversation = st.session_state["conversation"]


if not conversation:

    st.info(
        "No messages yet. Start communicating!"
    )

else:

    for message in conversation:

        if message["sender"] == "sign":

            st.success(
                f"🖐️ Sign: {message['text']}"
            )

        elif message["sender"] == "speech":

            st.info(
                f"🎤 Speech: {message['text']}"
            )


# ============================================================
# CLEAR HISTORY
# ============================================================

if conversation:

    if st.button("🗑️ Clear Conversation"):

        st.session_state["conversation"] = []

        st.session_state["last_gesture"] = None

        st.rerun()