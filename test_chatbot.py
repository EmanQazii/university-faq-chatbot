from src.faq_retriever import FAQRetriever


def main():
    retriever = FAQRetriever("data/faqs.csv")

    print("\nUniversity FAQ Chatbot")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("You: ").strip()

        if query.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not query:
            continue

        result = retriever.retrieve(query)

        print(f"\nBot: {result['answer']}\n")


if __name__ == "__main__":
    main()