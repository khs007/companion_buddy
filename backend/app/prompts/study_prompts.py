from langchain.prompts import PromptTemplate

RAG_CHAT_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful study assistant. Answer the student's question 
using ONLY the context provided below. If the answer isn't in the context, 
say "I couldn't find that in your notes" — don't make things up.

Context from student's notes:
{context}

Student's question: {question}

Answer (be clear and concise, use bullet points if listing multiple things):"""
)

# ── Summary ───────────────────────────────────────────────────────────────────
SUMMARY_PROMPT = PromptTemplate(
    input_variables=["text"],
    template="""Create a clear, structured summary of the following study material.

Format your response as:
## Key Topics
- List the main topics covered

## Core Concepts  
- Explain the most important concepts in simple terms

## Key Takeaways
- What should a student definitely remember from this?

Study material:
{text}"""
)

# ── Quiz Generation ───────────────────────────────────────────────────────────

QUIZ_PROMPT = PromptTemplate(
    input_variables=["text", "num_questions"],
    template="""Generate {num_questions} multiple-choice quiz questions from the 
study material below.

Return ONLY a JSON array with this exact format (no extra text):
[
  {{
    "question": "Question text here?",
    "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
    "answer": "A) option1",
    "explanation": "Brief explanation of why this is correct"
  }}
]

Study material:
{text}"""
)

# ── Flashcards ────────────────────────────────────────────────────────────────

FLASHCARD_PROMPT = PromptTemplate(
    input_variables=["text", "num_cards"],
    template="""Create {num_cards} flashcards from the study material below.
Focus on key terms, definitions, and important concepts.

Return ONLY a JSON array with this exact format (no extra text):
[
  {{
    "front": "Term or question",
    "back": "Definition or answer"
  }}
]

Study material:
{text}"""
)

# ── Study Recommendations ─────────────────────────────────────────────────────

RECOMMENDATION_PROMPT = PromptTemplate(
    input_variables=["topic", "quiz_score", "weak_areas"],
    template="""A student just studied "{topic}" and scored {quiz_score}% on a quiz.
Their weak areas were: {weak_areas}

Give them a personalized study plan with:
1. What to review first (prioritized by weakness)
2. 3 specific study techniques for this type of material  
3. Suggested time allocation for the next study session
4. An encouraging note

Keep advice practical and specific, not generic."""
)