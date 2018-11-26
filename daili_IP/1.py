import shutil

from PIL import Image

for n in range(300):
    for m in range(4):
        try:
            count = 0
            a = Image.open('./image1/' + str(n) + '_' + str(m) + '.jpg').convert('L').resize((15, 15))
            for i in range(4):
                a = a.transpose(Image.ROTATE_90)
                for l_n in range(n + 1, 300):
                    for l_m in range(4):
                        try:
                            count = 0
                            b = Image.open('./image1/' + str(l_n) + "_" + str(l_m) + '.jpg').convert('L').resize(
                                (15, 15))
                            # print(b)
                            for x in range(14):
                                for y in range(14):
                                    color1 = a.load()[x + 1, y] - a.load()[x, y]
                                    color2 = b.load()[x + 1, y] - b.load()[x, y]
                                    color3 = a.load()[x, y + 1] - a.load()[x, y]
                                    color4 = b.load()[x, y + 1] - b.load()[x, y]
                                    if color1 * color2 > 0 and color3 * color4 > 0:
                                        count += 1
                            if count > 90:
                                filename = str(l_n) + '_' + str(l_m) + '.jpg'
                                shutil.move("./image1/" + filename, "./image2/" + filename)
                                print(str(n) + "_" + str(m) + '.jpg', ' 相似 ', str(l_n) + '_' + str(l_m) + '.jpg')
                        except:
                            pass
        except:
            pass
    print('已处理 ', (n + 1) * 4, ' 张图片')
print('处理完毕')
