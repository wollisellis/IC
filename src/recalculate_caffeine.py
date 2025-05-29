import pandas as pd
import re

# Caffeine reference table (mg per typical serving)
# Based on RelatórioFinal_Éllis.md and web search
CAFFEINE_REFERENCE = {
    # Coffees
    "Expresso (Café forte e concentrado, feito sob alta pressão)": {"serving_ml": 50, "caffeine_mg": 60},
    "Coado (Café filtrado através de um coador de papel ou pano)": {"serving_ml": 100, "caffeine_mg": 80},
    "Instantâneo (Café em pó que dissolve em água quente)": {"serving_ml": 100, "caffeine_mg": 60},
    "Cápsula (Café preparado usando máquinas que funcionam com cápsulas pré-preparadas)": {"serving_ml": 50, "caffeine_mg": 60},
    "Frappuccino (Bebida gelada à base de café, com chantilly)": {"serving_ml": 300, "caffeine_mg": 90},
    "Café Descafeinado": {"serving_ml": 100, "caffeine_mg": 3},
    "Outro café": {"serving_ml": 100, "caffeine_mg": 70}, # Generic coffee if type is "Outro"

    # Teas
    "Chá preto": {"serving_ml": 200, "caffeine_mg": 50},
    "Chá verde": {"serving_ml": 200, "caffeine_mg": 30},
    "Chá mate": {"serving_ml": 200, "caffeine_mg": 30},
    "Chá gelado (Ice tea)": {"serving_ml": 350, "caffeine_mg": 35},
    "Chá de ervas (ex: camomila, hortelã, boldo, capim-limão, hibisco, erva-doce)": {"serving_ml": 200, "caffeine_mg": 0},
    "Outro chá": {"serving_ml": 200, "caffeine_mg": 20},

    # Sodas
    "Refrigerante tipo Cola": {"serving_ml": 350, "caffeine_mg": 40},
    "Refrigerante tipo Guaraná": {"serving_ml": 350, "caffeine_mg": 15},

    # Energy Drinks
    "Bebida Energética": {"serving_ml": 250, "caffeine_mg": 80}, # Generic
    "Red Bull": {"serving_ml": 250, "caffeine_mg": 80},
    "Monster": {"serving_ml": 473, "caffeine_mg": 160},
    "Outro energético": {"serving_ml": 250, "caffeine_mg": 80},

    # Chocolates - caffeine per 30g for solid, per serving for others
    "Chocolate ao leite": {"serving_ml": None, "caffeine_mg_30g": 10},
    "Chocolate meio amargo": {"serving_ml": None, "caffeine_mg_30g": 20},
    "Chocolate amargo (mais de 70% cacau)": {"serving_ml": None, "caffeine_mg_30g": 25},
    "Chocolate branco": {"serving_ml": None, "caffeine_mg_30g": 0},
    "Achocolatado (pó + leite)": {"serving_ml": 200, "caffeine_mg": 8}, # This is per 200ml drink
    "Trufas ou bombons de chocolate": {"serving_ml": None, "caffeine_mg_30g": 15},
    "Outro chocolate": {"serving_ml": None, "caffeine_mg_30g": 10},

    # Others
    "Pílula de Cafeína": {"serving_ml": None, "caffeine_mg": 150},
    "Cápsulas de Cafeína": {"serving_ml": None, "caffeine_mg": 150}, # Alias
    "Pré-treinos": {"serving_ml": None, "caffeine_mg": 200}
}

# Frequency conversion to daily multiplier
# Needs to be comprehensive based on all unique frequency strings in the dataset
FREQUENCY_MAP = {
    # General Frequencies from "Quantos dias por semana..."
    "Não consumo": 0,
    "Não Consumo": 0, # Alias
    "Raramente (algumas vezes por mês)": (1/30) * 2.5, # "algumas" as 2-3 times
    "Raramente": (1/30) * 2.5, # Alias
    "1 vez por semana": 1/7,
    "1-2 vezes por semana": 1.5/7,
    "2-3 vezes por semana": 2.5/7,
    "3-4 vezes por semana": 3.5/7,
    "4-6 vezes por semana": 5/7,
    "5-6 vezes por semana": 5.5/7,
    "Todos os dias": 1,
    # Daily frequencies from "quantas vezes no dia..."
    "1 vez ao dia": 1,
    "2 vezes ao dia": 2,
    "3 vezes ao dia": 3,
    "4 vezes ao dia": 4,
    "5 vezes ou mais ao dia": 5, # Assuming "ou mais" as 5 for simplicity here
    "1": 1, # If numeric string
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
}

