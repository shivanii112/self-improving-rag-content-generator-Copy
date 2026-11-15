from evaluator import evaluate_content
import json

# Step 1: Create intentionally incorrect content
print("\nTesting evaluator with incorrect content...\n")

bad_lesson = """
# What is RAG?

RAG stands for Random Automatic Generation.

RAG does not use external documents or databases.
It works without any retrieval process.

An LLM always has access to all private company
documents automatically.

Embeddings are images used to decorate documents.

A vector database is used only to store videos.

RAG guarantees that an AI system will never
produce incorrect answers.

There are no limitations to using RAG.
"""

print("INCORRECT TEST CONTENT CREATED!")

# Step 2: Evaluate the incorrect content
print("\nEvaluating incorrect content...\n")

evaluation = evaluate_content(bad_lesson)

# Step 3: Display evaluation results
print("\n========== EVALUATION RESULTS ==========\n")

print(json.dumps(evaluation, indent=4))

# Step 4: Display final status
print("\n========== FINAL STATUS ==========\n")

if evaluation["overall_status"] == "PASS":
    print("WARNING: Incorrect content was approved.")
else:
    print("SUCCESS: Incorrect content was rejected.")
