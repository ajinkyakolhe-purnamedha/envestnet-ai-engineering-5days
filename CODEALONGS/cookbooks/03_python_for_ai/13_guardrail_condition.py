# Guardrail condition
cash = 5_000
proposed_amount = 3_500
if cash - proposed_amount < 2_000:
    print("Rejected")
else:
    print("Allowed")

