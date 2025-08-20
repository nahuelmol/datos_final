import cv2
import os
import pyautogui
import imghdr

from abss.fs import current_project

def take_number(code, place):
    aux = 0
    if place == 'last':
        for each in os.listdir('prs\{}\outputs'.format(pname)):
            if code == (each.split("_")[0]):
                if int(n[1]) > aux:
                    aux = n
    elif place == 'first':
        for each in os.listdir('prs\{}\outputs'.format(pname)):
            if code == (each.split("_")[0]):
                if int(n[1]) > aux:
                    aux = n
    else:
        if place.isdigit():
            return True, int(place)
        else:
            print('not valid number introduced')
            return False, None

    return True, aux

def find_plt_file(code, number):
    files = []
    if number == 'last':
        res, number = take_number(code, 'last')
    elif number == 'first':
        res, number = take_number(code, 'first')
    else:
        res, number = take_number(None, number)

    pname = current_project(['project_name'])
    for each in os.listdir('prs\{}\outputs'.format(pname)):
        name = each.split("_")
        if(int(name[1]) == number) and (name[0] == code):
            files.append(each)

    outs = []
    for file in files:
        filepath = 'prs\{}\outputs\{}'.format(pname, file)
        if(imghdr.what(filepath) == 'png'):
            outs.append(1)
        else:
            outs.append(0)

    for idx, item in enumerate(outs):
        if item == 0:
            files.pop(idx)

    return files

def seePlot(cmd):
    pname = current_project(['project_name'])
    filenames = find_plt_file(cmd.cond, cmd.number)
    for filename in filenames:
        ppath = 'prs\{}\outputs\{}'.format(pname, filename)
        img = cv2.imread(ppath)

        screen_w, screen_h = pyautogui.size()
        p = 0.5 
        h, w  = img.shape[:2]
        new_h = int(screen_h * p)
        scale_factor = new_h / h
        new_w = int(w * scale_factor)

        resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
        cv2.imshow('imagen', resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

