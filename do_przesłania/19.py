import numpy as np
import pandas as pd
import math
from collections import defaultdict

#UniqueSet dziedziczy po wbudowanej klasie set, co oznacza, że przejmuje jej całą funkcjonalność.
#Nadpisujemy metodę add(), aby dodać dodatkową kontrolę:
#Sprawdzamy, czy obj już istnieje w zbiorze (self).
#Jeśli obiekt nie istnieje, dodajemy go przy użyciu metody add() z klasy set (super().add(obj)).
class UniqueSet(set):
    def add(self, obj):
        if obj not in self:
            super().add(obj)

#liczba.strip() usuwa białe znaki (spacje, tabulatory, nowe linie) z początku i końca ciągu znaków.
#eśli liczba to pusty ciąg ("") lub znak ?, zwracamy 0.0, co oznacza brak wartości liczbowej.
#Jeśli w ciągu znajduje się "more", próbujemy pobrać liczbę przed tym fragmentem, np. "50more" → 50.0.
#Zamieniamy , na . w przypadku europejskiego zapisu liczb ("3,14" → "3.14").
#Przypisujemy wartości liczbowe dla różnych kategorii (low, med, high, itp.).
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


#Usuwa białe znaki z liczba.strip(), a następnie konwertuje ją na liczbę całkowitą (int).
def string_to_int(liczba):
    try:
        return int(liczba.strip())
    except ValueError:
        raise Exception("Nie udało się skonwertować liczby do int")


#Usuwa zbędne białe znaki z końca i początku (strip())
#Przetwarza każdą linię (split('\n')) i usuwa puste linie (if line.strip()).
#Każda linia jest rozdzielana na komórki (split() → domyślnie dzieli po białych znakach).
#Każda komórka jest dodatkowo czyszczona (cell.strip()), a puste pomijane (if cell.strip()).
def string_to_tablica(sciezka_do_pliku):
    with open(sciezka_do_pliku, 'r') as f:
        tresc_pliku = f.read().strip()
    return [
        [cell.strip() for cell in line.split() if cell.strip()]
        for line in tresc_pliku.split('\n') if line.strip()
    ]


#Konwertuje wartości na liczby zmiennoprzecinkowe (string_to_double).
#Znajduje minimalną wartość (min()).
def find_min(data):
    return [min([string_to_double(row[i]) for row in data if row[i].strip() not in ('', '?')]) 
            for i in range(len(data[0]))]


#Analogiczna do find_min, ale zamiast min() używa max().
def find_max(data):
    return [max([string_to_double(row[i]) for row in data if row[i].strip() not in ('', '?')]) 
            for i in range(len(data[0]))]


#Sumuje wartości (sum()).
#Dzieli przez liczbę elementów (len(data)), obliczając średnią.
def avg(data):
    return [sum([string_to_double(row[i]) for row in data]) / len(data) for i in range(len(data[0]))]


# Iteruje przez kolumny, zbiera dane numeryczne i symboliczne, licząc sumę, ilość lub częstotliwość występowania.
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
        # Zastępuje brakujące wartości "?" średnią (dla liczb) lub najczęściej występującą wartością (dla tekstu).
        if count > 0:
            replacement = str(total_sum / count)
        else:
            replacement = max(frequency, key=frequency.get)

        for i in range(rows):
            if data[i][j] == "?":
                data[i][j] = replacement


# Przechodzi przez każdy wiersz i każdą wartość, konwertując je na liczby.
# Dodaje przekonwertowane wartości do obiektu UniqueSet, tworząc zbiór unikalnych elementów.
def get_unique(data):
    result = UniqueSet()
    for row in data:
        for val in row:
            result.add(string_to_double(val))
    return result

# Przegląda wybraną kolumnę, konwertując każdą wartość na typ numeryczny.
# Dodaje te wartości do UniqueSet, zwracając zbiór unikalnych wartości danej kolumny.
def get_unique_for_column(data, column):
    result = UniqueSet()
    for row in data:
        result.add(string_to_double(row[column]))
    return result

