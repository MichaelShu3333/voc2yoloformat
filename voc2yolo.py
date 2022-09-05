import os
from os import listdir
from os.path import join

import xml.etree.ElementTree as ET

def convert(size, box):
    # size=(width, height)  b=(xmin, xmax, ymin, ymax)
    # x_center = (xmax+xmin)/2        y_center = (ymax+ymin)/2
    # x = x_center / width            y = y_center / height
    # w = (xmax-xmin) / width         h = (ymax-ymin) / height

    # x_center = (box[0] + box[1]) / 2.0
    # y_center = (box[2] + box[3]) / 2.0
    # x = x_center / size[0]
    # y = y_center / size[1]
    cx = (box[0] + box[1]) / (2.0 * size[0])
    cy = (box[2] + box[3]) / (2.0 * size[1])

    w = (box[1] - box[0]) / size[0]
    h = (box[3] - box[2]) / size[1]

    # precision after the decimal point
    precision = 6
    cx = round(cx, precision)
    cy = round(cy, precision)
    w = round(w, precision)
    h = round(h, precision)

    # print(cx, cy, w, h)
    return (cx, cy, w, h)

def getALlFiles(filepath, files_list):
    files = os.listdir(filepath)

    for file in files :
        file = os.path.join(filepath, file)
        if os.path.isdir(file):
            getALlFiles(file, files_list)
        else :
            files_list.append(file)

def convert_annotation(xml_files_path, save_txt_files_path, classes, is_save_cur_path = 1, ignore_difficult = 0):
    xml_files = []
    getALlFiles(xml_files_path, xml_files)
    #for file in xml_files:
    #    print(file)
    # print(xml_files)
    # print(save_txt_files_path)

    for xml_file in xml_files:
        if xml_file.rsplit('.', maxsplit=1)[-1].lower() != 'xml':
            continue

        txt_path = None

        if is_save_cur_path :
            txt_path = os.path.join(xml_file.rsplit('.', maxsplit=1)[0] + '.txt')
        else :
            xmlfile = xml_file.rsplit(os.sep, maxsplit=1)[-1]
            txt_path = os.path.join(save_txt_files_path, xmlfile.rsplit('.', maxsplit=1)[0] + '.txt')

        print(txt_path)
        txt_file = open(txt_path, 'w', encoding="utf-8")

        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text

            # voc foramat difficult = 1 stand for difficult to recognize and ignore
            if ignore_difficult and 1 == int(difficult) :
                continue

            if cls not in classes:
                continue

            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            rect = (float(xmlbox.find('xmin').text),
                 float(xmlbox.find('xmax').text),
                 float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            # b=(xmin, xmax, ymin, ymax)
            # print(w, h, rect)

            yolo_cwh = convert((w, h), rect)
            txt_file.write(str(cls_id) + " " + " ".join([str(a) for a in yolo_cwh]) + '\n')

if __name__ == "__main__":
    # voc format xml label files convert to yolo format txt label files

    # classes
    classes = ['hat', 'person']

    # voc format xml label files' path
    xml_files_path = r'C:\Users\boe\Desktop\voc_tests'

    # save yolo format txt label files' path
    save_txt_path = r'C:\Users\boe\Desktop\1234'

    # whether or not save the same path with orignal path
    is_save_cur_path = 1

    # whether or not ignore to difficult recognize object
    ignore_difficult = 0

    convert_annotation(xml_files_path, save_txt_path, classes, is_save_cur_path, ignore_difficult)