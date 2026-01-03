import sys, pygame, random

from pygame.locals import *

pygame.init()

ancho = 900
alto = 500

screen = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Lola")
    


cposx = 0
cposy = 280

velocidad = 7

ce_posx = 0
ce_posy = 0

vegetales = []
puntuacion = 0

'''Fuente'''

fuente1 = pygame.font.Font(None, 26)
fuente2 = pygame.font.Font(None, 36)

negro = (0, 0, 0)

cian = (126, 192, 238)

blanco = (255, 255, 255)


musica = pygame.mixer.Sound("sonido.mp3")
death = pygame.mixer.Sound("muerte.mp3")
yummy = pygame.mixer.Sound("cui.mp3")


adelante = True

xixf = {}

Ixixf = {}

cont = 0

i = 0

def imagen(filename, transparent=False):

        try: image = pygame.image.load(filename)

        except pygame.error :

            raise SystemExit()


        if transparent:
    
            color = image.get_at((0,0))
        
            image.set_colorkey(color, RLEACCEL)
        
        return image


def teclado():
    
    teclado = pygame.key.get_pressed()
    
    global cposx, cont, adelante
    
    if teclado[pygame.K_LEFT] and cposx > -50:
        cposx -= 7
        cont+=1
        adelante = False
    if teclado[pygame.K_RIGHT] and cposx < ancho - 150:
        cposx += 7
        cont+=1
        adelante = True
    return


def sprite():
    
    global cont, i


    xixf[0] = (0,0,150,150)

    xixf[1] = (150,0,150,150)
    
    xixf[2] = (150,0,150,150)
    
    xixf[3] = (300,0,150,150)  
    
    
    Ixixf[0] = (450, 0, 300, 150)
    
    Ixixf[1] = (300, 0, 150, 150)
    
    Ixixf[2] = (300, 0, 150, 150)
    
    Ixixf[3] = (150, 0, 150, 150)


    
    if cont < 4 :
    
        i = cont
    
    else :
    
        i = (cont %4)
    
    
    return
    



def cerdo_mov():
    
    global ce_posx, velocidad
    
    ce_posx += velocidad
    
    if ce_posx <= 0:
    
        velocidad = -velocidad
        
    elif ce_posx >= ancho - 150:
        velocidad = -velocidad
        

def mov_vegetales():
    global vegetales, ce_posx, ce_posy
    for elemento in vegetales:
        elemento[1] += 6
        if elemento[1] > alto:
            elemento[0] = ce_posx + random.randint(-10, 10)
            elemento[1] = ce_posy

            
zanahoria = imagen("imagenes/zanahoria.png", True)
tomate = imagen("imagenes/tomate.png", True)
lechuga = imagen("imagenes/lechuga.png", True)
brocoli = imagen("imagenes/brocoli.png", True)
bomba = imagen("imagenes/bomba.png", True)


zanahoria = pygame.transform.scale(zanahoria, (60, 60))
tomate = pygame.transform.scale(tomate, (60, 60))
brocoli = pygame.transform.scale(brocoli, (60, 60))
lechuga = pygame.transform.scale(lechuga, (45, 45))
bomba = pygame.transform.scale(bomba, (80, 80))


def gen_vegetales():
    global vegetales, ce_posx
    if random.randint(0, 200) < 5:
        tipo_elemento = random.choice([zanahoria, brocoli, lechuga, tomate, bomba])
        vegetales.append([ce_posx + random.randint(-30, 30), ce_posy, tipo_elemento])


def colision_elementos():
    global puntuacion, vegetales
    for elemento in vegetales:
        if (
            cposx < elemento[0] < cposx + 45
            and cposy < elemento[1] < cposy + 45
        ):
            yummy.play()
            
            if elemento[2] == bomba:
                return True  # Indica que perdio
            else:
                puntuacion += 10
                vegetales.remove(elemento)


def puntaje():
    
    for elemento in vegetales:
        screen.blit(elemento[2], (elemento[0], elemento[1]))
    text = fuente1.render("Puntuación: {}".format(puntuacion), True, negro)
    screen.blit(text, (10, 10))
    pygame.display.flip()
    
def final():

    global ce_posx, velocidad
    
    ce_posx += velocidad + 5
    
    if ce_posx <= 0 or ce_posx >= ancho - 150:
        velocidad = -velocidad
        
        

def fin_del_juego():
    

    
    game_overtext = fuente2.render("FIN DEL JUEGO", True, negro)
    screen.blit(game_overtext, (ancho // 2 -90, alto // 2 - 20))

pygame.display.flip()


clock = pygame.time.Clock()



def main():
    
    
    global elementos, puntuacion
    
    musica.play()
    
    screen = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Lola")
    
    
    
    fondo = imagen("imagenes/fondo2.png")
    
    cobayo = imagen("imagenes/cobayoss.png", True)
    
    cerdito = imagen ("imagenes/cerdo.png", True)
    
    
    fondo = pygame.transform.scale(fondo, (900, 500))

    cobayo = pygame.transform.scale(cobayo, (600, 150))
    
    cerdito = pygame.transform.scale(cerdito, (180, 180))
    
    cobayoinv = pygame.transform.flip(cobayo, True, False)
    


    pygame.display.flip()
    
    clock = pygame.time.Clock()

    running = True

    
    while running:

        
        teclado()
        sprite()
        
        cerdo_mov()
        mov_vegetales()
        gen_vegetales()
        
        
        screen.blit(fondo, (0, 0))
        

        screen.blit(cerdito, (ce_posx, ce_posy))
        
        if adelante :

            screen.blit(cobayo, (cposx, cposy),(xixf[i]))
        
        else :
    
            screen.blit(cobayoinv, (cposx, cposy),(Ixixf[i]))

        
    

        for elemento in vegetales:
            screen.blit(elemento[2], (elemento[0], elemento[1]))


        
        if colision_elementos():
            musica.stop()
            death.play()
            pygame.time.delay(3000)
            screen.fill(cian)
            fin_del_juego()
            pygame.time.delay(2000)  # Espera 2 segundos antes de salir
            running = False
        else:
            
            if puntuacion == 1000:
                final()
                
                
                screen.fill(negro)
                
                texto_g = fuente2.render("GANASTE", True, blanco)
                screen.blit(texto_g, (ancho // 2 -90, alto // 2 - 20))

        puntaje()
        
        clock.tick(30)
        
        
        pygame.display.flip()
        

        # Posibles entradas del teclado y mouse

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                sys.exit()



    return 0


if __name__ == '__main__':

    main()