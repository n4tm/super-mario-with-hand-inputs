from math import dist
from keyboard import press, release

WRIST = 0
THUMB_CMC = 1
THUMB_MCP = 2
THUMB_IP = THUMB = 3
THUMB_TIP = 4
INDEX_FINGER_MCP = 5
INDEX_FINGER_PIP = 6
INDEX_FINGER_DIP = INDEX_FINGER = 7
INDEX_FINGER_TIP = 8
MIDDLE_FINGER_MCP = 9
MIDDLE_FINGER_PIP = 10
MIDDLE_FINGER_DIP = MIDDLE_FINGER = 11
MIDDLE_FINGER_TIP = 12
RING_FINGER_MCP = 13
RING_FINGER_PIP = 14
RING_FINGER_DIP = RING_FINGER = 15
RING_FINGER_TIP = 16
PINKY_MCP = 17
PINKY_PIP = 18
PINKY_DIP = PINKY = 19
PINKY_TIP = 20
THUMB_THRESHOLD = 80

class Hand:
  def __init__(self, side):
    self.side = side  # 'Left' or 'Right'
    self.is_horz = False
    self.is_thumbs_up = False
    self.is_index_up = False
    self.is_index_down = False
    self.is_middle_up = False
    self.is_ring_up = False
    self.is_pinky_up = False
    self.is_reversed = False

  def set_to_defaults(self):
    self.is_reversed = False
    # Set pawn to Vertical
    self.is_horz = False
    # Set all fingers Down
    self.is_thumbs_up = False
    self.is_index_up = False
    self.is_index_down = False
    self.is_middle_up = False
    self.is_ring_up = False
    self.is_pinky_up = False

  def detect_up_fingers(self, hand_coordinates):
    self.set_to_defaults()

    base_point = hand_coordinates[WRIST][1:]

    def dist_from_base(handPoint):
      return dist(base_point, hand_coordinates[handPoint][1:])
    
    def is_finger_up(finger):
      return dist_from_base(finger) < dist_from_base(finger+1)

    if hand_coordinates[THUMB_TIP][1] >= hand_coordinates[PINKY_TIP][1]: # Because image is mirrored
      self.is_reversed = True

    if dist([base_point[1], 0], [hand_coordinates[MIDDLE_FINGER_TIP][2], 0]) <= dist([base_point[0], 0], [hand_coordinates[MIDDLE_FINGER_TIP][1], 0]):
      self.is_horz = True
    
    if is_finger_up(THUMB) and abs(hand_coordinates[THUMB_TIP][1] - hand_coordinates[INDEX_FINGER_TIP][1]) > THUMB_THRESHOLD:
      self.is_thumbs_up = True
    if is_finger_up(INDEX_FINGER):
      if hand_coordinates[INDEX_FINGER_TIP][2] > hand_coordinates[MIDDLE_FINGER][2]:
        self.is_index_down = True
      else:
        self.is_index_up = True
    if is_finger_up(MIDDLE_FINGER):
      self.is_middle_up = True
    if is_finger_up(RING_FINGER):
      self.is_ring_up = True
    if is_finger_up(PINKY):
      self.is_pinky_up = True
  
class LeftHand(Hand):
  def __init__(self):
    super().__init__('Left')

  def process_inputs(self, hand_coordinates):
    self.detect_up_fingers(hand_coordinates)

    orientation = 'left' if self.is_reversed else 'right'
    if self.is_thumbs_up:
      press(orientation)
    else: 
      release('left')
      release('right')
      
    if self.is_index_up:
      press('up')
    else: 
      release('up')

    if self.is_index_down:
      press('down')
    else:
      release('down')
  
class RightHand(Hand):
  def __init__(self):
    super().__init__('Right')

  def process_inputs(self, hand_coordinates):
    self.detect_up_fingers(hand_coordinates)

    jump_mode = 'x' if self.is_reversed else 'z'
    if self.is_index_up:
      press(jump_mode)
    else:
      release(jump_mode)
      
    # TODO: read special buttons input