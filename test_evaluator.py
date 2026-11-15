from generator import generate_lesson
from evaluator import evaluate_content
from memory import save_failure
import json


# Step 1: Generate content
print("\nGenerating RAG lesson...\n")

lesson = generate_lesson()

print("CONTENT GENERATED SUCCESSFULLY!")


# Step 2: Evaluate generated content
print("\nEvaluating generated content...\n")

evaluation = evaluate_content(lesson)


# Step 3: Display evaluation results
print("\n========== EVALUATION RESULTS ==========\n")

print(json.dumps(evaluation, indent=4))


# Step 4: Check final status
print("\n========== FINAL STATUS ==========\n")

if evaluation["overall_status"] == "PASS":

    print("APPROVED: All six criteria passed.")

else:

    print("REJECTED: Content needs improvement.")

    # Step 5: Automatically save failure into memory
    save_failure(
        content=lesson,
        evaluation=evaluation,
        topic="RAG"
    )

    print("Failure stored in persistent memory.")
