import json
from pathlib import Path
from datetime import datetime


# Define the location of the memory file
BASE_DIR = Path(__file__).resolve().parent

MEMORY_FILE = BASE_DIR / "logs" / "rejection_logs.json"


def load_memory():
    """
    Load previously stored evaluation failures.
    """

    if not MEMORY_FILE.exists():
        return []

    with open(MEMORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_failure(content, evaluation, topic="RAG"):
    """
    Save rejected content and its evaluation feedback.
    """

    # Store only rejected content
    if evaluation.get("overall_status", "").upper() != "FAIL":
        return False

    # Identify failed criteria
    failed_criteria = []

    for criterion in evaluation.get("criteria", []):

        if criterion.get("status", "").upper() == "FAIL":

            failed_criteria.append({
                "criterion_id": criterion.get("criterion_id"),
                "reason": criterion.get("reason"),
                "improvement_suggestion": criterion.get(
                    "improvement_suggestion"
                )
            })

    # Create a memory record
    memory_record = {
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "overall_status": "FAIL",
        "content": content,
        "failed_criteria": failed_criteria
    }

    # Create logs folder automatically
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Load existing memory
    memories = load_memory()

    # Add latest failure
    memories.append(memory_record)

    # Save updated memory
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memories, file, indent=4, ensure_ascii=False)

    print("Previous failure saved successfully!")

    return True


def get_recent_failures(limit=5):
    """
    Retrieve the most recent evaluation failures.
    """

    memories = load_memory()

    if limit <= 0:
        return []

    return memories[-limit:]