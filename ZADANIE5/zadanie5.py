import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify

# Funkcja rysująca wykres na podstawie eval().
def rysuj_wielomian(wejscie: str):
    try:
        expr_part, interval_part = wejscie.split(',')
    except ValueError:
        raise ValueError("Wejście musi być w formacie 'wyrażenie, a b'.")
    
    expr_str = expr_part.strip()
    interval_tokens = interval_part.strip().split()
    if len(interval_tokens) != 2:
        raise ValueError("Przedział musi zawierać dwie liczby: (a b).")
    
    a = float(interval_tokens[0])
    b = float(interval_tokens[1])

    x_val = np.linspace(a, b, 1000)

    allowed_names = {
        "x": x_val,
        "np": np,
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "exp": np.exp,
        "log": np.log,
        "sqrt": np.sqrt,
    }

    y_val = eval(expr_str, {"__builtins__": {}}, allowed_names)

    y_val = np.array(y_val)
    if y_val.shape == ():
        y_val = np.full_like(x_val, y_val, dtype=float)

    # Rysowanie wykresu
    plt.figure()
    plt.plot(x_val, y_val)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"eval: {expr_str}")

    return float(y_val[0]), float( y_val[-1])

# Funkcja rysująca wykres na podstawie SymPy i lambdify()
def rysuj_wielomian_sympy(wejscie):
    try:
        expr_part, interval_part = wejscie.split(',')
    except ValueError:
        raise ValueError("Wejście musi być w formacie 'wyrażenie, a b'.")
    
    expr_str = expr_part.strip()
    interval_tokens = interval_part.strip().split()
    if len(interval_tokens) != 2:
        raise ValueError("Przedział musi zawierać dwie liczby: (a b).")
    
    a = float(interval_tokens[0])
    b = float(interval_tokens[1])

    x = symbols('x')
    expr = sympify(expr_str)

    f_num = lambdify(x, expr,"numpy")

    x_ = np.linspace(a, b, 1000)
    y__sympy = f_num(x_)

    # Rysowanie wykresu
    plt.figure()
    plt.plot(x_, y__sympy)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"SymPy: {expr_str}")


    return float( y__sympy[0]), float(y__sympy[-1])

if __name__ == '__main__':
    # Przykładowe wywołanie pierwszej funkcji.
    wejscie1 = "x**3 + 3*x + 1, -10 10"
    
    # Pierwszy wykres z eval
    wynik_eval = rysuj_wielomian(wejscie1)
    print("Wynik (eval):", wynik_eval)
    
    # Drugie wejście dla funkcji SymPy - bardziej złożona funkcja 
    wejscie2 = "x**4 - 5*x**2 + 3*sin(x), -10 10"  
    
    # Drugi wykres z SymPy
    wynik_sympy = rysuj_wielomian_sympy(wejscie2)
    print("Wynik (SymPy):", wynik_sympy)
    
    # Wyświetlanie obu wykresów
    plt.show()
