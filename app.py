"""
Self-Improving RAG Content Generator
Streamlit Frontend
"""

from __future__ import annotations

import inspect
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from memory import save_failure


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent

LOG_FILE = PROJECT_DIR / "logs" / "rejection_logs.json"


# --------------------------------------------------
# 2. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Self-Improving RAG Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# 3. FRONTEND STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.6rem;
        padding-bottom: 2.5rem;
    }

    div[data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,.20);
        border-radius: 12px;
        padding: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# 4. GENERATOR CONNECTION
# --------------------------------------------------

def _find_generator():

    import generator

    preferred = (
        "generate_content",
        "generate_lesson",
        "generate_rag_content",
        "generate",
    )

    for name in preferred:

        candidate = getattr(generator, name, None)

        if callable(candidate):
            return candidate, name

    for name, candidate in vars(generator).items():

        if (
            callable(candidate)
            and not name.startswith("_")
            and any(
                word in name.lower()
                for word in ("generate", "create")
            )
        ):
            return candidate, name

    raise RuntimeError(
        "No suitable generation function was found "
        "inside generator.py."
    )


# --------------------------------------------------
# 5. PASS INPUT TO GENERATOR
# --------------------------------------------------

def _call_generator(
    topic: str,
    audience: str,
    depth: str,
    extra_instructions: str
):

    fn, fn_name = _find_generator()

    signature = inspect.signature(fn)

    values = {
        "topic": topic,
        "subject": topic,
        "query": topic,
        "prompt": topic,
        "user_prompt": topic,
        "audience": audience,
        "level": audience,
        "difficulty": audience,
        "depth": depth,
        "detail_level": depth,
        "extra_instructions": extra_instructions,
        "instructions": extra_instructions,
    }

    kwargs = {}
    positional = []

    for param in signature.parameters.values():

        if param.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD
        ):
            continue

        if param.name in values:

            if param.kind == inspect.Parameter.POSITIONAL_ONLY:
                positional.append(values[param.name])

            else:
                kwargs[param.name] = values[param.name]

        elif param.default is inspect.Parameter.empty:

            if not positional and not kwargs:

                if param.kind == inspect.Parameter.POSITIONAL_ONLY:
                    positional.append(topic)

                else:
                    kwargs[param.name] = topic

            else:
                raise RuntimeError(
                    f"Unsupported required parameter: {param.name}"
                )

    result = fn(*positional, **kwargs)

    if isinstance(result, str):
        return result, fn_name

    if result is None:
        raise RuntimeError(
            f"{fn_name} returned no content."
        )

    return str(result), fn_name


# --------------------------------------------------
# 6. EVALUATOR CONNECTION
# --------------------------------------------------

def _evaluate(content: str):

    import evaluator

    fn = getattr(
        evaluator,
        "evaluate_content",
        None
    )

    if not callable(fn):

        raise RuntimeError(
            "evaluator.py does not expose "
            "evaluate_content(content)."
        )

    return fn(content)


# --------------------------------------------------
# 7. READ REJECTION LOGS
# --------------------------------------------------

def _read_rejection_logs():

    if not LOG_FILE.exists():
        return []

    try:

        raw = json.loads(
            LOG_FILE.read_text(encoding="utf-8")
        )

        if isinstance(raw, list):
            return raw

        if isinstance(raw, dict):

            for key in (
                "logs",
                "rejections",
                "records",
                "history"
            ):

                if isinstance(raw.get(key), list):
                    return raw[key]

            return [raw]

    except Exception:
        return []

    return []


# --------------------------------------------------
# 8. EXTRACT EVALUATION STATUS
# --------------------------------------------------

def _extract_status(result: Any):

    if isinstance(result, dict):

        return str(
            result.get(
                "overall_status",
                result.get("status", "UNKNOWN")
            )
        ).upper()

    return "UNKNOWN"


def _extract_criteria(result: Any):

    if isinstance(result, dict):

        criteria = result.get("criteria", [])

        if isinstance(criteria, list):
            return criteria

    return []


# --------------------------------------------------
# 9. DISPLAY EVALUATION REPORT
# --------------------------------------------------

