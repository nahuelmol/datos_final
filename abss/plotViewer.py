import cv2
import pyautogui
from abss.fs import currentProject

def seePlot(cmd):
    pname = currentProject(['project_name'])
    ppath = 'prs\{}\outputs\{}'.format(pname, cmd.target)
    img = cv2.imread(ppath)

    screen_w, screen_h = pyautogui.size()
    p = 0.5 
    max_w = int(screen_w * p)
    max_h = int(screen_h * p)
    h, w  = img.shape[:2]
    ratio = min(max_w / w, max_h / h)
    new_w = int(w * ratio)
    new_h = int(h * ratio)

    cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    cv2.imshow('imagen', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    

