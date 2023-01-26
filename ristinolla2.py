import os
import sys
import this
import tkinter as tk

from turtle import clear, color
import numpy as np
from scipy.misc import derivative

nappilista = []
vuoro = False

root= tk.Tk()
voittox = 0
voittoy = 0
def alusta():
   global nappilista, voittox, voittoy
   nappilista = []
   clear_frame()

   root.title('RistiXNollaO') 
   canvas1 = tk.Canvas(root, width = 400, height = 300,  relief = 'raised')
   canvas1.pack()

   label2 = tk.Label(root, text='Syötä ruudukon koko')
   label2.config(font=('helvetica', 10))
   canvas1.create_window(200, 100, window=label2)

   entry1 = tk.Entry (root) 
   canvas1.create_window(200, 120, window=entry1)

   label3 = tk.Label(root, text='Syötä voittorivin koko')
   label3.config(font=('helvetica', 10))
   canvas1.create_window(200, 150, window=label3)

   entry2 = tk.Entry (root) 
   canvas1.create_window(200, 170, window=entry2)

   button2 = tk.Button(text='pelaa', command=luoLauta, bg='grey', fg='black', font=('helvetica', 20, 'bold'))
   canvas1.create_window(200, 250, window=button2,width=100, height=50)

   label5 = tk.Label(root, text=f'{voittox} - {voittoy}')
   label5.config(font=('helvetica', 50,"bold"))
   canvas1.create_window(200, 50, window=label5)
   
   label4 = tk.Label(root, text='X    -    O')
   label4.config(font=('helvetica', 0))
   canvas1.create_window(200, 10, window=label4)

def luoLauta():
   global n, voitto, nappilista, mat
   #voitto = (entry2.get())
   #n = int(entry1.get())

   voitto = 2
   n = 6
   mat = np.full((n,n),np.inf)
   clear_frame()

   global nappilista
   l = 0
   for i in range(n):
      for j in range(n):
         nappilista.append(tk.Button(root, text = ' ', bd = '1', bg='black',
               highlightbackground="#000000",
               highlightcolor="#36454F",
               height = 1, width = 2, font = ('Helvetica',int(500/n),'bold')
               ,command=lambda l=l: klik(nappilista[l])))
         nappilista[l].grid(row = i, column = j)
         l = l + 1

def klik(nappi):

   tila = nappi['text']
   global vuoro, n, mat
   i = int(np.floor(nappilista.index(nappi)/n))
   j = nappilista.index(nappi)%n
   if tila != " ":
      pass
   elif tila == " " and vuoro:
      nappi['text'] = 'X'
      vuoro = False
      mat[i][j] = 1
      tutkiVoitto(mat, vuoro, i, j)
   else:
      nappi['text'] = 'O'
      vuoro = True
      mat[i][j] = 0
      tutkiVoitto(mat, vuoro, i, j)

def tutkiVoitto(mat, vuoro,i,j):
   pystytilanne = pysty(1,i,j,mat)
   if (pystytilanne[0] == voitto):
      palat = [nappilista[x:x+n] for x in range(0, len(nappilista),n)]
      ylin = pystytilanne[1]
      for pala in palat[ylin:ylin+voitto]:
         pala[j].configure(bg="red", fg="red")
      napitalkuun(vuoro)

   sivutilanne=sivu(1,i,j,mat)
   if (sivutilanne[0] == voitto):
      palat = [nappilista[x:x+n] for x in range(0, len(nappilista),n)]
      pala = palat[i]
      vasen = sivutilanne[1]
      for nappi in pala[vasen:vasen+voitto]:
         nappi.configure(bg="red", fg="red")
      napitalkuun(vuoro)

   laskutilanne=lasku(1,i,j,mat)
   if (laskutilanne[0] == voitto):
      palat = [nappilista[x:x+n] for x in range(0, len(nappilista),n)]
      ij = laskutilanne[1]
      for naatti in ij:
         palat[naatti[0]][naatti[1]].configure(bg="red", fg="red")
      napitalkuun(vuoro)   

   nousutilanne=nousu(1,i,j,mat)
   if (nousutilanne[0] == voitto):
      palat = [nappilista[x:x+n] for x in range(0, len(nappilista),n)]
      ij = nousutilanne[1]
      for naatti in ij:
         palat[naatti[0]][naatti[1]].configure(bg="red", fg="red")
      napitalkuun(vuoro) 

def napitalkuun(vuoro):
   global voittox, voittoy
   if(vuoro == False):
      voittox = voittox+1
   else: voittoy = voittoy+1
   for nappi in nappilista:
      nappi.configure(command=lambda : alusta())

def pysty(summa, i,j, mat):
   # kelaus ylös
   while(True):
      if(i == 0):
         break
      if(mat[i][j]==mat[i-1][j]):
         i = i-1
      else:
         break
   # lasketaan palikat  
   ylin = i
   while(True):
      if(i == len(mat)-1):
         break
      if(mat[i][j]==mat[i+1][j]):
         i = i+1
         summa = summa + 1
      else:
         break
   return summa, ylin

def sivu(summa, i,j, mat):
   # kelaus vasen
   while(True):
      if(j == 0):
         break
      if(mat[i][j]==mat[i][j-1]):
         j = j-1
      else:
         break
   # lasketaan palikat  
   pal  = j
   while(True):
      if(j == len(mat)-1):
         break
      if(mat[i][j]==mat[i][j+1]):
         j = j+1
         summa = summa + 1
      else:
         break
   return summa, pal

def lasku(summa, i,j, mat):
   while(True):
      if(j == 0 or i == 0):
         break
      if(mat[i][j]==mat[i-1][j-1]):
         j = j-1
         i = i-1
      else:
         break
   # lasketaan palikat
   pal = [[i,j]]
   
   koko = len(mat)-1
   while(True):
      if(j == koko or i ==koko):
         break
      if(mat[i][j]==mat[i+1][j+1]):
         j = j+1
         i = i+1
         pal.append([i,j])
         summa = summa + 1
         
      else:
         break
   return summa, pal

   
def nousu(summa, i,j, mat):
   #alalaitaan
   koko = len(mat)-1

   while(True):
      if(j == 0 or i == koko):
         break
      if(mat[i][j]==mat[i+1][j-1]):
         j = j-1
         i = i+1
      else:
         break
   # lasketaan palikat  
   pal = [[i,j]]
   while(True):
      if(j == koko or i ==0):
         break
      if(mat[i][j]==mat[i-1][j+1]):
         j = j+1
         i = i-1
         summa = summa + 1
         pal.append([i,j])
      else:
         break
   return summa, pal

def clear_frame():
   for widgets in root.winfo_children():
      widgets.destroy()
    

alusta()
root.mainloop()