from sentence_transformers import SentenceTransformer, util
import torch

class SymptomAnalyzer:
    def __init__(self):
        # Load the semantic model (lightweight)
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.semantic_enabled = True
        except Exception as e:
            print(f"Warning: Could not load Semantic Model: {e}")
            self.semantic_enabled = False

        # Dictionary of "Kill Words" with weights
        self.symptom_weights = {
            # CRITICAL (10) - Life Threatening
            "cardiac": 10, "arrest": 10, "stroke": 10, "heart": 10, "attack": 10,
            "seizure": 10, "choking": 10, "choke": 10, "anaphylaxis": 10,
            "suicide": 10, "dying": 10, "die": 10, "blue": 10, "cyanosis": 10,
            "unconscious": 10, "responsive": 10, "chest": 10, "crushing": 10,
            
            # HIGH (8-9) - Urgent
            "breath": 9, "breathing": 9, "shortness": 9, "air": 9, "gasping": 9,
            "bleeding": 9, "bleed": 9, "blood": 9, "hemorrhage": 9,
            "broken": 8, "fracture": 8, "bone": 8, "burn": 8, "burned": 8,
            "allergic": 9, "allergy": 9, "swelling": 8, "swollen": 8,
            "vision": 8, "blind": 8, "eye": 8,
            "speech": 8, "slur": 8, "slurred": 8,
            "numb": 8, "numbness": 8, "paralysis": 9, "paralyzed": 9,
            "pregnant": 8, "labor": 9, "baby": 8, "childbirth": 9,
            "faint": 8, "collapse": 8, "passed": 8,
            
            # MEDIUM (5-7) - Serious
            "pain": 6, "paining": 6, "hurts": 6, "hurt": 6, "ache": 5, "aching": 5,
            "stomach": 6, "abdominal": 6, "belly": 6, "gut": 6,
            "vomit": 6, "vomiting": 6, "nausea": 5, "diarrhea": 5,
            "flu": 5, "fever": 5, "temperature": 5, "hot": 4,
            "wound": 6, "cut": 5, "laceration": 6, "infection": 6, "infected": 6,
            "pus": 6, "oozing": 6, "rash": 5, "hives": 6,
            "headache": 5, "migraine": 6, "head": 5,
            "dizzy": 5, "dizziness": 5, "spinning": 5,
            
            # LOW (1-4) - Non-Urgent
            "cough": 3, "coughing": 3, "cold": 2, "runny": 1, "nose": 1,
            "sore": 2, "throat": 2,
            "itch": 2, "itchy": 2, "scratch": 1,
            "bruise": 2, "bruised": 2, "bump": 2,
            "tired": 2, "fatigue": 2, "weak": 3, "weakness": 3,
            "insomnia": 1, "sleep": 1,
            "worry": 2, "anxious": 2, "anxiety": 2, "nervous": 1,
            "scrape": 1, "minor": 1
        }
        
        # Pre-compute embeddings for keys if model is loaded
        if self.semantic_enabled:
            self.keys = list(self.symptom_weights.keys())
            self.key_embeddings = self.model.encode(self.keys, convert_to_tensor=True)

    def calculate_symptom_score(self, text):
        """
        Calculates a symptom score based on keywords found in the text.
        Uses both exact matching and semantic similarity.
        """
        if not text:
            return 0, []

        text_lower = text.lower()
        score = 0
        words_found = []
        matched_keys = set()

        # 1. Exact Match (Fast)
        for word, weight in self.symptom_weights.items():
            if word in text_lower:
                score += weight
                words_found.append(word)
                matched_keys.add(word)

        # 2. Semantic Match (Smart)
        if self.semantic_enabled:
            # Encode the patient text
            # We split by sentence or just encode the whole thing? 
            # Encoding the whole thing might dilute specific symptoms.
            # Let's try encoding the whole text for now, but comparing against single words might be weak.
            # Better: Encode the text and compare against keys.
            
            text_embedding = self.model.encode(text, convert_to_tensor=True)
            
            # Compute cosine similarities
            cosine_scores = util.cos_sim(text_embedding, self.key_embeddings)[0]
            
            # Find matches above threshold
            # Increased threshold to 0.7 to prevent "dizzy" (5) matching "dying" (10)
            threshold = 0.7
            for i, match_score in enumerate(cosine_scores):
                if match_score > threshold:
                    key = self.keys[i]
                    if key not in matched_keys: # Don't double count
                        score += self.symptom_weights[key]
                        words_found.append(f"{key} (Semantic: {match_score:.2f})")
                        matched_keys.add(key)
        
        # Cap the score at 10
        final_score = min(score, 10)
        
        return final_score, words_found
