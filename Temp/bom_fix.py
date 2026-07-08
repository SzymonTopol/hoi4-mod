import os
from pathlib import Path

# --- CONFIGURATION ---
# Point this directly to your mod's history/states folder
MOD_STATES_DIR = r"C:\Users\Szymon & Kuba\Documents\Paradox Interactive\Hearts of Iron IV\mod\hoi4-mod\history\states"
# ---------------------

def strip_boms():
    folder = Path(MOD_STATES_DIR)
    fixed_count = 0
    
    for filepath in folder.glob("*.txt"):
        # Read the raw bytes of the file
        with open(filepath, 'rb') as f:
            raw_data = f.read()

        # Check for the UTF-8 BOM signature (EF BB BF)
        if raw_data.startswith(b'\xef\xbb\xbf'):
            # Slice off the first 3 bytes (the BOM)
            raw_data = raw_data[3:]
            
            # Overwrite the file with the clean bytes
            with open(filepath, 'wb') as f:
                f.write(raw_data)
            fixed_count += 1
            
    print(f"✅ Stripped invisible BOM characters from {fixed_count} files. The game can read them now!")

if __name__ == "__main__":
    strip_boms()