def parse_volume_from_string(volume_str: str, default_volume: float = 0) -> float:
    """Extracts volume in ml from strings like 'Xícara pequena: 50 ml'."""
    if pd.isna(volume_str):
        return default_volume
    volume_str = str(volume_str).lower()
    # Try to find patterns like "50 ml", "250ml", "1 litro", "2 litros"
    match = re.search(r'(\d[\d,\.]*)\s*(ml|litro|litros|l)', volume_str)
    if match:
        value = float(match.group(1).replace(',', '.'))
        unit = match.group(2)
        if unit in ["litro", "litros", "l"]:
            return value * 1000
        return value
    # Fallback for simple numbers if no unit, assume ml if contextually appropriate
    match_simple = re.search(r'(\d[\d,\.]+)$', volume_str)
    if match_simple:
         return float(match_simple.group(1).replace(',', '.'))
    return default_volume

def get_daily_multiplier(freq_per_week_str: str, times_per_day_str: str = "1 vez ao dia") -> float:
    """Converts frequency strings to an overall daily multiplier."""
    # Get weekly frequency
    weekly_freq_val = FREQUENCY_MAP.get(str(freq_per_week_str).strip(), 0)

    # Get daily frequency (number of times on a consumption day)
    # If times_per_day_str is numeric or can be mapped
    try:
        daily_times_val = float(str(times_per_day_str).strip())
    except ValueError:
        daily_times_val = FREQUENCY_MAP.get(str(times_per_day_str).strip(), 1) # Default to 1 if not found or not numeric

    return weekly_freq_val * daily_times_val

def parse_chocolate_portion(portion_str: str) -> float:
    """Estimates grams of chocolate from descriptive strings."""
    if pd.isna(portion_str):
        return 0 # Default to 0g if not specified
    portion_str = str(portion_str).lower()
    
    # Specific known portions
    if "quadradinhos" in portion_str or "quadrados" in portion_str:
        match = re.search(r'(\d+)', portion_str)
        if match:
            return int(match.group(1)) * 5 # Assuming 1 quadradinho = 5g
    if "barra pequena" in portion_str or "barrinha pequena" in portion_str:
        return 25 # Approx for small bar
    if "barra media" in portion_str or "1 barra" in portion_str and "pequena" not in portion_str and "grande" not in portion_str : # if just "1 barra"
         if "90g" in portion_str : return 90
         return 50 # Approx for medium bar (could be 90-100g too)
    if "barra grande" in portion_str:
        return 100
    if "tablete" in portion_str:
        return 100 # Often 90-100g
    if "unidade" in portion_str and "kinder bueno" in portion_str: # Kinder Bueno is ~21.5g per bar, often comes in 2-packs
        return 21.5 
    if "unidade" in portion_str and "trufa" in portion_str or "bombom" in portion_str:
        return 15 # Approx for one truffle/bonbon
    if re.search(r'(\d+)\s*g', portion_str): # "20g", "50g"
        return float(re.search(r'(\d+)\s*g', portion_str).group(1))
    if "colheres" in portion_str and "cacau em pó" in portion_str or "achocolatado" in portion_str : # for "Cacau em pó" or "Achocolatado"
        match = re.search(r'(\d+)', portion_str)
        if match: # assume 5g per colher, this isn't for solid chocolate caffeine, but for powdered drinks
            return int(match.group(1)) * 5 # This amount will be used for achocolatado or similar, not solid chocolate.
    if "bis" in portion_str: # "4 ao dia" for Bis
        match = re.search(r'(\d+)', portion_str)
        if match:
            return int(match.group(1)) * 6 # Bis unit is ~6g
    # Fallback if no clear pattern, this is risky.
    # It might be better to return 0 or a very conservative estimate.
    # For now, let's try to extract any number and assume it's grams if small.
    match_num = re.search(r'(\d+)', portion_str)
    if match_num:
        val = int(match_num.group(1))
        if val < 50: # If it's a small number, could be count of small items (like quadradinhos)
            return val * 5 # Wild guess: treat as count of 5g items
        return val # Or assume it's grams directly if larger
    return 30 # Default to 30g if unparseable as a last resort

