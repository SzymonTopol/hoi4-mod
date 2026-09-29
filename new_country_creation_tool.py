import shutil
import os
import csv
import glob
import re

# To upewnia się, że działasz w głównym folderze moda (pod warunkiem, że tam właśnie leży ten skrypt)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def setup_directories():
    folders = [
        "common/countries",
        "common/country_tags",
        "history/countries",
        "history/states",
        "common/names",
        "localisation/english",
        "gfx/flags/medium",
        "gfx/flags/small",
        "Temp/medium",
        "Temp/small"
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

def create_country_common(name, color, graphic_culture):
    filepath = os.path.join("common", "countries", f"{name}.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"color = {{ {color} }}\n")
        f.write(f"graphical_culture = {graphic_culture}\n")
        f.write(f"graphical_culture_2d = {graphic_culture}\n")

def register_tag(tag, name):
    filepath = os.path.join("common", "country_tags", "99_bulk_countries.txt")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            if f"{tag} = " in f.read():
                return
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f'{tag} = "countries/{name}.txt"\n')

def create_localization(tag, name):
    os.makedirs("localisation/english", exist_ok=True)
    filepath = os.path.join("localisation", "english", "99_bulk_countries_l_english.yml")
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8-sig") as f:
            f.write("l_english:\n")
            
    with open(filepath, "a", encoding="utf-8-sig") as f:
        for ideology in ["", "_fascism", "_democratic", "_communism", "_neutrality"]:
            f.write(f' {tag}{ideology}:0 "{name}"\n')
            f.write(f' {tag}{ideology}_DEF:0 "The {name}"\n')

def create_history(tag, name, ideology, home_state):
    filepath = os.path.join("history", "countries", f"{tag} - {name}.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"capital = {home_state}\n\n")
        f.write(f"set_popularities = {{\n\t{ideology} = 100\n}}\n")
        f.write(f"set_politics = {{\n\truling_party = {ideology}\n\tlast_election = \"1936.1.1\"\n\telection_frequency = 48\n\telections_allowed = no\n}}\n\n")
        f.write("set_research_slots = 3\n")
        f.write("set_technology = {\n\tinfantry_weapons = 1\n}\n")

def modify_states(tag, states_list):
    for state in states_list:
        state = state.strip()
        if not state: continue
        
        search_pattern = os.path.join("history", "states", f"{state}-*.txt")
        files = glob.glob(search_pattern)
        
        if not files:
            print(f"  [!] Brak pliku stanu {state}. Skopiuj plik bazowy do history/states/.")
            continue
            
        filepath = files[0]
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Zmienia właściciela na nowy tag
        content = re.sub(r'owner\s*=\s*[A-Z]{3}', f'owner = {tag}', content)
        
        # Dodaje core, jeżeli jeszcze go nie ma
        if f"add_core_of = {tag}" not in content:
            content = re.sub(r'(history\s*=\s*\{)', f'\\1\n\t\tadd_core_of = {tag}', content, count=1)
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

def extract_name_block(names_ref, tag):
    if not os.path.exists("name_templates.txt"):
        print("  [!] Brak pliku name_templates.txt. Pomijam generowanie imion.")
        return

    with open("name_templates.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    capturing = False
    bracket_count = 0
    block = []
    
    for line in lines:
        # Regex omijający problemy z ilością spacji np. "FRA={" lub "FRA =  {"
        if not capturing and re.match(rf"^{names_ref}\s*=\s*\{{", line.strip()):
            capturing = True
            line = re.sub(rf"^{names_ref}\s*=\s*\{{", f"{tag} = {{", line.strip()) + "\n"
            
        if capturing:
            block.append(line)
            bracket_count += line.count('{') - line.count('}')
            if bracket_count <= 0:
                break
                
    if block:
        filepath = os.path.join("common", "names", f"{tag}_names.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(block)
    else:
        print(f"  [!] Nie znaleziono bloku '{names_ref}' w name_templates.txt.")

def copy_dummy_flags(tag):
    ideologies = ["_neutrality.tga", "_communism.tga", "_democratic.tga", "_fascism.tga"]
    sizes = ["", "medium", "small"]
    for i in ideologies:
        for s in sizes:
            origin = os.path.join("Temp", s, f"CCM{i}")
            destination = os.path.join("gfx", "flags", s, f"{tag}{i}")
            if os.path.exists(origin):
                shutil.copy(origin, destination)

def main():
    print("Rozpoczynam masowe generowanie krajów...")
    setup_directories()

    csv_path = "countries.csv"
    if not os.path.exists(csv_path):
        print(f"BŁĄD: Nie znaleziono pliku {csv_path}")
        return

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            tag = row['Tag'].strip().upper()
            name = row['Name'].strip()
            ideology = row['Ideology'].strip()
            home_state = row['HomeState'].strip()
            color = row['Color'].strip()
            graphic_culture = row['GraphicCulture'].strip()
            names_ref = row['NamesRef'].strip()
            other_states = row['OtherStates'].strip()

            if len(tag) != 3 or not tag.isalpha():
                continue

            print(f"Generowanie plików dla: {tag} - {name}")
            
            all_states = [home_state]
            if other_states:
                all_states.extend([s.strip() for s in other_states.split(",") if s.strip()])
            
            create_country_common(name, color, graphic_culture)
            register_tag(tag, name)
            create_localization(tag, name)
            create_history(tag, name, ideology, home_state)
            modify_states(tag, all_states)
            extract_name_block(names_ref, tag)
            copy_dummy_flags(tag)
            
    print("\nGenerowanie zakończone.")

if __name__ == "__main__":
    main()