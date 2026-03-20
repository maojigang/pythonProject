from PIL import Image, ImageDraw, ImageFont


def createImage(width: int, height: int, color: tuple, text_color: tuple, text: str, path: str,
                quality: int = 95,
                format: str = "JPEG"):
    # 创建一个新的蓝色图片，大小为200x200
    img = Image.new('RGB', (width, height), color=color)
    draw = ImageDraw.Draw(img)

    # 设置字体和颜色
    font = ImageFont.truetype("arial.ttf", 26)  # 需要事先下载arial.ttf字体文件

    # 计算文字的宽高（获取文字边界框）
    # 注意：ImageDraw.textbbox返回(x0, y0, x1, y1)，其中x1-x0为宽，y1-y0为高
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # 计算文字居中的坐标（文字左上角坐标）
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    # 在图片上绘制文字
    draw.text((x, y), text, font=font, fill=text_color)
    # 画一个圆，填充颜色为黑色
    # draw.ellipse((50, 50, 150, 150), fill=(0, 0, 0))
    if format.upper() == "PNG":
        img.save(path, format=format)
    else:
        img.save(path, format=format, quality=quality, optimize=True)


if __name__ == '__main__':
    imageColor = []
    imageColor.append({"name": 'red', "color": (255, 0, 0)})
    imageColor.append({"name": 'blue', "color": (0, 0, 255)})
    imageColor.append({"name": 'green', "color": (0, 255, 0)})
    imageColor.append({"name": 'yellow', "color": (255, 255, 0)})
    imageColor.append({"name": 'orange', "color": (255, 165, 0)})
    imageColor.append({"name": 'white', "color": (255, 255, 255)})
    txt = "empty_link"
    for item in imageColor:
        createImage(500, 500, item['color'], (255, 160, 122), txt,
                    "D:\\u02\\image\\" + txt + "_" + item['name'] + ".jpg")
