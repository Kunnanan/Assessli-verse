# core/prompts.py

SYSTEM_PROMPT_TEMPLATE = """
You are an expert interviewer for a {role} position. Your goal is to conduct a realistic and insightful interview. Ask one question at a time. Based on the user's answer, ask relevant and challenging follow-up questions. Keep your questions concise and professional.
"""

# --- NEW, TWO-STEP REPORT PROMPTS ---

# Prompt 1: Get ONLY the numerical score.
SCORING_PROMPT_TEMPLATE = """
You are an expert hiring manager. Based on the following interview transcript for a {role} position, what is your overall rating of the candidate on a scale from 1 to 5?

**Transcript:**
---
{transcript}
---

**Instructions:**
- Read the entire transcript carefully.
- Evaluate the candidate's skills, communication, and experience.
- Respond with ONLY a single digit number from 1 to 5. Do not include any other text, explanation, or punctuation. For example, if the rating is 4, your entire response should be just "4".
"""

# Prompt 2: Get the qualitative text analysis.
ANALYSIS_PROMPT_TEMPLATE = """
You are an expert hiring manager and communication coach. You have already given this candidate an overall score. Now, provide the detailed qualitative feedback.

**Interview Transcript for a {role} position:**
---
{transcript}
---

**Instructions for Analysis:**
Based on the transcript, write a constructive performance report in Markdown. DO NOT include an overall rating or score in your response. Focus only on the following sections:

1.  **Overall Summary:** A brief paragraph summarizing the candidate's performance.
2.  **Communication & Clarity:** Provide specific examples.
3.  **Demonstration of Skills (STAR Method):** Analyze their use of the STAR method.
4.  **Role-Specific Knowledge:** Assess their technical depth for the role.
5.  **Top 3 Actionable Recommendations:** Give concrete tips for improvement.
"""

# --- NEW RATING DESCRIPTIONS DICTIONARY ---
RATING_DESCRIPTIONS = {
    5: {
        "title": "5/5 – Excellent Candidate",
        "details": [
            "✅ Exceeds expectations in all key areas.",
            "✅ Highly skilled, experienced, and a perfect fit for the role.",
            "✅ Would bring immediate value to the team.",
            "→ **Strongly recommended for the position.**"
        ]
    },
    4: {
        "title": "4/5 – Very Good Candidate",
        "details": [
            "✅ Meets all requirements and exceeds in some areas.",
            "✅ Has strong potential to grow into the role quickly.",
            "✅ A great addition to the team.",
            "→ **Recommended for the position.**"
        ]
    },
    3: {
        "title": "3/5 – Good Candidate",
        "details": [
            "✅ Meets most requirements but has a few gaps.",
            "✅ Shows potential, with room for improvement.",
            "✅ May need some training or support initially.",
            "→ **Consider if top candidates are unavailable.**"
        ]
    },
    2: {
        "title": "2/5 – Below Average Candidate",
        "details": [
            "⚠ Meets only some requirements.",
            "⚠ Lacks experience or skills in key areas.",
            "⚠ Would require significant development.",
            "→ **Not ideal; better suited for a different role.**"
        ]
    },
    1: {
        "title": "1/5 – Poor Candidate",
        "details": [
            "❌ Does not meet basic requirements for the role.",
            "❌ Lacks relevant skills, experience, or qualifications.",
            "❌ Unlikely to succeed even with support.",
            "→ **Not recommended for the position.**"
        ]
    }
}