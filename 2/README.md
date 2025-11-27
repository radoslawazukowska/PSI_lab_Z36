## Zadanie 2

Napisz zestaw dwóch programów – klienta i serwera komunikujących się poprzez TCP. Klient oraz serwer musi być napisany w konfiguracji C + Python (do wyboru co w czym). 

Zmodyfikować serwer tak, aby miał konstrukcję współbieżną, tj. obsługiwał każdego klienta w osobnym procesie. Dla C należy posłużyć się funkcjami fork() oraz (obowiązkowo) wait(). Dla Pythona należy posłużyć się wątkami, do
wyboru: wariant podstawowy lub skorzystanie z ThreadPoolExecutor. Każdy połączony klient wysyła żądanie do serwera o obliczenie hasha przesłanej wiadomości. Przetestować dla kliku równolegle działających klientów.

## Uruchomienie

1. Zaloguj się do bigubu \
   `ssh <yourname>@bigubu.ii.pw.edu.pl`
2. Pobierz repozytorium \
   `git clone https://github.com/radoslawazukowska/PSI_lab_Z36.git`
3. Przejdź do folder tego zadania \
   `cd PSI_lab_Z36/2`
4. Uruchom skrypt run.sh \
   `sh testing_script.sh`
