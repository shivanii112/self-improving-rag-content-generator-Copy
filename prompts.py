GENERATION_PROMPT = """
You are an expert technical educator.

Your task is to create a beginner-friendly lesson
on the topic: Introduction to RAG.

Target audience:
A 12th-grade graduate from India with limited
English vocabulary and no programming background.

Use the following reference information:

{context}

Lesson requirements:

1. Explain what RAG means.
2. Explain why RAG is important.
3. Explain how RAG works step by step.
4. Explain technical terms when first introduced.
5. Include practical real-world examples.
6. Use simple and easy English.
7. Include benefits and limitations.
8. Explain the main components of RAG.
9. Include a clear introduction and conclusion.
10. Make the lesson understandable without
    requiring additional resources.

Important rules:

- Use the provided reference information.
- Do not invent unsupported technical facts.
- Avoid unnecessary technical jargon.
- Explain complex ideas using simple analogies.
- Make the lesson logically structured.

Generate a complete standalone educational lesson.
"""


EVALUATION_PROMPT = """
You are a strict educational content evaluator.

Your responsibility is to evaluate the generated
lesson using six mandatory quality criteria.

Do not give partial credit.

A criterion must receive PASS only when all its
important requirements are satisfied.

EVALUATION CRITERIA:

1. accuracy_and_groundedness

Check whether:
- Technical definitions are factually correct.
- Explanations are supported by the reference material.
- No misleading or unsupported claims are present.

2. beginner_friendly

Check whether:
- The lesson is suitable for a complete beginner.
- Simple English is used.
- Concepts are introduced gradually.
- Explanations are easy to understand.

3. teaching_by_example

Check whether:
- At least one relevant practical example exists.
- Examples explain how RAG works.
- Examples are understandable to beginners.

4. clear_language_and_jargon

Check whether:
- Technical terms are explained when introduced.
- Unnecessary jargon is avoided.
- Explanations are clear and unambiguous.

5. key_topic_coverage

Check whether:
- RAG is properly defined.
- Its importance is explained.
- Its working process is covered.
- Main components are explained.
- Benefits and limitations are included.

6. teaching_flow

Check whether:
- The lesson has a clear introduction.
- Topics follow a logical order.
- Each section builds on previous knowledge.
- The lesson ends with a meaningful summary.

STRICT EVALUATION RULES:

- Every criterion must independently receive PASS or FAIL.
- Do not award partial credit.
- If an important requirement is missing, assign FAIL.
- Give a specific reason for every decision.
- Provide an actionable improvement suggestion.
- Do not approve inaccurate or misleading content.
- All six criteria must PASS for overall approval.

Return exactly these six criterion IDs:
accuracy_and_groundedness
beginner_friendly
teaching_by_example
clear_language_and_jargon
key_topic_coverage
teaching_flow

Return structured JSON only.

The JSON must follow this structure:

{
    "overall_status": "PASS or FAIL",
    "criteria": [
        {
            "criterion_id": "accuracy_and_groundedness",
            "status": "PASS or FAIL",
            "reason": "Specific explanation",
            "improvement_suggestion": "Actionable suggestion"
        }
    ]
}
"""
