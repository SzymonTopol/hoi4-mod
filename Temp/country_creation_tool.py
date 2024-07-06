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

    neu = tag + "_neutrality.tga"

    com = tag + "_communism.tga"

    dem = tag + "_democratic.tga"

    fsc = tag + "_fascism.tga"

    path = os.path.join("gfx", "flags", neu)
    shutil.copy("Temp\CCM_neutrality.tga", path)
    path = os.path.join("gfx", "flags", "small", neu)
    shutil.copy("Temp\small\CCM_neutrality.tga", path)
    path = os.path.join("gfx", "flags", "medium", neu)
    shutil.copy("Temp\medium\CCM_neutrality.tga", path)

    path = os.path.join("gfx", "flags", com)
    shutil.copy("Temp\CCM_communism.tga", path)
    path = os.path.join("gfx", "flags", "small", com)
    shutil.copy("Temp\small\CCM_communism.tga", path)
    path = os.path.join("gfx", "flags", "medium", com)
    shutil.copy("Temp\medium\CCM_communism.tga", path)

    path = os.path.join("gfx", "flags", dem)
    shutil.copy("Temp\CCM_democratic.tga", path)
    path = os.path.join("gfx", "flags", "small", dem)
    shutil.copy("Temp\small\CCM_democratic.tga", path)
    path = os.path.join("gfx", "flags", "medium", dem)
    shutil.copy("Temp\medium\CCM_democratic.tga", path)

    path = os.path.join("gfx", "flags", fsc)
    shutil.copy("Temp\CCM_fascism.tga", path)
    path = os.path.join("gfx", "flags", "small", fsc)
    shutil.copy("Temp\small\CCM_fascism.tga", path)
    path = os.path.join("gfx", "flags", "medium", fsc)
    shutil.copy("Temp\medium\CCM_fascism.tga", path)


    print("Pomyślnie skopiowano pliki")

main()

'''
TO DO

2.Tag (sprawdzanie, czy istnieje)
3.gfx i graphical_culture
4.folder history (capital, ideologies)
5.Lokalizacja
6.Dodawanie prowincji
'''