# Non-Technical Function Guide

This document explains every function in the project for readers with no programming background.  
Each function has exactly two sections.

## File: `agentic_rag/src/rag_tools.py`

### `SimpleVectorIndex.__init__(self, documents)`

**What this function does (Minimum 50 words):**  
This function sets up a searchable library from a collection of written documents. Think of it like arranging books in a smart catalog before a customer asks a question. It takes all available text and prepares it so the system can quickly find the most useful pieces later. It does this preparation once at the beginning so future questions can be answered faster.

**What problem this function solves (Minimum 50 words):**  
Without this setup step, every question would require the system to scan all documents from scratch, which would be slow and inefficient. This function solves the speed and organization problem by doing early preparation work. It makes sure the question-answering experience feels responsive and practical, especially when many questions are asked one after another during normal use.

### `SimpleVectorIndex._tokenize(text)`

**What this function does (Minimum 50 words):**  
This function breaks a piece of writing into individual words in a clean and consistent way. It removes differences such as uppercase and lowercase so words are treated equally. In simple terms, it turns messy writing into a tidy word list that can be compared fairly with other text. This helps the system understand what topics appear inside sentences.

**What problem this function solves (Minimum 50 words):**  
People write the same idea in many forms, with different punctuation or letter style. If text is not cleaned first, the system may miss obvious matches. This function solves that confusion by standardizing words before search and comparison happen. The result is better matching quality, which means users get answers that are more relevant to what they asked.

### `SimpleVectorIndex._build(self)`

**What this function does (Minimum 50 words):**  
This function prepares a full relevance map for all stored documents. It studies which words appear often and which words are more unique, then uses that understanding to score how important each word is in each document. In everyday terms, it builds the “brains” behind document search so the system can tell strong matches from weak matches later.

**What problem this function solves (Minimum 50 words):**  
If every word were treated equally, common words could drown out important meaning and search results would feel random. This function solves that by giving more value to meaningful words and less value to overly common ones. That improves answer quality for users and reduces frustration, because the most helpful source material is much more likely to appear first.

### `SimpleVectorIndex._embed_query(self, query)`

**What this function does (Minimum 50 words):**  
This function converts a user’s question into the same comparable format used for stored documents. In plain terms, it translates the question into a “search profile” so the system can measure how close each document is to what the user asked. It also checks if the question has enough useful words to be searched meaningfully before continuing.

**What problem this function solves (Minimum 50 words):**  
Questions and stored documents must be compared in a fair, like-for-like way. Without this conversion, the system would struggle to decide which document is closest to the user’s request. This function solves that matching problem by creating a consistent question format. It also prevents weak or empty questions from producing misleading results, which protects overall answer reliability.

### `SimpleVectorIndex._dot(a, b)`

**What this function does (Minimum 50 words):**  
This function calculates how strongly two word profiles overlap. You can think of it as measuring shared meaning between two text summaries: one from the question and one from a document. It produces a single score showing how much they align. A higher score means the two pieces of text are more related and likely useful together.

**What problem this function solves (Minimum 50 words):**  
The system needs a clear numeric way to compare many documents quickly and fairly. This function solves that by giving a direct overlap score that can be used to rank results. Without this kind of comparison, the system would not know which document should come first. It helps deliver focused answers instead of random or weakly related information.

### `SimpleVectorIndex.search(self, query, top_k=3)`

**What this function does (Minimum 50 words):**  
This function finds the most relevant documents for a user question and returns the best few. It compares the question against every available source, scores each one, and keeps only the top matches. In practical terms, it is the main “finder” step that chooses which documents should be used to support the final response shown to the user.

**What problem this function solves (Minimum 50 words):**  
When there are multiple knowledge files, users need the system to focus on the most useful ones, not all of them. This function solves the ranking and selection problem by sorting results by relevance and limiting output to the best matches. That keeps responses focused, avoids information overload, and improves trust because cited content is more likely to be directly connected.

### `_load_documents(data_dir)`

**What this function does (Minimum 50 words):**  
This function reads all text files from a chosen folder and turns them into usable knowledge items for the system. In simple terms, it gathers the project’s reference material so the assistant can answer questions from it. It also assigns a clear name to each source, making it easier to identify where an answer came from later.

