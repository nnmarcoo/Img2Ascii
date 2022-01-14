import os
from PIL import Image
from blessed import Terminal
t = Terminal()

def img2ascii(img, scale, bg, c):
  ch = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """
  img = Image.open(img) 
  img = img.convert('RGB')
  p = img.load()

  w,h = img.width,img.height # get width and height of image
  skipx = int(w / (w * (scale/100)))
  skipy = int(h / (h * (scale/100)) * 2.3)

  for y in range(0,h,skipy): # how many lines
    for x in range(0,w,skipx): #how many characters per line
      r,g,b = p[x,y][0], p[x,y][1], p[x,y][2]
      lum = int(((0.2126*r + 0.7152*g + 0.0722*b) / 256) * 70)
      #print(col(ch[lum]), end='')
      #print(ch[lum], end='')
      #colorize(r,g,b,ch[lum])
      #print(t.black(ch[lum]), end='')
      if bg == 'W':
        if c in 'YT':
          col = t.color_rgb(r,g,b)
          print(t.on_white(col(ch[lum])),end='')
        else:
          print(ch[lum],end='')
      elif bg == 'B':
        if c in 'YT':
          col = t.color_rgb(r,g,b)
          print(t.on_black(col(ch[lum])),end='')
        else:
          print(ch[lum],end='')
      else:
        if c in 'YT':
          col = t.color_rgb(r,g,b)
          print(col(ch[lum]),end='')
        else:
          print(ch[lum],end='')
    print()

def clear():
  command = 'clear'
  if os.name in ('nt', 'dos'):
      command = 'cls'
  os.system(command)

def main():
  ask = True
  while ask:
    getImg = True
    while getImg:
      img = input('Enter an image to convert to ASCII: ')
      if os.path.isfile(img):
        getImg = False
    getScale = True
    while getScale:
      scale = input('Enter scale [1-100]: ')
      if scale.isnumeric():
        if int(scale) < 101 and int(scale) > 0:
          getScale = False
    getBGC = True
    while getBGC:
      BGC = input('Enter background color [W/B/NA]: ').upper()
      if BGC in 'WBNA':
        getBGC = False
    getColor = True  
    while getColor:
      isColor = input('Enter color preference [Y/N/T/F]: ').upper()
      if isColor in 'YNTF':
        getColor = False
    img2ascii(img, int(scale), BGC, isColor)



if __name__ == '__main__':
  main()
