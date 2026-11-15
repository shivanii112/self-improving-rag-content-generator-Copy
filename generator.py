"""
Self-Improving RAG Content Generator
Gemini-powered content generation with rejection memory.
"""

from pathlib import Path

from google.genai import errors

from config import get_client, GEMINI_MODEL
from prompts import GENERATION_PROMPT
from memory import get_recent_failures


# --------------------------------------------------
# 1. LOAD KNOWLEDGE BASE
# --------------------------------------------------

def load_knowledge_base():
    """Read the RAG reference material."""

    file_path = (
        Path(__file__).parent
        / "knowledge_base"
        / "rag_reference.md"
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"RAG reference file not found: {file_path}"
        )

    context = file_path.read_text(encoding="utf-8")

    if not context.strip():
        raise ValueError("Knowledge base is empty.")

    return context


# --------------------------------------------------
# 2. RETRIEVE PREVIOUS FAILURE FEEDBACK
# --------------------------------------------------

def get_memory_feedback():
    """Retrieve previous failures from persistent memory."""

    failures = get_recent_failures(limit=5)

    if not failures:
        return ""

    feedback_parts = []

    for index, failure in enumerate(failures, start=1):

        if not isinstance(failure, dict):
            continue

        feedback_parts.append(
            f"\nPrevious Failure {index}:"
        )

        feedback_parts.append(
            f"Topic: {failure.get('topic', 'Unknown')}"
        )

        failed_criteria = failure.get(
            "failed_criteria", []
        )

        for criterion in failed_criteria:

            if not isinstance(criterion, dict):
                continue

            feedback_parts.append(
                f"Failed Criterion: "
                f"{criterion.get('criterion_id', 'Unknown')}"
            )

            feedback_parts.append(
                f"Reason: "
                f"{criterion.get('reason', 'Not provided')}"
            )

            feedback_parts.append(
                f"Improvement Suggestion: "
                f"{criterion.get('improvement_suggestion', 'Not provided')}"
            )

    return "\n".join(feedback_parts)


# --------------------------------------------------
# 3. GENERATE LEARNING CONTENT
# --------------------------------------------------

def generate_lesson(topic="Retrieval-Augmented Generation",
                    feedback=None):
    """
    Generate beginner-friendly learning content using Gemini.

    Retrieves previous rejection feedback and uses it
    to improve future content.
    """

    if not topic or not str(topic).strip():
        raise ValueError("Please provide a valid topic.")

    topic = str(topic).strip()

    # Initialize Gemini client
    client = get_client()

    # Load RAG knowledge base
    context = load_knowledge_base()

    # Prepare generation prompt
    prompt = GENERATION_PROMPT.replace(
        "{context}", context
    )

    # Add the requested topic
    prompt += f"""

LEARNING TOPIC:
{topic}

GENERATION REQUIREMENTS:

1. Generate actual educational learning content.
2. Explain the topic in beginner-friendly language.
3. Use accurate information from the supplied knowledge base.
4. Include clear definitions and explanations.
5. Include practical examples wherever relevant.
6. Organize the content using meaningful headings.
7. Do not generate placeholder text.
8. Do not simply describe the generator function.
9. Do not invent facts that are unsupported by the reference material.
10. Make the content useful for someone learning this topic.
"""

    # Retrieve previous rejection feedback
    memory_feedback = get_memory_feedback()

    combined_feedback = []

    if feedback:
        combined_feedback.append(
            f"Additional User Feedback:\n{feedback}"
        )

    if memory_feedback:
        combined_feedback.append(
            f"Previous Rejection Memory:\n{memory_feedback}"
        )

    # Add feedback to prompt
    if combined_feedback:

        prompt += f"""

PREVIOUS EVALUATION FEEDBACK:

{" ".join(combined_feedback)}

IMPORTANT IMPROVEMENT INSTRUCTIONS:

1. Carefully review previous evaluation failures.
2. Avoid repeating previously identified mistakes.
3. Follow the improvement suggestions.
4. Prioritize accuracy and groundedness.
5. Generate improved educational content.
"""

    # Send request to Gemini
    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        # Validate Gemini response
        if not response.text or not response.text.strip():

            raise ValueError(
                "Gemini returned an empty response."
            )

        return response.text.strip()

    except errors.ClientError as error:

        if error.code == 429:

            raise RuntimeError(
                "Gemini API quota exceeded. "
                "Please wait until your quota resets."
            ) from error

        raise RuntimeError(
            f"Gemini API request failed: {error}"
        ) from error
