import pygame
import random
import time
import sqlite3

connection = sqlite3.connect("base.db")
cursor = connection.cursor()

req = cursor.execute("SELECT * FROM tt_user")



print("bienvenue sur  STAR-SKIFF !")
print("commande ->  SPACE pour selectionné")
print("flèche gauche et droite pour dirigé l'avion !")
input("appuyer sur une ENTRER pour demarrer !")



pygame.init()

resolution = (1500,780)

blue_color = (89,152,255)
black_color = (0,0,0)
white_color = (255,255,255)

niv1color1 = (111, 208, 30)
niv1color2 = (69,208,28)
niv1color3 = (60,149,6)
niv1color4 = (120,167,13)
niv1color5 = (141,191,25)

niv2color1 = (148, 27, 197)
niv2color2 = (110,6,151)
niv2color3 = (150,9,164)
niv2color4 = (186,23,206)
niv2color5 = (159,50,214)





screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("STAR-SKIF")

clock = pygame.time.Clock()

surface = pygame.display.get_surface()
size = (surface.get_width, surface.get_height)

niveau_actuel = 0

pas = 0
pas_degrade = 0




niv1_avion = pygame.image.load("avion.png")
chemin_1 = pygame.image.load("asteroide_1.png")
chemin_1 = pygame.transform.scale(chemin_1, (250, 200))

chemin_2 = pygame.image.load("asteroide_2.png")
chemin_2 = pygame.transform.scale(chemin_2, (250,250))




aster_pas = 0
pygame.display.flip()
start = True




pygame.display.flip()





class asteroide:

    def __init__(self, chemin , asteroide_pos_x, asteroide_pos_y, asteroide_pas):
        self.chemin = chemin
        self.asteroide_pos_x = asteroide_pos_x
        self.asteroide_pos_y = asteroide_pos_y
        self.asteroide_pas = asteroide_pas
        self.bis_cote = 0
        self.chance_double = 5

    def obstacle(self, mem_nbs, vitesse_aster, chance_double, choix_resolution):
        if choix_resolution == 1:
            ligne_1 = 125
            ligne_2 = 620
            ligne_3 = 1125
        elif choix_resolution == 2:
            ligne_1 = 30
            ligne_2 = 430
            ligne_3 = 850

        nbs_random_bis = random.randint(1,chance_double)
        nbs_random = random.randint(1,3)
        while mem_nbs != nbs_random:

            mem_nbs = nbs_random

            if (nbs_random == 1):
                self.asteroide_pos_x = ligne_1
                self.asteroide_pos_y = -200
                self.asteroide_pas = vitesse_aster


            if (nbs_random == 2):
                self.asteroide_pos_x = ligne_2
                self.asteroide_pos_y = -200
                self.asteroide_pas = vitesse_aster


            if (nbs_random == 3):
                self.asteroide_pos_x = ligne_3
                self.asteroide_pos_y = -200
                self.asteroide_pas = vitesse_aster

            if (nbs_random_bis == 1):
                self.bis_cote = 1


def niveau_sup(niveau_actuel):
    sup = niveau_actuel[0] + 1
    id = niveau_actuel[2]
    rass = (sup, id)
    cursor.execute("UPDATE tt_user SET user_level = ? WHERE user_id = ?", rass)
    connection.commit()


