# Function Understanding Guide (Simple Language)

This document explains every function in the project in plain, non-technical language.  
Each function section starts with one direct sentence, then gives clear details about the data it receives and the result it returns.

## File: `agentic_rag/src/rag_tools.py`

### Function Name
`SimpleVectorIndex.__init__(self, documents)`

**What this function does (Minimum 100 words):**  
This function takes a list of knowledge documents and prepares them so the system can search them quickly later. It receives stored text items as input, where each item has a name and content. It then organizes those items into an internal searchable collection and builds the base information needed for matching future user questions. The result is not a message shown to the user, but a ready search object that other parts of the project can use immediately. The real purpose is to do this setup once at the beginning, so every question does not need to rebuild everything from scratch. This makes later question answering practical, faster, and more reliable.

### Function Name
`SimpleVectorIndex._tokenize(text)`

**What this function does (Minimum 100 words):**  
This function takes one piece of text and turns it into a clean list of words that can be compared with other text. It receives a sentence or paragraph as input, changes it to a consistent style, and pulls out word-like parts while ignoring formatting noise. The result is a simple word list that the search system can understand much better than raw text. Its real purpose is to make sure a user question and stored document are treated in the same way before matching is attempted. If this cleaning step did not exist, small differences in writing style could hide obvious matches and lead to weaker answers.

### Function Name
`SimpleVectorIndex._build(self)`

**What this function does (Minimum 100 words):**  
This function studies all stored documents and creates the internal scoring information used to decide which document best matches a question. It reads every document text from the document list already loaded in the object. Then it calculates how important each word is across all documents and stores that information in memory. The result is a complete prepared search map that later functions use to rank document relevance for each user query. The real purpose is to build strong matching rules ahead of time, so the system can respond with useful sources quickly and consistently instead of doing heavy analysis again for each new question.

### Function Name
`SimpleVectorIndex._embed_query(self, query)`

**What this function does (Minimum 100 words):**  
This function takes a user question and converts it into the same comparable format used for stored documents. It receives one input string, reads the words in that question, and creates a weighted question profile that can be compared against document profiles. It also calculates a size value for that profile, which helps the search function score matches fairly. The result is a pair: the prepared question data and its size number. The real purpose is to make question text match-ready so the system can accurately find related documents. Without this step, document matching would be inconsistent because questions and documents would not be represented in the same style.

### Function Name
`SimpleVectorIndex._dot(a, b)`

**What this function does (Minimum 100 words):**  
This function compares two prepared text profiles and returns one number that shows how much they overlap. It takes two sets of word-weight data as input, usually one from the question and one from a document. It reads matching words between them and multiplies their values to produce a combined overlap score. The result is a single number used later to decide how relevant a document is. Its real purpose is to provide a clear, repeatable way to measure similarity between two text items. This allows the system to rank many documents fairly and pick the strongest matches for user-facing answers.

### Function Name
`SimpleVectorIndex.search(self, query, top_k=3)`

**What this function does (Minimum 100 words):**  
This function takes a user question and returns the top matching documents from the stored knowledge set. It receives two inputs: the question text and how many top results to return. It prepares the question for comparison, checks all stored documents, scores each one, sorts them by relevance, and keeps only the best few. The result is a list of matched document items with relevance scores. The real purpose is to select useful evidence for answer generation instead of scanning and returning everything. This helps keep responses focused, reduces clutter, and makes it easier for users to trust that the chosen sources are closely related to what they asked.

### Function Name
`_load_documents(data_dir)`

**What this function does (Minimum 100 words):**  
This function reads text files from a folder and turns them into the project’s internal document list. It takes one input: the folder path where knowledge files are stored. It goes through all `.txt` files in that folder, reads each file’s content, and creates a document item with a source name and full text. The result is a list of document entries ready for indexing and search. If no files are found, it stops with an error instead of pretending everything is fine. The real purpose is to guarantee that the assistant has real source content before answering any questions, which protects reliability and clarity.

### Function Name
`plan_query(user_query)`

**What this function does (Minimum 100 words):**  
This function takes the user’s question and returns a cleaned version plus a short plan note for the first search attempt. It receives one input string from the user and removes extra outer spaces. It then builds a small result object with two parts: the cleaned question and a plain strategy message explaining that direct search is attempted first. The output is simple, readable planning data that can be used by the assistant before retrieval begins. The real purpose is to give a consistent starting point for question handling, so every request enters search in a predictable way and later retry steps can follow the same pattern.

### Function Name
`refine_query_if_needed(user_query)`

