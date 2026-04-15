import streamlit as st
import requests
from bs4 import BeautifulSoup

# Page config
st.set_page_config(page_title="SEO Doctor AI", layout="wide")

# Custom styling
st.markdown("""
<style>
.big-title {
    font-size:40px !important;
    font-weight:700;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="big-title">🔍 SEO Doctor AI</p>', unsafe_allow_html=True)
st.caption("Analyze your website like a pro 🚀")

# Input
url = st.text_input("Enter Website URL (with https://)")

# Scraper function
def scrape(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title else "No title"

        meta = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta.get("content") if meta and meta.get("content") else "No meta description"

        content = soup.get_text()
        word_count = len(content.split())

        images = soup.find_all("img")

        return title, meta_desc, word_count, images

    except:
        return None, None, None, None


# Main button
if st.button("Analyze"):

    if not url.startswith("http"):
        st.error("Enter valid URL (with http/https)")
    else:
        with st.spinner("Analyzing website..."):

            title, meta_desc, word_count, images = scrape(url)

            if title is None:
                st.error("Unable to fetch website")
            else:
                issues = []

                # SEO checks
                if len(title) < 50:
                    issues.append("Title too short")

                if meta_desc == "No meta description":
                    issues.append("Meta description missing")

                if word_count < 300:
                    issues.append("Content too short")

                missing_alt = sum(1 for img in images if not img.get("alt"))
                if missing_alt > 0:
                    issues.append(f"{missing_alt} images missing ALT tags")

                score = max(100 - len(issues)*10, 0)

                # Dashboard
                st.subheader("📊 Dashboard")

                col1, col2, col3, col4 = st.columns(4)

                col1.metric("SEO Score", f"{score}/100")
                col2.metric("Word Count", word_count)
                col3.metric("Images", len(images))
                col4.metric("Issues", len(issues))

                st.progress(score / 100)

                # Website overview
                st.subheader("🌐 Website Overview")
                st.write("**Title:**", title)
                st.write("**Meta Description:**", meta_desc[:150])

                # Issues
                st.subheader("❌ Issues Found")

                if issues:
                    for i in issues:
                        st.write("❌", i)
                else:
                    st.write("No major issues 🎉")

                # Insights
                st.subheader("🔍 SEO Insight")

                if score > 80:
                    st.success("Your website SEO is strong 👍")
                elif score > 50:
                    st.warning("Your website needs improvement ⚠️")
                else:
                    st.error("Your website has poor SEO ❌")

                # Recommendations
                st.subheader("💡 Recommendations")

                for issue in issues:
                    if "Title" in issue:
                        st.write("👉 Improve title length to 50–60 characters")
                    elif "Meta" in issue:
                        st.write("👉 Add meta description (150–160 characters)")
                    elif "Content" in issue:
                        st.write("👉 Increase content depth (800+ words)")
                    elif "ALT" in issue:
                        st.write("👉 Add ALT text to images for SEO")
