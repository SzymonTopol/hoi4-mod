import os
import re
from pathlib import Path

# --- CONFIGURATION ---
VANILLA_DIR = r"G:\Steam\steamapps\common\Hearts of Iron IV\history\states"
MOD_DIR = r"C:\Users\Szymon & Kuba\Documents\Paradox Interactive\Hearts of Iron IV\mod\hoi4-mod\history\states"
OUTPUT_DIR = r"C:\Users\Szymon & Kuba\Documents\Paradox Interactive\Hearts of Iron IV\mod\hoi4-mod\history\states\fix"
# ---------------------

def read_state(file_path):
    with open(file_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
        content = f.read()
        
    id_match = re.search(r'\bid\s*=\s*(\d+)', content)
    state_id = int(id_match.group(1)) if id_match else None
    
    prov_match = re.search(r'provinces\s*=\s*\{([^}]+)\}', content, re.DOTALL)
    provinces = set()
    if prov_match:
        provinces = {int(p) for p in prov_match.group(1).split() if p.isdigit()}
        
    return state_id, provinces, content

def update_provinces(content, new_prov_set):
    # Formats the set of integers back into a space-separated string
    prov_string = " ".join(str(p) for p in sorted(new_prov_set))
    # Replaces the old provinces block with the new one
    new_content = re.sub(r'(provinces\s*=\s*\{)[^}]+(\})', rf'\1 {prov_string} \2', content, flags=re.DOTALL)
    return new_content

def set_unt_owner(content):
    # Changes owner and controller to UNT for new vanilla imports
    new_content = re.sub(r'\bowner\s*=\s*[A-Z0-9]{3}', 'owner = UNT', content)
    new_content = re.sub(r'\bcontroller\s*=\s*[A-Z0-9]{3}', 'controller = UNT', new_content)
    return new_content

def execute_migration():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    vanilla_path = Path(VANILLA_DIR)
    mod_path = Path(MOD_DIR)
    
    vanilla_data = {}
    mod_data = {}
    
    print("Loading Vanilla files...")
    for f in vanilla_path.glob("*.txt"):
        s_id, provs, txt = read_state(f)
        if s_id: vanilla_data[s_id] = {"name": f.name, "provs": provs, "txt": txt}
            
    print("Loading Mod files...")
    for f in mod_path.glob("*.txt"):
        s_id, provs, txt = read_state(f)
        if s_id: mod_data[s_id] = {"name": f.name, "provs": provs, "txt": txt}

    # 1. Identify Custom States & Claimed Provinces
    custom_ids = set(mod_data.keys()) - set(vanilla_data.keys())
    custom_claimed_provinces = set()
    
    for c_id in custom_ids:
        custom_claimed_provinces.update(mod_data[c_id]["provs"])
        
    print(f"Identified {len(custom_ids)} apex custom states claiming {len(custom_claimed_provinces)} provinces.")

    # 2. Process all Vanilla States (The Priority Logic)
    for v_id, v_info in vanilla_data.items():
        # What vanilla says this state should own, MINUS what custom states stole
        allowed_provs = v_info["provs"] - custom_claimed_provinces
        target_filename = v_info["name"]
        
        if v_id in mod_data:
            # State exists in mod. Use mod's custom text (keeps your UNT), but update provinces.
            # This also automatically fixes filenames by saving it under target_filename.
            final_content = update_provinces(mod_data[v_id]["txt"], allowed_provs)
        else:
            # 134 New Vanilla States! Import them, subtract custom provinces, and paint them UNT.
            final_content = update_provinces(v_info["txt"], allowed_provs)
            final_content = set_unt_owner(final_content)
            
        # Write to output folder
        with open(os.path.join(OUTPUT_DIR, target_filename), 'w', encoding='utf-8-sig') as f:
            f.write(final_content)

    # 3. Process Custom States
    for c_id in custom_ids:
        target_filename = mod_data[c_id]["name"]
        with open(os.path.join(OUTPUT_DIR, target_filename), 'w', encoding='utf-8-sig') as f:
            f.write(mod_data[c_id]["txt"])
            
    print("\n✅ Migration Complete! Check the MOD_OUTPUT_FIXED folder.")

if __name__ == "__main__":
    execute_migration()