# Accuracy
expected = ["buy", "hold", "sell"]
predicted = ["buy", "hold", "hold"]
correct = sum(a == b for a, b in zip(expected, predicted))
accuracy = correct / len(expected)
print(accuracy)