**What this function does (Minimum 100 words):**  
This function takes a question and adds related words when the original phrasing might be too short or narrow. It receives one question string, checks it for known trigger terms such as auth, db, rules, price, or hosting, and appends helpful related phrases for better matching. The result is a response object containing the refined question text and a true/false flag showing whether expansion happened. The real purpose is to increase the chance of finding relevant source documents when direct wording misses important terms found in the knowledge files. This gives the assistant a stronger second attempt and reduces empty-search outcomes.

### Function Name
`retrieve_context(query, top_k=3)`

**What this function does (Minimum 100 words):**  
This function takes a question and returns a short set of best evidence snippets from stored knowledge documents. It receives the question text and a requested number of results, limits that number to a safe range, and runs search against the prebuilt index. It then collects each match into a simple structure containing source name, score, and a short opening snippet from the document text. The result is a compact evidence package with query text, total count, and context list. The real purpose is to give the assistant grounded source material before answering, so replies are based on known content and not only on general language generation.

### Function Name
`list_knowledge_sources()`

**What this function does (Minimum 100 words):**  
This function returns a clear list of all document sources currently loaded in the knowledge set. It takes no user input. It reads the already loaded document collection and pulls each source name into a list, then also includes the total count of sources. The output is a small summary object that tells users or operators exactly what content is available for question answering. The real purpose is visibility: people can quickly check what the assistant can read before asking detailed questions. This helps set expectations, makes troubleshooting easier, and highlights when important documents are missing from the knowledge folder.

## File: `agentic_rag/src/agentic_rag.py`

### Function Name
`SimpleVectorIndex.__init__(self, documents)`

**What this function does (Minimum 100 words):**  
This function takes loaded documents and prepares the search engine used by the interactive assistant in this file. It receives a list of source items that include source names and text content. It stores those items inside the search object, creates empty places for scoring data, and then builds the matching information needed for later question lookups. The result is a ready-to-search object that can immediately answer lookup requests. The real purpose is startup preparation: do one setup step early so repeated questions in an interactive session can be answered quickly and consistently without rebuilding all internal search data each time.

### Function Name
`SimpleVectorIndex._tokenize(text)`

**What this function does (Minimum 100 words):**  
This function takes any text and converts it into a basic word list that is easier to compare across different sources. It receives one text input, normalizes letter style, and extracts usable words while ignoring formatting characters. The result is a consistent list of words that can be used in matching and scoring. The real purpose is to reduce confusion caused by writing differences. By making document text and question text look similar at word level, the system has a better chance of connecting related ideas. This directly improves how well the assistant finds relevant content for users without requiring perfect wording.

### Function Name
`SimpleVectorIndex._build(self)`

**What this function does (Minimum 100 words):**  
This function reads all stored documents and creates the internal relevance map that powers question matching. It takes no new outside input because it uses the documents already saved in the object. It counts word presence across documents, calculates word importance, and stores each document’s prepared profile and score base in memory. The result is a complete search foundation used by later matching steps. The real purpose is to precompute ranking information once so responses stay quick and stable during conversation. It also helps the assistant prioritize meaningful terms when deciding which source text should support a user’s answer.

### Function Name
`SimpleVectorIndex._embed_query(self, query)`

**What this function does (Minimum 100 words):**  
This function takes a user question and creates a prepared question profile for document comparison. It receives the question text as input, breaks it into cleaned words, measures their importance using already prepared word weights, and produces both the profile and its size value. The result is a ready comparison form that other matching steps can use directly. The real purpose is to transform plain language into a consistent question representation that aligns with document representation. That alignment allows fair relevance scoring and helps the system avoid weak matches when a question has little useful wording or empty input.

### Function Name
`SimpleVectorIndex._dot(a, b)`

**What this function does (Minimum 100 words):**  
This function takes two prepared text profiles and calculates one overlap number that reflects how related they are. It receives two sets of word values and compares them by checking shared words and combining their values. The result is a single similarity component used in final document ranking. The real purpose is to create a clear numeric signal of connection between question and source text. This helps the assistant sort candidate documents from most relevant to least relevant. Without this overlap measurement, choosing evidence would be guesswork and final answers would likely be less accurate and less trustworthy.

### Function Name
`SimpleVectorIndex.search(self, query, top_k=3)`

**What this function does (Minimum 100 words):**  
This function takes a user question and returns the best matching document results, limited to a chosen number. It receives the question text and a top result count, converts the question into comparison form, evaluates every stored document, and ranks matches by strength. The output is an ordered list of top document matches with score values. The real purpose is to choose useful source material quickly so answer creation can focus on strong evidence instead of all available text. This makes responses cleaner and more practical for users, and helps keep the assistant focused on the most relevant knowledge available.

