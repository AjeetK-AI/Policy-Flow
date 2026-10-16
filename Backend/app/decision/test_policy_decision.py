from app.decision.policy_decision import make_policy_decision


facts = {
    "amount": 5000,
    "days_since_purchase": 10,
    "evidence_present": True,
    "fraud_indicator": False
}


result = make_policy_decision(
    action="refund",
    facts=facts
)

print(result)