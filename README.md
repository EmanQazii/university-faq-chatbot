#  SafeX University FAQ Chatbot

A retrieval-based AI chatbot prototype that answers common university
and SafeX internship questions using a structured FAQ knowledge base.

The project uses **Sentence Transformers** for semantic embeddings and
**cosine similarity** to retrieve the most relevant FAQ answer. It
includes a professional Streamlit interface, FAQ shortcuts, session chat
history, clear/new chat functionality, light/dark themes, fallback
handling, evaluation logging, and public deployment.

##  Live Demo

**Streamlit App:**\
https://university-faq-safex.streamlit.app/

------------------------------------------------------------------------

##  Project Objective

Universities and internship programs receive repetitive questions about
admissions, programs, deadlines, fees, scholarships, campus facilities,
and internship opportunities.

This prototype provides quick answers from a controlled FAQ knowledge
base without using a generative language model.

------------------------------------------------------------------------

##  Features

-   Semantic FAQ retrieval using
    `sentence-transformers/all-MiniLM-L6-v2`
-   Cosine-similarity matching
-   40 structured FAQ pairs
-   Admissions, programs, application, fees, scholarships, campus, and
    SafeX internship categories
-   Fallback handling for questions outside the knowledge base
-   Streamlit chat interface
-   Frequently Asked Questions sidebar
-   One-click FAQ questions
-   Session chat history
-   New/Clear chat functionality
-   Light and dark themes
-   Responsive UI
-   Automated evaluation and CSV accuracy log
-   Streamlit Community Cloud deployment

------------------------------------------------------------------------

##  How It Works

``` text
User Question
      ↓
Sentence Transformer
      ↓
Query Embedding
      ↓
Cosine Similarity
      ↓
Compare with FAQ Embeddings
      ↓
Highest Similarity FAQ
      ↓
Similarity ≥ Threshold?
   ↙              ↘
 Yes               No
  ↓                 ↓
Return FAQ       Return Fallback
 Answer
```

### Retrieval Process

1.  `data/faqs.csv` is loaded.
2.  Every FAQ question is converted into an embedding.
3.  A user's query is converted into an embedding using the same model.
4.  Cosine similarity is calculated between the query and FAQ
    embeddings.
5.  The FAQ with the highest score is selected.
6.  If the score is below `THRESHOLD = 0.45`, the chatbot returns a
    fallback response instead of guessing.

------------------------------------------------------------------------

##  Project Structure

``` text
university-faq-chatbot/
│
├── app.py
├── test_chatbot.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── faqs.csv
│
├── outputs/
│   └── accuracy_test_log.csv
│
├── src/
│   ├── faq_retriever.py
│   └── evaluate.py
│
└── .streamlit/
    └── config.toml
```

### Main Files

  File                              Purpose
  --------------------------------- -------------------------------------------
  `app.py`                          Main Streamlit application and UI
  `src/faq_retriever.py`            Embedding and retrieval logic
  `src/evaluate.py`                 Automated evaluation and accuracy logging
  `test_chatbot.py`                 Interactive terminal testing
  `data/faqs.csv`                   40-question FAQ knowledge base
  `outputs/accuracy_test_log.csv`   Saved evaluation results
  `.streamlit/config.toml`          Streamlit configuration
  `requirements.txt`                Python dependencies

------------------------------------------------------------------------

##  Dataset

The knowledge base contains **40 FAQ question-answer pairs** in CSV
format.

Fields:

-   `id`
-   `category`
-   `question`
-   `answer`

Categories include:

-   Admissions
-   Programs
-   Application Process
-   Fees
-   Scholarships
-   Campus
-   SafeX Internship
-   Internship Process

The dataset can be expanded without changing the retrieval architecture.

------------------------------------------------------------------------

##  Evaluation

The evaluation script contains **20 test questions** covering three
types of cases:

### Exact Questions

Questions that directly correspond to FAQ entries.

### Paraphrased Questions

Questions written differently from the original FAQ wording to test
semantic retrieval.

Examples:

``` text
What do I need to get admitted?
```

``` text
Which degrees can I study here?
```

``` text
How can I submit my application?
```

### Irrelevant Questions

Questions outside the knowledge base, such as:

``` text
What is the weather like today?
Tell me a joke
What is the capital of France?
```

These are expected to trigger the fallback response.

------------------------------------------------------------------------

##  Evaluation Result

Latest evaluation:

``` text
Total Questions : 20
Correct         : 19
Incorrect       : 1
Accuracy        : 95.00%
```

The evaluation demonstrates that:

-   Exact FAQ matching works.
-   Paraphrased questions can be matched semantically.
-   Irrelevant questions trigger the fallback mechanism.
-   The project exceeds the required **70% success criterion**.

One paraphrased fee question was retrieved as a different but related
fee FAQ because the two questions have overlapping semantic meaning.
This is a normal limitation of nearest-neighbor retrieval and can be
improved through additional paraphrases, better threshold tuning, or
more advanced retrieval.