### Function Name
`AgenticRAG.__init__(self, data_dir)`

**What this function does (Minimum 100 words):**  
This function creates a full question-answer assistant instance from a folder of knowledge documents. It receives one input: the folder path where source text files are stored. It loads those files into document items, then builds a searchable index from that content. The result is a ready assistant object that can answer questions using the loaded knowledge. The real purpose is to set up everything needed in one place before user interaction starts. By combining content loading and search preparation at creation time, it reduces setup mistakes and ensures the assistant starts in a known working state for demos and daily use.

### Function Name
`AgenticRAG._load_documents(data_dir)`

**What this function does (Minimum 100 words):**  
This function takes a folder path and returns all text files in that folder as structured knowledge items. It reads each `.txt` file, captures the file name as source label, and stores the file text for later searching. The result is a list of source entries that the assistant can use as its knowledge base. If the folder has no text files, it raises an error so the user knows setup is incomplete. The real purpose is to ensure the assistant has real readable content before answering questions. This prevents empty answers caused by missing source files and helps users catch setup issues early.

### Function Name
`AgenticRAG._plan_query(user_query)`

**What this function does (Minimum 100 words):**  
This function takes a user question and returns a cleaned version of that same question for search use. It receives one input string and removes extra spaces around it. The output is a tidy question text that can be passed into search without formatting noise. The real purpose is to keep question input consistent from one request to another, even when users type with extra spacing. It also acts as a clear place where future question-improvement logic can be added later. For now, it gives a simple, stable first step that helps the rest of the assistant behave predictably and clearly.

### Function Name
`AgenticRAG._expand_query_if_needed(original_query, first_pass)`

**What this function does (Minimum 100 words):**  
This function takes the original question and first search results, then decides whether to broaden the question with related words. It receives two inputs: the original user text and the first set of matches. If good matches already exist, it returns the original question unchanged. If not, it checks for known short terms and adds related phrases to create a stronger second search phrase. The result is one final question string for possible retry search. The real purpose is to recover from missed matches caused by short wording, giving users a better chance of getting useful results without rewriting their question manually.

### Function Name
`AgenticRAG._compose_answer(query, contexts)`

**What this function does (Minimum 100 words):**  
This function takes the user question and selected source matches, then writes the final response text shown to the user. It receives the original question and a list of matched source entries. If no entries are available, it returns a clear message saying relevant context was not found. If entries exist, it builds a readable summary with short snippets and source names so users can see supporting evidence. The result is one final answer string. The real purpose is to turn raw search output into human-friendly communication that is understandable, transparent, and useful for decision-making or learning tasks.

### Function Name
`AgenticRAG.ask(self, user_query, top_k=3)`

**What this function does (Minimum 100 words):**  
This function takes a user question and runs the complete answer journey from question input to final written reply. It receives the question text and a top-result limit. It first cleans the question, runs search, checks if results are good enough, optionally broadens the question for a second search, and then creates the final answer from the chosen sources. The output is a complete response string ready to display. The real purpose is simplicity for users: one request in, one answer out. It combines all major steps so people do not need to run separate actions manually to get useful document-based answers.

### Function Name
`run_cli()`

**What this function does (Minimum 100 words):**  
This function starts a command-line conversation session where a person can ask multiple questions one after another. It loads the assistant with local knowledge documents, prints a short welcome message, waits for user input, and shows an answer for each entered question. It also watches for exit words and stops the session cleanly when asked. The result is an interactive text-based experience in the terminal. The real purpose is quick testing and onboarding: new team members can try real questions immediately without building extra interfaces. It offers a simple hands-on way to understand how the project behaves in practice.

## File: `agentic_rag/main.py`

### Function Name
`demo(query)`

**What this function does (Minimum 100 words):**  
This function takes one sample question and runs a short demonstration of the document-search steps. It receives a single query input, creates a first planned version, runs the first context search, and if nothing is found, creates a refined question and runs search again. It then prints both planning and retrieval results to show what happened. The output is console display information rather than a polished user response. The real purpose is educational and diagnostic: it helps people quickly see whether search logic and refinement logic are working as expected on one test question without starting the full interactive session.

## File: `metaagent/remote_a2a/time_agent/agent.py`

### Function Name
`get_current_time()`

**What this function does (Minimum 100 words):**  
This function reads the current date and time from the system clock and returns it in a clear text format. It takes no input from the user beyond being called. It fetches “now” from the machine running the service and creates a simple result with one field named current time. The output is a structured time value that can be displayed directly to users when they ask for date or time information. The real purpose is to provide a precise factual answer for time questions, rather than relying on guesswork. It gives users an immediate, exact, and practical utility response.
