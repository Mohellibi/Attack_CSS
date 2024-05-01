Question 1) 
Le programme python qui represente le LFSR de 17 bits est la class LFSR_17 et la variable self.etat représente s1 un binaire de 17 bits.

La fonction test_LFSR_17() vérifie que l'état prend bien les 2^17 - 1 valeurs différentes pour une initialisation.
Pour la tester vous pouvez:
-taper print(test_LFSR_17())     Le teste doit renvoyer TRUE 
-ou décommenter le print deja écrit après cette meme fonction avec un #TEST devant

Question 2) 
Le programme python qui represente le LFSR de 25 bits est la class LFSR_25.

Question 3)
La fonction principale pour crypter un message a partir d'une clé est resultat_message_crypter(cle,message)
Pour la tester vous pouvez:
-print(resultat_message_crypter(0x0,0xffffffffff)) Le print doit renvoyer le message chiffré  
-décommenter le print avec un #TEST

La fonction de teste, try_decrypt(message,cle) crypte un message le décrypte et le compare au message initial 
pour verifier qu'il sont égaux.
Pour la tester vous pouvez:
-print(try_decrypt(0xfffffff, 0x0 ))  Le teste doit renvoyer TRUE 

-ou decommenter le print #TEST


Question 6)
La fonction crypt_CSS(cle, tours) renvoie une liste de z exemple crypt_CSS(0x0, 3) renvoie z1,z2,z3 pour s = 0x0,
Attack_css(liste_de_z) fait une attaque A partir d'une liste de z1,z2....z6
Pour tester l'attaque vous pouvez:
-taper:
liste_de_z = crypt_CSS(0xfffbbbcf, 6)
print(Attack_css(liste_de_z))               L'attaque doit renvoyer la clé initial à l'origine des z1,z2....z6

-ou decommenter les commentaire avec le #TEST