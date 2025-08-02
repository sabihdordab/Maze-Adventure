import cv2
import mediapipe as mp
import time
from config import HandGestureSettings, CameraSettings

class HandGestureController:
    def __init__(self):
        self.last_positions = []
        self.position_history_size = HandGestureSettings.POSITION_HISTORY_SIZE
        self.movement_threshold = HandGestureSettings.MOVEMENT_THRESHOLD
        self.last_direction = (0, 0)
        self.direction_hold_time = HandGestureSettings.DIRECTION_HOLD_TIME
        self.last_direction_time = 0
        self.center_zone = HandGestureSettings.CENTER_ZONE
        
        # MediaPipe setup
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=HandGestureSettings.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=HandGestureSettings.MIN_TRACKING_CONFIDENCE
        )
        
    def add_position(self, x, y):
        self.last_positions.append((x, y))
        if len(self.last_positions) > self.position_history_size:
            self.last_positions.pop(0)
    
    def get_smoothed_position(self):
        if not self.last_positions:
            return None
        
        avg_x = sum(pos[0] for pos in self.last_positions) / len(self.last_positions)
        avg_y = sum(pos[1] for pos in self.last_positions) / len(self.last_positions)
        return avg_x, avg_y
    
    def get_direction(self, results, frame_width, frame_height):
        if not results.multi_hand_landmarks:
            return 0, 0
        
        current_time = time.time()
        
        for hand_landmarks in results.multi_hand_landmarks:
            index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x = int(index_tip.x * frame_width)
            y = int(index_tip.y * frame_height)
            
            self.add_position(x, y)
            
            smoothed_pos = self.get_smoothed_position()
            if not smoothed_pos:
                return 0, 0
            
            smooth_x, smooth_y = smoothed_pos
            
            center_x, center_y = frame_width // 2, frame_height // 2
            
            dx = smooth_x - center_x
            dy = smooth_y - center_y
            
            if abs(dx) < self.center_zone and abs(dy) < self.center_zone:
                return 0, 0
            
            new_direction = (0, 0)
            
            if abs(dx) > abs(dy): 
                if abs(dx) > self.movement_threshold:
                    new_direction = (1 if dx > 0 else -1, 0)
            else:
                if abs(dy) > self.movement_threshold:
                    new_direction = (0, 1 if dy > 0 else -1)
            
            if (new_direction != self.last_direction and 
                current_time - self.last_direction_time < self.direction_hold_time):
                return self.last_direction
            
            if new_direction != (0, 0):
                self.last_direction = new_direction
                self.last_direction_time = current_time
            
            return new_direction
        
        return 0, 0
    
    def process_frame(self, frame):
        frame = cv2.flip(frame, 1)
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                )
                
                index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                h, w, _ = frame.shape
                tip_x, tip_y = int(index_tip.x * w), int(index_tip.y * h)
                cv2.circle(frame, (tip_x, tip_y), 10, (255, 255, 0), -1)
                
                center_x, center_y = w // 2, h // 2
                cv2.rectangle(frame, 
                             (center_x - self.center_zone, center_y - self.center_zone), 
                             (center_x + self.center_zone, center_y + self.center_zone), 
                             (0, 255, 255), 2)
        
        return frame, results
    
    def close(self):
        self.hands.close()


class CameraManager:
    def __init__(self):
        self.cap = None
        self.is_active = False
        
    def start_camera(self):
        try:
            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CameraSettings.WIDTH)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CameraSettings.HEIGHT)
                self.cap.set(cv2.CAP_PROP_FPS, CameraSettings.FPS)
                self.is_active = True
                return True
            else:
                self.cap = None
                return False
        except Exception as e:
            print(f"Error starting camera: {e}")
            self.cap = None
            return False
            
    def stop_camera(self):
        if self.cap:
            self.cap.release()
            self.cap = None
        self.is_active = False
        
    def get_frame(self):
        if not self.is_active or not self.cap:
            return None
            
        ret, frame = self.cap.read()
        if ret:
            return frame
        return None
        
    def toggle_camera(self):
        if self.is_active:
            self.stop_camera()
            return False
        else:
            return self.start_camera()
            
    def __del__(self):
        """Cleanup when object is destroyed"""
        if self.cap:
            self.cap.release()