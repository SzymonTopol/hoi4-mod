import shutil
import os

#program przeznaczony do ułatwienia tworzenia krajów w hoi4
def main():
    print("Witaj w przyśpieszonym tworzeniu kajów")
    print("Przed przystąpieniem do pracy nad plikami, pamiętaj, aby uważać na potencjalne niespodziewane zachowania programu, \nsprawdzaj wyniki jego działania, opisuj uważnie commity")

    is_new = True

    tag = "N"
    while tag == "N":
        tag, is_new = pick_tag()

    option = 999

    while option != 0: #menu główne do wyboru opcji
        print ("Tag na którym działasz to: " + tag)
        if is_new:
            print ("UWAGA, TAG NIE ISTNIEJE W GRZE")
            #1 - TWORZENIE kraju w liście tagów, tylko jeżeli is_new == False
        print ("Aby utworzyć nowy kraj wpisz 1")
        print ()
        print ("Aby dodać defaultowe flagi wpisz 2")
        print ()
        print ("Aby opuścić program wpisz 0")
        option = int(input())

        match option:
            case 1:
                if is_new:
                    create_country(tag)
                else:
                    print("Twój kraj już istnieje")
            case 2:
                flags(tag)        

def pick_tag():
    is_new = True
    sure = False
    good_tag = False

    while not sure:
        while not good_tag:
            tag = input("Podaj TAG wybieranego kraju: ")
            tag = tag.upper()

            if len(tag) != 3 or not tag.isalpha():
                print("Wprowadzony tag jest niepoprawny")
            else:
                good_tag = True

        tags_list = open("common/country_tags/00_countries.txt")

        for line in tags_list:
            if len(line) > 2 or len: #sprawdza kilka dodatkowych linijek, lecz nie wpływa znacząco na efektywność
                if tag == line[0:3]:
                    is_new = False
        
        tags_list.close()
        if is_new:
            print("UWAGA, TWÓJ TAG NIE ISTNIEJE W ZBIORZE TAGÓW")

        print("Czy jesteś pewny? t - tak")
        odp = input()
        if odp == "t":
            sure = True
        else:    
            good_tag = False
    
    print(tag)
    return tag, is_new

### TWORZENIE KRAJU ###

def create_country(tag):
    print ("FUNCTION UNDER CONSTRUCTION")

####   FLAGI   ####
def flags(tag):    
    ideologies = ["_neutrality.tga","_communism.tga","_democratic.tga","_fascism.tga"]
    sizes = ["","medium","small"]

    for i in ideologies:
        for s in sizes:
            destination = os.path.join("gfx","flags",s,tag+i)
            origin = os.path.join("Temp",s,"CCM"+i)
            print(origin)
            print(destination)

            shutil.copy(origin,destination)
    
main()


'''
TO DO

2.5 Wybieranie co chcę zrobić (że wpisujesz numer i to robi)
3.gfx i graphical_culture
4.folder history (capital, ideologies)
5.Lokalizacja
6.Dodawanie prowincji
7.Sprawdzanie, czy dostępne są pliki potrzebne do dalszego działania (jak ich nie ma to wyskakuje error)
8. Sprawdzenie czy wydane polecenie istnieje w rejestrze (aby nie wybombiło błędu na konwersji str na int)
'''