import requests, re, time, sys
from collections import Counter

URL = "https://pl.wikipedia.org/api/rest_v1/page/random/summary"
N = 100  # liczba losowań
HEADERS = {
    "User-Agent": "wp-edu-wiki-stats/0.1 (kontakt: twoj-email@domena)",
    "Accept": "application/json",
}

# przygotowanie wyrażenia regularnego wyłapującego słowa (litery)
WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)


def selekcja(text: str):
    # Zwróć listę słów wydobytych z 'text', spełniających warunki zadania:
    #  - słowa zapisane małymi literami
    #  - długość każdego słowa > 3 znaki
    slowa = WORD_RE.findall(text)
    wynik = [slowo.lower() for slowo in slowa if len(slowo) > 3]
    return wynik


def ramka(text: str, width: int = 80) -> str:
    if width < 2:
        raise ValueError("Szerokość ramki musi być co najmniej 2.")
    
    inner_width = width - 2
    if len(text) > inner_width:
        text = text[:inner_width - 1] + "…"

    centered = text.center(inner_width)
    return f"[{centered}]"


def main():
    cnt = Counter()
    licznik_slow = 0
    pobrane = 0

    # linia statusu
    print(ramka("Start"), end="", flush=True)

    while pobrane < N:
        try:
            data = requests.get(URL, headers=HEADERS, timeout=10).json()
        except Exception:
            # timeout / brak JSON → spróbuj ponownie
            time.sleep(0.1)
            continue
        
        #tytuł hasła
        title = data.get("title") or ""
        line = "\r" + ramka(title, 80)
        print(line, end="", flush=True)
        
        #tekst hasła
        extract = data.get("extract") or ""
        slowa = selekcja(extract)

        cnt.update(slowa)
        licznik_slow += len(slowa)
        pobrane += 1

        time.sleep(0.1)  
       
    print()  

    print(f"Pobrano wpisów: {pobrane}")
    print(f"Słów (>=4) lącznie:  {licznik_slow}")
    print(f"Unikalnych (>=4):  {len(cnt)}\n")

    print("Top 15 słów (>=4):")
    for slowo, ile in cnt.most_common(15):
        print(f"{slowo:15} {ile}")

if __name__ == "__main__":
    main()
