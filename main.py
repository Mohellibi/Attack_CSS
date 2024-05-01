# 1)

class LFSR_17:
    def __init__(self, vec):
        self.etat = vec & 0x1FFFF #initialisation avec un vecteur de 17 bits

    def shift(self):
        bit_de_sortie = self.etat & 1 #recupere le dernier bit du vecteur soit la position 0
        xor_bit = ((bit_de_sortie) ^ ((self.etat >> 14) & 1)) # XOR entre bit 14 et 0
        self.etat = ((self.etat >> 1) | (xor_bit << 16)) & 0x1FFFF #actualisation du vecteur apres un tour
        return bit_de_sortie


def test_LFSR_17():
    vec_inits = range(1, 2**17)  # range de toutes les valeurs possible non nulles

    # boucle pour verifier que l’état prend bien les 2^17 − 1 valeurs différentespour une initialisation quelconque non-nulle du registre
    for v in vec_inits: 
        lfsr = LFSR_17(v)
        if v != lfsr.etat:
            return False
    return True
        
#print(test_LFSR_17())          #TEST

# 2)

class LFSR_25:
    def __init__(self, vec):
        self.etat = vec & 0x1FFFFFF #initialisation avec un vecteur de 25 bits

    def shift(self):
        bit_de_sortie = self.etat & 1   #recupere le dernier bit du vecteur soit la position 0
        xor_bit = ((bit_de_sortie) ^ ((self.etat >> 3)& 1) ^ ((self.etat >> 4)& 1) ^ ((self.etat >> 12) & 1)) # XOR entre bit 12,3,4 et 0
        self.etat = ((self.etat >> 1) | (xor_bit << 24)) & 0x1FFFFFF #actualisation du vecteur apres un tour
        return bit_de_sortie


#3) 

# fonction pour inverser les bits ex: 10011 -> 11001
def inverse(binaire):
    inverse = 0
    while binaire:
        inverse = (inverse << 1) | (binaire & 1)
        binaire >>= 1
    return inverse

# Algo de CSS en python
def crypt_CSS(cle, tours):
    # Initialisation
    
    # Extraire les 16 premiers bits puis rajouter 1||s1
    s1 = (cle >> 24 ) + (1 << 16)
    # Extraire les 24 suivants puis rajouter 1||s2
    s2 = (cle & 0xFFFFFF) + (1 << 24)

    lfsr_17 = LFSR_17(s1)
    lfsr_25 = LFSR_25(s2)
    c = 0
    liste_des_Z = []

    # Exécuter les LFSRs et faire le (x + y + c) modulo 256
    for _ in range(tours):  # le nombre de bloc du lfsr sortie
        x = 0
        y = 0
        for _ in range(8):
            x = (x << 1) | lfsr_17.shift()
            y = (y << 1) | lfsr_25.shift()
        # Calculer z = x + y + c mod 256
        x = inverse(x)
        y = inverse(y)
        z = (x + y + c) % 256
        
        # Mettre à jour le carry bit
        if x + y > 255:
            c = 1
        else:
            c = 0

        # Ajouter z au résultat du lfsr
        liste_des_Z.append(z)
    return liste_des_Z


# fonction pour diviser le message pour XOR des blocs de 8 bits
def message_bloc(nombre):
    # Boucle pour diviser le nombre en blocs de 8 bits
    blocs_de_8_bits = []

    while nombre:
        octet = nombre & 0xFF
        blocs_de_8_bits.append(bin(octet))
        nombre >>= 8

    # Inverser l'ordre des blocs pour avoir le bon ordre de gauche à droite
    blocs_de_8_bits.reverse()
    return blocs_de_8_bits


# fonction pour XOR m(i) et z[i] pour crypter le message
def Xor_mi_zi(sortie_css:list,message):
    hex_crypte = 0
    crypte = []

    for indice,mes in enumerate(message):
        crypte.append(int(mes,2) ^ sortie_css[indice] )
    #converti le tableau en un hexadecimal
    for i in crypte:
        hex_crypte = hex_crypte << 8 | i
    return hex(hex_crypte)


# fonction principale utiliser pour crypter un message a partir d'une cle avec CSS
def resultat_message_crypter(cle,message):
    table_mess = message_bloc(message) #division du message en blocs
    tours = len(table_mess) 
    css_tableau = crypt_CSS(cle, tours) #faire un tableau des z de 8bits avec CSS
    message_crypter = Xor_mi_zi(css_tableau,table_mess)  #XOR des deux tableaux et conversion en hexadecimal
    return message_crypter


#print(resultat_message_crypter(0x0,0xffffffffff))     #TEST

# le resultat du 0xffffffffff est 0xffff6d36d7 avec s = 0x0 , nous n'obtenons pas c = 0xffffb66c39 mais 0xffffb6b5ab
# le decryptage sysmetrique ce passe correctement

def try_decrypt(message,cle):
    crypter = resultat_message_crypter(cle, message) #crypter le message avec la cle
    decrypter = resultat_message_crypter(cle, int(crypter,16)) #decrypter le message crypter avec la cle
    if decrypter == hex(message): #comparer le message de base avec le message crypter , decrypter
        return True
    else:
        return False
    
#print(try_decrypt(0xfffffff, 0x0 )) #TEST



# 6)

# calcul x3 a partir de x1 et x2 en O(8)

def calcul_de_x3(x1,x2):
    bin_x2_x1 = x2 << 8 | x1
    s1 = bin_x2_x1 + (1<<16)
    lfsr_x3 = LFSR_17(s1) # faire tourner s1 et recuperer x3
     
    for i in range(3):
        x3=0
        for _ in range(8):
            x3 = (x3 << 1) | ((lfsr_x3.etat ) & 1)
            lfsr_x3.shift()
        
    x3 = inverse(x3)

    return x3


# montrer dans le 4. et complexité en O(1)
def calcul_de_y1_a_3(x1,x2,x3,z1,z2,z3):
    y1 = (z1-x1) % 256
    if x1+y1>255:
        y2 = (z2-x2 -1) % 256
    else:
        y2 = (z2-x2) % 256

    if x2+y2>255:
        y3 = (z3-x3 -1) % 256
    else:
        y3 = (z3-x3) % 256
    return [y1,y2,y3]



def Attack_css(liste_de_z):
    #enumere les 2^16 possibilité de x1,x2
    for x2 in range(2**8):
        for x1 in range(2**8):

            x3 = calcul_de_x3(x1,x2)
            y1,y2,y3 = calcul_de_y1_a_3(x1,x2,x3,liste_de_z[0],liste_de_z[1],liste_de_z[2])
            x2_x1_y3_y2_y1 = (((x2 << 8 | x1)<< 8 | y3) << 8 | y2) << 8 | y1 #recomposer s avec s1 et s2

            if crypt_CSS(x2_x1_y3_y2_y1,6) == liste_de_z: #test si la cle renvoie bin les memes z1,z2...z6
                
                return hex(x2_x1_y3_y2_y1)
            
    print('erreur')

#liste_de_z = crypt_CSS(0xfffbbbcf, 6)    #TEST
#print(Attack_css(liste_de_z))            #TEST
