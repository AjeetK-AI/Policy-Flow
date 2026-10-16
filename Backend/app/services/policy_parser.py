import json

from app.llm.client import client
from app.llm.prompts import POLICY_EXTRACTION_PROMPT
from app.policy.rules import PolicyRule


MODEL = "openai/gpt-oss-120b"


def extract_policy_rules_with_llm(
    rule_blocks: list[dict[str, str]],
) -> list[PolicyRule]:

    all_rules: list[PolicyRule] = []

    for rule in rule_blocks:

        rule_id = rule["rule_id"]
        rule_text = rule["text"]

        prompt = POLICY_EXTRACTION_PROMPT.format(
            rule_id=rule_id,
            rule_text=rule_text,
        )

        response = client.chat.completions.create(
            model=MODEL,
            temperature=0,
            response_format={
                "type": "json_object"
            },
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a policy extraction system. "
                        "Convert the supplied policy rule into "
                        "structured JSON. Return JSON only."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError(
                f"LLM returned an empty response "
                f"for rule {rule_id}"
            )

        data = json.loads(content)

        rule_data = data.get("rule", data)

        all_rules.append(
            PolicyRule(**rule_data)
        )

    return all_rules