
import streamlit as st
import pandas as pd
import hashlib

# --------------------------------------------------
# IMPORT PROJECT MODULES
# --------------------------------------------------

from utils.resume_parser import extract_resume_text
from utils.candidate_profile import extract_candidate_profile
from utils.job_extractor import extract_job_skills
from utils.matcher import compare_skills

from model.text_matcher import calculate_text_similarity
from model.scoring import calculate_final_score
from model.ranker import rank_candidates


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="HireMatch AI",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2rem;
}

[data-testid="stMetric"] {
    background-color: rgba(128,128,128,0.08);
    padding: 18px;
    border-radius: 12px;
    border: 1px solid rgba(128,128,128,0.15);
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🤖 HireMatch AI")

st.subheader("AI Resume Screening & Job Matching System")

st.caption(
    "Analyze resumes, identify skills, compare candidates "
    "and rank profiles against a job description."
)

st.divider()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("🤖 HireMatch AI")

    st.caption("AI Resume Screening System")

    st.divider()

    st.caption("Resume Analysis & Candidate Ranking")


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.header("📄 Resume Analysis")

col1, col2 = st.columns([1, 1])

with col1:

    uploaded_resumes = st.file_uploader(
        "Upload Candidate Resumes (PDF)",
        type=["pdf"],
        accept_multiple_files=True
    )

with col2:

    job_description = st.text_area(
        "Enter Job Description",
        height=220,
        placeholder="Paste the complete job description here..."
    )


# --------------------------------------------------
# ANALYSIS BUTTON
# --------------------------------------------------

if st.button(
    "🚀 Analyze Candidates",
    type="primary",
    use_container_width=True
):

    if not uploaded_resumes:

        st.warning("Please upload at least one resume.")

    elif not job_description.strip():

        st.warning("Please enter a job description.")

    else:

        # ------------------------------------------
        # DUPLICATE DETECTION
        # ------------------------------------------

        unique_resumes = []

        seen_hashes = set()

        duplicate_count = 0

        for resume_file in uploaded_resumes:

            file_bytes = resume_file.getvalue()

            file_hash = hashlib.sha256(
                file_bytes
            ).hexdigest()

            if file_hash in seen_hashes:

                duplicate_count += 1

            else:

                seen_hashes.add(file_hash)

                unique_resumes.append(resume_file)

        st.session_state["duplicate_count"] = duplicate_count


        # ------------------------------------------
        # EXTRACT REQUIRED JOB SKILLS
        # ------------------------------------------

        job_skills = extract_job_skills(job_description)

        st.session_state["job_skills"] = job_skills


        # ------------------------------------------
        # PROCESS UNIQUE CANDIDATES
        # ------------------------------------------

        candidates = []

        progress_bar = st.progress(0)

        status_text = st.empty()

        total_resumes = len(unique_resumes)

        for index, resume_file in enumerate(unique_resumes):

            status_text.write(
                f"Processing {resume_file.name}..."
            )

            try:

                # Reset file pointer
                resume_file.seek(0)

                # Extract resume text
                resume_text = extract_resume_text(resume_file)

                # Extract candidate profile
                profile = extract_candidate_profile(resume_text)

                # Compare skills
                skill_result = compare_skills(
                    profile["skills"],
                    job_skills
                )

                # Calculate TF-IDF similarity
                text_score = calculate_text_similarity(
                    resume_text,
                    job_description
                )

                # Calculate final combined score
                final_score = calculate_final_score(
                    skill_result["matching_score"],
                    text_score
                )

                # Candidate information
                candidate = {

                    "name": resume_file.name,

                    "resume_text": resume_text,

                    "profile": profile,

                    "skill_result": skill_result,

                    "skill_score": skill_result["matching_score"],

                    "text_score": text_score,

                    "final_score": final_score,

                    "match_status": skill_result["match_status"],

                    "skill_report": skill_result["skill_report"]

                }

                candidates.append(candidate)

            except Exception as e:

                st.error(
                    f"Error processing {resume_file.name}: {e}"
                )

            progress_bar.progress(
                (index + 1) / total_resumes
            )

        status_text.empty()

        progress_bar.empty()


        # ------------------------------------------
        # STORE RESULTS
        # ------------------------------------------

        if candidates:

            ranked_candidates = rank_candidates(candidates)

            st.session_state["ranked_candidates"] = ranked_candidates

            st.session_state["analysis_job_description"] = job_description

            st.session_state["analysis_complete"] = True

            st.session_state["job_skills"] = job_skills

            st.success(
                f"Successfully analyzed {len(candidates)} unique candidate(s)."
            )

            if duplicate_count > 0:

                st.info(
                    f"Skipped {duplicate_count} duplicate resume(s)."
                )

        else:

            st.session_state["analysis_complete"] = False

            st.error("No resumes could be successfully analyzed.")


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

if st.session_state.get("analysis_complete", False):

    ranked_candidates = st.session_state["ranked_candidates"]

    job_skills = st.session_state["job_skills"]

    duplicate_count = st.session_state.get(
        "duplicate_count",
        0
    )

    st.divider()

    st.header("📊 Recruitment Dashboard")


    # --------------------------------------------------
    # OVERALL METRICS
    # --------------------------------------------------

    total_candidates = len(ranked_candidates)

    average_score = round(
        sum(
            candidate["final_score"]
            for candidate in ranked_candidates
        ) / total_candidates,
        2
    )

    top_candidate = ranked_candidates[0]

    high_skill_matches = sum(
        1
        for candidate in ranked_candidates
        if candidate["skill_score"] >= 80
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👥 Candidates",
        total_candidates
    )

    col2.metric(
        "📊 Average Score",
        f"{average_score}%"
    )

    col3.metric(
        "🏆 Highest Score",
        f"{top_candidate['final_score']}%"
    )

    col4.metric(
        "🎯 Strong Skill Matches",
        high_skill_matches
    )


    # --------------------------------------------------
    # DUPLICATE INFORMATION
    # --------------------------------------------------

    if duplicate_count > 0:

        st.info(
            f"🔄 {duplicate_count} duplicate resume(s) "
            "were skipped during analysis."
        )


    # --------------------------------------------------
    # REQUIRED JOB SKILLS
    # --------------------------------------------------

    with st.expander("📋 Required Job Skills", expanded=True):

        if job_skills:

            st.write(
                " · ".join(job_skills)
            )

        else:

            st.warning(
                "No skills were detected in the job description."
            )


    # --------------------------------------------------
    # TABS
    # --------------------------------------------------

    tab1, tab2, tab3, tab4 = st.tabs([
        "🏆 Leaderboard",
        "👤 Candidate Profiles",
        "⚖️ Comparison",
        "📥 Reports"
    ])


    # ==================================================
    # TAB 1: LEADERBOARD
    # ==================================================

    with tab1:

        st.subheader("🏆 Candidate Ranking")

        for rank, candidate in enumerate(
            ranked_candidates,
            start=1
        ):

            with st.container(border=True):

                col1, col2 = st.columns([3, 1])

                with col1:

                    st.markdown(
                        f"### {rank}. {candidate['name']}"
                    )

                    st.caption(
                        candidate["match_status"]
                    )

                with col2:

                    st.metric(
                        "Combined Score",
                        f"{candidate['final_score']}%"
                    )

                st.progress(
                    min(
                        max(candidate["final_score"] / 100, 0.0),
                        1.0
                    )
                )

                score_col1, score_col2 = st.columns(2)

                score_col1.metric(
                    "Skill Match",
                    f"{candidate['skill_score']}%"
                )

                score_col2.metric(
                    "Text Similarity",
                    f"{candidate['text_score']}%"
                )

                skill_col1, skill_col2 = st.columns(2)

                with skill_col1:

                    st.markdown("#### 🟢 Matched Skills")

                    matched_skills = (
                        candidate["skill_result"]["matched_skills"]
                    )

                    if matched_skills:

                        for skill in matched_skills:

                            st.markdown(
                                f"- 🟢 {skill}"
                            )

                    else:

                        st.write("No matched skills detected.")

                with skill_col2:

                    st.markdown("#### 🔴 Missing Skills")

                    missing_skills = (
                        candidate["skill_result"]["missing_skills"]
                    )

                    if missing_skills:

                        for skill in missing_skills:

                            st.markdown(
                                f"- 🔴 {skill}"
                            )

                    else:

                        st.write("No missing required skills.")

                st.caption(
                    "Scores are screening indicators, not measures "
                    "of candidate suitability or hiring decisions."
                )


    # ==================================================
    # TAB 2: CANDIDATE PROFILES
    # ==================================================

    with tab2:

        st.subheader("👤 Candidate Details")

        candidate_names = [
            candidate["name"]
            for candidate in ranked_candidates
        ]

        selected_candidate_name = st.selectbox(
            "Select a candidate",
            candidate_names
        )

        selected_candidate = next(
            candidate
            for candidate in ranked_candidates
            if candidate["name"] == selected_candidate_name
        )

        st.divider()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Combined Score",
            f"{selected_candidate['final_score']}%"
        )

        col2.metric(
            "Skill Match",
            f"{selected_candidate['skill_score']}%"
        )

        col3.metric(
            "Text Similarity",
            f"{selected_candidate['text_score']}%"
        )

        st.progress(
            min(
                max(selected_candidate["final_score"] / 100, 0.0),
                1.0
            )
        )

        st.markdown("### 🟢 Matched Skills")

        matched_skills = (
            selected_candidate["skill_result"]["matched_skills"]
        )

        if matched_skills:

            st.write(" · ".join(matched_skills))

        else:

            st.info("No matched skills detected.")

        st.markdown("### 🔴 Missing Skills")

        missing_skills = (
            selected_candidate["skill_result"]["missing_skills"]
        )

        if missing_skills:

            st.write(" · ".join(missing_skills))

        else:

            st.success("No missing required skills detected.")

        st.markdown("### 🎓 Education")

        education = selected_candidate["profile"]["education"]

        if education:

            for item in education:

                st.write(f"- {item}")

        else:

            st.info("No education information detected.")

        st.markdown("### 💼 Experience")

        experience = selected_candidate["profile"]["experience"]

        if experience:

            for item in experience:

                st.write(f"- {item}")

        else:

            st.info("No experience information detected.")

        st.markdown("### 📋 Detailed Skill Report")

        skill_report = (
            selected_candidate["skill_report"]
        )

        if skill_report:

            skill_report_df = pd.DataFrame(skill_report)

            st.dataframe(
                skill_report_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No required skills to report.")

        with st.expander("📄 Extracted Resume Text"):

            st.text(
                selected_candidate["resume_text"]
            )


    # ==================================================
    # TAB 3: CANDIDATE COMPARISON
    # ==================================================

    with tab3:

        st.subheader("⚖️ Candidate Comparison")

        candidate_names = [
            candidate["name"]
            for candidate in ranked_candidates
        ]

        selected_candidates = st.multiselect(
            "Select candidates to compare",
            options=candidate_names,
            default=candidate_names[:2]
        )

        comparison_data = []

        for candidate in ranked_candidates:

            if candidate["name"] in selected_candidates:

                comparison_data.append({

                    "Candidate": candidate["name"],

                    "Combined Score (%)": candidate["final_score"],

                    "Skill Match (%)": candidate["skill_score"],

                    "Text Similarity (%)": candidate["text_score"],

                    "Match Status": candidate["match_status"],

                    "Matched Skills": ", ".join(
                        candidate["skill_result"]["matched_skills"]
                    ),

                    "Missing Skills": ", ".join(
                        candidate["skill_result"]["missing_skills"]
                    ),

                    "Education": ", ".join(
                        candidate["profile"]["education"]
                    ),

                    "Experience": ", ".join(
                        candidate["profile"]["experience"]
                    )

                })

        if comparison_data:

            comparison_df = pd.DataFrame(
                comparison_data
            )

            st.dataframe(
                comparison_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("Select candidates to compare.")


    # ==================================================
    # TAB 4: CSV REPORTS
    # ==================================================

    with tab4:

        st.subheader("📥 Candidate Ranking Report")

        ranking_data = []

        for rank, candidate in enumerate(
            ranked_candidates,
            start=1
        ):

            ranking_data.append({

                "Rank": rank,

                "Candidate": candidate["name"],

                "Combined Score (%)": candidate["final_score"],

                "Skill Match (%)": candidate["skill_score"],

                "Text Similarity (%)": candidate["text_score"],

                "Match Status": candidate["match_status"],

                "Matched Skills": ", ".join(
                    candidate["skill_result"]["matched_skills"]
                ),

                "Missing Skills": ", ".join(
                    candidate["skill_result"]["missing_skills"]
                ),

                "Education": ", ".join(
                    candidate["profile"]["education"]
                ),

                "Experience": ", ".join(
                    candidate["profile"]["experience"]
                )

            })

        ranking_df = pd.DataFrame(ranking_data)

        st.dataframe(
            ranking_df,
            use_container_width=True,
            hide_index=True
        )

        csv_data = ranking_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download Ranking Report (CSV)",
            data=csv_data,
            file_name="hirematch_candidate_ranking.csv",
            mime="text/csv",
            use_container_width=True
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "HireMatch AI | AI Resume Screening & Job Matching System"
)

st.caption(
    "This tool provides automated screening indicators. "
    "It should not be used as the sole basis for hiring, "
    "rejection or other employment decisions."
)
