# import cv2 library
import cv2

sensor = '38873_028_2-S_MAIN0'
picdate = '03-22-22'
img0 = 1

batch = sensor[0:5]
if '2-S' in sensor:
    h_imgs = 26
    v_imgs = 32
    type = '2S'
else:
    h_imgs = 13
    v_imgs = 33
    type = 'PSS'

#h_dir = 'S:\\PreProduction\\Visual Inspection\\2S\\36797\\36797_020_2-S_MAIN0\\11-1-21\\'
h_dir = 'S:\\PreProduction\\Visual Inspection\\'+type+'\\'+batch+'\\'+sensor+'\\'+picdate+'\\'
img_pfx = '2S_Pos1-'

for j in range(h_imgs):
    print(h_dir+img_pfx+str(img0+j)+'.PNG')
    img1 = cv2.imread(h_dir+img_pfx+str(img0+j)+'.png')
    #cv2.imshow("test", img1)
    for i in range(v_imgs-1):
        #print(h_dir + img_pfx + str(img0 + j) + '.PNG', h_dir + img_pfx + str(img0 + h_imgs*(i + 1)) + '.PNG')
        img2 = cv2.imread(h_dir + img_pfx + str(img0 + j + h_imgs*(i + 1)) + '.PNG')
        img1 = cv2.vconcat([img2, img1])

    imcol = cv2.imwrite(h_dir + 'Col_' + str(j) + ".PNG", img1)

print("Making big picture")
img1 = cv2.imread(h_dir + 'Col_0.PNG')
for j in range(h_imgs-1):
    img2 = cv2.imread(h_dir + 'Col_' + str(j+1) + ".PNG")
    img1 = cv2.hconcat([img1, img2])

imwhole = cv2.imwrite(h_dir + 'Whole.PNG', img1)