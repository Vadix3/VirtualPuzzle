import cv2
import mediapipe as mp


class HandDetector():
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode  # detection mode, pic or video
        self.maxHands = maxHands  # max number of hands
        self.detectionCon = 0.5  # detection confidence
        self.trackCon = 0.5  # detection track confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils  # The drawing tool to draw the hands stuff

    def findHands(self, img, draw=False):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)  # process the frame and give the results
        # print(results.multi_hand_landmarks) # None if no hands

        if self.results.multi_hand_landmarks:  # if I have hands detected
            for handLms in self.results.multi_hand_landmarks:  # extract info of each hand
                for id, lm, in enumerate(handLms.landmark):  # index and the landmark
                    if draw:
                        self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNum=0, draw=False):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNum]  # specific hand
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape  # height width and channels
                cx, cy = int(lm.x * w), int(lm.y * h)  # Pixel positions of the landmarks
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 25, (210, 0, 210), cv2.FILLED)
        return lmList