The complete results are saved to:

``` text
outputs/accuracy_test_log.csv
```

------------------------------------------------------------------------

##  Run Locally

### 1. Clone the repository

``` bash
git clone <your-github-repository-url>
cd university-faq-chatbot
```

### 2. Create a virtual environment

Windows PowerShell:

``` powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

``` powershell
pip install -r requirements.txt
```

The Sentence Transformer model downloads automatically the first time it
is used.

### 4. Run the Streamlit app

From the project root:

``` powershell
streamlit run app.py
```

------------------------------------------------------------------------

## Run Evaluation

From the project root:

``` powershell
python -m src.evaluate
```

The evaluation script:

1.  Loads the FAQ dataset.
2.  Loads the retrieval model.
3.  Runs all 20 test questions.
4.  Compares predicted and expected FAQ IDs.
5.  Calculates accuracy.
6.  Reports failed cases.
7.  Saves the complete log to `outputs/accuracy_test_log.csv`.

------------------------------------------------------------------------

## Run Terminal Testing

``` powershell
python test_chatbot.py
```

Example questions:

``` text
What are the admission requirements?
Who is eligible for the SafeX internship?
Can I lose my scholarship?
What is the weather today?
```

The final example should use the fallback because it is outside the FAQ
knowledge base.

------------------------------------------------------------------------

## Technologies

-   **Python**
-   **Pandas** --- dataset handling and evaluation logs
-   **NumPy** --- numerical operations
-   **Scikit-learn** --- cosine similarity
-   **Sentence Transformers** --- semantic embeddings
-   **Streamlit** --- web interface
-   **Git/GitHub** --- version control
-   **Streamlit Community Cloud** --- deployment

------------------------------------------------------------------------

## Requirements

The direct Python dependencies are:

``` text
streamlit
pandas
numpy
scikit-learn
sentence-transformers
```

Built-in modules such as `html` and `textwrap` do not need to be listed
in `requirements.txt`.

For Streamlit Community Cloud, dependencies should be declared in a
`requirements.txt` file in the repository root or alongside the app
entrypoint.

------------------------------------------------------------------------

## Deployment

The application is deployed with **Streamlit Community Cloud**.

### Live URL

https://university-faq-safex.streamlit.app/

The deployed app is connected to the GitHub repository. After changes
are committed and pushed, the deployed application can automatically
update from the repository.

### Updating the Deployment

After making a change:

``` powershell
git add .
git commit -m "Update chatbot"
git push
```

Normal code and UI changes are picked up automatically. Changes to
dependencies can require a longer redeployment because packages need to
be installed again.

------------------------------------------------------------------------

## `.gitignore`

The local virtual environment and Python cache files should not be
committed.

Recommended entries:

``` gitignore
.venv/
__pycache__/
*.pyc
.env
.streamlit/secrets.toml
```

Project source code, the FAQ dataset, requirements, configuration,
README, and evaluation log can remain tracked because they are project
deliverables.

------------------------------------------------------------------------

## Limitations

This is a **retrieval-based prototype**, not a generative chatbot.

Therefore:

-   It only answers from the available FAQ knowledge base.
-   It does not generate new factual information.
-   Ambiguous questions can retrieve a related FAQ instead of the exact
    intended one.
-   Answer quality depends on the coverage and wording of the FAQ
    dataset.
-   Chat history is maintained for the current Streamlit session rather
    than stored permanently.
-   The embedding model is downloaded when the application environment
    first needs it.

------------------------------------------------------------------------

## Future Improvements

Possible extensions include:

-   More FAQ pairs and multiple paraphrases per FAQ
-   Threshold tuning using a larger validation set
-   Top-k retrieval
-   Confidence indicators
-   FAQ category filtering
-   Persistent chat storage
-   Admin interface for updating FAQs
-   Conversation analytics
-   Urdu/English multilingual support
-   Hybrid TF-IDF + embedding retrieval
-   Vector database integration
-   User authentication

------------------------------------------------------------------------

## Task Requirements Checklist

  -----------------------------------------------------------------------
  Requirement                         Status
  ----------------------------------- -----------------------------------
  25+ FAQ pairs                       40 FAQ pairs

  Structured CSV/JSON dataset         CSV

  Working retrieval logic             Sentence Transformers + cosine
                                      similarity

  Simple chat interface               Streamlit

  15+ sample questions                20 test questions

  Paraphrased questions               Included

  Accuracy test log                   CSV generated

  70%+ success criterion              95%

  Fallback handling                   Implemented

  Public deployment                   Streamlit Community Cloud

  -----------------------------------------------------------------------

------------------------------------------------------------------------

## Project Summary

The project demonstrates an end-to-end retrieval-based FAQ chatbot:

**FAQ Dataset → Semantic Embeddings → Similarity Matching → Fallback
Handling → Streamlit UI → Evaluation → Deployment**

It provides a lightweight, explainable approach for automating
repetitive university and internship support questions while keeping
answers grounded in a controlled knowledge base.
