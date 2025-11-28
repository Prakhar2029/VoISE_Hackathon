import cv2

class Camera:
    def __init__(self, source=0):
        self.cap = cv2.VideoCapture(source)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def release(self):
        self.cap.release()

    def record_video(self, output_path, duration=5):
        """
        Records video from the camera for a specified duration.
        """
        if not self.cap.isOpened():
            return False
            
        # Define codec and create VideoWriter
        # mp4v is generally compatible
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = 20.0
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        start_time = cv2.getTickCount()
        
        # Record for 'duration' seconds
        # cv2.getTickCount() returns ticks, getTickFrequency() returns ticks per second
        while (cv2.getTickCount() - start_time) / cv2.getTickFrequency() < duration:
            ret, frame = self.cap.read()
            if ret:
                out.write(frame)
            else:
                break
                
        out.release()
        return True
