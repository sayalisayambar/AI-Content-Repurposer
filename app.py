import streamlit as st
from google import genai

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Content Repurposer",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# GEMINI CLIENT
# -----------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("Gemini API key is not configured correctly.")
    st.stop()

MODEL = "gemini-3.5-flash"


# -----------------------------
# AI GENERATION FUNCTION
# -----------------------------
def generate_content(prompt):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text


# -----------------------------
# CONTENT UNDERSTANDING
# -----------------------------
def understand_content(content):

    prompt = f"""
You are an AI content analysis assistant.

Analyze the following original content:

-------------------------
{content}
-------------------------

Extract:

1. Main Topic
2. Main Message
3. 3-5 Key Points
4. Target Audience
5. Tone
6. Important Keywords
7. Suggested Content Angle

Rules:
- Use only information present in the original content.
- Do not invent facts.
- Keep the analysis concise and clear.
"""

    return generate_content(prompt)


# -----------------------------
# PLATFORM REPURPOSING
# -----------------------------
def repurpose_content(content, platform):

    instructions = {

        "Instagram": """
Create:
1. Instagram caption
2. Short Reel hook/script
3. 5-8 relevant hashtags
4. Call-to-action

Make it engaging, readable and suitable for Instagram.
""",

        "LinkedIn": """
Create:
1. Professional LinkedIn post
2. Strong opening hook
3. 3-5 relevant hashtags
4. Call-to-action

Make it informative, professional and discussion-friendly.
""",

        "X": """
Create:
1. A concise X post
2. If useful, create a 3-post thread
3. 2-4 relevant hashtags
4. Call-to-action

Keep it concise and engaging.
""",

        "YouTube": """
Create:
1. Attention-grabbing YouTube title
2. YouTube description
3. 5 relevant keywords/tags
4. Short video hook

Keep the title interesting but accurate.
"""
    }

    prompt = f"""
You are an AI social media content repurposing assistant.

ORIGINAL CONTENT:
-------------------------
{content}
-------------------------

TARGET PLATFORM:
{platform}

TASK:
Repurpose the original content specifically for {platform}.

{instructions[platform]}

IMPORTANT RULES:
- Preserve the original meaning.
- Do not invent facts.
- Do not copy the original text word-for-word.
- Adapt the content to the platform.
- Make the output ready to publish.
"""

    return generate_content(prompt)


# -----------------------------
# UI
# -----------------------------
st.title("🤖 AI-Based Social Media Content Repurposing System")

st.write(
    "Transform one original piece of content into "
    "platform-specific content for Instagram, LinkedIn, X and YouTube."
)

st.divider()

# -----------------------------
# INPUT
# -----------------------------
st.subheader("📝 Enter Your Original Content")

content = st.text_area(
    "Paste your content below:",
    height=250,
    placeholder="Example: Artificial intelligence is changing the way students learn..."
)

# -----------------------------
# PLATFORM SELECTION
# -----------------------------
st.subheader("🎯 Select Platforms")

platforms = st.multiselect(
    "Choose the platforms you want to generate content for:",
    ["Instagram", "LinkedIn", "X", "YouTube"],
    default=["Instagram", "LinkedIn", "X", "YouTube"]
)

# -----------------------------
# GENERATE BUTTON
# -----------------------------
if st.button("🚀 Repurpose Content", use_container_width=True):

    if not content.strip():
        st.warning("Please enter some original content first.")

    elif not platforms:
        st.warning("Please select at least one platform.")

    else:

        # -----------------------------
        # CONTENT UNDERSTANDING
        # -----------------------------
        st.subheader("🧠 AI Content Understanding")

        with st.spinner("AI is understanding your content..."):
            analysis = understand_content(content)

        st.markdown(analysis)

        st.divider()

        # -----------------------------
        # PLATFORM CONTENT
        # -----------------------------
        st.subheader("📱 Platform-Specific Content")

        for platform in platforms:

            with st.expander(f"✨ {platform}", expanded=True):

                with st.spinner(f"Generating {platform} content..."):

                    result = repurpose_content(
                        content,
                        platform
                    )

                st.markdown(result)

                st.download_button(
                    label=f"⬇️ Download {platform} Content",
                    data=result,
                    file_name=f"{platform.lower()}_content.txt",
                    mime="text/plain"
                )

        st.success(
            "🎉 Content repurposing completed successfully!"
        )

        st.divider()

        st.info(
            "💡 One original content → AI understanding → "
            "platform-specific optimization → ready-to-use content"
        )
