import os
from PIL import Image
from blessed import Terminal
t = Terminal()

def img2ascii(img, scale):
  ch = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """
  line = ''
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
      line += ch[lum]
    #print(t.on_white(t.black(line)))
    print(line)
    line = ''

def clear():
  command = 'clear'
  if os.name in ('nt', 'dos'):
      command = 'cls'
  os.system(command)

def main():
  ask = True
  while ask:
      getFile = True
      while getFile:
          file = input('Enter a file to convert to ASCII: ')
          if os.path.isfile(file) :
            scale = int(input('Enter the scale of the ASCII image (1-100): '))
            if scale < 101 and scale > 0:
              img2ascii(file, scale)
              getFile = False
          else:
              print(file + ' is not a valid file.')
          askAgain = True
      while askAgain:
          response = input('Do you want to enter another file? Y/YES/N/NO ==> ')
          response = response.upper()
          if response in ("Y", "YES"):
              clear()
              askAgain = False
          elif response in ("N", "NO"):
              askAgain = False
              ask = False


if __name__ == '__main__':
  main()