from memory import save_failure, get_recent_failures

sample_content = """
RAG is a database that guarantees
100% correct answers.
"""

sample_evaluation = {
    "overall_status": "FAIL",
    "criteria": [
        {
            "criterion_id": "accuracy_and_groundedness",
            "status": "FAIL",
            "reason": "RAG is incorrectly defined.",
            "improvement_suggestion": "Explain RAG correctly."
        },
        {
            "criterion_id": "teaching_by_example",
            "status": "FAIL",
            "reason": "No practical example provided.",
            "improvement_suggestion": "Add a practical example."
        }
    ]
}

# Save failure
save_failure(sample_content, sample_evaluation)

# Retrieve stored failures
print("\n========== STORED MEMORY ==========")

failures = get_recent_failures()

for failure in failures:
    print("\nTopic:", failure["topic"])
    print("Status:", failure["overall_status"])

    for criterion in failure["failed_criteria"]:
        print("-", criterion["criterion_id"])
        print("  Reason:", criterion["reason"])