def _render_evaluation(result: Any):

    status = _extract_status(result)

    criteria = _extract_criteria(result)

    if status == "PASS":

        st.success(
            "Evaluation passed! Content meets the criteria."
        )

    elif status == "FAIL":

        st.error(
            "Evaluation failed. Review the feedback."
        )

    else:

        st.info(
            "Evaluation completed. Review the response below."
        )

    if criteria:

        rows = []

        for item in criteria:

            if isinstance(item, dict):

                rows.append({

                    "Criterion": item.get(
                        "criterion_id",
                        "Criterion"
                    ),

                    "Result": str(
                        item.get("status", "UNKNOWN")
                    ).upper(),

                    "Feedback": item.get(
                        "reason",
                        ""
                    ),

                })

        if rows:

            st.dataframe(
                rows,
                use_container_width=True,
                hide_index=True
            )

    with st.expander("View complete evaluator response"):

        st.json(
            result
            if isinstance(result, (dict, list))
            else {"result": str(result)}
        )


# --------------------------------------------------
# 10. SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:

    st.title("🧠 Project Menu")

    page = st.radio(
        "Navigate",

        [
            "Generate & Evaluate",
            "Rejection Memory",
            "Project Overview"
        ],

        label_visibility="collapsed"
    )

    st.divider()

    st.caption(
        "Self-Improving RAG Content Generator"
    )

    st.caption(
        "Python · Gemini · RAG · Evaluation · Memory"
    )


# --------------------------------------------------
# 11. MAIN PAGE HEADER
# --------------------------------------------------

st.title("🧠 Self-Improving RAG Content Generator")

st.write(
    "Generate learning content, evaluate its quality, "
    "and use feedback to improve future outputs."
)

st.divider()


# --------------------------------------------------
# 12. SESSION STATE
# --------------------------------------------------

if "generated_content" not in st.session_state:

    st.session_state.generated_content = ""


if "evaluation_result" not in st.session_state:

    st.session_state.evaluation_result = None


if "last_generator" not in st.session_state:

    st.session_state.last_generator = ""


# --------------------------------------------------
# 13. GENERATE AND EVALUATE PAGE
# --------------------------------------------------

if page == "Generate & Evaluate":

    st.subheader("Create Learning Content")

    st.write(
        "Enter a topic to generate and evaluate content."
    )

    with st.form("generation_form"):

        topic = st.text_input(
            "Enter Topic",

            placeholder="Example: Retrieval-Augmented Generation"
        )

        col_a, col_b = st.columns(2)

        with col_a:

            audience = st.selectbox(
                "Target Audience",

                [
                    "Beginner",
                    "Intermediate",
                    "Advanced"
                ],

                index=0
            )

        with col_b:

            depth = st.selectbox(
                "Content Depth",

                [
                    "Short overview",
                    "Detailed lesson",
                    "Step-by-step tutorial"
                ],

                index=1
            )

        extra = st.text_area(
            "Additional Instructions",

            placeholder=(
                "Example: Include a simple real-world example."
            ),

            height=90
        )

        submitted = st.form_submit_button(
            "✨ Generate and Evaluate",

            type="primary",

            use_container_width=True
        )


    # --------------------------------------------------
    # 14. GENERATE CONTENT
    # --------------------------------------------------

    if submitted:

        if not topic.strip():

            st.warning(
                "Please enter a topic first."
            )

        else:

            try:

                with st.spinner(
                    "Generating content..."
                ):

                    content, generator_name = _call_generator(
                        topic.strip(),
                        audience,
                        depth,
                        extra.strip()
                    )

                st.session_state.generated_content = content

                st.session_state.last_generator = generator_name

                # --------------------------------------
                # 15. EVALUATE GENERATED CONTENT
                # --------------------------------------

                with st.spinner(
                    "Evaluating generated content..."
                ):

                    evaluation = _evaluate(content)

                st.session_state.evaluation_result = evaluation

                # --------------------------------------
                # 16. SAVE REJECTED CONTENT
                # --------------------------------------

                status = _extract_status(evaluation)

                if status == "FAIL":

                    if not isinstance(evaluation, dict):
                        raise ValueError(
                            "Evaluator returned FAIL but its response "
                            "is not a dictionary."
                        )

                    saved = save_failure(
                        content=content,
                        evaluation=evaluation,
                        topic=topic.strip()
                    )

                    if saved:

                        st.warning(
                            "Content rejected. Feedback saved "
                            "to rejection memory."
                        )

                    else:

                        st.error(
                            "Failed content could not be saved."
                        )

                elif status == "PASS":

                    st.success(
                        "Content passed evaluation. "
                        "No rejection record was added."
                    )

                st.toast(
                    "Generation and evaluation completed.",
                    icon="✅"
                )

            except Exception as exc:

                st.error(
                    "The frontend could not complete the backend workflow."
                )

                st.exception(exc)

                st.info(
                    "Check the generator and evaluator function "
                    "names and parameters in the backend adapter."
                )


    # --------------------------------------------------
    # 17. DISPLAY GENERATED CONTENT
    # --------------------------------------------------

    if st.session_state.generated_content:

        st.divider()

        st.subheader("Generated Content")

        if st.session_state.last_generator:

            st.caption(
                f"Generator function: "
                f"{st.session_state.last_generator}"
            )

        st.text_area(
            "Content Output",

            value=st.session_state.generated_content,

            height=360,

            key="content_display"
        )

        st.download_button(
            "⬇️ Download Generated Content",

            data=st.session_state.generated_content,

            file_name="generated_rag_content.md",

            mime="text/markdown"
        )


    # --------------------------------------------------
    # 18. DISPLAY EVALUATION RESULTS
    # --------------------------------------------------

    if st.session_state.evaluation_result is not None:

        st.divider()

        st.subheader("Evaluation Report")

        _render_evaluation(
            st.session_state.evaluation_result
        )


