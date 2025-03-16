#!/bin/bash
# Skrypt na macOS

echo "Bartosz Ochnik - Projekt"

# Menu Główne
while true; do
    clear
    echo "==============================="
    echo "        MENU GLOWNE"
    echo "==============================="
    echo "1. Uruchom gre"
    echo "2. Stworz raport"
    echo "3. Opis"
    echo "4. Backup"
    echo "5. Wyjscie"
    echo "==============================="
    read -p "Wybierz opcje 1 - 5: " menu
    echo ""

    case $menu in
        1) program ;;
        2) raport ;;
        3) opis ;;
        4) backup ;;
        5) exit ;;
        *) echo "Zly wybor, wybierz ponownie." ;;
    esac
done

# Funkcja uruchamiająca grę
program() {
    clear
    if [ ! -d "Input" ]; then
        echo "Brak katalogu Input. Prosze sprobowac ponownie."
        read -p "Naciśnij ENTER, aby powrócić do menu..."
        return
    fi

    echo "==============================="
    echo "       URUCHAMIANIE GRY"
    echo "==============================="
    if [ ! -d "Output" ]; then
        mkdir Output
    fi
    python3 main.py
    read -p "Naciśnij ENTER, aby powrócić do menu..."
}

# Funkcja tworzenia raportu
raport() {
    clear
    if [ ! -d "Output" ]; then
        echo "Brak katalogu Output. Prosze sprobowac ponownie."
        read -p "Naciśnij ENTER, aby powrócić do menu..."
        return
    fi

    echo "==============================="
    echo "     TWORZENIE RAPORTU"
    echo "==============================="
    if [ -f "Raport.html" ]; then
        rm Raport.html
    fi

    file_list=""
    for f in Output/*; do
        file_list="$file_list $f"
    done

    python3 Raport.py $file_list
    echo "==============================="
    echo "Raport zostal stworzony!"
    read -p "Naciśnij ENTER, aby powrócić do menu..."
}

# Funkcja wyświetlająca opis
opis() {
    clear
    echo "==============================="
    echo "           OPIS"
    echo "==============================="
    echo "Gra w tabliczke polega na tym, aby zmieszana tablica liczb zostala"
    echo "ulozona w taki sposob, aby liczby byly poukladane rosnaco, a na"
    echo "ostatniej pozycji znajdowalo sie pole puste (0). Gracz moze przesuwac"
    echo "liczby w tablicy, ale tylko te, ktore znajduja sie obok pustego pola."
    echo "Celem gry jest ulozenie tablicy w taki sposob, aby liczby byly w"
    echo "kolejnosci, a 0 bylo na koncu."
    echo ""
    echo "Gracz moze przerwac gre w kazdym momencie wpisujac 'quit'."
    echo ""
    echo "Dodatkowo program generuje raporty z wynikow gry, ktore zawieraja"
    echo "szczegoly o graczu, tablicy oraz czasie i liczbie ruchow. Program"
    echo "umozliwia takze tworzenie backupow danych, w tym kopii wynikow i raportu."
    echo "==============================="
    read -p "Naciśnij ENTER, aby powrócić do menu..."
}

# Funkcja wykonująca backup
backup() {
    clear
    if [ ! -f "Raport.html" ]; then
        echo "Brak raportu. Prosze sprobowac ponownie."
        read -p "Naciśnij ENTER, aby powrócić do menu..."
        return
    fi

    echo "==============================="
    echo "     WYKONYWANIE BACKUPU"
    echo "==============================="
    if [ ! -d "Backups" ]; then
        mkdir Backups
    fi

    # Tworzenie dynamicznej nazwy folderu backupu
    folder_name="Backup__$(date +%Y-%m-%d__%H-%M-%S)"
    mkdir "Backups/$folder_name"

    echo "==============================="
    echo "Kopiowanie danych wejsciowych..."
    cp -R Input "Backups/$folder_name/Input"
    echo "==============================="
    echo "Kopiowanie danych wyjsciowych..."
    cp -R Output "Backups/$folder_name/Output"
    echo "==============================="
    echo "Kopiowanie raportu..."
    cp Raport.html "Backups/$folder_name/"
    echo "==============================="
    echo "Backup zostal wykonany pomyslnie!"
    echo "==============================="
    read -p "Naciśnij ENTER, aby powrócić do menu..."
}