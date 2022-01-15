import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from blessed import Terminal
from alive_progress import alive_bar
t = Terminal()

# https://code-maven.com/create-images-with-python-pil-pillow

def img2ascii(img, scale, bg, c, format):
  ch = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """
  img = Image.open(img) 
  img = img.convert('RGB')
  p = img.load()
  upscale = 15

  w,h = img.width,img.height # get width and height of image
  skipx = int(w / (w * (scale/100)))
  skipy = int(h / (h * (scale/100)) * 2.3)

  if format == 'I':
    if bg == 'B':
      asciiimg = Image.new('RGB', (w*upscale, h*upscale), color = 'black')
    elif bg == 'W':
      asciiimg = Image.new('RGB', (w*upscale, h*upscale), color = 'white')
    else:
      asciiimg = img.resize((w*upscale, h*upscale)).filter(ImageFilter.BoxBlur(75))
      darkness = ImageEnhance.Brightness(asciiimg)
      asciiimg = darkness.enhance(.5)

    fnt = ImageFont.truetype('Arial.ttf', int((upscale * 3) / 1.5))
    d = ImageDraw.Draw(asciiimg)
  elif format == 'T':
    if os.path.isfile('ASCIIoutput.txt'):
      os.remove('ASCIIoutput.txt')
    txt = open('ASCIIoutput.txt', 'w')

    
  with alive_bar((h//skipy)*(w//skipx), bar='filling', spinner='vertical') as bar:
    for y in range(0,h,skipy): # how many line
      for x in range(0,w,skipx): #how many characters per line
        bar()
        r,g,b = p[x,y][0], p[x,y][1], p[x,y][2]
        lum = int(((0.2126*r + 0.7152*g + 0.0722*b) / 256) * 70)
        if format == 'I':
          d.text((x*upscale,y*upscale), ch[::-1][lum], font=fnt, fill=(r, g, b))
        if format == 'T':
          txt.write(ch[lum])
      if format == 'T':
        txt.write('\n')
      
        
  if format == 'I':
    asciiimg.save('pil_text_font.png')

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