# --------------------------------------------------
# 19. REJECTION MEMORY PAGE
# --------------------------------------------------

elif page == "Rejection Memory":

    st.subheader("Rejection Memory")

    st.write(
        "View previously saved rejection records."
    )

    records = _read_rejection_logs()

    col1, col2 = st.columns(2)

    col1.metric(
        "Recorded Log Entries",
        len(records)
    )

    col2.metric(
        "Log File",
        "Found" if LOG_FILE.exists() else "Not Found"
    )

    if records:

        st.caption(
            "Source: logs/rejection_logs.json"
        )

        st.json(records)

        st.download_button(
            "⬇️ Download Rejection Logs",

            data=json.dumps(
                records,
                indent=2,
                ensure_ascii=False
            ),

            file_name="rejection_logs.json",

            mime="application/json"
        )

    else:

        st.info(
            "No readable rejection records were found yet."
        )


# --------------------------------------------------
# 20. PROJECT OVERVIEW PAGE
# --------------------------------------------------

else:

    st.subheader("How the Project Works")

    steps = [

        (
            "1. Generate",
            "Gemini generates content using the available "
            "knowledge-base context."
        ),

        (
            "2. Evaluate",
            "The evaluator checks generated content "
            "against quality criteria."
        ),

        (
            "3. Reject and Record",
            "Failed content is rejected and feedback "
            "is saved in rejection logs."
        ),

        (
            "4. Retrieve Memory",
            "The generator retrieves previous failure "
            "information."
        ),

        (
            "5. Improve",
            "The generator uses feedback to create "
            "improved content."
        ),

        (
            "6. Re-evaluate",
            "The revised content can be evaluated again."
        ),

    ]

    for title, description in steps:

        with st.container(border=True):

            st.markdown(
                f"**{title}**"
            )

            st.write(description)


    st.divider()

    st.subheader("Project Components")

    components = [

        (
            "generator.py",
            "Generates content using Gemini."
        ),

        (
            "prompts.py",
            "Stores generation and evaluation prompts."
        ),

        (
            "evaluator.py",
            "Evaluates generated content."
        ),

        (
            "memory.py",
            "Handles previous failure information."
        ),

        (
            "knowledge_base/rag_reference.md",
            "Contains reference material."
        ),

        (
            "logs/rejection_logs.json",
            "Stores rejection records."
        ),

        (
            "app.py",
            "Provides the frontend interface."
        ),

    ]

    st.table(

        [
            {
                "File / Area": name,
                "Purpose": purpose
            }

            for name, purpose in components
        ]

    )

    st.info(
        "The frontend provides an interface to your "
        "existing Python backend."
    )


# --------------------------------------------------
# 21. FOOTER
# --------------------------------------------------

st.divider()

st.caption(

    f"Self-Improving RAG Content Generator · "
    f"{datetime.now().year} · Frontend Interface"

)
