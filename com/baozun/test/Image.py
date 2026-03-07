from PIL import Image, ImageDraw, ImageFont
# 创建一个新的蓝色图片，大小为200x200
width = 500
height = 500
text_color=(0, 0, 0)
color = (250, 250, 250)
img = Image.new('RGB', (width, height), color = color)

draw = ImageDraw.Draw(img)

text = "hello world"
# 设置字体和颜色
font = ImageFont.truetype("arial.ttf", 26)  # 需要事先下载arial.ttf字体文件
# draw.text((10, 10), "Hello, World!", fill=(0, 0, 0), font=font)

# 计算文字的宽高（获取文字边界框）
# 注意：ImageDraw.textbbox返回(x0, y0, x1, y1)，其中x1-x0为宽，y1-y0为高
text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]

# 计算文字居中的坐标（文字左上角坐标）
x = (width - text_width) // 2
y = (height - text_height) // 2

# 在图片上绘制文字
draw.text((x, y), text, font=font, fill = text_color)

# 画一个圆，填充颜色为黑色
# draw.ellipse((50, 50, 150, 150), fill=(0, 0, 0))

img.save('D:\\u02\\image\\red.png')
