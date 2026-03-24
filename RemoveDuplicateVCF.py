import re
import sys

prefix = "+39"

#Add the italian prefix to numbers without prefix. Change this if you want another prefix
def clean_phone_number(phone):
    phone = re.sub(r'\s+', '', phone)
    if re.match(r'^\d{10}$', phone):
        return prefix + phone
    return phone

def normalize_vcard(vcard_lines):
    phone_numbers = set()
    cleaned_vcard = ["VERSION:3.0"]
    
    for line in vcard_lines:
        line = line.strip()
        if not line: continue
        
        if line.startswith("TEL"):
            parts = line.split(':')
            if len(parts) > 1:
                raw_phone = re.sub(r'[^0-9+]', '', parts[-1])
                phone = clean_phone_number(raw_phone)
                if phone not in phone_numbers:
                    phone_numbers.add(phone)
                    cleaned_vcard.append(f"TEL;TYPE=CELL:{phone}")
        
        elif line.startswith(("FN:", "N:", "ORG:", "EMAIL:")):
            cleaned_vcard.append(line)
            
    return phone_numbers, cleaned_vcard

def remove_duplicate_vcards(input_file, output_file):
    unique_contacts = {}
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Errore: File {input_file} non trovato.")
        return

    # Dividiamo il file per ogni contatto
    raw_vcards = re.findall(r'BEGIN:VCARD.*?END:VCARD', content, re.DOTALL | re.IGNORECASE)
    
    for vcard_block in raw_vcards:
        lines = vcard_block.splitlines()
        phone_numbers, cleaned_vcard = normalize_vcard(lines)
        
        if phone_numbers:
            # Creiamo una chiave unica basata sui numeri (ordinati)
            key = tuple(sorted(list(phone_numbers)))
            if key not in unique_contacts:
                unique_contacts[key] = cleaned_vcard

    if not unique_contacts:
        print("Nessun vCard valido trovato! Controlla il formato del file di input.")
        return
    
    with open(output_file, "w", encoding="utf-8", newline='\r\n') as output_f:
        for vcard in unique_contacts.values():
            output_f.write("BEGIN:VCARD\n")
            output_f.write("\n".join(vcard) + "\n")
            output_f.write("END:VCARD\n")
    
    print(f"Elaborazione completata. Salvati {len(unique_contacts)} contatti unici in: {output_file}")

if __name__ == "__main__":
    # Controlliamo se l'utente ha passato i file
    if len(sys.argv) < 2:
        print("Usage: python RemoveDuplicateVCF.py input.vcf output.vcf")
        sys.exit(1)

    input_vcf = sys.argv[1]
    
    if len(sys.argv) > 2:
        output_vcf = sys.argv[2] + ".vcf"
    else:
        output_vcf = "cleaned_" + input_vcf

    remove_duplicate_vcards(input_vcf, output_vcf)