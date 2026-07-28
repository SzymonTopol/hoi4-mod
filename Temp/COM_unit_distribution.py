import json
import random

# --- CONFIGURATION ---
INPUT_FILE = "COM_oob_data.json"
OUTPUT_FILE = "COM_1936_OOB.txt"
TOTAL_DIVISIONS = 90

EQUIPMENT_SIGMA = 0.15 
EXPERIENCE_MEAN = 0.25 
EXPERIENCE_SIGMA = 0.10

TEMPLATES = [
    {"name": "Dywizja Piechoty", "chance": 0.60, "eq_mean": 0.50},
    {"name": "Oddział Kawalerii", "chance": 0.15, "eq_mean": 0.50},
    {"name": "Garnizon Lokalny", "chance": 0.15, "eq_mean": 0.30},
    {"name": "Piechota Wybraniecka", "chance": 0.10, "eq_mean": 0.82}
]

HOI4_TEMPLATES_BLOCK = """
division_template = {
\tname = "Dywizja Piechoty"
\tregiments = {
\t\tinfantry = { x = 0 y = 0 } infantry = { x = 0 y = 1 } infantry = { x = 0 y = 2 }
\t\tinfantry = { x = 1 y = 0 } infantry = { x = 1 y = 1 } infantry = { x = 1 y = 2 }
\t}
\tsupport = {
\t\tengineer = { x = 0 y = 0 }
\t}
}

division_template = {
\tname = "Oddział Kawalerii"
\tregiments = {
\t\tcavalry = { x = 0 y = 0 } cavalry = { x = 0 y = 1 } cavalry = { x = 0 y = 2 }
\t\tcavalry = { x = 1 y = 0 } cavalry = { x = 1 y = 1 } cavalry = { x = 1 y = 2 }
\t\tcavalry = { x = 2 y = 0 } cavalry = { x = 2 y = 1 } cavalry = { x = 2 y = 2 }
\t}
\tsupport = {
\t\trecon = { x = 0 y = 0 }
\t}
}

division_template = {
\tname = "Garnizon Lokalny"
\tregiments = {
\t\tinfantry = { x = 0 y = 0 } infantry = { x = 0 y = 1 } infantry = { x = 0 y = 2 }
\t}
}

division_template = {
\tname = "Piechota Wybraniecka"
\tregiments = {
\t\tinfantry = { x = 0 y = 0 } infantry = { x = 0 y = 1 } infantry = { x = 0 y = 2 }
\t\tinfantry = { x = 1 y = 0 }
\t\tcavalry = { x = 2 y = 0 } cavalry = { x = 2 y = 1 } cavalry = { x = 2 y = 2 }
\t\tartillery_brigade = { x = 3 y = 0 }
\t}
\tsupport = {
\t\tengineer = { x = 0 y = 0 }
\t}
}
"""

def generate_oob():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            state_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found. Run Step 1 first!")
        return

    # 1. Setup State Lottery
    state_list = list(state_data.keys())
    state_weights = []
    
    for state_id in state_list:
        data = state_data[state_id]
        prov_count = len(data.get("provinces", []))
        
        if prov_count == 0:
            state_weights.append(0)
            continue
            
        # Give a small bonus to states with high total VPs, but rely mostly on size
        vp_total = sum(data.get("victory_points", {}).values())
        
        # Base weight is number of provinces (e.g., 10 provinces = 100 weight)
        # VP adds a flat bonus so it doesn't exponentially dwarf rural states
        weight = (prov_count * 10) + vp_total
        state_weights.append(weight)

    template_names = [t["name"] for t in TEMPLATES]
    template_chances = [t["chance"] for t in TEMPLATES]
    template_counters = {name: 0 for name in template_names}

    oob_text = HOI4_TEMPLATES_BLOCK + "\nunits = {\n"

    for _ in range(TOTAL_DIVISIONS):
        # Pick Template
        chosen_name = random.choices(template_names, weights=template_chances, k=1)[0]
        template_data = next(t for t in TEMPLATES if t["name"] == chosen_name)
        template_counters[chosen_name] += 1
        unit_number = template_counters[chosen_name]

        # 2. Pick Location (Two-Step process)
        # First, pick a state
        chosen_state_id = random.choices(state_list, weights=state_weights, k=1)[0]
        chosen_state_data = state_data[chosen_state_id]
        
        state_provinces = chosen_state_data.get("provinces", [])
        state_vp_dict = chosen_state_data.get("victory_points", {})
        
        # Second, pick a province inside that state
        prov_weights = []
        for prov in state_provinces:
            vp_value = state_vp_dict.get(str(prov), 0)
            # Give local cities a high chance to be chosen, but limited strictly to this state
            prov_weights.append(10 + (vp_value * 5))
            
        chosen_location = random.choices(state_provinces, weights=prov_weights, k=1)[0]

        # Stats
        eq_factor = random.gauss(template_data["eq_mean"], EQUIPMENT_SIGMA)
        eq_factor = max(0.05, min(1.0, eq_factor))

        ex_factor = random.gauss(EXPERIENCE_MEAN, EXPERIENCE_SIGMA)
        ex_factor = max(0.0, min(1.0, ex_factor))

        # Formatting
        oob_text += "\tdivision = {\n"
        oob_text += f"\t\tname = \"{unit_number}. {chosen_name}\"\n"
        oob_text += f"\t\tlocation = {chosen_location}\n"
        oob_text += f"\t\tdivision_template = \"{chosen_name}\"\n"
        oob_text += f"\t\tstart_equipment_factor = {eq_factor:.3f}\n"
        oob_text += f"\t\tstart_experience_factor = {ex_factor:.3f}\n"
        oob_text += "\t}\n"

    oob_text += "}\n"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(oob_text)
    
    print(f"SUCCESS: Generated {TOTAL_DIVISIONS} divisions distributed geographically and saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_oob()