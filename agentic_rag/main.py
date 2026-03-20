from src.rag_tools import plan_query, refine_query_if_needed, retrieve_context


def demo(query: str) -> None:
    plan = plan_query(query)
    first = retrieve_context(plan["planned_query"], top_k=3)

    if first["count"] == 0:
        refined = refine_query_if_needed(plan["planned_query"])
        second = retrieve_context(refined["refined_query"], top_k=3)
        result = second
    else:
        result = first

    print("Plan:", plan)
    print("Retrieval:", result)


if __name__ == "__main__":
    demo("How do firebase rules work?")
