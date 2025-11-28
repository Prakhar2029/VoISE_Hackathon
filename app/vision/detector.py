from deepface import DeepFace
import cv2

class EmotionDetector:
    def __init__(self):
        # Pre-load model if possible or just rely on analyze
        pass

    def analyze_frame(self, frame):
        try:
            # DeepFace expects path or numpy array.
            # enforce_detection=False allows it to return even if no face is found (sometimes useful, or handle error)
            results = DeepFace.analyze(img_path=frame, actions=['emotion'], enforce_detection=False, silent=True)
            
            if not results:
                return 0, "neutral"

            # DeepFace returns a list of dicts (one for each face)
            # We take the first one for simplicity
            result = results[0]
            dominant_emotion = result['dominant_emotion']
            
            # Map emotions to urgency
            # 'fear': 9, 'sad': 7, 'angry': 5, 'neutral': 1, 'happy': 0
            pain_map = {'fear': 9, 'sad': 7, 'angry': 5, 'neutral': 1, 'happy': 0, 'surprise': 3, 'disgust': 4}
            visual_score = pain_map.get(dominant_emotion, 1)
            
            return visual_score, dominant_emotion, result['emotion']
            
        except Exception as e:
            # print(f"Error in emotion detection: {e}")
            return 0, "error", {}

    def process_video(self, video_path, sample_rate=10):
        """
        Scans a video file and returns the frame with the highest urgency score.
        sample_rate: Analyze every Nth frame.
        """
        cap = cv2.VideoCapture(video_path)
        max_score = -1
        best_frame = None
        best_emotion = "neutral"
        best_emotion_dict = {}
        
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            if frame_count % sample_rate != 0:
                continue
                
            # Analyze frame
            score, emotion, emotion_dict = self.analyze_frame(frame)
            
            if score > max_score:
                max_score = score
                best_frame = frame
                best_emotion = emotion
                best_emotion_dict = emotion_dict
                
                # Optimization: If we find a very high score, stop early?
                # For now, let's scan the whole thing (or limit to first 10 seconds)
        
        cap.release()
        
        if best_frame is None:
            # Fallback: try to get the first frame if sampling missed everything
            cap = cv2.VideoCapture(video_path)
            ret, frame = cap.read()
            cap.release()
            if ret:
                s, e, d = self.analyze_frame(frame)
                return s, e, frame, d
            return 0, "N/A", None, {}
            
        return max_score, best_emotion, best_frame, best_emotion_dict
