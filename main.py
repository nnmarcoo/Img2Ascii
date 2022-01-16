import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from blessed import Terminal
from alive_progress import alive_bar
t = Terminal()

def toTxt():
  pass

def toImg(img, scale, bg, c, ch):
  up = 10 
  fntsize = 15
  downscale = img.resize((int(img.width*(scale/100)), int(img.height*(scale/100))))
  upscale = downscale.resize((downscale.width*up, downscale.height*up))
  i = upscale.load()
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

  with alive_bar(int((w/fntsize)*(h/fntsize)), bar='filling', spinner='vertical') as bar:
    for y in range(0,h,fntsize):
      for x in range(0,w,fntsize):
        r,g,b = i[x,y][0], i[x,y][1], i[x,y][2]
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
  p = img.load()
  w,h = img.width,img.height # get width and height of image
  skipx = int(w / (w * (scale/100)))
  skipy = int(h / (h * (scale/100)) * 2.3)

  if format == 'I':
    toImg(img, scale, bg, c, ch)
  elif format == 'T':
    toTxt()


  #elif format == 'T':
    #if os.path.isfile('ASCIIoutput.txt'):
     # os.remove('ASCIIoutput.txt')
 #   txt = open('ASCIIoutput.txt', 'w')
      
        
  #if format == 'I':
    #asciiimg.save('pil_text_font.png')

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
      BGC = input('Enter background color [W/B/O]: ').upper()
      if BGC in 'WBO' and BGC != '':
        getBGC = False
    getExport = True
    while getExport:
      export = input('Enter what you want to export to [I/C/T]: ').upper()
      if export in 'ICT' and export != '':
        getExport = False
      if export == 'T':
        img2ascii(img,int(scale), BGC, 'N', export)
        getColor = False
      else:
        getColor = True  
    while getColor:
      isColor = input('Enter color preference [Y/N]: ').upper()
      if isColor in 'YN' and isColor != '':
        getColor = False
        img2ascii(img, int(scale), BGC, isColor, export)

if __name__ == '__main__':
  main()