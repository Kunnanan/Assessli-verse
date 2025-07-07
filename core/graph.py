# core/graph.py 

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

from core.prompts import ANALYSIS_PROMPT_TEMPLATE, RATING_DESCRIPTIONS, SCORING_PROMPT_TEMPLATE, SYSTEM_PROMPT_TEMPLATE

# Initialize the Groq models
llm = ChatGroq(model_name="llama3-8b-8192", temperature=0.7)
report_llm = ChatGroq(model_name="llama3-70b-8192", temperature=0.5)

def get_agent_response(role: str, conversation_history: list):
    """Gets the next response from the LLM."""
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(role=role)
    messages = [HumanMessage(content=system_prompt)] + conversation_history
    response = llm.invoke(messages)
    return response

def get_final_report(role: str, conversation_history: list) -> str:
    """Generates the final report using the two-step process."""
    transcript = "\n".join([f"{msg.type.replace('human', 'Candidate').replace('ai', 'Interviewer')}: {msg.content}" for msg in conversation_history])
    
    # STEP 1: Get the numerical score from the AI
    scoring_prompt = SCORING_PROMPT_TEMPLATE.format(transcript=transcript, role=role)
    score_response = report_llm.invoke(scoring_prompt).content
    try:
        score = int(score_response.strip())
        if score < 1 or score > 5: score = 3
    except (ValueError, TypeError):
        score = 3

    # STEP 2: Get the qualitative analysis from the AI
    analysis_prompt = ANALYSIS_PROMPT_TEMPLATE.format(transcript=transcript, role=role)
    analysis_text = report_llm.invoke(analysis_prompt).content

    # --- THIS IS THE NEW, POLISHED REPORT FORMATTING ---
    # Add icons and proper subheaders to the analysis text
    analysis_text = analysis_text.replace("Overall Summary", "### 🎯 Overall Summary")
    analysis_text = analysis_text.replace("Communication & Clarity", "### 🗣️ Communication & Clarity")
    analysis_text = analysis_text.replace("Demonstration of Skills (STAR Method)", "### 🛠️ Demonstration of Skills (STAR Method)")
    analysis_text = analysis_text.replace("Role-Specific Knowledge", "### 📚 Role-Specific Knowledge")
    analysis_text = analysis_text.replace("Top 3 Actionable Recommendations", "### 💡 Top 3 Actionable Recommendations")
    
    # Create the big star rating string
    star_rating = "★" * score + "☆" * (5 - score)
    rating_info = RATING_DESCRIPTIONS.get(score, RATING_DESCRIPTIONS[3])
    rating_title = rating_info["title"]
    rating_details_html = "".join([f"<div>{item}</div>" for item in rating_info["details"]])

    # Assemble the final report string
    full_report = f"""
<div style="text-align: center; font-size: 5em; letter-spacing: 0.2em; color: #FFD700;">{star_rating}</div>
<div style="text-align: center; margin-bottom: 2em; padding: 1.5em; border: 1px solid #444; border-radius: 10px; background-color: #1E1E1E;">
    <h3>{rating_title}</h3>
    <div style="text-align: left; display: inline-block;">{rating_details_html}</div>
</div>
<hr>
{analysis_text}
"""
    return full_report