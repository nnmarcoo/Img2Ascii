import os
from PIL import Image
from blessed import Terminal
t = Terminal()

def colorize(r,g,b):
  vals = {'black': (0,0,0), 'red': (255,0,0), 'green': (0,255,0), 'yellow': (255,255,0), 'blue': (0,0,255), 'magenta': (255,0,255), 'cyan': (0,255,255), 'white': (255,255,255)}
  match = ''
  dist = 256
  for i in vals:
    check = abs(vals[i][0] - r) + abs(vals[i][1] - g) + abs(vals[i][2] - b)
    if check < dist:
      dist = check
      match = i
  return match

def img2ascii(img, scale):
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
      #print(ch[lum], end='')
      colorize(r,g,b,ch[lum])
      #print(t.black(ch[lum]), end='')
    print()

def clear():
  command = 'clear'
  if os.name in ('nt', 'dos'):
      command = 'cls'
  os.system(command)

def main():
  print(colorize(5,255,10))
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
