import os
import time
import threading
import sys

# Stałe konfiguracyjne
LICZBA_KROKOW = 80_000_000
LICZBA_WATKOW = sorted({1, 2, 4, os.cpu_count() or 4})


def policz_fragment_pi(pocz: int, kon: int, krok: float, wyniki: list[float], indeks: int) -> None:
    # Funkcja oblicza częściową sumę przybliżenia liczby pi metodą prostokątów.
    # Argumenty:
    #     pocz, kon - zakres iteracji (indeksy kroków całkowania),
    #     krok      - szerokość pojedynczego prostokąta (1.0 / LICZBA_KROKOW),
    #     wyniki    - lista, do której należy wpisać wynik dla danego wątku na pozycji indeks,
    #     indeks    - numer pozycji w liście 'wyniki' do zapisania rezultatu.

    # Każdy wątek powinien:
    #   - obliczyć lokalną sumę dla przydzielonego przedziału,
    #   - wpisać wynik do wyniki[indeks].
    lokalna_suma = 0.0

    for i in range(pocz, kon):
        x = (i + 0.5) * krok         
        lokalna_suma += 4.0 / (1.0 + x * x)

    wyniki[indeks] = lokalna_suma * krok
    


def main():
    print(f"Python: {sys.version.split()[0]}  (tryb bez GIL? {getattr(sys, '_is_gil_enabled', lambda: None)() is False})")
    print(f"Liczba rdzeni logicznych CPU: {os.cpu_count()}")
    print(f"LICZBA_KROKOW: {LICZBA_KROKOW:,}\n")

    krok = 1.0 / LICZBA_KROKOW
    wyniki = [0.0]
    w = threading.Thread(target=policz_fragment_pi, args=(0, LICZBA_KROKOW, krok, wyniki, 0))
    w.start()
    w.join()

    # ---------------------------------------------------------------
    # Tu zaimplementować:
    #   - utworzenie wielu wątków (zgodnie z LICZBY_WATKOW),
    #   - podział pracy na zakresy [pocz, kon) dla każdego wątku,
    #   - uruchomienie i dołączenie wątków (start/join),
    #   - obliczenie przybliżenia π jako sumy wyników z poszczególnych wątków,
    #   - pomiar czasu i wypisanie przyspieszenia.
    # ---------------------------------------------------------------

    czasy = {}
    baza_czas = None  # czas dla 1 wątku, do liczenia przyspieszenia

    for n_w in LICZBA_WATKOW:
        print(f"\n== Liczba watkow: {n_w} ==")

        wyniki = [0.0] * n_w
        watki = []

        # podział pracy na przedziały [pocz, kon)
        kroki_na_watek = LICZBA_KROKOW // n_w
        reszta = LICZBA_KROKOW % n_w

        start_idx = 0
        for i in range(n_w):
            ile = kroki_na_watek + (1 if i < reszta else 0)
            pocz = start_idx
            kon = pocz + ile
            start_idx = kon

            t = threading.Thread(target=policz_fragment_pi, args=(pocz, kon, krok, wyniki, i))
            watki.append(t)

        t0 = time.perf_counter()

        # startujemy wszystkie wątki
        for t in watki:
            t.start()

        # czekamy na wszystkie
        for t in watki:
            t.join()

        t1 = time.perf_counter()
        czas = t1 - t0
        czasy[n_w] = czas

        pi_przybl = sum(wyniki)

        if baza_czas is None:
            baza_czas = czas
            przysp = 1.0
        else:
            przysp = baza_czas / czas if czas > 0 else float("inf")

        print(f"pi ~= {pi_przybl:.12f}")
        print(f"Czas: {czas:.3f} s")
        print(f"Przyspieszenie wzgledem 1 watku: {przysp:.2f}x")

if __name__ == "__main__":
    main()
