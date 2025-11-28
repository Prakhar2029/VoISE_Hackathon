class UrgencyScorer:
    def __init__(self):
        pass

    def calculate_final_score(self, visual_score, symptom_score):
        """
        Combines Visual + Symptom scores into a final priority score.
        Formula: Final_Urgency_Score = (Visual_Pain_Score * 0.6) + (Symptom_Word_Score * 0.4)
        """
        # Ensure scores are numbers
        visual_score = float(visual_score)
        symptom_score = float(symptom_score)
        
        # Calculate weighted score
        final_score = (visual_score * 0.6) + (symptom_score * 0.4)
        
        return round(final_score, 2)
