Algoritmus D* lite vytvořen na základě originálního článku Svena Koeniga D* lite dostupného z [1]
Vykreslování bylo z části převzato z tutoriálu k Pygame a z GitHubu z

Pokyny pro ovládání
Otevřít main.py. Zde je několik možností pro nastavení:
	3 způsoby generování grafu:
		a) vygenerování grafu s náhodně rozmístěnými překážkami - není zaručeno, že existuje cesta k cíli
			--> GenerateRandom = True
		b) načtení předem vytvořeného grafu - jeden je v příloze
			--> GenerateRandom = False, LoadGrid = True
		c) vytvoření uživatelem - klikáním levým tlačítkem myši do myšleného umístění překážky
			--> GenerateRandom = False, LoadGrid = False
	Vždy se může během chodu programu vytvořit nová překážka kliknutím na požadované místo a robot podle toho upraví cestu k cíli.

	Nastavení VIEWING_RANGE:
		Jedná se o oblast, ve které je robot schopen detekovat překážku. Hodnota VIEWING_RANGE je myšlena jako počet buňěk na každou stranu, které je
		robot schopen detekovat.
		Pokud je nastavená hodnota malá, jedná se o pohyb robota v neznámém prostředí.
		Pokud je nastavena hodnota jako max(x_div, y_div) jedná se o pohyb robota v předem známém prostředí. Robot ovšem detekuje překážky až po prvním kroku.

	Další možnosti nastavení jsou jasné z komentářů v souboru.

Běh programu:
	Další krok programu se provede zmáčknutím mezerníku. Posunutí o několik kroků (možno nastavit) se provede při zmáčknutí klávesy "f".
	Pokud cesta neexistuje program spadne a vypíše chybovou hlášku.
	Výjimečně program zamrznul během hledání cesty - zatím nezjištěn důvod - v tom případě nutno ukončit a spustit znovu, případně změnit graf.
