import json

from config import get_client, GEMINI_MODEL
from prompts import EVALUATION_PROMPT


# The evaluator must return exactly these six criteria.
EXPECTED_CRITERIA = {
    "accuracy_and_groundedness",
    "beginner_friendly",
    "teaching_by_example",
    "clear_language_and_jargon",
    "key_topic_coverage",
    "teaching_flow",
}


def evaluate_content(content):
    """
    Evaluate generated lesson content against
    six mandatory quality criteria.
    """

    client = get_client()

    prompt = f"""
    {EVALUATION_PROMPT}

    CONTENT TO EVALUATE:

    {content}

    Important:
    Return exactly six criteria.
    Include each expected criterion ID only once.
    Return valid JSON using the required structure.
    """

    # Ask Gemini to evaluate the lesson.
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    if not response.text:
        raise ValueError(
            "Evaluator returned an empty response."
        )

    # Convert Gemini's JSON response into a Python dictionary.
    try:
        result = json.loads(response.text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Evaluator returned invalid JSON."
        ) from exc

    if not isinstance(result, dict):
        raise ValueError(
            "Evaluation response must be a JSON object."
        )

    criteria = result.get("criteria")

    # Check that exactly six criteria were returned.
    if not isinstance(criteria, list) or len(criteria) != 6:
        raise ValueError(
            "Evaluator must return exactly six criteria."
        )

    # Check that all expected IDs are present without duplicates.
    criterion_ids = [
        item.get("criterion_id")
        for item in criteria
        if isinstance(item, dict)
    ]

    if (
        len(criterion_ids) != 6
        or set(criterion_ids) != EXPECTED_CRITERIA
    ):
        raise ValueError(
            "Evaluator returned missing, duplicate, "
            "or unexpected criterion IDs."
        )

    # Validate and normalize each criterion.
    for item in criteria:

        status = item.get("status")

        if not isinstance(status, str):
            raise ValueError(
                "Each criterion must have a valid status."
            )

        status = status.upper()

        if status not in {"PASS", "FAIL"}:
            raise ValueError(
                f"Invalid evaluation status: {status}"
            )

        item["status"] = status

        for field in ("reason", "improvement_suggestion"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ValueError(
                    f"Each criterion must include a non-empty {field}."
                )

    # Python independently decides the final result.
    all_passed = all(
        item["status"] == "PASS"
        for item in criteria
    )

    result["overall_status"] = (
        "PASS" if all_passed else "FAIL"
    )

    return result
