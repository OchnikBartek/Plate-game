import os

def create_html_report(output_dir):
    # Tworzenie nagłówka raportu HTML
    report_html = """
    <html>
    <head>
        <title>Raport z gry</title>
        <link rel="stylesheet" type="text/css" href="style.css">  <!-- Dodanie pliku CSS -->
    </head>
    <body>
        <h1>Raport z gry</h1>
        <p>Raport przedstawia wyniki wszystkich zakończonych gier w systemie.</p>
    """

    games_by_level = {}

    # Ustalanie dynamicznej ścieżki do folderu 'output'
    output_dir = os.path.join(os.getcwd(), "output")

    # Iteracja po wszystkich plikach w folderze 'output'
    try:
        for file_name in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file_name)

            # Sprawdź, czy to plik .txt
            if os.path.isfile(file_path) and file_path.endswith(".txt"):
                try:
                    with open(file_path, "r") as f:
                        data = f.readline().strip()

                    # Sprawdzenie poprawności danych
                    if data:
                        fields = data.split(";")
                        if len(fields) == 6:
                            imie_gracza, poziom, table_str, liczba_ruchow, czas, data = fields

                            # Rozdzielanie tablicy na wiersze, przy /nowa_linia
                            table_rows = table_str.split("/nowa_linia")
                            table = [row.strip().split() for row in table_rows]

                            # Obliczanie rozmiaru planszy (liczba wierszy * liczba kolumn)
                            table_size = len(table), len(table[0]) if table else 0

                            # Sprawdzamy, czy liczba ruchów jest liczbą, jeśli nie to pozostawiamy tekst 'Nie rozwiązano'
                            try:
                                liczba_ruchow = int(liczba_ruchow)
                            except ValueError:
                                liczba_ruchow = liczba_ruchow  # Zostawiamy tekst, np. 'Nie rozwiązano'

                            # Czas zawsze jest liczbą, ale możemy go pozostawić jako tekst 'Nie rozwiązano' w przypadku problemu
                            try:
                                czas = float(czas)
                            except ValueError:
                                czas = "Nie rozwiązano"

                            # Dodanie danych do odpowiedniego poziomu trudności
                            if poziom not in games_by_level:
                                games_by_level[poziom] = []
                            games_by_level[poziom].append(
                                (imie_gracza, poziom, table, table_size, liczba_ruchow, czas, data))

                        else:
                            print(f"Niepoprawny format danych w pliku {file_name}.")
                except Exception as e:
                    print(f"Nie udało się odczytać pliku {file_name}: {e}")
            else:
                print(f"Plik {file_name} nie jest plikiem .txt, pomijam go.")

    except FileNotFoundError:
        print(f"Nie znaleziono folderu: {output_dir}")
        return

    # Dla każdego poziomu trudności, sortujemy gry
    for level, games in games_by_level.items():
        # Sortowanie po liczbie ruchów, a w przypadku równości po czasie
        games.sort(key=lambda game: (
            game[4] == "Nie rozwiązano",  # Gry nierozwiązane będą miały najniższą priorytetową wartość
            float('inf') if game[4] == "Nie rozwiązano" else game[4],
            # Jeśli liczba ruchów to "Nie rozwiązano", traktujemy jako nieskończoność
            float('inf') if game[5] == "Nie rozwiązano" else game[5]
        # Jeśli czas to "Nie rozwiązano", traktujemy jako nieskończoność
        ))

        # Dodanie sekcji dla danego poziomu trudności
        report_html += f"<h2>{level.capitalize()}</h2>"
        report_html += "<table border='1'>"
        report_html += """
            <tr>
                <th>Imię gracza</th>
                <th>Poziom trudności</th>
                <th>Tablica przed rozwiązaniem</th>
                <th>Liczba ruchów</th>
                <th>Czas gry</th>
                <th>Data</th>
            </tr>
        """

        # Dodanie wierszy z grami do sekcji
        for game in games:
            imie_gracza, poziom, table, table_size, liczba_ruchow, czas, data = game

            # Formatowanie tablicy do wyświetlenia w HTML
            table_html = "<table border='1'>"
            for row in table:
                table_html += "<tr>" + "".join(f"<td>{x}</td>" for x in row) + "</tr>"
            table_html += "</table>"

            # Dodanie wiersza do tabeli HTML
            report_html += f"""
            <tr>
                <td>{imie_gracza}</td>
                <td>{poziom}</td>
                <td>{table_html}</td>
                <td>{liczba_ruchow}</td>
                <td>{czas}</td>
                <td>{data}</td>
            </tr>
            """

        report_html += "</table>"

    # Zakończenie raportu HTML
    report_html += """
    </body>
    </html>
    """

    # Zapisanie raportu do pliku HTML z kodowaniem UTF-8
    output_file_path = os.path.join(os.getcwd(), "Raport.html")
    with open(output_file_path, "w", encoding='utf-8') as report_file:
        report_file.write(report_html)
    print(f"Raport został wygenerowany: {output_file_path}")


# Wywołanie funkcji
create_html_report(os.path.join(os.getcwd(), "output"))