**What problem this function solves (Minimum 50 words):**  
The assistant cannot provide grounded answers if source documents are missing or unread. This function solves that startup problem by collecting available files and making sure there is real content to search. It also stops early if nothing is found, preventing a false impression that the system is working normally when it actually has no knowledge loaded.

### `plan_query(user_query)`

**What this function does (Minimum 50 words):**  
This function takes a user question, cleans extra spaces, and creates a simple plan for the first search attempt. It gives back the cleaned question and a short note describing the search approach. In everyday terms, it is the “first thinking step” that makes sure the question is ready before the system starts looking through documents.

**What problem this function solves (Minimum 50 words):**  
Users may type questions with inconsistent spacing or unclear formatting. This function solves that by creating a cleaner starting point for search, so early matching is more stable. It also communicates the initial approach in plain terms, helping the system stay consistent in how it handles requests. That consistency improves user experience and makes behavior easier to trust.

### `refine_query_if_needed(user_query)`

**What this function does (Minimum 50 words):**  
This function expands a question with related words when helpful. For example, if the user mentions a short term, it adds common related terms so the search can find more useful material. In plain language, it gives the question extra context words that might be missing, especially when the first wording is too brief to find good matches.

**What problem this function solves (Minimum 50 words):**  
People often ask short questions that omit key terms found in documentation. This function solves the “too little wording” problem by broadening the search phrase with related language. That increases the chance of finding relevant source text instead of returning nothing. The practical outcome is fewer dead-end searches and a better chance of receiving a useful, grounded answer.

### `retrieve_context(query, top_k=3)`

**What this function does (Minimum 50 words):**  
This function gathers the best supporting text snippets for a question. It chooses a limited number of top matches, extracts short preview passages, and packages them with source names and relevance scores. In simple terms, it gives the assistant a shortlist of evidence pieces to use when forming a response so the answer can point to real material.

**What problem this function solves (Minimum 50 words):**  
An assistant should not answer from guesswork when trusted sources are available. This function solves that by collecting direct evidence before an answer is written. It also limits result volume so responses stay focused and readable. For users and business stakeholders, this means clearer traceability: you can see which source files support the final answer and why.

### `list_knowledge_sources()`

**What this function does (Minimum 50 words):**  
This function lists all knowledge sources currently available to the assistant and reports how many there are. It gives a simple inventory of what the system can use to answer questions. In everyday terms, it is like opening a library catalog and seeing which books are on the shelf before deciding what questions the librarian can realistically answer.

**What problem this function solves (Minimum 50 words):**  
Users and operators need visibility into available knowledge, especially when answers seem incomplete. This function solves the “what content is loaded?” uncertainty by exposing a clear source list. That helps teams quickly spot missing documents, verify setup, and explain limitations to stakeholders. The practical benefit is faster troubleshooting and better expectations about what the assistant can answer confidently.

## File: `agentic_rag/src/agentic_rag.py`

### `SimpleVectorIndex.__init__(self, documents)`

**What this function does (Minimum 50 words):**  
This function prepares the search engine used by the interactive question tool in this file. It takes loaded documents and organizes them so searching can happen quickly during conversation. You can think of it as building the internal index at startup, so each question does not have to reprocess all text from the beginning every single time.

**What problem this function solves (Minimum 50 words):**  
Interactive tools must feel responsive. If setup work were repeated for every question, response time would become slow and frustrating. This function solves that by doing heavy preparation once, then reusing it. The result is smoother user interaction, especially when someone asks many questions in one session and expects reliable speed throughout the conversation.

### `SimpleVectorIndex._tokenize(text)`

**What this function does (Minimum 50 words):**  
This function separates text into clean words so different pieces of writing can be compared more accurately. It ignores case differences and captures the core word content. In non-technical terms, it turns raw sentences into standardized word lists that are easier for the search process to understand and compare, whether the text came from a document or a user question.

**What problem this function solves (Minimum 50 words):**  
Without word standardization, small writing differences can hide clear matches. This function solves that by ensuring text is treated consistently, so relevant documents are less likely to be missed. For users, this means the assistant is better at finding the right source even when wording varies. It improves match quality and reduces confusion from weak or unexpected search results.

### `SimpleVectorIndex._build(self)`

