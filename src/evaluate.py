import pandas as pd
from src.faq_retriever import FAQRetriever

# test set: exact, paraphrased, and irrelevant queries
TEST_CASES = [
    # exact
    ("What are the admission requirements for undergraduate programs?", 1),
    ("What undergraduate programs are offered at the university?", 6),
    ("How do I apply for admission?", 11),
    ("What is the tuition fee structure?", 16),
    ("What scholarships are available for students?", 21),

    # paraphrased
    ("What do I need to get admitted?", 1),
    ("Which degrees can I study here?", 6),
    ("How can I submit my application?", 11),
    ("How much are the fees?", 16),
    ("Is financial aid available?", 21),
    ("When is the last date to apply for fall?", 12),
    ("Who can join the SafeX internship?", 32),
    ("How long does the SafeX internship last?", 33),
    ("Will I get a certificate from SafeX?", 37),
    ("What is my minimum GPA to keep my scholarship?", 25),

    # irrelevant — expected faq_id is None (fallback)
    ("What is the weather like today?", None),
    ("Tell me a joke", None),
    ("What is the capital of France?", None),
    ("Who won the cricket match yesterday?", None),
    ("What should I eat for lunch?", None),
]


def run_evaluation(faq_path: str = "data/faqs.csv"):
    retriever = FAQRetriever(faq_path)
    results = []

    for query, expected_id in TEST_CASES:
        result = retriever.retrieve(query)
        predicted_id = result["faq_id"]

        # correct if both matched the same FAQ, or both correctly returned fallback
        correct = predicted_id == expected_id
        results.append({
            "query": query,
            "expected_id": expected_id,
            "predicted_id": predicted_id,
            "similarity": round(result["similarity"], 4),
            "matched_question": result["matched_question"],
            "correct": correct,
        })

    df = pd.DataFrame(results)
    df.to_csv("outputs/accuracy_test_log.csv", index=False)

    total = len(df)
    correct = df["correct"].sum()
    accuracy = (correct / total) * 100

    print(f"\nTotal Questions : {total}")
    print(f"Correct         : {correct}")
    print(f"Incorrect       : {total - correct}")
    print(f"Accuracy        : {accuracy:.2f}%\n")

    # show failures
    failures = df[df["correct"] == False]
    if not failures.empty:
        print("Failed cases:")
        for _, row in failures.iterrows():
            print(f"  Q: {row['query']}")
            print(f"     Expected {row['expected_id']} | Got {row['predicted_id']} | Score {row['similarity']}")

    return df


if __name__ == "__main__":
    run_evaluation()