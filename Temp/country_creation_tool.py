import shutil
import os


#program przeznaczony do ułatwienia tworzenia krajów w hoi4
def main():
    print("Witaj w przyśpieszonym tworzeniu kajów")
    print("Przed przystąpieniem do pracy nad plikami, pamiętaj, aby uważać na potencjalne niespodziewane zachowania programu, sprawdzaj wyniki jego działania, opisuj uważnie commity")

    #uznajemy, że tag jest nowy, dopuki nie zacznę tworzyć faktycznego tworzenia krajów
    tag = input("Podaj TAG nowego kraju: ")
    tag = tag.upper()
    
    print(tag)


####   FLAGI   ####

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

2.Tag (sprawdzanie, czy istnieje)
2.5 Wybieranie co chcę zrobić (że wpisujesz numer i to robi)
3.gfx i graphical_culture
4.folder history (capital, ideologies)
5.Lokalizacja
6.Dodawanie prowincji
'''