import os
import re
from pathlib import Path

# --- CONFIGURATION ---
# Replace these paths with your actual folder directories
VANILLA_DIR = r"G:\Steam\steamapps\common\Hearts of Iron IV\history\states"
MOD_DIR = r"C:\Users\Szymon & Kuba\Documents\Paradox Interactive\Hearts of Iron IV\mod\hoi4-mod\history\states"
# ---------------------

def extract_state_data(file_path):
    with open(file_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
        content = f.read()
    
    # Clean up comments to avoid parsing dead code
    content = re.sub(r'#.*', '', content)
    
    # Extract internal ID
    id_match = re.search(r'\bid\s*=\s*(\default|\d+)', content)
    state_id = id_match.group(1) if id_match else None
    
    # Extract owner
    owner_match = re.search(r'\bowner\s*=\s*([A-Z0-9]{3})', content)
    owner = owner_match.group(1) if owner_match else None
    
    # Extract provinces block
    # Matches 'provinces = { ... }' even across multiple lines
    prov_match = re.search(r'provinces\s*=\s*\{([^}]+)\}', content, re.DOTALL)
    provinces = []
    if prov_match:
        # Split by whitespace to get individual province IDs
        provinces = [int(p) for p in prov_match.group(1).split() if p.isdigit()]
        
    return {
        "id": state_id,
        "owner": owner,
        "provinces": sorted(provinces),
        "prov_count": len(provinces)
    }

def compare_states():
    vanilla_path = Path(VANILLA_DIR)
    mod_path = Path(MOD_DIR)
    
    if not vanilla_path.exists() or not mod_path.exists():
        print("Error: Check your VANILLA_DIR or MOD_DIR paths!")
        return

    vanilla_files = {f.name: f for f in vanilla_path.glob("*.txt")}
    mod_files = {f.name: f for f in mod_path.glob("*.txt")}
    
    print("--- HOI4 MAP DIFFERENCE REPORT ---")
    print(f"Vanilla States Tracked: {len(vanilla_files)}")
    print(f"Mod States Tracked: {len(mod_files)}\n")
    
    # 1. Check for entirely new files in Vanilla (DLC updates)
    new_in_vanilla = set(vanilla_files.keys()) - set(mod_files.keys())
    if new_in_vanilla:
        print(f"⚠️ [CRITICAL] {len(new_in_vanilla)} NEW baseline vanilla states found (Missing from your Mod folder):")
        for f in sorted(new_in_vanilla):
            print(f"   - {f}")
        print("-" * 50)

    # 2. Check for custom files only in your Mod
    only_in_mod = set(mod_files.keys()) - set(vanilla_files.keys())
    if only_in_mod:
        print(f"ℹ️ [INFO] {len(only_in_mod)} Custom states found exclusively in your mod:")
        for f in sorted(only_in_mod):
            print(f"   - {f}")
        print("-" * 50)

    # 3. Deep comparison of overlapping files
    overlapping_files = set(vanilla_files.keys()) & set(mod_files.keys())
    
    mismatched_provinces = []
    id_collisions = []
    
    for filename in sorted(overlapping_files):
        v_data = extract_state_data(vanilla_files[filename])
        m_data = extract_state_data(mod_files[filename])
        
        # Check internal ID mismatch
        if v_data["id"] != m_data["id"]:
            id_collisions.append((filename, v_data["id"], m_data["id"]))
            
        # Check province count or list differences
        if v_data["provinces"] != m_data["provinces"]:
            # If the only difference is ownership = UNT, we ignore it. 
            # But if provinces don't match, we report it.
            v_set = set(v_data["provinces"])
            m_set = set(m_data["provinces"])
            added_to_mod = m_set - v_set
            removed_from_mod = v_set - m_set
            
            mismatched_provinces.append({
                "file": filename,
                "v_count": v_data["prov_count"],
                "m_count": m_data["prov_count"],
                "added": added_to_mod,
                "removed": removed_from_mod
            })

    if id_collisions:
        print(f"⚠️ [CONFLICT] Internal ID Mismatches (Filename doesn't match internal text):")
        for file, v_id, m_id in id_collisions:
            print(f"   - {file}: Vanilla ID={v_id} vs Mod ID={m_id}")
        print("-" * 50)

    if mismatched_provinces:
        print(f"🚨 [CRITICAL] Province Discrepancies (Cannibalized or Changed map layouts):")
        for item in mismatched_provinces:
            print(f"   - {item['file']}: Vanilla has {item['v_count']} provs, Mod has {item['m_count']} provs.")
            if item['added']:
                print(f"     -> Provinces added to mod state: {list(item['added'])}")
            if item['removed']:
                print(f"     -> Provinces vanilla added here (missing from your mod): {list(item['removed'])}")
        print("-" * 50)
        
    if not new_in_vanilla and not id_collisions and not mismatched_provinces:
        print("✅ No critical structural differences found (excluding UNT owners). Your map layout matches vanilla perfectly!")

if __name__ == "__main__":
    compare_states()