**What this function does (Minimum 50 words):**  
This function creates the scoring setup that allows the system to judge document relevance. It reviews all loaded documents, identifies meaningful words, and prepares values used to compare future questions against those documents. In plain language, it builds the lookup intelligence that helps decide which source text should be considered strongest evidence for a specific user question.

**What problem this function solves (Minimum 50 words):**  
A search feature needs a fair method to rank many documents, not just return random matches. This function solves that ranking problem by preparing importance values ahead of time. It helps important topic words influence results more than generic words. The practical outcome is that users receive better-targeted answers supported by more appropriate source passages, improving trust and usefulness.

### `SimpleVectorIndex._embed_query(self, query)`

**What this function does (Minimum 50 words):**  
This function transforms a question into a form that can be compared to stored documents. It creates a measurable profile of the question’s words and their importance. In everyday terms, it gives the question a “shape” that can be matched against document “shapes,” making it possible to score which source is closest to what the user is asking.

**What problem this function solves (Minimum 50 words):**  
If questions and documents are represented differently, comparison becomes unreliable. This function solves that by preparing questions in the same style as stored sources. It also handles weak or empty input safely, which prevents bad comparisons. For the user, this means more consistent search quality and fewer confusing results when a question is too short or not clearly stated.

### `SimpleVectorIndex._dot(a, b)`

**What this function does (Minimum 50 words):**  
This function measures overlap between two text profiles and produces one number showing how related they are. One profile usually represents the user’s question and the other represents a document. A higher value means stronger connection. In simple terms, it is one of the math checks that helps the system decide whether a source likely contains useful information.

**What problem this function solves (Minimum 50 words):**  
The system must compare many candidate documents quickly and consistently. This function solves that need by giving a repeatable overlap score used in ranking. Without a clear score, result ordering would be unclear and often unreliable. The practical benefit is better prioritization of source material, which directly improves how focused and relevant the assistant’s final responses feel to users.

### `SimpleVectorIndex.search(self, query, top_k=3)`

**What this function does (Minimum 50 words):**  
This function performs the full search step for a question and returns the top matching sources. It checks all available documents, scores each one, and keeps only the strongest few. In practical terms, this is the step that decides which pieces of written knowledge will be considered evidence when the assistant prepares the final answer shown to the user.

**What problem this function solves (Minimum 50 words):**  
Users need concise, high-quality evidence, not a large unfiltered dump of text. This function solves that by ranking and limiting results to the most relevant sources. It prevents overload and keeps answers centered on useful information. From a business perspective, this improves clarity and confidence, because responses can focus on strong matches rather than broad or weakly related content.

### `AgenticRAG.__init__(self, data_dir)`

**What this function does (Minimum 50 words):**  
This function creates a ready-to-use question assistant from a folder of text knowledge. It first gathers the documents, then prepares a searchable index so the assistant can answer immediately. In plain language, it is the “startup setup” for the interactive assistant in this file, ensuring both content and search capability are prepared before users begin asking questions.

**What problem this function solves (Minimum 50 words):**  
A question assistant cannot function if content is missing or unprepared. This function solves that by combining two essential startup tasks: loading source material and building search readiness. It makes sure the assistant is truly ready before use. The practical outcome is fewer runtime failures and a more reliable first experience for new users testing the system.

### `AgenticRAG._load_documents(data_dir)`

**What this function does (Minimum 50 words):**  
This function reads text files from a data folder and converts them into a usable collection for the assistant. It gives each source a clear name and stores its full text. In everyday terms, it is like stocking shelves in a knowledge room so the assistant has actual reference material available before any question is asked.

**What problem this function solves (Minimum 50 words):**  
If source files are not collected properly, the assistant has nothing reliable to draw from. This function solves the content availability problem by loading documents in a consistent way and stopping if none exist. That protects users from false expectations. It ensures the system only starts when there is real information available, which supports dependable, evidence-based responses.

### `AgenticRAG._plan_query(user_query)`

**What this function does (Minimum 50 words):**  
This function creates a cleaned version of the user’s question for searching. It removes unnecessary outer spacing and keeps the main wording intact. In simple terms, it is a light preparation step that makes the question neater before searching begins. It does not change meaning, but it helps the assistant work with a consistent question format.

