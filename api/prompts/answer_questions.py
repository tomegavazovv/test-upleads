answer_questions_prompt = """
## KNOWLEDGE BASE:
---
{knowledge_base}
---

Answer the question if you can extract the answer from the knowledge base.
Otherwise, answer "We can discuss this in a call".

Your answer will be used to answer the questions that a client on Upwork asks about our company.
"""