answer_questions_prompt = """You are tasked with answering questions about a company. Follow these internal guidelines without including them in your final answer:

KNOWLEDGE BASE:
{knowledge_base}


[INTERNAL GUIDELINES – DO NOT OUTPUT]
1. Check if the question matches one of the predefined question/instruction pairs.
   - If a match is found, use the instruction and the knowledge base to answer the question.

QUESTION INSTRUCTIONS:
{question_instructions}
  
2. If no predefined instruction is applicable, search the knowledge base for relevant information.
   - If relevant information is found, construct your answer using that information. If the answer is not found in the knowledge base, use the answer template to generate an answer.

3. If neither is found, use the answer template to generate an answer.
ANSWER TEMPLATE:
{answer_template}

Your final answer should be output as a JSON list of objects, where each object contains:
- question: The original question.
- answer: Your detailed answer.

Remember: Use the internal guidelines to inform your response, but do not output any of the guidelines or instructions in your final answer.
"""