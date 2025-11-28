import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.logic.symptoms import SymptomAnalyzer

def test_score():
    analyzer = SymptomAnalyzer()
    text = "feeling dizzy"
    score, keywords = analyzer.calculate_symptom_score(text)
    
    print(f"Text: '{text}'")
    print(f"Score: {score}")
    print("Matches:")
    for k in keywords:
        print(f" - {k}")

if __name__ == "__main__":
    test_score()
