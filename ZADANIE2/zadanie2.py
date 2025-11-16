def rzymskie_na_arabskie(rzymskie):
    if not isinstance(rzymskie, str):
        raise ValueError("Liczba rzymska musi być napisem (str).")
    
    r = rzymskie.strip().upper()
    if not r:
        raise ValueError("Pusty napis nie jest poprawną liczbą rzymską.")
    
    dozwolone = set("IVXLCDM")
    if any(ch not in dozwolone for ch in r):
        raise ValueError("Liczba rzymska zawiera niedozwolone znaki.")
    
    ROMAN_VALUES = {
        'I': 1,
        'V': 5, 
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,   
        'M': 1000
    }

    wartosc = 0
    poprzednia = 0

    for ch in reversed(r):
        v = ROMAN_VALUES[ch]
        if v < poprzednia:
            wartosc -= v
        else:
            wartosc += v
            poprzednia = v

    if not (1 <= wartosc <= 3999):
        raise ValueError("Liczba rzymska musi być w zakresie od 1 do 3999.")

    if arabskie_na_rzymskie(wartosc) != r:
        raise ValueError("Niepoprawny format liczby rzymskiej.")

    return wartosc

def arabskie_na_rzymskie(arabskie):
    if not isinstance(arabskie, int):
        raise ValueError("Liczba arabska musi być liczbą całkowitą (int).")
    if not (1 <= arabskie <= 3999):
        raise ValueError("Liczba arabska musi być w zakresie od 1 do 3999.")
    
    wartosci_rzymskie = [
        (1000, 'M'),
        (900, 'CM'),
        (500, 'D'),
        (400, 'CD'),
        (100, 'C'),
        (90, 'XC'),
        (50, 'L'),
        (40, 'XL'),
        (10, 'X'),
        (9, 'IX'),
        (5, 'V'),
        (4, 'IV'),
        (1, 'I')
    ]

    n = arabskie
    rzymskie = ""

    for wartosc, symbol in wartosci_rzymskie:
        while n >= wartosc:
            rzymskie += symbol
            n -= wartosc
            
    return rzymskie

if __name__ == '__main__':
    try:
        # Przykłady konwersji rzymskiej na arabską.
        rzymska = "MCMXCIV"
        print(f"Liczba rzymska {rzymska} to {rzymskie_na_arabskie(rzymska)} w arabskich.")
        
        # Przykłady konwersji arabskiej na rzymską
        arabska = 1994
        print(f"Liczba arabska {arabska} to {arabskie_na_rzymskie(arabska)} w rzymskich.")
        
    except ValueError as e:
        print(e)
