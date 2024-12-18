import os
import json
import csv
from bs4 import BeautifulSoup

def convert_to_utf8(input_file, output_file):
    with open(input_file, 'r', encoding='windows-1252') as f:
        content = f.read()
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

def convert_to_windows1252(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(output_file, 'w', encoding='windows-1252') as f:
        f.write(content)

def extract_table_data(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')

    data = []
    for row in rows[1:]:  # Skip header row
        cells = row.find_all('td')
        row_data = [cell.get_text(strip=True) for cell in cells]
        # Add the href from the anchor tag, if present
        if link := cells[0].find('a'):
            row_data[0] = link['href']
        # Add html_file name to the last column
        row_data += [os.path.basename(html_file).replace(".html", "")]
        data.append(row_data)

    return data

def save_to_csv(data, output_file):
    headers = ["Link", "Data", "Comarca", "Vara", "Juiz", "Réu", "Tipo"]
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

def main(input_folder, output_csv):
    all_data = []
    temp_folder = os.path.join(input_folder, 'converted')

    os.makedirs(temp_folder, exist_ok=True)

    # Convert and process each HTML file
    for file in os.listdir(input_folder):
        if file.endswith('.html'):
            input_file = os.path.join(input_folder, file)
            converted_file = os.path.join(temp_folder, file)
            
            # Convert to UTF-8
            convert_to_utf8(input_file, converted_file)

            # Extract table data
            all_data.extend(extract_table_data(converted_file))

    # Save consolidated data to CSV
    save_to_csv(all_data, output_csv)

# Example usage
input_folder = 'html_files'  # Folder containing HTML files
output_csv = 'processos.csv'  # Output CSV file
main(input_folder, output_csv)

# Leia o arquivo CSV
csv_file = "processos.csv"
json_file = "processos.json"

# Converta CSV para JSON
data = []
with open(csv_file, encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(row)

# Sort data by "Data"
data.sort(key=lambda x: x["Data"])

# Salve o arquivo JSON
with open(json_file, "w", encoding="utf-8") as jsonfile:
    json.dump(data, jsonfile, ensure_ascii=False, indent=2)

print(f"Arquivo {json_file} gerado com sucesso!")
