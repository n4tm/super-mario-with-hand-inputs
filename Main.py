import mediapipe as mp
import cv2 as cv
from subprocess import call
from Hand import LeftHand, RightHand
from keyboard import release

def release_all_possible_keys():
  release('x')
  release('right')
  release('left')

def process_hand_inputs(multi_hand_landmarks):
  for hand_landmarks in multi_hand_landmarks:
    # Get Hand Cordinates (HC values)
    hand_coordinates = []
    for index , landmark in enumerate(hand_landmarks.landmark):
      x_cordinate , y_cordinate = landmark.x*imgW , landmark.y*imgH
      hand_coordinates.append([index,x_cordinate,y_cordinate])
    is_on_right_side = hand_coordinates[0][1] < imgW/2 # Because image is mirrored
    hand = right_hand if is_on_right_side else left_hand
    hand.process_inputs(hand_coordinates)

call(['super_mario_world.html'], shell=True)

mp_hands = mp.solutions.hands
cap = cv.VideoCapture(0)

left_hand = LeftHand()
right_hand = RightHand()

with mp_hands.Hands(max_num_hands=2) as hands_dectection:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue

    # To improve performance, marking the image as not writeable 
    image.flags.writeable = False
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = hands_dectection.process(image)

    # Flip the image horizontally for a selfie-view display.
    cv.imshow('Hand gestures detection', cv.flip(image,1))

    # Images shape
    imgH,imgW=image.shape[:2]
    if not results.multi_hand_landmarks:
      print('no hands detected')
      release_all_possible_keys()
      continue

    process_hand_inputs(results.multi_hand_landmarks)
    
    is_esc_key_pressed = cv.waitKey(5) & 0xFF == ord('\x1b')
    if is_esc_key_pressed:
      break

cap.release()
release_all_possible_keys()