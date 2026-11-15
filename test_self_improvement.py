from generator import generate_lesson
from evaluator import evaluate_content
from memory import save_failure, get_recent_failures
import json


# STEP 1: Create intentionally incorrect content

print("\n========== STEP 1: INITIAL TEST ==========\n")

bad_lesson = """
# What is RAG?

RAG stands for Random Automatic Generation.

RAG does not use external documents or databases.
It works without any retrieval process.

Embeddings are images used to decorate documents.

A vector database is used only to store videos.

RAG guarantees that an AI system will never
produce incorrect answers.

There are no limitations to using RAG.
"""


# STEP 2: Evaluate incorrect content

print("Evaluating intentionally incorrect content...\n")

initial_evaluation = evaluate_content(bad_lesson)

print(json.dumps(initial_evaluation, indent=4))


# STEP 3: Save failure into persistent memory

if initial_evaluation["overall_status"].upper() == "FAIL":

    print("\nIncorrect content rejected!")

    save_failure(
        content=bad_lesson,
        evaluation=initial_evaluation,
        topic="RAG"
    )

else:

    print("\nWARNING: Incorrect content was approved.")


# STEP 4: Retrieve previous failures

print("\n========== STEP 2: RETRIEVING MEMORY ==========\n")

failures = get_recent_failures(limit=5)

print("Previous failures retrieved:", len(failures))


# STEP 5: Generate improved content using memory

print("\n========== STEP 3: REGENERATION ==========\n")

improved_lesson = generate_lesson()

print("IMPROVED CONTENT GENERATED SUCCESSFULLY!")


# STEP 6: Evaluate improved content

print("\n========== STEP 4: FINAL EVALUATION ==========\n")

final_evaluation = evaluate_content(improved_lesson)

print(json.dumps(final_evaluation, indent=4))


# STEP 7: Display final result

print("\n========== FINAL RESULT ==========\n")

if final_evaluation["overall_status"].upper() == "PASS":

    print("SUCCESS: Improved content passed all six criteria.")

else:

    print("REJECTED: Improved content still needs improvement.")

    save_failure(
        content=improved_lesson,
        evaluation=final_evaluation,
        topic="RAG"
    )
