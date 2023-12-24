import pygame
import random
import sys


pygame.init()

BLANC = (255, 255, 255)
NOIR = (0, 0, 255)

police = pygame.font.Font(None, 36)


def demander_rejouer():
    texte = police.render("Voulez-vous rejouer ? (O/N)", True, BLANC)
    fenetre.blit(texte, (largeur // 2 - texte.get_width() // 2, hauteur // 2))
    pygame.display.flip()

    attente = True
    while attente:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_o:
                    return True
                elif evenement.key == pygame.K_n:
                    return False

def choisir_mot():
    with open("mots.txt", "r") as fichier_mots:
        mots = fichier_mots.read().splitlines()
    return random.choice(mots).upper()

def afficher_mot_cache(mot, lettres_trouvees):
    mot_cache = ""
    for lettre in mot:
        if lettre in lettres_trouvees:
            mot_cache += lettre
        else:
            mot_cache += "_"
    return mot_cache


images_pendu = [
    pygame.image.load('capture1.png'),
    pygame.image.load('capture2.png'),
    pygame.image.load('capture3.png'),
    pygame.image.load('capture4.png'),
    pygame.image.load('capture5.png'),
    pygame.image.load('capture6.png'),
    pygame.image.load('capture7.png')
]

def dessiner_pendu(erreurs): 
    
    if 0 <= erreurs < len(images_pendu):
        image = images_pendu[erreurs]
        
        fenetre.blit(image, (60, 60))
    

def nouvelle_partie():
    global mot_a_deviner, lettres_jouees, erreurs, mot_cache
    mot_a_deviner = choisir_mot()
    lettres_jouees = set()
    erreurs = 0
    mot_cache = ['_'] * len(mot_a_deviner)

def afficher_menu():
    texte_titre = police.render("Jeu du Pendu", True, BLANC)
    fenetre.blit(texte_titre, (largeur // 2 - texte_titre.get_width() // 2, 50))

    texte_nouvelle_partie = police.render("Appuyez sur une touche pour commencer", True, BLANC)
    fenetre.blit(texte_nouvelle_partie, (largeur // 2 - texte_nouvelle_partie.get_width() // 2, hauteur // 2 - texte_nouvelle_partie.get_height() // 2))

    pygame.display.flip()

    attente_touche()

def attente_touche():
    attente = True
    while attente:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evenement.type == pygame.KEYDOWN:
                attente = False


largeur, hauteur = 1100, 800
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu Pendu")


while True:
    afficher_menu()

    nouvelle_partie()

   
    while True:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            

            if evenement.type == pygame.KEYDOWN:
                if evenement.key >= pygame.K_a and evenement.key <= pygame.K_z:
                    lettre = chr(evenement.key - pygame.K_a + ord('A'))
                    if lettre not in lettres_jouees:
                        lettres_jouees.add(lettre)
                        if lettre in mot_a_deviner:
                            for j in range(len(mot_a_deviner)):
                                if mot_a_deviner[j] == lettre:
                                    mot_cache[j] = lettre
                        else:
                            erreurs += 1
        
        
        texte_mot = police.render(" ".join(mot_cache), True, BLANC)
        fenetre.fill(NOIR)
        fenetre.blit(texte_mot, (largeur // 2 - texte_mot.get_width() // 2, 50))

       
        dessiner_pendu(erreurs)

        
        texte_lettres = police.render("Lettres jouées: " + " ".join(sorted(lettres_jouees)), True, BLANC)
        fenetre.blit(texte_lettres, (20, 500))

        pygame.display.flip()

        
        if '_' not in mot_cache:
            if demander_rejouer():
                break
            else:
                pygame.quit()
                sys.exit()

       
        if erreurs >= 7:
            if demander_rejouer():
                break
            else:
                pygame.quit()
                sys.exit()