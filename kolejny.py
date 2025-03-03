import numpy as np
import pandas as pd
import math
from collections import defaultdict

class UniqueSet(set):
    def add(self, obj):
        if obj not in self:
            super().add(obj)

def string_to_double(liczba):
    liczba = liczba.strip()

    if not liczba or liczba == "?":
        return 0.0  # Zwracamy domyślną wartość dla brakujących danych

    if 'more' in liczba:
        try:
            return float(liczba.split('more')[0].strip())
        except:
            return 0.0

    try:
        return float(liczba.replace(',', '.'))
    except ValueError:
        pass

    categorical_map = {
        'low': 1, 'med': 2, 'high': 3, 'vhigh': 4,
        'small': 5, 'big': 6, 'unacc': 7, 'acc': 8,
        'good': 9, 'vgood': 10
    }

    if liczba.lower() in categorical_map:
        return categorical_map[liczba.lower()]
    
    print(f"OSTRZEŻENIE: Nieznana wartość kategoryczna: '{liczba}'. Zwracam 0.0")
    return 0.0





def string_to_int(liczba):
    try:
        return int(liczba.strip())
    except ValueError:
        raise Exception("Nie udało się skonwertować liczby do int")

def string_to_tablica(sciezka_do_pliku):
    with open(sciezka_do_pliku, 'r') as f:
        tresc_pliku = f.read().strip()
    return [
        [cell.strip() for cell in line.split() if cell.strip()]
        for line in tresc_pliku.split('\n') if line.strip()
    ]

def find_min(data):
    return [min([string_to_double(row[i]) for row in data if row[i].strip() not in ('', '?')]) 
            for i in range(len(data[0]))]

def find_max(data):
    return [max([string_to_double(row[i]) for row in data if row[i].strip() not in ('', '?')]) 
            for i in range(len(data[0]))]

def avg(data):
    return [sum([string_to_double(row[i]) for row in data]) / len(data) for i in range(len(data[0]))]

def fill_missing_values(data):
    rows = len(data)
    cols = len(data[0])

    for j in range(cols):
        frequency = defaultdict(int)
        total_sum = 0
        count = 0

        for i in range(rows):
            if data[i][j] != "?":
                try:
                    num = string_to_double(data[i][j])
                    total_sum += num
                    count += 1
                except:
                    frequency[data[i][j]] += 1
        
        if count > 0:
            replacement = str(total_sum / count)
        else:
            replacement = max(frequency, key=frequency.get)

        for i in range(rows):
            if data[i][j] == "?":
                data[i][j] = replacement

def get_unique(data):
    result = UniqueSet()
    for row in data:
        for val in row:
            result.add(string_to_double(val))
    return result

def get_unique_for_column(data, column):
    result = UniqueSet()
    for row in data:
        result.add(string_to_double(row[column]))
    return result

def calculate_standard_deviation(data):
    numeric_data = list(map(string_to_double, data))
    mean = np.mean(numeric_data)
    variance = np.var(numeric_data)
    return math.sqrt(variance)

def normalize_into_intervals(data, a, b):
    size = len(data)
    column_size = len(data[0])
    min_values = find_min(data)
    max_values = find_max(data)

    for j in range(column_size):
        if min_values[j] == max_values[j]:
            continue
        for i in range(size):
            parsed_data = string_to_double(data[i][j])
            normalized_value = ((b - a) * (parsed_data - min_values[j])) / (max_values[j] - min_values[j]) + a
            data[i][j] = f"{normalized_value:.2f}"
    return data

def std_dev(data):
    size = len(data)
    column_size = len(data[0])
    return [calculate_standard_deviation([data[i][j] for i in range(size)]) for j in range(column_size)]

def normalize(data):
    size = len(data)
    column_size = len(data[0])
    averages = avg(data)
    std_devs = std_dev(data)

    for j in range(column_size):
        if std_devs[j] == 0:
            continue
        for i in range(size):
            parsed_data = string_to_double(data[i][j])
            normalized_value = (parsed_data - averages[j]) / std_devs[j]
            data[i][j] = f"{normalized_value:.2f}"
    return data

def calculate_variance(data):
    numeric_data = list(map(string_to_double, data))
    mean = np.mean(numeric_data)
    variance = np.var(numeric_data)
    return variance

def variance(data):
    size = len(data)
    column_size = len(data[0])
    return [calculate_variance([data[i][j] for i in range(size)]) for j in range(column_size)]

