import os
import shutil

valid_images_path = r'valid_images'
valid_label_path = r'valid_labels'
images_path = r'images'
labels_path = r'labels'
image_suffix = 'jpg'
label_suffix = 'txt'
num = 10

def getALlFiles(filepath, files_list):
    files = os.listdir(filepath)

    for file in files :
        file = os.path.join(filepath, file)
        if os.path.isdir(file):
            getALlFiles(file, files_list)
        else :
            files_list.append(file)

def getALlSuffixFiles(filepath, suffix_files_list, suffix):
    files = os.listdir(filepath)
    suffix = suffix.lower()

    for file in files :
        if suffix == file.rsplit('.', maxsplit=1)[-1].lower():
            file = os.path.join(filepath, file)
            if os.path.isdir(file):
                getALlSuffixFiles(file, suffix_files_list, suffix)
            else :
                suffix_files_list.append(file)
                #print(file)

def shuffle(image_path, label_path, image_suffix, num, valid_images_path, valid_label_path, label_suffix):
    images = []
    labels = []
    getALlSuffixFiles(image_path, images, image_suffix)
    getALlSuffixFiles(labels_path, labels, label_suffix)
    print(len(images))

    if (False == os.path.exists(valid_images_path)) or (False == os.path.isdir(valid_images_path)):
        os.mkdir(valid_images_path)

    if (False == os.path.exists(valid_label_path)) or (False == os.path.isdir(valid_label_path)):
        os.mkdir(valid_label_path)

    valid_images_path += os.sep
    valid_label_path += os.sep
    print(valid_images_path)
    print(valid_label_path)

    i = 0
    for image in images:
        #print(image)
        # image = valid_label_path + os.sep + image.rsplit(os.sep, maxsplit=1)[-1].rsplit('.', maxsplit=1)[-2] + '.' + label_suffix
        label = label_path + os.sep + image.rsplit(os.sep, maxsplit=1)[-1].rsplit('.', maxsplit=1)[-2] + '.' + label_suffix
        if os.path.exists(label):
            #print(image)
            #print(label)
            i +=1
            if 0 == i % num :
                #print("i = %d"%i)
                shutil.move(image, valid_images_path)
                shutil.move(label, valid_label_path)
        else :
            os.remove(image)
            print("label file is not exist:%s" % label)

shuffle(images_path, labels_path, image_suffix, num, valid_images_path, valid_label_path, label_suffix)
