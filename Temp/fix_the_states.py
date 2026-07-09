import os
import re

def fix_hoi4_cores(directory_path):
    """
    Scans HOI4 state files, removes existing cores,
    and adds a core exclusively for the current owner.
    """
    # Regex to find "owner = TAG" and capture the 3-character TAG
    owner_regex = re.compile(r'^\s*owner\s*=\s*([A-Z0-9]{3})', re.IGNORECASE)
    # Regex to find any "add_core_of = TAG" line so we can delete them
    core_regex = re.compile(r'^\s*add_core_of\s*=\s*[A-Z0-9]{3}', re.IGNORECASE)

    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' not found.")
        return

    files_processed = 0

    for filename in os.listdir(directory_path):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(directory_path, filename)

        # Read all lines (HOI4 files often use UTF-8 BOM, occasionally cp1252)
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as file:
                lines = file.readlines()
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='cp1252') as file:
                lines = file.readlines()

        owner_tag = None
        
        # 1st Pass: Find the owner tag
        for line in lines:
            match = owner_regex.search(line)
            if match:
                owner_tag = match.group(1).upper()
                break

        if not owner_tag:
            print(f"Skipping {filename}: No owner tag found.")
            continue

        new_lines = []
        core_added = False

        # 2nd Pass: Rebuild the file content
        for line in lines:
            # Skip any existing add_core_of lines (this effectively removes them)
            if core_regex.search(line):
                continue

            # Add the current line to our new file content
            new_lines.append(line)

            # If this is the owner line, insert the new core right below it
            if owner_regex.search(line) and not core_added:
                # Grab the whitespace/indentation of the owner line to keep it pretty
                indent = line[:len(line) - len(line.lstrip())]
                new_lines.append(f"{indent}add_core_of = {owner_tag}\n")
                core_added = True

        # Write the updated lines back to the file
        try:
            with open(filepath, 'w', encoding='utf-8-sig') as file:
                file.writelines(new_lines)
            files_processed += 1
        except Exception as e:
            print(f"Failed to write {filename}: {e}")

    print(f"\nDone! Successfully updated cores in {files_processed} state files.")

# ==========================================
# SETUP AND EXECUTION
# ==========================================

# Replace the path below with the exact path to your mod's 'history/states' folder.
# Keep the 'r' before the quotes so Windows file paths don't break.
MOD_STATES_FOLDER = r"C:\Users\Szymon & Kuba\Documents\Paradox Interactive\Hearts of Iron IV\mod\hoi4-mod\history\states"

if __name__ == "__main__":
    # WARNING: Always backup your states folder before running automated scripts!
    fix_hoi4_cores(MOD_STATES_FOLDER)