def main():
    nazwa_pliku_z_danymi = 'car.txt'
    nazwa_pliku_z_typami_atrybutow = 'car-type.txt'

    wczytane_dane = string_to_tablica(nazwa_pliku_z_danymi)
    atr_type = string_to_tablica(nazwa_pliku_z_typami_atrybutow)

    print("Dane systemu")
    for row in wczytane_dane:
        print(" ".join(row))

    print("\nDane pliku z typami")
    for row in atr_type:
        print(" ".join(row))

    decision_class_map = {
        7: 'unacc',  # "unacceptable"
        8: 'acc',    # "acceptable"
        9: 'good',   # "good"
        10: 'vgood'  # "very good"
    }

    decision_classes = get_unique_for_column(wczytane_dane, len(wczytane_dane[0]) - 1)  # Ostatnia kolumna to klasy decyzyjne
    print("\nDostępne klasy decyzyjne:")
    for class_value in decision_classes:
        # Wypisujemy nazwę klasy zamiast liczby
        print(decision_class_map.get(class_value, f"Nieznana klasa: {class_value}"))

    # Miejsce na rozwiązanie:
    print("Wielkości klas decyzyjnych")
    print(len(wczytane_dane))

    min_result = find_min(wczytane_dane)
    print("Minimalne:")
    for item in min_result:
        print(item)

    max_result = find_max(wczytane_dane)
    print("Maksymalne:")
    for item in max_result:
        print(item)

    # Lista unikalnych wartości
    uniq = get_unique(wczytane_dane)
    print("Unikalne")
    for item in uniq:
        print(item)

    # Poszczególne unikalne wartości
    for i in range(len(wczytane_dane[0])):
        unique_for_column = get_unique_for_column(wczytane_dane, i)
        for item in unique_for_column:
            print(item)
        print(f"Liczba wszystkich: {len(unique_for_column)}")
        print("--------------------------")

    # Odchylenie standardowe
    for i in range(len(wczytane_dane[0])):
        data = [wczytane_dane[j][i] for j in range(len(wczytane_dane))]
        standard_deviation = calculate_standard_deviation(data)
        print(standard_deviation)

    # Zadanie 4 i 5: Generowanie 10% więcej danych
    original_rows = len(wczytane_dane)
    cols = len(wczytane_dane[0])
    extra_rows = original_rows // 10
    new_rows = original_rows + extra_rows

    expanded_data = wczytane_dane + [['?'] * cols for _ in range(extra_rows)]
    fill_missing_values(expanded_data) 

    normalized_data = normalize_into_intervals(wczytane_dane, -1, 1)
    print("Dane znormalizowane na przedział <-1, 1>")
    for row in normalized_data:
        print(" ".join(row))

    normalized_data2 = normalize_into_intervals(wczytane_dane, 0, 1)
    print("Dane znormalizowane na przedział <0, 1>")
    for row in normalized_data2:
        print(" ".join(row))

    normalized_data3 = normalize_into_intervals(wczytane_dane, -10, 10)
    print("Dane znormalizowane na przedział <-10, 10>")
    for row in normalized_data3:
        print(" ".join(row))

    normalized_data4 = normalize(wczytane_dane)
    print("Dane znormalizowane")
    for row in normalized_data4:
        print(" ".join([f"{float(val):.2f}" for val in row]))

    average_values = avg(normalized_data4)
    print(" ".join(map(str, average_values)))

    variances = variance(normalized_data4)
    print(" ".join(map(str, variances)))

    #Wczytanie pliku CSV
    readable_data = []
    geography_values = UniqueSet()
    with open("Churn_Modelling.csv", 'r') as file:
        header_line = file.readline().strip()
        headers = header_line.split(',')

        for line in file:
            values = line.strip().split(',')
            row_dict = {headers[i]: values[i] if i < len(values) else "MISSING" for i in range(len(headers))}
            geography_values.add(values[headers.index("Geography")])
            readable_data.append(row_dict)

    # Tworzenie dummy attributes dla kolumny Geography
    for row in readable_data:
        for country in geography_values:
            row[country] = "1" if row["Geography"] == country else "0"
        del row["Geography"]
        del row[list(geography_values)[0]]  # Usunięcie jednego z dummy attributes

    for row in readable_data:
        for kvp in row.items():
            print(f"{kvp[0]}: {kvp[1]} ", end="")
        print()

if __name__ == "__main__":
    main()
