## Zadanie 1.2

Klient ma za zadanie odczytać plik z dysku (proszę wygenerować plik z losowymi 10000B) i wysłać do serwera jego zawartość w paczkach po 100B. Serwer ma zrekonstruować cały plik i obliczyć jego hash. Jako dowód działania proszę m.in. porównać hash obliczony przez serwer z hashem obliczonym przez klienta (może to być wydrukowane w konsoli klienta/serwera, hashe muszą być identyczne). Należy zaimplementować prosty protokół niezawodnej transmisji, uwzględniający możliwość gubienia datagramów. Gubione pakiety muszą być wykrywane i retransmitowane aby serwer mógł odtworzyć cały plik. Należy uruchomić program w środowisku symulującym błędy gubienia pakietów.

### Implementacja

- Każdy pakiet to sturktura (numer sekwencji, dane)
- Klient wysyła pakiet i czeka na ACK od serwera przez okreslony czas. Jesli ACK nie nadejdzie, wysyła pakiet jeszcze raz.
- Serwer po otrzymaniu pakietu od klienta sprawdza czy numer sekwencyjny w otrzymanym pakiecie zgadza się z oczekiwanym. Jeśli jest mniejszy niż oczekiwany, wysłane ACK nie doszło, wiec po prostu wysyla jeszcze raz.
- Na koniec sprawdzamy wyliczony hash w obu.