# Konwertuje listę wartości (w formie string) na liczby i oblicza ich średnią.
# Wyznacza wariancję za pomocą numpy, a następnie zwraca pierwiastek z wariancji jako odchylenie standardowe.
def calculate_standard_deviation(data):
    numeric_data = list(map(string_to_double, data))
    mean = np.mean(numeric_data)
    variance = np.var(numeric_data)
    return math.sqrt(variance)

# Oblicza minimalne i maksymalne wartości dla każdej kolumny macierzy danych.
# Przekształca każdą wartość do przedziału [a, b] według wzoru normalizacyjnego, formatując wynik do dwóch miejsc po przecinku.
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

# Iteruje przez kolumny macierzy, zbierając wartości każdej z nich.
# Dla każdej kolumny wywołuje calculate_standard_deviation i zwraca listę obliczonych odchyleń standardowych.
def std_dev(data):
    size = len(data)
    column_size = len(data[0])
    return [calculate_standard_deviation([data[i][j] for i in range(size)]) for j in range(column_size)]

# Oblicza średnie i odchylenia standardowe dla każdej kolumny przy użyciu funkcji avg i std_dev.
# Normalizuje każdą wartość metodą standaryzacji (z-score), o ile odchylenie nie wynosi zero.
# Aktualizuje dane, formatując wynik do dwóch miejsc po przecinku i zwraca znormalizowaną macierz.
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

# Konwertuje listę wartości (string) na numeryczne i oblicza ich średnią.
# Wylicza wariancję przy użyciu funkcji numpy, co mierzy rozproszenie danych.
# Zwraca obliczoną wartość wariancji dla podanego zbioru danych.
def calculate_variance(data):
    numeric_data = list(map(string_to_double, data))
    mean = np.mean(numeric_data)
    variance = np.var(numeric_data)
    return variance

# Iteruje przez każdą kolumnę macierzy, zbierając wartości do osobnych list.
# Dla każdej kolumny wywołuje calculate_variance, aby obliczyć jej wariancję.
# Zwraca listę wariancji odpowiadającą poszczególnym kolumnom danych.
def variance(data):
    size = len(data)
    column_size = len(data[0])
    return [calculate_variance([data[i][j] for i in range(size)]) for j in range(column_size)]

def main():
    # Nazwy plików: 'car.txt' zawiera główne dane systemu, a 'car-type.txt' definiuje typy atrybutów
    nazwa_pliku_z_danymi = 'car.txt'
    nazwa_pliku_z_typami_atrybutow = 'car-type.txt'

    wczytane_dane = string_to_tablica(nazwa_pliku_z_danymi)
    atr_type = string_to_tablica(nazwa_pliku_z_typami_atrybutow)

