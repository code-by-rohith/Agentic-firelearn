# Project Walkthrough (Simple End-to-End Guide)

## Project Purpose

This project is a small AI assistant system built to answer questions in a smarter and safer way.  
It solves a common real-world problem: people ask many kinds of questions, but one single answer method is not always best.

Some questions need facts from trusted company documents.  
Some questions are general conversation.  
Some questions need a direct utility answer, like the current date and time.

So this project combines these ideas:

1. A document-based assistant that answers using local Firebase knowledge files.
2. A coordinator assistant that decides where each question should go.
3. A specialized time assistant that gives the current date/time.

The goal is clear: give more useful and reliable answers by using the right helper for each type of question.

---

## Overall Working Flow

At a high level, the system works like this:

1. A user asks a question.
2. The system decides which helper is best for that question.
3. If the question is about known document topics, it searches local text files.
4. If the question is about current time/date, it uses the time helper.
5. If it is a general chat question, it uses the general chat helper.
6. The final answer is returned to the user.

The project is designed so answers are not just random guesses.  
For document questions, it first finds matching source text, then responds using that evidence.

---

## Main Parts of the Project

### 1) `agentic_rag` (Document Question Assistant)

This part is responsible for reading local text files and finding the best matching content for a question.

It includes:

- `agentic_rag/data/`: source text files (Firebase topics).
- `agentic_rag/src/rag_tools.py`: reusable question-planning and document-search tools.
- `agentic_rag/src/agentic_rag.py`: interactive question flow for command-line usage.
- `agentic_rag/agent.py`: assistant setup that tells the AI to always use retrieved evidence.
- `agentic_rag/main.py`: simple demo run.

In simple terms, this is the “find answers from our own documents” part.

### 2) `metaagent` (Coordinator Assistant)

This part acts like a smart receptionist.

It includes:

- `metaagent/agent.py`: creates a top-level assistant that delegates questions.
- A local chat helper for general conversation.
- A remote time helper for date/time questions.

In simple terms, this is the “send each question to the right specialist” part.

### 3) `metaagent/remote_a2a/time_agent` (Time Specialist)

This part has one focused job: return the current date/time.

It includes:

- `metaagent/remote_a2a/time_agent/agent.py`: function to read current time and expose it through the assistant interface.

In simple terms, this is the “clock service” used when users ask for time.

---

## How Information Moves Through the System

### Document-based question path

1. User asks a question.
2. Question is cleaned.
3. System searches local knowledge files.
4. If nothing useful is found, it expands the question with related words and searches again.
5. Best matching snippets are selected.
6. Final answer is prepared with source references.
7. Answer is shown to user.

### Time question path

1. User asks for current date/time.
2. Coordinator sends request to time specialist.
3. Time specialist reads current system clock.
4. Formatted time is returned.
5. User sees the result.

### General conversation path

1. User asks a general question.
2. Coordinator sends it to chat helper.
3. Chat helper responds.
4. Final response is returned to user.

---

## How Different Components Work Together

The project works because each part has a clear role:

- The document assistant knows how to search trusted local content.
- The coordinator knows how to choose the right helper.
- The time specialist gives exact current time quickly.

They connect in a simple chain:

User question -> coordinator decision (or direct RAG flow) -> specialist/helper -> final response.

This separation keeps the system easy to understand and improve:

- Want better document answers? Improve document files or search logic.
- Want more special skills? Add another specialist helper.
- Want better routing? Update coordinator instructions.

---

## Typical User Journey

Imagine a new user opening this system.

1. They ask: “How do Firebase rules work?”
2. The document assistant looks through local Firebase text files.
3. It finds matching lines from the rules-related source.
4. It returns a grounded answer based on those matches.
5. The user gets a clear response tied to known source content.

Now imagine the same user asks: “What time is it?”

1. The coordinator recognizes this as a time request.
2. It calls the time specialist.
3. The specialist returns current date/time.
4. The user gets an exact time response.

Now user asks: “Explain this in simple words.”

1. Coordinator sends it to general chat helper.
2. Chat helper responds conversationally.
3. User gets a normal chat-style answer.

---

## End-to-End Process Explanation

From beginning to end, this project is a practical multi-helper assistant:

1. It receives user input.
2. It chooses a suitable path based on question type.
3. It either:
   - searches trusted local documents, or
   - gets live time from a specialist, or
   - handles general chat.
4. It returns a final answer in user-facing format.

For document questions, it does an extra quality step:

- first search directly,
- then retry with expanded wording if needed,
- then answer using found evidence.

That design makes answers more reliable than a single generic chat flow.

In onboarding terms:

- Think of `agentic_rag` as the knowledge librarian.
- Think of `metaagent` as the receptionist/router.
- Think of `time_agent` as the clock desk.

Together, they create a simple but strong foundation for building a larger assistant platform.

