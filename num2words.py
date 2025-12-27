import re
import os

# Natural Nepali numbers 0–99
upto_99 = {
    0:"शून्य",1:"एक",2:"दुई",3:"तीन",4:"चार",5:"पाँच",6:"छ",7:"सात",8:"आठ",9:"नौ",
    10:"दश",11:"एघार",12:"बाह्र",13:"तेह्र",14:"चौध",15:"पन्ध्र",16:"सोह्र",17:"सत्र",
    18:"अठार",19:"उन्नाइस",20:"बीस",21:"एक्काइस",22:"बाइस",23:"तेइस",24:"चौबिस",
    25:"पच्चिस",26:"छब्बिस",27:"सत्ताइस",28:"अठ्ठाइस",29:"उनन्तीस",30:"तीस",
    31:"एकतीस",32:"बत्तीस",33:"तेत्तीस",34:"चौतीस",35:"पैंतीस",36:"छत्तीस",
    37:"सैंतीस",38:"अठतीस",39:"उनन्चालीस",40:"चालिस",41:"एकचालीस",42:"बयालीस",
    43:"त्रियालीस",44:"चवालीस",45:"पैंतालीस",46:"छयालीस",47:"सच्चालीस",
    48:"अठचालीस",49:"उनन्चास",50:"पचास",51:"एकाउन्न",52:"बाउन्न",53:"त्रिपन्न",
    54:"चउन्न",55:"पचपन्न",56:"छप्पन्न",57:"सन्ताउन्न",58:"अन्ठाउन्न",59:"उनन्साठी",
    60:"साठी",61:"एकसट्ठी",62:"बैसट्ठी",63:"त्रिसट्ठी",64:"चौंसठी",65:"पैंसट्ठी",
    66:"छयासट्ठी",67:"सतसट्ठी",68:"अठसट्ठी",69:"उनन्सत्तरी",70:"सत्तरी",
    71:"एकहत्तर",72:"बहत्तर",73:"त्रिहत्तर",74:"चौहत्तर",75:"पचहत्तर",76:"छयहत्तर",
    77:"सतहत्तर",78:"अठहत्तर",79:"उनासी",80:"असी",81:"एकासी",82:"बयासी",
    83:"त्रियासी",84:"चौरासी",85:"पचासी",86:"छयासी",87:"सतासी",88:"अठासी",
    89:"उनान्नब्बे",90:"नब्बे",91:"एकान्नब्बे",92:"बयान्नब्बे",93:"त्रियान्नब्बे",
    94:"चौरान्नब्बे",95:"पचान्नब्बे",96:"छयान्नब्बे",97:"सन्तान्नब्बे",
    98:"अन्ठान्नब्बे",99:"उनान्सय"
}

hundred = "सय"
scales = [
    (10**12, "खर्ब"),
    (10**9,  "अर्ब"),
    (10**7,  "करोड"),
    (10**5,  "लाख"),
    (10**3,  "हजार"),
]

def nepali_num_to_int(s):
    trans = str.maketrans("०१२३४५६७८९", "0123456789")
    return int(s.translate(trans))

def num_under_thousand(n):
    if n < 100:
        return upto_99.get(n, str(n))
    h = n // 100
    r = n % 100
    text = upto_99[h] + " " + hundred
    if r:
        text += " " + num_under_thousand(r)
    return text

def convert_year_style(n):
    """Convert years like 1986 → उन्नाइस सय छयालिस"""
    if 1000 <= n <= 2999:  # typical year range
        hundreds = n // 100
        remainder = n % 100
        return upto_99[hundreds] + " " + hundred + " " + upto_99.get(remainder, str(remainder))
    return None

def num_to_words(n):
    year_style = convert_year_style(n)
    if year_style:
        return year_style

    if n < 1000:
        return num_under_thousand(n)

    parts = []
    for value, label in scales:
        if n >= value:
            q = n // value
            n %= value
            parts.append(num_to_words(q) + " " + label)
    if n:
        parts.append(num_under_thousand(n))
    return " ".join(parts)

def replace_numbers_in_line(line):
    """Detects different number forms: years, decimals, phone numbers"""
    def repl(m):
        num_str = m.group(0)
        try:
            clean_num = num_str.replace(",", "")
            n = nepali_num_to_int(clean_num)
            return num_to_words(n)
        except:
            return num_str
    return re.sub(r"[0-9०-९]+(?:,[0-9०-९]+)?", repl, line)

def convert_file(inp_path, out_path):
    with open(inp_path, encoding="utf-8") as f:
        lines = f.readlines()
    result = []
    for line in lines:
        if "-->" in line or re.fullmatch(r"\s*\d+\s*\n?", line):
            result.append(line)
        else:
            result.append(replace_numbers_in_line(line))
    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(result)

def convert_folder(folder_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith((".srt", ".vtt")):
                inp_path = os.path.join(root, filename)
                out_path = os.path.join(output_folder, filename)
                convert_file(inp_path, out_path)
                print(f"Converted: {filename}")

if __name__ == "__main__":
    folder = input("Enter folder path containing subtitle files: ")
    output_folder = input("Enter output folder path: ")
    convert_folder(folder, output_folder)
    print("All files processed!")