# WYPISYWANIE DANYCH
    print("Dane systemu")
    # Dla każdej linii z pliku 'car.txt' wypisujemy wiersz złączony spacjami,
    for row in wczytane_dane: 
        print(" ".join(row))

    print("\nDane pliku z typami")
    # Analogicznie, dla każdej linii z pliku 'car-type.txt' wypisujemy wiersz,
    for row in atr_type:
        print(" ".join(row))

    decision_class_map = {
        7: 'unacc',  # "unacceptable"
        8: 'acc',    # "acceptable"
        9: 'good',   # "good"
        10: 'vgood'  # "very good"
    }
    # Pobieramy unikalne wartości z ostatniej kolumny, gdzie znajdują się klasy decyzyjne
    decision_classes = get_unique_for_column(wczytane_dane, len(wczytane_dane[0]) - 1)  # Ostatnia kolumna to klasy decyzyjne
    print("\nDostępne klasy decyzyjne:")
    # Dla każdej unikalnej klasy wypisujemy odpowiadającą jej etykietę tekstową,
    for class_value in decision_classes:
        # Wypisujemy nazwę klasy zamiast liczby
        print(decision_class_map.get(class_value, f"Nieznana klasa: {class_value}"))

    print("Wielkości klas decyzyjnych")
    # Wypisujemy liczbę wierszy danych, co w tym kontekście reprezentuje rozmiar zbioru
    print(len(wczytane_dane))

    min_result = find_min(wczytane_dane)
    print("Minimalne:")
    # Dla każdej kolumny wypisujemy najmniejszą wartość, uzyskaną funkcją find_min.
    for item in min_result:
        print(item)

    max_result = find_max(wczytane_dane)
    print("Maksymalne:")
    # Analogicznie, dla każdej kolumny wypisujemy największą wartość.
    for item in max_result:
        print(item)

    # Lista unikalnych wartości
    uniq = get_unique(wczytane_dane)
    print("Unikalne")
    # Wypisujemy każdą unikalną wartość znalezioną w całym zbiorze danych.
    for item in uniq:
        print(item)

    # # Poszczególne unikalne wartości
    # # Dla każdej kolumny w danych:
    # # - Funkcja get_unique_for_column zbiera unikalne wartości z danej kolumny.
    # # - Następnie każda unikalna wartość jest wypisywana.
    # # - Po wypisaniu wartości wyświetlana jest liczba wszystkich unikalnych elementów dla kolumny,
    # for i in range(len(wczytane_dane[0])):
    #     unique_for_column = get_unique_for_column(wczytane_dane, i)
    #     for item in unique_for_column:
    #         print(item)
    #     print(f"Liczba wszystkich: {len(unique_for_column)}")
    #     print("--------------------------")

    # # Odchylenie standardowe
    # # Dla każdej kolumny:
    # # - Tworzona jest lista wartości.
    # # - Obliczane jest odchylenie standardowe tej listy przy użyciu funkcji calculate_standard_deviation.
    # # - Wynik jest wypisywany dla każdej kolumny.
    # for i in range(len(wczytane_dane[0])):
    #     data = [wczytane_dane[j][i] for j in range(len(wczytane_dane))]
    #     standard_deviation = calculate_standard_deviation(data)
    #     print(standard_deviation)

    # # Zadanie 4 i 5: Generowanie 10% więcej danych
    # # - Oblicza się liczbę oryginalnych wierszy oraz liczbę kolumn.
    # # - Wyznaczana jest liczba dodatkowych wierszy, stanowiących 10% oryginalnych.
    # # - Tworzony jest rozszerzony zbiór danych, który składa się z oryginalnych wierszy
    # #   oraz dodatkowych wierszy wypełnionych wartością "?".
    # # - Funkcja fill_missing_values uzupełnia brakujące wartości w rozszerzonym zbiorze.
    # original_rows = len(wczytane_dane)
    # cols = len(wczytane_dane[0])
    # extra_rows = original_rows // 10
    # new_rows = original_rows + extra_rows

    # expanded_data = wczytane_dane + [['?'] * cols for _ in range(extra_rows)]
    # fill_missing_values(expanded_data) 

    # # - Funkcja normalize_into_intervals skaluje wartości danych do zadanego przedziału,
    # #   tutaj od -1 do 1.
    # # - Wynik (macierz znormalizowanych danych) jest wypisywany wiersz po wierszu.
    # normalized_data = normalize_into_intervals(wczytane_dane, -1, 1)
    # print("Dane znormalizowane na przedział <-1, 1>")
    # for row in normalized_data:
    #     print(" ".join(row))

    # # - Analogicznie, tym razem dane są skalowane do przedziału od 0 do 1.
    # # - Każdy wiersz znormalizowanych danych jest wypisywany.
    # normalized_data2 = normalize_into_intervals(wczytane_dane, 0, 1)
    # print("Dane znormalizowane na przedział <0, 1>")
    # for row in normalized_data2:
    #     print(" ".join(row))
    # # - Wywołanie normalize_into_intervals z przedziałem od -10 do 10.
    # # - Wynik prezentowany jest wierszami, gdzie wartości zostały przeskalowane do tego zakresu.
    # normalized_data3 = normalize_into_intervals(wczytane_dane, -10, 10)
    # print("Dane znormalizowane na przedział <-10, 10>")
    # for row in normalized_data3:
    #     print(" ".join(row))

    # # - Funkcja normalize przelicza dane według wzoru standaryzacji (z-score),
    # #   czyli odejmuje średnią i dzieli przez odchylenie standardowe.
    # # - Każdy wiersz znormalizowanych danych jest wypisywany z formatowaniem
    # #   wartości do dwóch miejsc po przecinku.
    # normalized_data4 = normalize(wczytane_dane)
    # print("Dane znormalizowane")
    # for row in normalized_data4:
    #     print(" ".join([f"{float(val):.2f}" for val in row]))

    # # - Funkcja avg oblicza średnią wartość dla każdej kolumny w znormalizowanych danych.
    # # - Wyniki są wypisywane jako ciąg wartości oddzielonych spacjami.
    # average_values = avg(normalized_data4)
    # print(" ".join(map(str, average_values)))

    # # - Funkcja variance oblicza wariancję (rozproszenie wartości) dla każdej kolumny.
    # # - Wypisuje wyniki jako ciąg wartości oddzielonych spacjami.
    # variances = variance(normalized_data4)
    # print(" ".join(map(str, variances)))

    # #Wczytanie pliku CSV
    # readable_data = []   #Lista, która będzie przechowywać wiersze z pliku w formacie słownikowym
    # geography_values = UniqueSet()  #Obiekt klasy UniqueSet, który przechowuje unikalne wartości kolumny "Geography"
    # with open("Churn_Modelling.csv", 'r') as file:  #Otwieramy plik Churn_Modelling.csv w trybie tylko do odczytu ('r')
    #     header_line = file.readline().strip()   #Wczytujemy pierwszą linię, usuwamy zbędne białe znaki (strip()) i dzielimy po ,, 
    #                                             #uzyskując listę nazw kolumn (headers).
    #     headers = header_line.split(',')

    #     for line in file:       #Pętla for line in file – iterujemy po każdej linii w pliku (poza nagłówkiem)
    #         values = line.strip().split(',')
    #         row_dict = {headers[i]: values[i] if i < len(values) else "MISSING" for i in range(len(headers))} #Tworzymy słownik, gdzie kluczami są nagłówki (headers[i]), 
    #                                                                                                             #a wartościami są odpowiednie wartości z values.
    #         geography_values.add(values[headers.index("Geography")])    #Dodajemy odpowiednią wartość do geography_values
    #         readable_data.append(row_dict)  #Każdy wiersz w postaci słownika (row_dict) dodajemy do readable_data

    # # Tworzenie dummy attributes dla kolumny Geography
    # for row in readable_data:       #Przechodzimy przez każdy wiersz (row) w readable_data
    #     for country in geography_values:        #Dla każdego kraju w geography_values tworzymy nową kolumnę
    #         row[country] = "1" if row["Geography"] == country else "0"
    #     del row["Geography"]        #Usuwamy oryginalną kolumnę "Geography"
    #     del row[list(geography_values)[0]]  # Usunięcie jednego z dummy attributes

    # for row in readable_data:       #Iteracja przez readable_data, aby uzyskać każdy wiersz (row)
    #     for kvp in row.items():     #Iteracja przez pary klucz-wartość (.items())
    #         print(f"{kvp[0]}: {kvp[1]} ", end="")       #Wyświetlamy każdą parę w jednym wierszu (end="" pozwala uniknąć nowej linii po każdym elemencie).
    #     print()

if __name__ == "__main__":
    main()