def calculate_caffeine_for_item(consumed_volume_ml: float, standard_serving_ml: float, caffeine_per_standard_serving: float) -> float:
    """Calculates caffeine for an item based on consumed volume vs standard."""
    if standard_serving_ml > 0 and consumed_volume_ml > 0:
        return (caffeine_per_standard_serving / standard_serving_ml) * consumed_volume_ml
    elif consumed_volume_ml == 0 and standard_serving_ml is None : # Items like pills, or chocolate where serving is by unit/weight
        return caffeine_per_standard_serving
    elif consumed_volume_ml > 0 and standard_serving_ml is None: # Item defined by unit but volume provided (e.g. for pre-workout if user specified ml) - less common
        # This case needs careful thought. If pre-workout is 200mg/dose, and user says 100ml, how to interpret?
        # For now, assume the caffeine_mg is for the typical way it's taken, and volume is just extra info not used for calculation directly
        # unless the standard_serving_ml was also defined.
        return caffeine_per_standard_serving
    return 0

def calculate_caffeine(row: pd.Series) -> tuple[float, float]:
    total_daily_caffeine = 0.0

    # --- Coffee ---
    if str(row.get("Você consome café?")).strip().lower() == "sim":
        freq_cafe_per_week = str(row.get("Quantos dias por semana você consome café?"))
        times_cafe_per_day = str(row.get("Com base no recipiente que você selecionou anteriormente ( ___ \"), quantas vezes no dia você consome café nesse recipiente?"))
        daily_mult_cafe = get_daily_multiplier(freq_cafe_per_week, times_cafe_per_day)

        if daily_mult_cafe > 0:
            coffee_type_primary = str(row.get("Qual tipo de café você mais costuma consumir?")).strip()
            
            # Prioritize "Café - Quantidade (ml)" if it exists and is valid, otherwise parse from recipient
            volume_cafe_ml_direct = pd.to_numeric(row.get("Café - Quantidade (ml)"), errors='coerce')
            if pd.notna(volume_cafe_ml_direct) and volume_cafe_ml_direct > 0:
                 consumed_volume_ml_primary = volume_cafe_ml_direct
            else:
                recipient_primary = str(row.get("Em qual tipo de recipiente você costuma consumir seu café?"))
                consumed_volume_ml_primary = parse_volume_from_string(recipient_primary, default_volume=100) # Default 100ml if unparseable

            if coffee_type_primary in CAFFEINE_REFERENCE:
                details = CAFFEINE_REFERENCE[coffee_type_primary]
                caffeine_val = calculate_caffeine_for_item(consumed_volume_ml_primary, details["serving_ml"], details["caffeine_mg"])
                total_daily_caffeine += caffeine_val * daily_mult_cafe
            
            # Check for "Outro tipo de café"
            consumes_other_coffee_str = str(row.get("Além do tipo de café selecionado anteriormente, você costuma consumir outro tipo no mesmo dia ou tem a frequência de alternar ao longo dos dias?"))
            if consumes_other_coffee_str.strip().lower() not in ["não", "geralmente consumo o mesmo tipo de café", "nan"]: # Needs to be more robust
                other_coffee_type = str(row.get("Qual outro tipo de café você costuma consumir?")).strip()
                if other_coffee_type and other_coffee_type in CAFFEINE_REFERENCE:
                    # Assuming same frequency and volume for the "other" coffee type for simplicity
                    # This could be refined if there are separate frequency/volume questions for "other" coffee
                    details_other = CAFFEINE_REFERENCE[other_coffee_type]
                    # Assuming the "other" coffee is an additional consumption, not a replacement.
                    # And assuming it's consumed with the same daily multiplier and volume as primary. This is a simplification.
                    caffeine_val_other = calculate_caffeine_for_item(consumed_volume_ml_primary, details_other["serving_ml"], details_other["caffeine_mg"])
                    total_daily_caffeine += caffeine_val_other * daily_mult_cafe #This might double count if "alterno entre os dias"

    # --- Energy Drinks ---
    if str(row.get("Você consome energéticos?")).strip().lower() == "sim":
        freq_ener_per_week = str(row.get("Quantos dias por semana você consome energético?"))
        times_ener_per_day = str(row.get("No dia que você costuma consumir energético, quantas vezes você toma essa porção ___?"))
        daily_mult_ener = get_daily_multiplier(freq_ener_per_week, times_ener_per_day)

        if daily_mult_ener > 0:
            ener_type = str(row.get("Qual tipo de energético você mais costuma consumir?")).strip()
            ener_volume_str = str(row.get("Qual o tamanho da lata ou recipiente do ___ que você costuma consumir?"))
            
            consumed_volume_ml = parse_volume_from_string(ener_volume_str, default_volume=250)

            details = CAFFEINE_REFERENCE.get(ener_type, CAFFEINE_REFERENCE["Outro energético"]) # Fallback to generic
            
            # Adjust caffeine if volume differs from standard reference for that specific energy drink type
            # For Monster, reference is 473ml/160mg. For Red Bull/Generic, 250ml/80mg.
            std_vol = details["serving_ml"]
            std_caf = details["caffeine_mg"]
            
            caffeine_val = (std_caf / std_vol) * consumed_volume_ml if std_vol > 0 else std_caf # Proportional
            total_daily_caffeine += caffeine_val * daily_mult_ener

    # --- Tea ---
    if str(row.get("Você consome chá?")).strip().lower() == "sim":
        freq_tea_per_week = str(row.get("Quantos dias por semana você consome chá?"))
        times_tea_per_day = str(row.get("Com base no recipiente que você selecionou anteriormente ( ___ ), quantas vezes ao dia você consome chá nesse recipiente?"))
        daily_mult_tea = get_daily_multiplier(freq_tea_per_week, times_tea_per_day)

        if daily_mult_tea > 0:
            tea_type_primary = str(row.get("Qual tipo de chá você mais consome?")).strip()
            recipient_tea_primary = str(row.get("Em qual tipo de recipiente você costuma consumir seu chá?"))
            consumed_volume_ml_tea_primary = parse_volume_from_string(recipient_tea_primary, default_volume=200)

            if tea_type_primary in CAFFEINE_REFERENCE:
                details_tea = CAFFEINE_REFERENCE[tea_type_primary]
                if details_tea["caffeine_mg"] > 0: # Only add if it's a caffeinated tea
                    caffeine_val_tea = calculate_caffeine_for_item(consumed_volume_ml_tea_primary, details_tea["serving_ml"], details_tea["caffeine_mg"])
                    total_daily_caffeine += caffeine_val_tea * daily_mult_tea
            
            # Check for "Outro tipo de chá"
            consumes_other_tea_str = str(row.get("Além do seu chá principal ( ___ ), você consome outro tipo de chá?")).strip().lower()
            # This condition needs to check for affirmative responses like "sim", or if a type is listed in the "outro" column
            if consumes_other_tea_str not in ["não", "geralmente consumo o mesmo tipo de chá", "nan", ""] and pd.notna(row.get("Qual outro tipo de chá você costuma consumir?")):
                other_tea_types_str = str(row.get("Qual outro tipo de chá você costuma consumir?")).strip()
                # Handle multiple "other teas" if listed (e.g. "Chá verde, Chá gelado")
                other_tea_list = [t.strip() for t in re.split(r',|e ', other_tea_types_str)] # Split by comma or " e "
                for other_tea in other_tea_list:
                    if other_tea and other_tea in CAFFEINE_REFERENCE:
                        details_other_tea = CAFFEINE_REFERENCE[other_tea]
                        if details_other_tea["caffeine_mg"] > 0:
                             # Assuming same frequency and volume for the "other" tea type for simplicity
                            caffeine_val_other_tea = calculate_caffeine_for_item(consumed_volume_ml_tea_primary, details_other_tea["serving_ml"], details_other_tea["caffeine_mg"])
                            total_daily_caffeine += caffeine_val_other_tea * daily_mult_tea # Might overcount if "alterno"

    # --- Soda (Cola) ---
    if str(row.get("Você consome bebidas a base de cola? (Tipo Coca-Cola, Pepsi)")).strip().lower() == "sim":
        freq_cola_per_week = str(row.get("Quantos dias por semana você consome refrigerante a base de cola (Pepsi ou Coca-cola)?"))
        times_cola_per_day = str(row.get("Com base no tamanho da porção que você selecionou anteriormente ( ___ ), quantas vezes ao dia você consome essa porção de refrigerante?"))
        daily_mult_cola = get_daily_multiplier(freq_cola_per_week, times_cola_per_day)

        if daily_mult_cola > 0:
            cola_volume_str = str(row.get("Qual é o tamanho da porção que você costuma beber o seu refrigerante?"))
            consumed_volume_ml_cola = parse_volume_from_string(cola_volume_str, default_volume=350)
            
            details_cola = CAFFEINE_REFERENCE["Refrigerante tipo Cola"]
            caffeine_val_cola = calculate_caffeine_for_item(consumed_volume_ml_cola, details_cola["serving_ml"], details_cola["caffeine_mg"])
            total_daily_caffeine += caffeine_val_cola * daily_mult_cola
    
    # --- Supplements (Pills, Pre-workout) ---
    if str(row.get("Você consome algum suplemento que contenha cafeína?")).strip().lower() == "sim":
        freq_supp_per_week = str(row.get("Quantos dias na semana você consome suplemento com cafeína?"))
        # Assuming 1 time per day if not specified, as supplement dosage is usually once on consumption days
        daily_mult_supp = get_daily_multiplier(freq_supp_per_week, "1 vez ao dia") 

        if daily_mult_supp > 0:
            supp_type = str(row.get("Qual tipo de suplemento você mais consome?")).strip()
            supp_dose_str = str(row.get("Qual a dose que você toma de cafeína em suplemento por dia?")).lower()
            
            caffeine_from_dose = 0
            # Try to parse numeric dose like "400mg" or "200 mg"
            match_dose_mg = re.search(r'(\d+)\s*mg', supp_dose_str)
            if match_dose_mg:
                caffeine_from_dose = float(match_dose_mg.group(1))
            
            if caffeine_from_dose > 0:
                total_daily_caffeine += caffeine_from_dose * daily_mult_supp
            else: # Fallback to reference if specific mg not found or unparseable
                ref_key = None
                if "pré-treino" in supp_type.lower() or "pre-treinos" in supp_type.lower():
                    ref_key = "Pré-treinos"
                elif "cápsula" in supp_type.lower() or "pilula" in supp_type.lower(): # Check for "pilula" if "pílula" has accent issues
                    ref_key = "Pílula de Cafeína"
                
                if ref_key and ref_key in CAFFEINE_REFERENCE:
                    details_supp = CAFFEINE_REFERENCE[ref_key]
                    total_daily_caffeine += details_supp["caffeine_mg"] * daily_mult_supp

    # --- Chocolate ---
    if str(row.get("Você consome chocolate regularmente?")).strip().lower() == "sim":
        freq_choco_per_week = str(row.get("Quantas dias na semana você consome chocolate?"))
         # Chocolate frequency often implies "1 portion on consumption day" unless specified otherwise.
        daily_mult_choco = get_daily_multiplier(freq_choco_per_week, "1 vez ao dia")

        if daily_mult_choco > 0:
            choco_types_str = str(row.get("Que tipo(s) de chocolate você consome mais frequentemente?")).strip()
            choco_portion_str = str(row.get("Especifique a porção média de chocolate no dia que consome ( ___ )"))
            
            consumed_grams_choco = parse_chocolate_portion(choco_portion_str)

            if consumed_grams_choco > 0:
                # Handle multiple chocolate types if listed. For simplicity, take the first one or highest caffeine one.
                # A more complex approach would be to average or ask for proportions.
                # For now, let's try to find the highest caffeine chocolate mentioned.
                
                best_choco_type_key = "Outro chocolate" # Default
                max_caffeine_per_30g = 0

                chocolate_type_list = [ct.strip().lower() for ct in re.split(r',|e ', choco_types_str)]

                for choco_key_ref, choco_details_ref in CAFFEINE_REFERENCE.items():
                    if "caffeine_mg_30g" in choco_details_ref: # Ensure it's a chocolate entry
                        # Check if any part of the reference key is in the user's listed chocolate types
                        for user_choco_type in chocolate_type_list:
                            if user_choco_type and user_choco_type in choco_key_ref.lower(): # Simple substring match
                                if choco_details_ref["caffeine_mg_30g"] > max_caffeine_per_30g:
                                    max_caffeine_per_30g = choco_details_ref["caffeine_mg_30g"]
                                    best_choco_type_key = choco_key_ref
                                break # Found a match for this reference key

                final_choco_details = CAFFEINE_REFERENCE.get(best_choco_type_key, CAFFEINE_REFERENCE["Achocolatado (pó + leite)"]) # fallback
                
                # If the selected type is achocolatado, special handling (caffeine is per 200ml, not 30g)
                if best_choco_type_key == "Achocolatado (pó + leite)":
                    # This implies the "portion" was for a drink.
                    # parse_chocolate_portion might have returned e.g. 10g if "2 colheres" for powder.
                    # The caffeine for achocolatado is 8mg/200ml.
                    # This needs a rethink if "Que tipo(s)" can be "Achocolatado" AND "Especifique a porção" refers to the drink.
                    # For now, if it's Achocolatado, we use its standard definition.
                    # Let's assume if "Achocolatado" is chosen, the "portion_str" might be for the powder, not the final drink volume.
                    # Or it could be that "Que tipo(s)" means solid chocolate, and there's a separate question for achocolatado.
                    # Given "Achocolatado (pó + leite)" in CAFFEINE_REFERENCE has serving_ml, we should use that.
                    # The current logic of parse_chocolate_portion and then scaling by 30g is for SOLID chocolates.
                    # If it's achocolatado, we should use its direct caffeine value.
                    # This requires knowing if "Achocolatado" is a response in "Que tipo(s) de chocolate..."
                    # For now, if best_choco_type_key ends up being "Achocolatado (pó + leite)",
                    # we'll use its direct caffeine_mg value, assuming one serving (200ml)
                    if "Achocolatado" in best_choco_type_key:
                         total_daily_caffeine += final_choco_details["caffeine_mg"] * daily_mult_choco
                    elif "caffeine_mg_30g" in final_choco_details : # It's a solid chocolate
                        caffeine_per_gram = final_choco_details["caffeine_mg_30g"] / 30.0
                        total_daily_caffeine += caffeine_per_gram * consumed_grams_choco * daily_mult_choco

    # --- Chimarrão/Tereré --- (Already in script, seems okay - uses Chá Mate as proxy)
    if str(row.get("CHIMARRÃO / TERERÉ (Consumo)")).strip().lower() == "sim":
        freq_chimarrao = get_daily_multiplier(str(row.get("Frequência Chimarrão/Tereré")), "1 vez ao dia") # Assuming 1 preparation on consumption day
        if freq_chimarrao > 0:
            chimarrao_details = CAFFEINE_REFERENCE["Chá mate"] # Using Chá Mate as proxy
            total_daily_caffeine += chimarrao_details["caffeine_mg"] * freq_chimarrao

    total_weekly_caffeine = total_daily_caffeine * 7
    return total_daily_caffeine, total_weekly_caffeine

