import json
from concurrent.futures import ThreadPoolExecutor

from app.llm.client import client
from app.llm.prompts import POLICY_EXTRACTION_PROMPT
from app.policy.rules import PolicyRule


MODEL = "openai/gpt-oss-120b"


def _extract_rule_with_llm(rule: dict[str, str]) -> PolicyRule:
    rule_id = rule["rule_id"]
    rule_text = rule["text"]

    prompt = POLICY_EXTRACTION_PROMPT.format(
        rule_id=rule_id,
        rule_text=rule_text,
    )

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a policy extraction system. "
                    "Convert the supplied policy rule into "
                    "structured JSON. Return JSON only."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError(f"LLM returned an empty response for rule {rule_id}")

    data = json.loads(content)
    print("\nLLM RAW JSON:")
    print(json.dumps(data, indent=2))

    rule_data = data.get("rule", data)
    return PolicyRule(**rule_data, source=rule_text)


def extract_policy_rules_with_llm(
    rule_blocks: list[dict[str, str]],
) -> list[PolicyRule]:
    if not rule_blocks:
        return []

    with ThreadPoolExecutor(max_workers=min(4, len(rule_blocks))) as executor:
        return list(executor.map(_extract_rule_with_llm, rule_blocks))