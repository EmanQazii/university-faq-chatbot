import pandas as pd
from src.faq_retriever import FAQRetriever


# TEST DATA
TEST_CASES = [
    # ---------------- EXACT ----------------
    ("EXACT", "What are the admission requirements for undergraduate programs?", 1),
    ("EXACT", "What undergraduate programs are offered at the university?", 6),
    ("EXACT", "How do I apply for admission?", 11),
    ("EXACT", "What is the tuition fee structure?", 16),
    ("EXACT", "What scholarships are available for students?", 21),

    # ---------------- PARAPHRASED ----------------
    ("PARAPHRASED", "What do I need to get admitted?", 1),
    ("PARAPHRASED", "Which degrees can I study here?", 6),
    ("PARAPHRASED", "How can I submit my application?", 11),
    ("PARAPHRASED", "How much are the fees?", 16),
    ("PARAPHRASED", "Is financial aid available?", 21),
    ("PARAPHRASED", "When is the last date to apply for fall?", 12),
    ("PARAPHRASED", "Who can join the SafeX internship?", 32),
    ("PARAPHRASED", "How long does the SafeX internship last?", 33),
    ("PARAPHRASED", "Will I get a certificate from SafeX?", 37),
    ("PARAPHRASED", "What is my minimum GPA to keep my scholarship?", 25),

    # ---------------- FALLBACK / IRRELEVANT ----------------
    ("FALLBACK", "What is the weather like today?", None),
    ("FALLBACK", "Tell me a joke", None),
    ("FALLBACK", "What is the capital of France?", None),
    ("FALLBACK", "Who won the cricket match yesterday?", None),
    ("FALLBACK", "What should I eat for lunch?", None),
]


def run_evaluation(faq_path: str = "data/faqs.csv"):

    retriever = FAQRetriever(faq_path)
    results = []

    print("\n" + "=" * 70)
    print("              UNIVERSITY FAQ CHATBOT EVALUATION")
    print("=" * 70)

    current_category = None

    for category, query, expected_id in TEST_CASES:

        # Print category heading when category changes
        if category != current_category:

            if current_category is not None:
                print()

            if category == "EXACT":
                print("\n[1] EXACT FAQ QUESTIONS")
            elif category == "PARAPHRASED":
                print("\n[2] PARAPHRASED FAQ QUESTIONS")
            elif category == "FALLBACK":
                print("\n[3] IRRELEVANT QUESTIONS / FALLBACK TEST")

            print("-" * 70)
            current_category = category

        result = retriever.retrieve(query)

        predicted_id = result["faq_id"]
        similarity = round(result["similarity"], 4)

        correct = predicted_id == expected_id

        results.append({
            "category": category,
            "query": query,
            "expected_id": expected_id,
            "predicted_id": predicted_id,
            "similarity": similarity,
            "matched_question": result["matched_question"],
            "correct": correct,
        })

        status = "PASS" if correct else "FAIL"

        print(f"\n[{status}] {query}")
        print(f"    Expected FAQ : {expected_id}")
        print(f"    Predicted FAQ: {predicted_id}")
        print(f"    Similarity   : {similarity}")

        if expected_id is None:
            if predicted_id is None:
                print("    Response     : FALLBACK triggered correctly")
            else:
                print("    Response     : Incorrectly matched an FAQ")
        else:
            if result["matched_question"]:
                print(f"    Matched FAQ  : {result['matched_question']}")

    # CREATE DATAFRAME AND SAVE LOG
    df = pd.DataFrame(results)

    df.to_csv(
        "outputs/accuracy_test_log.csv",
        index=False
    )

    # OVERALL RESULTS
    total = len(df)
    correct = int(df["correct"].sum())
    incorrect = total - correct
    accuracy = (correct / total) * 100

    # CATEGORY RESULTS
    exact_df = df[df["category"] == "EXACT"]
    paraphrased_df = df[df["category"] == "PARAPHRASED"]
    fallback_df = df[df["category"] == "FALLBACK"]

    exact_correct = int(exact_df["correct"].sum())
    paraphrased_correct = int(paraphrased_df["correct"].sum())
    fallback_correct = int(fallback_df["correct"].sum())

    exact_accuracy = (exact_correct / len(exact_df)) * 100
    paraphrased_accuracy = (
        paraphrased_correct / len(paraphrased_df)
    ) * 100
    fallback_accuracy = (
        fallback_correct / len(fallback_df)
    ) * 100

    # FINAL SUMMARY
    print("\n")
    print("                     EVALUATION SUMMARY")
    print("=" * 70)

    print(
        f"\nExact Questions       : "
        f"{exact_correct}/{len(exact_df)} correct "
        f"({exact_accuracy:.2f}%)"
    )

    print(
        f"Paraphrased Questions : "
        f"{paraphrased_correct}/{len(paraphrased_df)} correct "
        f"({paraphrased_accuracy:.2f}%)"
    )

    print(
        f"Fallback Questions    : "
        f"{fallback_correct}/{len(fallback_df)} correct "
        f"({fallback_accuracy:.2f}%)"
    )

    print("\n" + "-" * 70)

    print(f"Total Questions       : {total}")
    print(f"Correct               : {correct}")
    print(f"Incorrect             : {incorrect}")
    print(f"Overall Accuracy      : {accuracy:.2f}%")

    print("-" * 70)

    # FALLBACK SUCCESS
    if fallback_correct == len(fallback_df):
        print("Fallback Handling     : PASS")
        print("All irrelevant queries correctly triggered fallback.")
    else:
        print("Fallback Handling     : NEEDS IMPROVEMENT")

    # FAILURES
    failures = df[df["correct"] == False]

    if not failures.empty:

        print("\n" + "=" * 70)
        print("                         FAILED CASES")
        print("=" * 70)

        for _, row in failures.iterrows():

            print(f"\nQuestion       : {row['query']}")
            print(f"Category       : {row['category']}")
            print(f"Expected FAQ   : {row['expected_id']}")
            print(f"Predicted FAQ  : {row['predicted_id']}")
            print(f"Similarity     : {row['similarity']}")

    else:
        print("\nAll test cases passed successfully!")

    print("\n" + "=" * 70)
    print("Evaluation log saved to:")
    print("outputs/accuracy_test_log.csv")
    print("=" * 70 + "\n")

    return df


if __name__ == "__main__":
    run_evaluation()