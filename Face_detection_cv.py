# A code designed to identify if there is a facial image in a photo located in a specific location (in this case used to identify if there is an ID card on the contract).
# If the face is contained then the code returns 1

import pandas as pd
import cv2
from os import listdir
from os.path import isfile, join


# choose your windows path
docpath = r'your_windows_path'  # change path  your_windows_path

# making a list of files to checking
docfiles = [f.upper() for f in listdir(docpath) if isfile(join(docpath, f))]
# cut file extension
doc = [f for f in docfiles if '.JPG' in f[-4:]]

path = []
file = []
result= []

# cv2 reading images and try to rotate on every side
for i in doc:

    image = cv2.imread(rf'{docpath}\{i}')

    r = 1200.0 / image.shape[1]
    dim = (1200, int(image.shape[0] + r))

    image_resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    # of the image
    (h, w) = image_resized.shape[:2]
    center = (w / 2, h / 2)
    scale = 0.55

    # rotate the image by 360 degrees
    M_1 = cv2.getRotationMatrix2D(center, 360, scale)
    img_1 = cv2.warpAffine(image_resized, M_1, (w, h))
    # rotate the image by 90 degrees
    M_2 = cv2.getRotationMatrix2D(center, 90, scale)
    img_2 = cv2.warpAffine(image_resized, M_2, (w, h))
    # rotate the image by 180 degrees
    M_3 = cv2.getRotationMatrix2D(center, 180, scale)
    img_3 = cv2.warpAffine(image_resized, M_3, (w, h))
    # rotate the image by 270 degrees
    M_4 = cv2.getRotationMatrix2D(center, 270, scale)
    img_4 = cv2.warpAffine(image_resized, M_4, (w, h))

    tolerance = 0

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


    def rotation_img(img):

        # Read the image
        image = img
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        l_id = len(faces)
        return l_id

# checking the photo in each position
    check_0 = int(rotation_img(img_1)) + int(rotation_img(img_2)) + int(rotation_img(img_3)) + int(rotation_img(img_4))

    if check_0 > 0:
        check = 1
    else:
        check = 0

    # print(check)

    path.append((rf'{docpath}\{i}'))
    file.append(i)
    result.append(check)


summary_list = list(zip(path, file, result))

#sumamry list extract to Excel file
summary_df = pd.DataFrame(summary_list, columns=('sciezka', 'plik', 'wynik'))
summary_df.to_excel("ID_check.xlsx",
                    sheet_name='ID_check_')


