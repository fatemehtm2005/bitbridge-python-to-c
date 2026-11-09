name = input("Name: ")
score_text = input("Score: ")
score = int(score_text)

if score >= 10:
    print("Excellent", name, sep=", ")
else:
    print("Keep practicing", name, sep=", ")
