import random
import collections
import string


art = '''
    .-.
  _/oo \\
 ( \\v  /__
  \\/   ___)
  /     \\
 /       \\_
 \\_.-.__   ) 
        `-`'''
fehler1='''
  
     
     
     
     
  
========='''
fehler2='''
  ║
  ║    
  ║    
  ║   
  ║   
  ║
========='''
fehler3='''
  ╔═════
  ║    
  ║    
  ║   
  ║   
  ║
========='''
fehler4='''
  ╔════╗
  ║    ║
  ║    
  ║   
  ║   
  ║
========='''
fehler5='''
  ╔════╗
  ║    ║
  ║    🥵
  ║   
  ║   
  ║
========='''
fehler6='''
  ╔════╗
  ║    ║
  ║    😵
  ║    |
  ║   
  ║
========='''
fehler7='''
  ╔════╗
  ║    ║
  ║    😶
  ║   /|
  ║   
  ║
========='''
fehler8='''
  ╔════╗
  ║    ║
  ║    😪
  ║   /|\\
  ║   
  ║
========='''
fehler9='''
  ╔════╗
  ║    ║
  ║    😬
  ║   /|\\
  ║   / 
  ║
========='''

fehler10='''
  ╔════╗
  ║    ║
  ║    😑
  ║   /|\\
  ║   / \\
  ║
=========
YOU FAILED'''

def printFehler(anzahl): #Ausgabe des Fehlerzustands
    name = "fehler"
    name += str(anzahl)
    print(globals()[name]) #Globals() sucht nach globalen Variablen mit Name 
    
def printWord(word): #Prints Array 
    print("Wort: ")
    for i in range(len(word)):
        print(word[i], end = ' ') 
        
def fragenMehrmalsVorhanden(buchstabe, anzahlBuchstaben):
    while True:
        erg = input(f"Ist der Buchstabe {buchstabe} noch an einer anderen Stelle vorhanden? Wenn ja, dann gib die Stelle an: ")
        try:
            erg = int(erg) 
            if erg > 0 and erg <= anzahlBuchstaben:
                return erg-1 #BUG: Springt bei Eingabe groesser len() zurück an Start
        except:
            return -1
    
def fragenBuchstabe(buchstabe): #Verwendung durch compRaten()
    while True: #falls vertippt
        antwort = input(f"Ist der Buchstabe {buchstabe} enthalten? Antworte mit 'y' oder 'n': ")
        if antwort == "y":
            stelle = int(input("An welcher Stelle ist der Buchstabe enthalten? (Beginnt mit 1) ")) #Eingabe Stelle schon belegt?
            return stelle-1
        elif antwort == "n":
            return -1
        
def wortErratenPruefen(word):
    erg = True 
    for i in range(len(word)):
        if word[i] == "_":
            erg = False
    return erg

def searchLetterFrequency(words):
    letters = []
    for word in words:
        for char in word:
            letters.append(char)
    
    frequency = collections.Counter(letters)
    frequency = frequency.most_common()
    return frequency


def compRaten(anzahlBuchstaben):
    with open('Galgenmaenchen_Wordlist.txt', 'r') as data_file: 
        words = [line.rstrip('\n') for line in data_file]

    for i in range(len(words)-1, 0, -1): #Sortiert alle Woerter aus words aus, die nicht dieselbe Laenge haben
        if len(words[i]) != anzahlBuchstaben:
            del words[i]
    
    frequency = searchLetterFrequency(words)

    word = []
    for i in range(anzahlBuchstaben):
        word.append("_")
    printWord(word)
    
    print("Nagut, dann fange ich mal an zu raten...")
    fehler = 0
    index = 0
    testedLetters = [] #enthaelt schon geratene Buchstaben
        
    while fehler < 10:      
        if wortErratenPruefen(word) == False: 
            if frequency[index][0] not in testedLetters: #Prueft ob Buchstabe schonmal gefragt
                
                erg = fragenBuchstabe(frequency[index][0]) #Fragt ob Buchstabe enthalten
                testedLetters.append(frequency[index][0]) 
                
                if erg >= 0: #Buchstabe enthalten
                    word[erg] = frequency[index][0]
                    printWord(word)
                    while erg >= 0 and wortErratenPruefen(word) == False:
                        erg = fragenMehrmalsVorhanden(frequency[index][0], anzahlBuchstaben)
                        if erg >=0: #Ansonsten fuegt er Buchstabe bei Rueckgabe -1 an letzter Stelle im Wort ein
                            word[erg] = frequency[index][0]
                            printWord(word) 
                            
                    for i in range(len(words)-1, -1, -1): #Entfernt alle Woerter, die nicht die richtigen Buchstaben beinhalten
                        deleted = False #Abbruchbedingung, ansonsten 'index out of range'
                        for k in range(len(word)):
                            if deleted == False:
                                if word[k] != '_':
                                    if words[i][k] != word[k]:
                                        del words[i]
                                        deleted = True
                                        
                    frequency = searchLetterFrequency(words) #Wenn keine Woerter enthalten springt zurück an den Anfang?!
                    index = -1

                else: #Buchstabe nicht enthalten
                    fehler += 1
                    printFehler(fehler)
            
            index += 1 
       
        else:
            print("Yay, ich hab es erraten!")
            return 
        
    print("Oh schade...")   
    return
    
def spielerRaten():
    with open('Galgenmaenchen_Wordlist.txt', 'r') as data_file: 
        words = [line.rstrip('\n') for line in data_file]
    word = random.choice(words) 
    
    ausgabe = []
    for i in range(len(word)):
        ausgabe += "_"
    
    fehler = 0
    while fehler<10:
        printWord(ausgabe)
        versuch = input("Sag mir einen Buchstaben: ").upper() 
        
        if versuch in list(string.ascii_uppercase):
            enthalten = False
            for i in range(len(word)):
                if word[i] == versuch:
                    print("Der Buchstabe ist dabei! ")
                    ausgabe[i] = versuch
                    enthalten = True
                    
            if not enthalten:
                fehler += 1
                printFehler(fehler) 
                print(f"Der Buchstabe {versuch} ist leider nicht dabei. ")
            
            if wortErratenPruefen(ausgabe) == True:
                print("\nDu hast es geschafft!!!")
                print(art) 
                return 
        else:
            print("Nochmal?")  
                 
    print(f"Schade, das Wort waere '{word}' gewesen...")
    
def hangman():
    print("Es gibt zwei Modi:")
    print("1: Du ueberlegst dir ein Wort und sagst mir die Anzahl der Buchstaben, damit ich es erraten kann.")
    print("2: Ich ueberlege mir ein Wort und du darfst die Buchstaben raten.")
    
    while True: #falls vertippt
        modus = input("Schreibe '1' oder '2' je nachdem welchen Modus du waehlst: ")
        try:
            modus = int(modus)
            if modus == 1:
                anzahl = int(input("Okay, dann sag mir die Anzahl der Buchstaben von deinem Wort (Denke daran, dass ae, oe, und ue als zwei Buchstaben gewertet werden!): "))
                return compRaten(anzahl)
                
            elif modus == 2:
                print("\nNa dann auf gehts, ich hab ein Wort.")
                return spielerRaten()
            
        except:
            print("Wie bitte? Probiers nochmal! ")
            
        
   
hangman() #Aufruf des Programms




  
