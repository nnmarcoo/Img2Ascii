import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from blessed import Terminal
from alive_progress import alive_bar
t = Terminal() #object creation usage :O

def toCli(img, scale, bg, c, ch):
  p = img.load()
  w,h = img.width,img.height # get width and height of image
  skipx = int(w / (w * (scale/100)))
  skipy = int(h / (h * (scale/100)) * 2.3)
  for y in range(0,h,skipy):
    for x in range(0,w,skipx):
      r,g,b = p[x,y][0], p[x,y][1], p[x,y][2]
      lum = int(((0.2126*r + 0.7152*g + 0.0722*b) / 256) * 70)
      if bg == 'W':
        if c == 'Y':
          color = t.color_rgb(r,g,b)
          print(t.on_white(color(ch[lum])),end='')
        else:
          print(t.on_white(t.black(ch[lum])),end='')
      elif bg == 'B':
        if c == 'Y':
          color = t.color_rgb(r,g,b)
          print(t.on_black(color(ch[lum])),end='')
        else:
          print(t.on_black(t.white(ch[lum])),end='')
      else:
        bcolor = t.on_color_rgb(r-30,g-30,b-30)
        if c == 'Y':
          color = t.color_rgb(r,g,b)
          print(bcolor(color(ch[lum])),end='')
        else:
          print(bcolor(t.white(ch[lum])),end='')
    print()

def toTxt(img, scale,ch):
  p = img.load()
  w,h = img.width,img.height # get width and height of image
  skipx = int(w / (w * (scale/100)))
  skipy = int(h / (h * (scale/100)) * 2.3)
  if os.path.isfile('ASCIIoutput.txt'):
    os.remove('ASCIIoutput.txt')
  txt = open('ASCIIoutput.txt', 'w')
  with alive_bar(int((w/skipx)*(h/skipy)), bar='classic', spinner='classic', stats=False) as bar:
    for y in range(0,h,skipy):
      for x in range(0,w,skipx):
        r,g,b = p[x,y][0], p[x,y][1], p[x,y][2]
        lum = int(((0.2126*r + 0.7152*g + 0.0722*b) / 256) * 70)
        txt.write(ch[lum])
        bar()
      txt.write('\n')

def toImg(img, scale, bg, c, ch):
  up = 15 
  fntsize = 20
  downscale = img.resize((int(img.width*(scale/100)), int(img.height*(scale/100))))
  upscale = downscale.resize((downscale.width*up, downscale.height*up))
  p = upscale.load()
  w,h = upscale.width,upscale.height

  if bg == 'B':
      asciiimg = Image.new('RGB', (w, h), color = 'black')
  elif bg == 'W':
    asciiimg = Image.new('RGB', (w, h), color = 'white')
  else:
    asciiimg = upscale.filter(ImageFilter.BoxBlur(25))
    darkness = ImageEnhance.Brightness(asciiimg)
    asciiimg = darkness.enhance(.4)
  fnt = ImageFont.truetype('Arial.ttf', fntsize)
  d = ImageDraw.Draw(asciiimg)
  
  with alive_bar(int((w/fntsize)*(h/fntsize)), bar='filling', spinner='vertical', stats=False) as bar:
    for y in range(0,h,fntsize):
      for x in range(0,w,fntsize):
        r,g,b = p[x,y][0], p[x,y][1], p[x,y][2]
        lum = int(((0.2126*r + 0.7152*g + 0.0722*b) / 256) * 70)
        if c == 'Y':
          d.text((x,y), ch[::-1][lum], font=fnt, fill=(r, g, b))
        else:
          if bg == 'W':
            d.text((x,y), ch[::-1][lum], font=fnt, fill=(0, 0, 0))
          else:
            d.text((x,y), ch[::-1][lum], font=fnt, fill=(255, 255, 255))
        bar()
    asciiimg.save('ASCIIoutput.png')

def img2ascii(img, scale, bg, c, format):
  ch = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """
  img = Image.open(img) 
  img = img.convert('RGB')

  if format == 'I':
    toImg(img, scale, bg, c, ch)
  elif format == 'T':
    toTxt(img, scale, ch)
  else:
    toCli(img, scale, bg, c, ch)

def clear():
  command = 'clear'
  if os.name in ('nt', 'dos'):
      command = 'cls'
  os.system(command)

def desc():
  print('This is a simple tool to convert images to ASCII.\n\nUsage:\n\tBG Color:\n\t [W] White background\n\t [B] Black background\n\t [O] Original image behind the ASCII\n\tExport Type:\n\t [I] Image file\n\t [T] Text file\n\t [C] Console\nWarning:\n\tThis calculation gets exponentially longer as the input gets larger\n\tYou will need to lower the scale for large images')

def main():
  desc()
  ask = True
  while ask:
    getImg = True
    while getImg:
      img = input('\n→ Enter an image to convert to ASCII: ')
      if os.path.isfile(img):
        getImg = False
    getScale = True
    while getScale:
      scale = input('→ Enter scale [1-100]: ')
      if scale.isnumeric():
        if int(scale) < 101 and int(scale) > 0:
          getScale = False
    getBGC = True
    while getBGC:
      BGC = input('→ Enter background color [W/B/O]: ').upper()
      if BGC in 'WBO' and BGC != '':
        getBGC = False
    getExport = True
    while getExport:
      export = input('→ Enter what you want to export to [I/C/T]: ').upper()
      if export in 'ICT' and export != '':
        getExport = False
      if export == 'T':
        img2ascii(img,int(scale), BGC, 'N', export)
        getColor = False
      else:
        getColor = True  
    while getColor:
      isColor = input('→ Enter color preference [Y/N]: ').upper()
      if isColor in 'YN' and isColor != '':
        getColor = False
        img2ascii(img, int(scale), BGC, isColor, export)

if __name__ == '__main__':
  main()