def nouveau_joueur():
    nouveau_joueur_boucle = True
    joueur = None
    arial = pygame.font.SysFont("arial", 30, True)
    dem = []
    nbs = 0
    screen.fill(black_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            nouveau_joueur_boucle = False
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                nouveau_joueur_boucle = False



    text_info = arial.render("entré le nouveaux joueur sur la console !", True, blue_color)
    screen.blit(text_info, [500, 430])

    pygame.display.flip()

    joueur = input("nouveau joueur ->>")
    try:
        joueur = str(joueur)
        print(joueur)

        for raw in req.fetchall():
            dem.append(raw[1])

        nbs = int(len(dem))

        new_user = (nbs, f"{joueur}", 1)
        cursor.execute("INSERT INTO tt_user VALUES(?,?,?)", new_user)
        connection.commit()

        print("relancer le jeu !")

    except:
        print("erreur ! , entré juste des lettres en minuscule!")
        print("relancer le jeu !")







def charger_joueur(niveau_actuel, liste_joueur, liste_level, liste_id, choix_resolution):
    arial = pygame.font.SysFont("arial", 30, True)

    deplacement_fleche = 1
    entre = False
    charger_joueur_boucle = True
    tour_render = -1
    profil_actuel = None

    while charger_joueur_boucle:
        screen.fill(black_color)

        if choix_resolution == 2:
            ecart_mot = 430
            ecart_fleche = ecart_mot - 50
        elif choix_resolution == 1:
            ecart_mot = 720
            ecart_fleche = 650

        for raw in req.fetchall():
            liste_joueur.append(raw[1])
            liste_level.append(raw[2])
            liste_id.append(raw[0])


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                boucle_menu = False
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    entre = True
                elif event.key == pygame.K_UP:
                    deplacement_fleche = deplacement_fleche + 1
                elif event.key == pygame.K_DOWN:
                    deplacement_fleche = deplacement_fleche - 1


        if entre == True:
            entre = False
            if deplacement_fleche == 8:
                charger_joueur_boucle = False


            elif (deplacement_fleche == 7) and (nbs_liste >= 1):
                niveau_actuel = liste_level[0]
                profil_actuel = liste_joueur[0]
                id_actuel = liste_id[0]
                return niveau_actuel, profil_actuel, id_actuel

            elif deplacement_fleche == 6 and (nbs_liste >= 2):
                niveau_actuel = liste_level[1]
                profil_actuel = liste_joueur[1]
                id_actuel = liste_id[1]
                return niveau_actuel, profil_actuel, id_actuel

            elif deplacement_fleche == 5 and (nbs_liste >= 3):
                niveau_actuel = liste_level[2]
                profil_actuel = liste_joueur[2]
                id_actuel = liste_id[2]
                return niveau_actuel, profil_actuel, id_actuel

            elif deplacement_fleche == 4 and (nbs_liste >= 4):
                niveau_actuel = liste_level[3]
                profil_actuel = liste_joueur[3]
                id_actuel = liste_id[3]
                return niveau_actuel, profil_actuel, id_actuel

            elif deplacement_fleche == 3 and (nbs_liste >= 5):
                niveau_actuel = liste_level[4]
                profil_actuel = liste_joueur[4]
                id_actuel = liste_id[4]
                return niveau_actuel, profil_actuel, id_actuel

            elif deplacement_fleche == 2 and (nbs_liste >= 6):
                niveau_actuel = liste_level[0]
                profil_actuel = liste_joueur[0]
                id_actuel = liste_id[0]
                return niveau_actuel, profil_actuel, id_actuel

            elif deplacement_fleche == 1 and (nbs_liste >= 7):
                niveau_actuel = liste_level[5]
                profil_actuel = liste_joueur[5]
                id_actuel = liste_id[5]
                return niveau_actuel, profil_actuel, id_actuel

            elif deplacement_fleche == 0 and (nbs_liste >= 8):
                niveau_actuel = liste_level[6]
                profil_actuel = liste_joueur[6]
                id_actuel = liste_id[6]
                return niveau_actuel, profil_actuel, id_actuel



        if deplacement_fleche == 8:
            y_fleche = 270
        elif deplacement_fleche == 7:
            y_fleche = 310
        elif deplacement_fleche == 6:
            y_fleche = 350
        elif deplacement_fleche == 5:
            y_fleche = 390
        elif deplacement_fleche == 4:
            y_fleche = 430
        elif deplacement_fleche == 3:
            y_fleche = 470
        elif deplacement_fleche == 2:
            y_fleche = 510
        elif deplacement_fleche == 1:
            y_fleche = 550
        elif deplacement_fleche == 0:
            y_fleche = 590

        elif deplacement_fleche == -1:
            y_fleche = 590
            deplacement_fleche = 0
        elif deplacement_fleche == 9:
            y_fleche = 310
            deplacement_fleche = 8






        nbs_liste = int(len(liste_joueur))


        text_fleche = arial.render("-->", True, blue_color)
        screen.blit(text_fleche, [ecart_fleche, y_fleche])

        text_retour = arial.render("retour !", True, blue_color)
        screen.blit(text_retour, [ecart_mot, 270])

        for ii in range(310, 590, 40):
            tour_render += 1
            if tour_render < nbs_liste:
                text_repete = arial.render("{}".format(liste_joueur[tour_render]), True, blue_color)
                screen.blit(text_repete, [ecart_mot, ii])

        if tour_render == 6:
            tour_render = -1

        clock.tick(30)
        pygame.display.flip()












def menu_profil(niveau_actuel,  liste_joueur, liste_level, liste_id, choix_resolution):
    menu_profil_boucle = True
    y_fleche = 390
    entre = False
    deplacement_fleche = 1

    if choix_resolution == 2:
        ecart_mot = 430
        ecart_fleche = ecart_mot - 50
    elif choix_resolution == 1:
        ecart_mot = 720
        ecart_fleche = 650

    while menu_profil_boucle:
        screen.fill(black_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_profil_boucle = False
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    entre = True
                elif event.key == pygame.K_UP:
                    deplacement_fleche = deplacement_fleche + 1
                elif event.key == pygame.K_DOWN:
                    deplacement_fleche = deplacement_fleche - 1

        if entre == True:
            entre = False
            if deplacement_fleche == 0:
                nouveau_joueur()
            elif deplacement_fleche == 1:
                niveau_actuel = charger_joueur(niveau_actuel, liste_joueur, liste_level, liste_id, choix_resolution)
                print(niveau_actuel)
                return niveau_actuel
            elif deplacement_fleche == 2:
                menu_profil_boucle = False

        if deplacement_fleche == 2:
            y_fleche = 310
        elif deplacement_fleche == 1:
            y_fleche = 350
        elif deplacement_fleche == 0:
            y_fleche = 390
        elif deplacement_fleche == -1:
            y_fleche = 390
            deplacement_fleche = 0
        elif deplacement_fleche == 3:
            y_fleche = 310
            deplacement_fleche = 2


        arial = pygame.font.SysFont("arial", 30, True)

        text_fleche = arial.render("nouveaux joueur !", True, blue_color)
        screen.blit(text_fleche, [ecart_mot, 390])

        text_fleche = arial.render("chargé joueur !", True, blue_color)
        screen.blit(text_fleche, [ecart_mot, 350])

        text_fleche = arial.render("retour !", True, blue_color)
        screen.blit(text_fleche, [ecart_mot, 310])

        text_fleche = arial.render("-->", True, blue_color)
        screen.blit(text_fleche, [ecart_fleche,y_fleche])

        clock.tick(30)
        pygame.display.flip()



def changer_resolution(choix_resolution):
    if choix_resolution == 2:
        screen = pygame.display.set_mode((1100, 720))
    elif choix_resolution == 1:
        screen = pygame.display.set_mode((1500, 780))


def menu(niveau_actuel,  liste_joueur, liste_level, liste_id, choix_resolution):
    boucle_menu = True
    deplacement_fleche = 0
    y_fleche = 390
    entre = False

    ecart_mot = 720
    ecart_fleche = ecart_mot - 50


    while boucle_menu:

        if choix_resolution == 2:
            ecart_mot = 430
            ecart_fleche = ecart_mot - 50
        elif choix_resolution == 1:
            ecart_mot = 720
            ecart_fleche = 650


        screen.fill(black_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                boucle_menu = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    entre = True
                elif event.key == pygame.K_UP:
                    deplacement_fleche = deplacement_fleche + 1
                elif event.key == pygame.K_DOWN:
                    deplacement_fleche = deplacement_fleche - 1



        if entre == True:
            entre = False
            if deplacement_fleche == 0:
                try:
                    choix_niveau(niveau_actuel, choix_resolution)
                except:
                    print("profil non selectionné !")

            if deplacement_fleche == 1:
                niveau_actuel = menu_profil(niveau_actuel, liste_joueur, liste_level, liste_id, choix_resolution)

            if deplacement_fleche == 2:
                boucle_menu = False

            if deplacement_fleche == 3:
                if choix_resolution == 1:
                    choix_resolution = 2
                    changer_resolution(choix_resolution)
                else:
                    choix_resolution = 1
                    changer_resolution(choix_resolution)


        if deplacement_fleche == 4:
            deplacement_fleche = 3
            y_fleche = 270
        if deplacement_fleche == 3:
            y_fleche = 270
        elif deplacement_fleche == 2:
            y_fleche = 310
        elif deplacement_fleche == 1:
            y_fleche = 350
        elif deplacement_fleche == 0:
            y_fleche = 390
        elif deplacement_fleche == -1:
            y_fleche = 390
            deplacement_fleche = 0

        arial = pygame.font.SysFont("arial", 30, True)

        text_fleche = arial.render("-->", True, blue_color)
        screen.blit(text_fleche, [ecart_fleche,y_fleche])

        text_commencer = arial.render("commencer", True, blue_color)
        screen.blit(text_commencer, [ecart_mot, 390])

        text_profil = arial.render("profil", True, blue_color)
        screen.blit(text_profil, [ecart_mot, 350])

        text_profil = arial.render("quitter !", True, blue_color)
        screen.blit(text_profil, [ecart_mot, 310])

        text_profil = arial.render("changer la taille de l'affichage", True, blue_color)
        screen.blit(text_profil, [ecart_mot, 270])

        clock.tick(30)
        pygame.display.flip()




def choix_niveau(niveau_actuel, choix_resolution):
    if niveau_actuel[0] != 0:
        entre = False
        deplacement_fleche = 0
        boucle_choix_niveau = True
        niveau_joue = 1
        print(niveau_actuel)
        while boucle_choix_niveau:
            screen.fill(black_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    boucle_choix_niveau = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        entre = True
                    elif event.key == pygame.K_UP:
                        deplacement_fleche = deplacement_fleche - 1
                    elif event.key == pygame.K_DOWN:
                        deplacement_fleche = deplacement_fleche + 1

            if entre == True:
                entre = False

                if deplacement_fleche == 3:
                    if niveau_actuel[0] >= 3:
                        niveau_joue = 3
                        main(start, pas, pas_degrade, niveau_joue, choix_resolution)


                if deplacement_fleche == 2:
                    if niveau_actuel[0] >= 2:
                        niveau_joue = 2
                        main(start, pas, pas_degrade, niveau_joue, niveau_actuel, choix_resolution)

                if deplacement_fleche == 1:
                    if niveau_actuel[0] >= 1:
                        niveau_joue = 1
                        main(start, pas, pas_degrade, niveau_joue, niveau_actuel, choix_resolution)
                if deplacement_fleche == 0:
                    boucle_choix_niveau = False


            if deplacement_fleche == -1:
                y_fleche = 390
            elif deplacement_fleche == 0:
                y_fleche = 310
            elif deplacement_fleche == 1:
                y_fleche = 350
            elif deplacement_fleche == 2:
                y_fleche = 390
            elif deplacement_fleche == 3:
                y_fleche = 430
            elif deplacement_fleche == 4:
                y_fleche = 430

            arial = pygame.font.SysFont("arial", 30, True)

            text_fleche = arial.render("-->", True, blue_color)
            screen.blit(text_fleche, [650, y_fleche])

            text_retour = arial.render("retour !", True, blue_color)
            screen.blit(text_retour, [720, 310])


            text_commencer = arial.render("niveau 1", True, blue_color)
            screen.blit(text_commencer, [720, 350])

            text_profil = arial.render("niveau 2", True, blue_color)
            screen.blit(text_profil, [720, 390])

            text_profil_niveau_2 = arial.render("niveau 3", True, blue_color)
            screen.blit(text_profil_niveau_2, [720, 430])

            clock.tick(30)
            pygame.display.flip()











def main(start, pas, pas_degrade, niveau_joue, niveau_actuel, choix_resolution):


    if niveau_joue != 0:

        pygame.mixer.music.stop()
        couleur_fond = white_color
        choix_couleur = 0
        temps_1 = time.time() + 1.5
        temps_2 = time.time()
        tempo = time.time() + 0.3
        temps = -1
        mem_nbs = None
        bis_1_y = -200
        bis_1_pas = 0
        bis_1_x = 0
        asteroide_1 = asteroide(chemin_1, 200, -400, 0)
        asteroide_2 = asteroide(chemin_2, 200, -400, 0)
        barre_jeu = 0
        arial = pygame.font.SysFont("arial", 50, True)
        changer_couleur = 1
        temps_couleur = 1
        print(niveau_joue)


        vitesse_aster = 12
        vitesse_app_aster = 3

        if niveau_joue == 1:
            pygame.mixer.music.load("cloche.wav")
            bpm = 0.4761904761904761904
            bpm_barre = 2.613240418118467

        elif niveau_joue == 2:
            pygame.mixer.music.load("caprice.wav")
            bpm = 0.4535147392290249
            bpm_barre = 2.536231884057971

        elif niveau_joue == 3:
            print("vev")

        if choix_resolution == 1:
            detect_av = 620
            detect_ap = 420
            decalage = 690
            ligne_1 = 125
            ligne_2 = 620
            ligne_3 = 1125
            hauteur_avion = 600
            reso_degrade = 500
            acc_avion = 50
            espace_bar = 375
        else:
            detect_av = 600
            detect_ap = 400
            decalage = 490
            ligne_1 = 30
            ligne_2 = 430
            ligne_3 = 850
            hauteur_avion = 580
            reso_degrade = 400
            acc_avion = 50
            espace_bar = 200



        pygame.mixer.music.play(0)

        while start:
            screen.fill(couleur_fond)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start = False
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if not pas == (-reso_degrade):
                            pas = pas - reso_degrade
                            gauche = True
                    elif event.key == pygame.K_RIGHT:
                        if not pas == reso_degrade:
                            pas = pas + reso_degrade
                            gauche = False




            if (time.time() - temps_1) >= vitesse_app_aster:
                temps_1 = time.time()
                asteroide.obstacle(asteroide_1, mem_nbs, vitesse_aster, chance_double, choix_resolution)


            if (time.time() - temps_2) >= vitesse_app_aster:
                temps_2 = time.time()
                asteroide.obstacle(asteroide_2, mem_nbs, vitesse_aster, chance_double, choix_resolution)

            if (time.time() - tempo) >= 0:
                tempo = tempo + bpm
                temps += 1
                print(temps)
                barre_jeu = barre_jeu + bpm_barre



                if niveau_joue == 1:
                    if temps_couleur == temps:

                        temps_couleur = temps_couleur + changer_couleur
                        choix_couleur = choix_couleur + 1
                        if choix_couleur == 1:
                            couleur_fond = niv1color1
                        elif choix_couleur == 2:
                            couleur_fond = niv1color2
                        elif choix_couleur == 3:
                            couleur_fond = niv1color3
                        elif choix_couleur == 4:
                            couleur_fond = niv1color4
                        else:
                            couleur_fond = niv1color5
                            choix_couleur = 0

                    chance_double = 11

                    if temps == 48:
                        vitesse_aster = 15
                        vitesse_app_aster = 2
                        temps_1 = time.time() + 1
                        temps_2 = time.time()

                    elif temps == 84:
                        vitesse_aster = 18


                    elif temps == 144:
                        vitesse_aster = 17
                        vitesse_app_aster = 1.5
                        temps_1 = time.time() + 0.75
                        temps_2 = time.time()

                    elif temps == 204:
                        vitesse_app_aster = 1.25
                        vitesse_aster = 18
                        temps_1 = time.time() + 0.625
                        temps_2 = time.time()

                    elif temps == 272:
                        vitesse_aster = 19
                        vitesse_app_aster = 1
                        temps_1 = time.time() + 0.5
                        temps_2 = time.time()
                        changer_couleur = 2

                    elif temps == 288:
                        vitesse_aster = 0
                        niveau_sup(niveau_actuel)

                        start = False

                elif niveau_joue == 2:
                    if temps_couleur == temps:
                        temps_couleur = temps_couleur + changer_couleur
                        choix_couleur = choix_couleur + 1

                        if choix_couleur == 1:
                            couleur_fond = niv2color1
                        elif choix_couleur == 2:
                            couleur_fond = niv2color2
                        elif choix_couleur == 3:
                            couleur_fond = niv2color3
                        elif choix_couleur == 4:
                            couleur_fond = niv2color4
                        else:
                            couleur_fond = niv2color5
                            choix_couleur = 0



                    if temps == 2:
                        chance_double = 6
                        vitesse_aster = 14
                        vitesse_app_aster = 2.5
                        temps_1 = time.time() + 1.25
                        temps_2 = time.time()
                        changer_couleur = 2

                    elif temps == 16:
                        vitesse_aster = 16
                        vitesse_app_aster = 2
                        temps_1 = time.time() + 1
                        temps_2 = time.time()


                    elif temps == 66:
                        vitesse_aster = 17
                        vitesse_app_aster = 2
                        temps_1 = time.time() + 1
                        temps_2 = time.time()
                        changer_couleur = 1

                    elif temps == 92:
                        vitesse_app_aster = 3
                        vitesse_aster = 18
                        temps_1 = time.time() + 1.5
                        temps_2 = time.time()
                        changer_couleur = 2

                    elif temps == 122:
                        chance_double = 18
                        vitesse_aster = 20
                        vitesse_app_aster = 1.25
                        temps_1 = time.time() + 0.625
                        temps_2 = time.time()
                        changer_couleur = 1

                    elif temps == 184:
                        chance_double = 7
                        vitesse_aster = 21
                        vitesse_app_aster = 1
                        temps_1 = time.time() + 0.5
                        temps_2 = time.time()

                    elif temps == 214:
                        chance_double = 9
                        vitesse_aster = 19
                        vitesse_app_aster = 0.75
                        temps_1 = time.time() + 0.375
                        temps_2 = time.time()

                    elif temps == 248:
                        chance_double = 7
                        vitesse_aster = 15
                        vitesse_app_aster = 1.5
                        temps_1 = time.time() + 0.75
                        temps_2 = time.time()
                        changer_couleur = 2

                    elif temps == 276:
                        vitesse_aster = 1
                        niveau_sup(niveau_actuel)
                        start = False

                elif niveau_joue == 2:
                    if temps_couleur == temps:
                        temps_couleur = temps_couleur + changer_couleur
                        choix_couleur = choix_couleur + 1

                        if choix_couleur == 1:
                            couleur_fond = niv2color1
                        elif choix_couleur == 2:
                            couleur_fond = niv2color2
                        elif choix_couleur == 3:
                            couleur_fond = niv2color3
                        elif choix_couleur == 4:
                            couleur_fond = niv2color4
                        else:
                            couleur_fond = niv2color5
                            choix_couleur = 0



                    if temps == 2:
                        chance_double = 6
                        vitesse_aster = 14
                        vitesse_app_aster = 2.5
                        temps_1 = time.time() + 1.25
                        temps_2 = time.time()
                        changer_couleur = 2

                    elif temps == 16:
                        vitesse_aster = 16
                        vitesse_app_aster = 2
                        temps_1 = time.time() + 1
                        temps_2 = time.time()


                    elif temps == 66:
                        vitesse_aster = 17
                        vitesse_app_aster = 2
                        temps_1 = time.time() + 1
                        temps_2 = time.time()
                        changer_couleur = 1

                    elif temps == 92:
                        vitesse_app_aster = 3
                        vitesse_aster = 18
                        temps_1 = time.time() + 1.5
                        temps_2 = time.time()
                        changer_couleur = 2

                    elif temps == 122:
                        chance_double = 18
                        vitesse_aster = 20
                        vitesse_app_aster = 1.25
                        temps_1 = time.time() + 0.625
                        temps_2 = time.time()
                        changer_couleur = 1

                    elif temps == 184:
                        chance_double = 7
                        vitesse_aster = 21
                        vitesse_app_aster = 1
                        temps_1 = time.time() + 0.5
                        temps_2 = time.time()

                    elif temps == 214:
                        chance_double = 9
                        vitesse_aster = 19
                        vitesse_app_aster = 0.75
                        temps_1 = time.time() + 0.375
                        temps_2 = time.time()

                    elif temps == 248:
                        chance_double = 7
                        vitesse_aster = 15
                        vitesse_app_aster = 1.5
                        temps_1 = time.time() + 0.75
                        temps_2 = time.time()
                        changer_couleur = 2

                    elif temps == 276:
                        vitesse_aster = 1
                        niveau_sup(niveau_actuel)
                        start = False






            if pas == (- reso_degrade):
                if pas_degrade != (-reso_degrade):
                    pas_degrade = pas_degrade + (- acc_avion)

            if pas == 0:
                if pas_degrade != 0:
                    if gauche == True:
                        pas_degrade = pas_degrade - acc_avion
                    else:
                        pas_degrade = pas_degrade + acc_avion

            if pas == reso_degrade:
                if pas_degrade != reso_degrade:
                    pas_degrade = pas_degrade + acc_avion



            if asteroide_1.bis_cote == 1:
                if asteroide_1.asteroide_pos_x == ligne_1:
                    bis_1_x = ligne_3
                    bis_1_pas = vitesse_aster
                    bis_1_y = -200
                elif asteroide_1.asteroide_pos_x == ligne_2:
                    bis_1_x = ligne_1
                    bis_1_pas = vitesse_aster
                    bis_1_y = -200
                elif asteroide_1.asteroide_pos_x == ligne_3:
                    bis_1_x = ligne_2
                    bis_1_pas = vitesse_aster
                    bis_1_y = -200
                asteroide_1.bis_cote = 0


            if (decalage + pas_degrade) == (decalage - reso_degrade):
                if asteroide_1.asteroide_pos_x == ligne_1 and detect_av > asteroide_1.asteroide_pos_y >= detect_ap:
                    start = False
                    return True
                elif asteroide_2.asteroide_pos_x == ligne_1 and detect_av > asteroide_2.asteroide_pos_y >= detect_ap:
                    start = False
                    return True
                if bis_1_x == ligne_1 and detect_av > bis_1_y >= detect_ap:
                    start = False
                    return True

            if (decalage + pas_degrade) == decalage:
                if asteroide_1.asteroide_pos_x == ligne_2 and detect_av > asteroide_1.asteroide_pos_y >= detect_ap:
                    start = False
                    return True
                elif asteroide_2.asteroide_pos_x == ligne_2 and detect_av > asteroide_2.asteroide_pos_y >= detect_ap:
                    start = False
                    return True
                if bis_1_x == ligne_2 and detect_av > bis_1_y >= detect_ap:
                    start = False
                    return True

            if (decalage + pas_degrade) == (decalage + reso_degrade):
                if asteroide_1.asteroide_pos_x == ligne_3 and detect_av > asteroide_1.asteroide_pos_y >= detect_ap:
                    start = False
                elif asteroide_2.asteroide_pos_x == ligne_3 and detect_av > asteroide_2.asteroide_pos_y >= detect_ap:
                    start = False
                if bis_1_x == ligne_3 and detect_av > bis_1_y >= detect_ap:
                    start = False

            pas_1 = asteroide_1.asteroide_pas
            pas_2 = asteroide_2.asteroide_pas

            myrect_back = pygame.Rect(espace_bar, 1, 750, 20)
            pygame.draw.rect(screen, black_color, myrect_back, 1)


            my_rect = pygame.Rect(espace_bar, 1,barre_jeu, 20)
            pygame.draw.rect(screen, black_color, my_rect)


            asteroide_1.asteroide_pos_y = asteroide_1.asteroide_pos_y + pas_1
            screen.blit(asteroide_1.chemin, [asteroide_1.asteroide_pos_x, asteroide_1.asteroide_pos_y])
            asteroide_2.asteroide_pos_y = asteroide_2.asteroide_pos_y + pas_2
            screen.blit(asteroide_2.chemin, [asteroide_2.asteroide_pos_x, asteroide_2.asteroide_pos_y])

            bis_1_y = bis_1_y + bis_1_pas
            screen.blit(asteroide_1.chemin, [bis_1_x, bis_1_y])

            screen.blit(niv1_avion, [decalage + pas_degrade, hauteur_avion])



            clock.tick(60)
            pygame.display.flip()

        print("erreur !")


liste_joueur = []
liste_level = []
liste_id = []

choix_resolution = 1
menu(niveau_actuel, liste_joueur, liste_level, liste_id, choix_resolution)


