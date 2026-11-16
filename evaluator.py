import json
from pathlib import Path

from config import get_client, GEMINI_MODEL
from prompts import EVALUATION_PROMPT


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent

RUBRIC_FILE = PROJECT_DIR / "rubric.json"


# --------------------------------------------------
# 2. LOAD EVALUATION RUBRIC
# --------------------------------------------------

def load_rubric():
    """
    Load evaluation criteria from rubric.json.
    """

    if not RUBRIC_FILE.exists():
        raise FileNotFoundError(
            f"Evaluation rubric not found: {RUBRIC_FILE}"
        )

    try:
        with open(RUBRIC_FILE, "r", encoding="utf-8") as file:
            rubric = json.load(file)

    except json.JSONDecodeError as exc:
        raise ValueError(
            "rubric.json contains invalid JSON."
        ) from exc

    criteria = rubric.get("evaluation_criteria")

    if not isinstance(criteria, list) or not criteria:
        raise ValueError(
            "rubric.json must contain a non-empty "
            "evaluation_criteria list."
        )

    criterion_ids = []

    for item in criteria:

        if not isinstance(item, dict):
            raise ValueError(
                "Each evaluation criterion must be a JSON object."
            )

        criterion_id = item.get("criterion_id")
        description = item.get("description")

        if not isinstance(criterion_id, str) or not criterion_id.strip():
            raise ValueError(
                "Every criterion must have a valid criterion_id."
            )

        if not isinstance(description, str) or not description.strip():
            raise ValueError(
                "Every criterion must have a valid description."
            )

        criterion_ids.append(criterion_id)

    if len(criterion_ids) != len(set(criterion_ids)):
        raise ValueError(
            "Duplicate criterion IDs found in rubric.json."
        )

    return criteria


# Load the expected criteria from the JSON rubric.
RUBRIC = load_rubric()

EXPECTED_CRITERIA = {
    item["criterion_id"]
    for item in RUBRIC
}


# --------------------------------------------------
# 3. EVALUATE GENERATED CONTENT
# --------------------------------------------------

def evaluate_content(content):
    """
    Evaluate generated lesson content using
    the criteria defined in rubric.json.
    """

    if not isinstance(content, str) or not content.strip():
        raise ValueError(
            "Content to evaluate cannot be empty."
        )

    client = get_client()

    # Prepare evaluation criteria for Gemini.
    criteria_description = "\n".join(
        [
            f"{index}. {item['criterion_id']}: "
            f"{item['description']}"
            for index, item in enumerate(RUBRIC, start=1)
        ]
    )

    prompt = f"""
    {EVALUATION_PROMPT}

    EVALUATION CRITERIA:

    {criteria_description}

    CONTENT TO EVALUATE:

    {content}

    IMPORTANT INSTRUCTIONS:

    1. Evaluate using exactly the criteria provided above.
    2. Return every criterion ID exactly once.
    3. Each criterion must have PASS or FAIL status.
    4. Include a specific reason for every decision.
    5. Include an actionable improvement suggestion.
    6. Return valid JSON only.
    """

    # Ask Gemini to evaluate the generated content.
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

    # Convert Gemini's JSON response into Python.
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

    expected_count = len(EXPECTED_CRITERIA)

    # Validate the number of returned criteria.
    if not isinstance(criteria, list) or len(criteria) != expected_count:
        raise ValueError(
            f"Evaluator must return exactly {expected_count} criteria."
        )

    # Validate criterion IDs and prevent duplicates.
    criterion_ids = []

    for item in criteria:

        if not isinstance(item, dict):
            raise ValueError(
                "Each returned criterion must be a JSON object."
            )

        criterion_ids.append(item.get("criterion_id"))

    if (
        len(criterion_ids) != len(set(criterion_ids))
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

            if (
                not isinstance(item.get(field), str)
                or not item[field].strip()
            ):
                raise ValueError(
                    f"Each criterion must include "
                    f"a non-empty {field}."
                )

    # Python independently determines the final result.
    all_passed = all(
        item["status"] == "PASS"
        for item in criteria
    )

    result["overall_status"] = (
        "PASS" if all_passed else "FAIL"
    )

    return result