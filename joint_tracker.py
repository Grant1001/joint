import cv2
import mediapipe as mp
import numpy as np

class JointStressTracker:
    def __init__(self):
        # Initialize MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Colors (B, G, R)
        self.COLOR_SAFE = (0, 255, 0)    # Green
        self.COLOR_WARN = (0, 255, 255)  # Yellow
        self.COLOR_DANGER = (0, 0, 255)  # Red

    def calculate_angle(self, a, b, c):
        """
        Calculates the angle between three points (a, b, c).
        b is the vertex (the joint).
        """
        a = np.array(a) # First point
        b = np.array(b) # Vertex point
        c = np.array(c) # End point
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle > 180.0:
            angle = 360-angle
            
        return angle

    def get_stress_level(self, angle):
        """
        Heuristic for stress based on joint deviation from neutral.
        For an elbow:
        - 80-120 degrees is generally 'neutral' (Low Stress)
        - < 50 or > 150 implies extreme flexion/extension (High Stress)
        """
        if angle > 160 or angle < 40:
            return "HIGH", self.COLOR_DANGER
        elif angle > 140 or angle < 60:
            return "MEDIUM", self.COLOR_WARN
        else:
            return "LOW", self.COLOR_SAFE

    def run(self):
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not access the camera.")
            return

        print("Starting video stream. Press 'q' to quit.")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = self.pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # --- LEFT ARM ANALYSIS ---
                # Get coordinates
                shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                         landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                         landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                # Calculate angle
                angle = self.calculate_angle(shoulder, elbow, wrist)
                
                # Determine stress/risk level
                stress_label, stress_color = self.get_stress_level(angle)

                # Visualize
                # Get actual pixel coordinates for the elbow to place text
                h, w, _ = image.shape
                elbow_px = tuple(np.multiply(elbow, [w, h]).astype(int))

                cv2.putText(image, str(int(angle)), 
                           elbow_px, 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                
                # Status Box
                cv2.rectangle(image, (0,0), (250, 85), (245, 117, 16), -1)
                
                # Display Angle
                cv2.putText(image, 'JOINT ANGLE', (15,12), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(image, str(int(angle)), 
                            (10,70), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
                
                # Display Stress
                cv2.putText(image, 'STRESS LEVEL', (120,12), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(image, stress_label, 
                            (115,70), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, stress_color, 2, cv2.LINE_AA)
                
            except Exception as e:
                # pass if landmarks not visible
                pass

            # Render detections
            self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                    self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                     )               

            cv2.imshow('Joint Stress Tracker', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    tracker = JointStressTracker()
    tracker.run()