def main():
    # Load the dataframe
    try:
        df = pd.read_csv("IC_Dados_Curados - Worksheet (1).csv", encoding='utf-8')
    except FileNotFoundError:
        print("Error: The file 'IC_Dados_Curados - Worksheet (1).csv' was not found.")
        print("Please ensure the file is in the same directory as the script or provide the full path.")
        return
    except Exception as e:
        print(f"Error loading the CSV file: {e}")
        return

    # Clean column names (optional, but good practice if names have extra spaces)
    df.columns = df.columns.str.strip()

    # Apply the calculation to each row
    results = df.apply(calculate_caffeine, axis=1)

    df['MG_CAFEINA_TOTAL_DIA_RECALCULADA'] = [res[0] for res in results]
    df['MG_CAFEINA_TOTAL_SEMANA_RECALCULADA'] = [res[1] for res in results]

    try:
        df.to_csv("IC_Dados_Curados_Cafeina_Recalculada_v3.csv", index=False, encoding='utf-8-sig') # utf-8-sig for excel compatibility
        print("Successfully recalculated caffeine and saved to 'IC_Dados_Curados_Cafeina_Recalculada_v3.csv'")
    except Exception as e:
        print(f"Error saving the updated CSV file: {e}")

    print("\nSample of recalculated data vs original (first 15 rows):")
    print(df[['Mg cafeína dia', 'MG_CAFEINA_TOTAL_DIA_RECALCULADA', 'Mg cafeína semana', 'MG_CAFEINA_TOTAL_SEMANA_RECALCULADA']].head(15))
    
    # Check for rows where original and recalculated differ significantly (example)
    # df['DIFF_DIA'] = (df['MG_CAFEINA_TOTAL_DIA_RECALCULADA'] - pd.to_numeric(df['Mg cafeína dia'].str.replace(',', '.'), errors='coerce')).abs()
    # print("\nRows with significant difference in daily calculation (diff > 50mg):")
    # print(df[df['DIFF_DIA'] > 50][['ID','Mg cafeína dia', 'MG_CAFEINA_TOTAL_DIA_RECALCULADA', 'DIFF_DIA']])

if __name__ == "__main__":
    main() 