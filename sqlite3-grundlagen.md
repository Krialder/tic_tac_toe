# SQLite3 in Python: anlegen, schreiben, lesen (und der `:memory:`-Trick)

Diese Datei erklärt das kleine sqlite3-Beispiel: was es tut, wie jede Zeile arbeitet und warum es im Online-Compiler mit `unable to open database file` abbricht.

## Was das Skript macht

In einem Durchlauf baut das Skript eine winzige Datenbank auf und liest sie wieder aus: Es verbindet sich mit einer SQLite-Datenbank, legt eine Tabelle `products` an, schreibt eine Zeile hinein, holt alle Zeilen zurück und gibt sie aus. Zum Schluss schließt es die Verbindung. SQLite braucht keinen Server; die ganze Datenbank steckt in einer einzigen Datei oder im Arbeitsspeicher.

## Wie es funktioniert, Schritt für Schritt

- `sqlite3.connect('example.db')` öffnet die Datenbankdatei `example.db` und gibt ein Connection-Objekt zurück. Fehlt die Datei, legt SQLite sie an. Fehlen die Schreibrechte im Verzeichnis, scheitert genau diese Zeile.
- `conn.cursor()` liefert einen Cursor. Über ihn schickst du SQL und liest Ergebnisse zurück. Denk an einen Lesezeiger über den Ergebniszeilen.
- `cursor.execute('CREATE TABLE IF NOT EXISTS products ...')` legt die Tabelle mit den Spalten `id`, `name`, `price` an. `IF NOT EXISTS` heißt: beim zweiten Lauf nicht noch einmal anlegen und keinen Fehler werfen. `INTEGER PRIMARY KEY` zählt `id` automatisch hoch, drum gibst du sie beim Insert nicht selbst an.
- `cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", ('Laptop', 999.99))` fügt eine Zeile ein. Die beiden `?` sind Platzhalter, die Werte folgen als Tupel im zweiten Argument. Nimm immer Platzhalter, nie String-Bastelei wie `f"... VALUES ('{name}')"`: Platzhalter setzen Anführungszeichen und Sonderzeichen korrekt und sperren SQL-Injection aus.
- `conn.commit()` schreibt die Änderung fest. Ohne `commit` ist das Insert nach dem Schließen verloren, weil SQLite in einer Transaktion arbeitet.
- `cursor.execute("SELECT * FROM products")` plus `cursor.fetchall()` holt alle Zeilen als Liste von Tupeln, hier `[(1, 'Laptop', 999.99)]`. Jede Spalte wird ein Eintrag im Tupel, in Spaltenreihenfolge.
- `for row in rows: print(row)` gibt jede Zeile aus.
- `conn.close()` schließt die Verbindung und gibt die Datei wieder frei.

## Warum der Fehler im Online-Compiler kommt

`unable to open database file` klingt nach einem Bug im Code, ist aber eine Sache der Umgebung. `connect('example.db')` will eine Datei im Arbeitsverzeichnis anlegen. Viele Online-Compiler (OneCompiler, diverse Sandboxes) sperren das Schreiben dorthin oder haben ein Nur-Lese-Dateisystem. SQLite kann die Datei dann weder öffnen noch erzeugen und meldet genau das. Auf deinem eigenen Rechner tritt der Fehler nicht auf, da darfst du ins Verzeichnis schreiben.

## Die Lösung: Datenbank im Arbeitsspeicher

Tausch das Dateiziel gegen den Sonderwert `:memory:`:

```python
conn = sqlite3.connect(':memory:')
```

`:memory:` legt die ganze Datenbank im RAM an, ganz ohne Datei. Kein Schreibzugriff aufs Dateisystem nötig, also läuft es in jeder Sandbox. Der Preis: Die Daten sind weg, sobald `conn.close()` läuft oder das Programm endet. Für ein Skript, das in einem Durchlauf anlegt, schreibt, liest und schließt, passt das genau.

Vollständig lauffähig:

```python
import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL
    )
''')

cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", ('Laptop', 999.99))
conn.commit()

cursor.execute("SELECT * FROM products")
for row in cursor.fetchall():
    print(row)

conn.close()
```

Ausgabe:

```
(1, 'Laptop', 999.99)
```

### Wenn du doch eine echte Datei brauchst

Sollen die Daten mehrere Läufe überdauern, brauchst du einen beschreibbaren Pfad. In vielen Online-Compilern ist nur `/tmp` beschreibbar:

```python
conn = sqlite3.connect('/tmp/example.db')
```

Auf OneCompiler überlebt aber auch diese Datei den Lauf nicht, drum bleibt `:memory:` dort der sauberere Weg. Lokal nimmst du einfach `'example.db'`.

## Stolperfallen auf einen Blick

- Ohne `conn.commit()` landet ein Insert nicht dauerhaft in der Datenbank.
- Werte immer per `?`-Platzhalter übergeben, nie in den SQL-String einbauen (SQL-Injection, falsches Quoting).
- `fetchall()` gibt eine Liste von Tupeln zurück, kein Dict. Die Spalten kommen in Definitionsreihenfolge.
- `id` nicht selbst setzen; `INTEGER PRIMARY KEY` zählt automatisch hoch.
