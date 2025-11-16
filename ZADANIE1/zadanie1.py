def dodaj_element(wejscie):
    # może warto zdefiniować zagnieżdżoną funkcję
    najglebsze_listy = []
    max_glebokosc = -1

    def szukaj(obj, glebokosc):
        nonlocal max_glebokosc, najglebsze_listy

        if isinstance(obj, list):
            if glebokosc > max_glebokosc:
                max_glebokosc = glebokosc
                najglebsze_listy = [obj]
            elif glebokosc == max_glebokosc:
                najglebsze_listy.append(obj)

            for element in obj:
                szukaj(element, glebokosc + 1)

        elif isinstance(obj, tuple):
            for element in obj:
                szukaj(element, glebokosc + 1)

        elif isinstance(obj, dict):
            for value in obj.values():
                szukaj(value, glebokosc + 1)

    szukaj(wejscie, 0)

    for lista in najglebsze_listy:
        if lista:
            ostatni = lista[-1]
            nowy = ostatni + 1
        else:
            nowy = 1
        lista.append(nowy)

    return wejscie

if __name__ == '__main__':
    input_list = [
     1, 2, [3, 4, [5, {"klucz": [5, 6], "tekst": [1, 2]}], 5],
     "hello", 3, [4, 5], 5, (6, (1, [7, 8]))
    ]
    output_list = dodaj_element(input_list)
    print(input_list)   