**What problem this function solves (Minimum 50 words):**  
Even small formatting issues in user input can create inconsistency. This function solves that by standardizing the question text before search. It also provides a dedicated place for future improvements in question preparation without changing other parts of the assistant. The practical benefit is steady behavior today and easier improvements tomorrow, while keeping user interactions simple and predictable.

### `AgenticRAG._expand_query_if_needed(original_query, first_pass)`

**What this function does (Minimum 50 words):**  
This function decides whether to broaden a question after the first search attempt. If useful matches are already found, it keeps the original wording. If not, it adds related terms to improve the second attempt. In plain language, it is like rephrasing a question with extra hints when the first ask did not find good answers.

**What problem this function solves (Minimum 50 words):**  
First searches can fail when users ask in short or narrow wording. This function solves that by giving the system a second chance with expanded language. It helps reduce “no result” situations and improves answer coverage. For users, this means fewer dead ends and less need to manually rewrite questions themselves, which makes the tool feel more helpful and resilient.

### `AgenticRAG._compose_answer(query, contexts)`

**What this function does (Minimum 50 words):**  
This function creates the final message shown to the user using the selected source passages. If no source is found, it provides a clear “not enough information” message. If sources are found, it summarizes key snippets and names where they came from. In everyday terms, it turns raw search findings into a readable answer with clear evidence labels.

**What problem this function solves (Minimum 50 words):**  
Raw search results are hard to read and do not feel like a direct answer. This function solves that communication problem by producing a simple, human-readable response. It also handles empty results honestly, which avoids false confidence. The practical benefit is better user trust: people can understand the response quickly and see the source references supporting it.

### `AgenticRAG.ask(self, user_query, top_k=3)`

**What this function does (Minimum 50 words):**  
This function handles a full question from start to finish. It cleans the question, searches documents, optionally broadens the wording if needed, and then creates the final response text. In simple terms, this is the main “answer my question” function for the interactive assistant. It combines all major steps into one complete user-facing action.

**What problem this function solves (Minimum 50 words):**  
Users should not need to run separate steps manually to get an answer. This function solves that by combining preparation, search, retry logic, and response writing into a single action. It reduces complexity for end users and ensures consistent behavior each time. The practical outcome is a smoother, more reliable experience where one question request produces one complete response.

### `run_cli()`

**What this function does (Minimum 50 words):**  
This function starts a console-based chat session where users can ask questions repeatedly. It loads the assistant, displays instructions, receives typed questions, returns answers, and exits when the user types a quit command. In everyday terms, it creates a simple question-and-answer screen in the terminal so people can try the assistant without extra setup tools.

**What problem this function solves (Minimum 50 words):**  
Teams need an easy way to test and demonstrate the assistant quickly. This function solves that by offering a straightforward interactive mode that runs directly from the command line. It lowers adoption friction for new users and stakeholders because they can try real questions immediately. The practical benefit is faster validation, easier demos, and quicker onboarding feedback.

## File: `agentic_rag/main.py`

### `demo(query)`

**What this function does (Minimum 50 words):**  
This function runs a single demonstration of how question handling works. It prepares the question, searches for supporting text, tries an expanded version if needed, and prints the result details. In plain language, it is a quick showcase mode for one question so someone can see the process and outputs without entering the full interactive session.

**What problem this function solves (Minimum 50 words):**  
Sometimes stakeholders want a fast one-question example instead of a full chat loop. This function solves that need by running a compact demonstration path. It helps people understand whether the search and answer process is working, and it makes troubleshooting easier during setup. The practical result is quicker verification and easier communication during testing or onboarding.

## File: `metaagent/remote_a2a/time_agent/agent.py`

### `get_current_time()`

**What this function does (Minimum 50 words):**  
This function gives the current date and time in a clear text format. It checks the machine’s clock and returns one simple value that can be shown to users. In everyday terms, it acts like a digital clock helper for the assistant, answering time-related requests with a direct and precise timestamp instead of conversational guesswork.

**What problem this function solves (Minimum 50 words):**  
General chat responses may not always provide precise real-time clock values. This function solves that by returning an exact time reading directly from the system clock. The practical benefit is accuracy and consistency for time questions. For business and user trust, this matters because time-based responses need to be factual, not approximate, especially in task-oriented interactions.
