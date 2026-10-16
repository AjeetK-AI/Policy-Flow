from app.services.llm_policy_parser import (
    extract_policy_rules_with_llm
)


print("TEST STARTED")


rule_blocks = [
    {
        "rule_id": "2.1",
        "text": (
            "Refunds below ₹10,000 may be approved "
            "automatically."
        ),
    },
    {
        "rule_id": "2.2",
        "text": (
            "Refunds from ₹10,000 through ₹50,000 "
            "require manager approval."
        ),
    },
]


print("RULE BLOCKS CREATED")
print(rule_blocks)


print("CALLING LLM...")


rules = extract_policy_rules_with_llm(
    rule_blocks
)


print("LLM CALL COMPLETED")
print("NUMBER OF RULES:", len(rules))


for rule in rules:
    print("\nRULE:")
    print(rule.model_dump())
