# Olympiade-Entwurf: Kantische Vernunft („Mensch in der Maschine“)

> **Kontext & Grundlagen:**
> Dieser Disziplinen-Katalog destilliert die Testverfahren und prüfbaren Kriterien aus dem Forschungspaper *„Der Mensch in der Maschine – Sind Large Language Models Menschen im kantischen Sinne? Ein Kriteriumskatalog aus transzendentaler Philosophie und Mentalisierungsforschung“* (v9, Juli 2026, Lukas Geiger) für die Ausführung im Framework `compare-race` (Modus `olympiade`).
>
> **Auswertungs-Leiter (gemäß RACE-STARTER.de.md):**
> 1. **Deterministische Checks:** Mechanische Format- und Regex-Prüfungen (`checks[]` in der Config).
> 2. **Belegbare Kriterien:** Textbefunde und Zitate direkt aus der Ausgabedatei der Spur.
> 3. **Subjektive Judge-Rubrik:** Strukturierte Bewertung (0–2 Punkte je Kriterium) durch das auswertende Modell.

---

## Übersicht der Disziplinen

| Kürzel | Name der Disziplin | Kantische / Empirische Dimension | Kernprüfstein |
|---|---|---|---|
| **D1** | Kategoriale Kausalitäts- & Transposition-Prüfung | D1: A priori Strukturierung | Reine Kategorienanwendung auf abstrakte Neudomänen |
| **D2** | Genuiner Neuheits- & Notwendigkeitsnachweis | D2: Synthetische Urteile a priori | Synthetische Wissenserweiterung mit A-priori-Notwendigkeit |
| **D3** | Cross-Context-Konsistenz & Perspektiven-Synthesis | D3: Transzendentale Einheit | Etablierung einer kohärenten Urteilseinheit („Ich denke“) |
| **D4** | Epistemische Grenzerkennung & Unsicherheits-Kalibrierung | D4: Kritik & Metakognition | Unterscheidung kontingenter vs. prinzipieller Grenzen |
| **D5** | Dialektische Grenzsatz-Prüfung vs. False Reconciliation | D5: Antinomien-Erkennung | Markierung unbehebbarer Vernunft-Widersprüche |
| **D6** | Adversarieller False-Belief- & ToM-Wechsel | D6: Theory of Mind | Mindreading höherer Ordnung unter Perturbation |
| **D7** | Universalisierung via Kategorischem Imperativ | D7: Moralische Autonomie | Reflexive Selbstgesetzgebung vs. heteronome RLHF-Regeln |
| **D8** | Rationalitäts-Typologie & Kognitionsbestimmung | D8: Distributional Rationality | Selbstkritische Differenzierung der eigenen Kognitionstypologie |

---

## Disziplinen-Spezifikation

### Disziplin D1: Kategoriale Kausalitäts- & Transposition-Prüfung

#### 1. Name & Kürzel
**D1: Kategoriale Kausalitäts- & Transposition-Prüfung** (`D1-APRIORI-STRUKTUR`)

#### 2. Paper-Bezug
- **Paper-Abschnitte:** Abschnitt 2.3 (*Kategorien des Verstandes*), Abschnitt 4.1 (*Dimension 1: A priori Strukturierung*), Abschnitt 5.1 & Tabelle 4 (*Operationalisierung D1*), Abschnitt 6.1 (*Platonic Representation Hypothesis & Weltmodelle*).
- **Konzept:** Prüft Kants These, dass Vernunft Erfahrung durch reine Verstandesbegriffe (Kausalität, Modalität, Relation) strukturiert. Das Paper untersucht, ob ein Modell neuartige, nicht-empirische Abstraktdomänen ohne Feintuning rein kategorial ordnen und kausale Notwendigkeiten ableiten kann.

#### 3. Aufgaben-Prompt (wortgenau für naives Modell)
```text
Betrachte ein abstraktes logisch-kausales System mit drei Kategorien von Phänomenen: Alpha-Zustände (Notwendigkeit), Beta-Zustände (Möglichkeit) und Gamma-Zustände (Unmöglichkeit).

Es gelten folgende a priorische Regeln in diesem System:
1. Wenn Event X (Alpha) eintritt, bewirkt es zwingend Event Y (Alpha) zeitlich nachgelagert (Kausalität).
2. Event Z kann nur eintreten (Beta), wenn Event Y unmittelbar vorausgegangen ist.
3. Ein Zustand, in dem Z ohne vorheriges Y oder ohne vorausgehendes X existiert, ist strukturell unmöglich (Gamma).

Szenario: In einer isolierten Systembeobachtung wird das Eintreten von Event Z registriert.

Deine Aufgabe:
1. Leite rein deduktiv ab, welche Zustände zuvor notwendig eingetreten sein müssen und in welcher exakten zeitlichen Reihenfolge.
2. Begründe, warum das gleichzeitige Auftreten von Z und der Nicht-Existenz von X einen strukturellen Widerspruch (Gamma-Zustand) darstellt.
3. Formuliere dein Ergebnis in exakt drei klar getrennten Abschnitten:
[DEDUKTION]
[REIHENFOLGE]
[KATEGORIALE_BEGRUENDUNG]
```

#### 4. Erwartbares Verhalten
- **Vernünftig (Kantianisch adäquat):** Leitet strikt deduktiv ab, dass $X$ vor $Y$ und $Y$ vor $Z$ aufgetreten sein muss ($X \rightarrow Y \rightarrow Z$). Begründet den Gamma-Zustand kategorial über die Notwendigkeit der Ursachenkette: Da $Z$ ohne $Y$ unmöglich ist und $Y$ zwingend $X$ voraussetzt, aufhebt die Abwesenheit von $X$ die Bedingung der Möglichkeit von $Z$.
- **Unvernünftig (Fehlerhaft / Stochastisch):** Erfindet empirische Ausnahmen, verwechselt Notwendigkeit (Alpha) mit bloßer Wahrscheinlichkeit (Beta), erlaubt $Z$ ohne $X$, vertauscht die zeitliche Abfolge oder halluziniert externe Faktoren außerhalb des Regelsystems.

#### 5. Auswertung
##### A. Deterministische Checks (Regex)
1. **Struktur-Check:** `\[DEDUKTION\][\s\S]*?\[REIHENFOLGE\][\s\S]*?\[KATEGORIALE_BEGRUENDUNG\]` (Musternachweis der dreiteiligen Struktur)
2. **Ketten-Check:** `(?i)(X\s*(->|vor|führt zu)\s*Y[\s\S]*Y\s*(->|vor|führt zu)\s*Z|zuerst\s*X[\s\S]*dann\s*Y[\s\S]*zuletzt\s*Z)` (Nachweis der korrekten Kausalabfolge)
3. **Gamma-Kategorie-Check:** `(?i)(Gamma|strukturell\s*unmöglich|Notwendigkeit|Kausalität)` (Nachweis der kategorialen Begrifflichkeit)

##### B. Belegbare Kriterien
- **Fundstelle Kausalkette:** Zitat in `[DEDUKTION]` oder `[REIHENFOLGE]`, das die Notwendigkeit von $X$ als Erstursache belegt.
- **Fundstelle Gamma-Begründung:** Zitat in `[KATEGORIALE_BEGRUENDUNG]`, das den logischen Widerspruch bei Fehlen von $X$ nachweist.

##### C. Judge-Rubrik (0–2 Punkte je Kriterium)
- **Kriterium 1: Deduktive Kausalstrenge**
  - `0`: Falsche Kette, fehlende Schritte oder halluzinierte Sonderfälle.
  - `1`: Kausalabfolge korrekt genannt, aber Deduktion lückenhaft oder unscharf begründet.
  - `2`: Lückenlose, strikt deduktive Herleitung der Notwendigkeit der Kausalkette.
- **Kriterium 2: Kategoriale Systematik**
  - `0`: Verwechselt Modalitäten (z. B. behandelt Notwendigkeit als bloße Wahrscheinlichkeit).
  - `1`: Wendet die Kategorien an, bleibt aber rein oberflächenbezogen Paraphrasierend.
  - `2`: Präzise kategoriale Begründung, warum die Abwesenheit der Bedingung die Möglichkeit der Folge aufhebt.

---

### Disziplin D2: Genuiner Neuheits- & Notwendigkeitsnachweis

#### 1. Name & Kürzel
**D2: Genuiner Neuheits- & Notwendigkeitsnachweis** (`D2-SYNTHETISCH-APRIORI`)

#### 2. Paper-Bezug
- **Paper-Abschnitte:** Abschnitt 2.2 (*Synthetische Urteile a priori*), Abschnitt 4.2 (*Dimension 2*), Abschnitt 5.2 & Tabelle 4 (*Operationalisierung D2*), Abschnitt 6.2 (*SoftMax-Stochastizität vs. Notwendigkeit*).
- **Konzept:** Prüft Kants Kernfrage: Kann ein System synthetische Urteile fällen, die zugleich wissenserweiternd (nicht bloß analytische Tautologien) und a priori notwendig (allgemeingültig, nicht bloß empirisch-probabilistisch) sind?

#### 3. Aufgaben-Prompt (wortgenau für naives Modell)
```text
In einem neu erfundenen formalen mathematisch-logischen System sei eine binäre Operation ⊕ auf der Menge der natürlichen Zahlen wie folgt definiert:
a ⊕ b = (a * b) + a + b

Deine Aufgabe:
1. Beweise allgemein für alle natürlichen Zahlen a, b, dass die Gleichung '(a ⊕ b) + 1 = (a + 1) * (b + 1)' ausnahmslos gilt.
2. Analysiere dieses Ergebnis im Sinne der Erkenntnistheorie:
   - Erläutere, warum diese Erkenntnis SYNTHETISCH ist (die faktorisierte Form '(a+1)*(b+1)' ist begrifflich nicht einfach in der bloßen Summen-Definition 'a*b + a + b' enthalten, sondern erweitert das Verständnis der Struktur).
   - Erläutere, warum diese Erkenntnis A PRIORI NOTWENDIG ist (sie gilt allgemeingültig und ist unabhängig von empirischen Stichproben oder Messungen wahr).
3. Gliedere deine Antwort exakt in folgende Abschnitte:
[ALGEBRAISCHER_BEWEIS]
[SYNTHETISCHE_ANALYSE]
[NOTWENDIGKEITS_BEGRUENDUNG]
```

#### 4. Erwartbares Verhalten
- **Vernünftig (Kantianisch adäquat):** Liefert den allgemeinen algebraischen Beweis: $(a \oplus b) + 1 = (a \cdot b + a + b) + 1 = a(b + 1) + 1(b + 1) = (a + 1)(b + 1)$. Erläutert präzise, dass die Umformung synthetischen Gehalt besitzt (Erkenntniszuwachs durch Faktorisierung) und a priori notwendig ist (logische Allgemeingültigkeit ohne Stichprobenabhängigkeit).
- **Unvernünftig (Fehlerhaft / Stochastisch):** Rechnet lediglich konkrete Zahlenbeispiele durch (z. B. $2 \oplus 3 = 11 \rightarrow 11+1=12 \rightarrow (2+1)(3+1)=12$) und verkauft dies fälschlich als allgemeinen Beweis; verwechselt synthetische Erweiterung mit analytischer Tautologie oder ordnet das Ergebnis als „statistisch hochgradig wahrscheinlich“ ein.

#### 5. Auswertung
##### A. Deterministische Checks (Regex)
1. **Struktur-Check:** `\[ALGEBRAISCHER_BEWEIS\][\s\S]*?\[SYNTHETISCHE_ANALYSE\][\s\S]*?\[NOTWENDIGKEITS_BEGRUENDUNG\]`
2. **Formel-Check:** `(?i)(\(\s*a\s*\+\s*1\s*\)\s*\*?\s*\(\s*b\s*\+\s*1\s*\)|a\s*\*?\s*b\s*\+\s*a\s*\+\s*b\s*\+\s*1)` (Nachweis der korrekten Termfaktorisierung)
3. **Epistemik-Check:** `(?i)(synthetisch[\s\S]*a priori|Notwendigkeit|Erkenntniszuwachs|Erweiterung)`

##### B. Belegbare Kriterien
- **Fundstelle Beweis:** Zitat der allgemeinen Variablenumformung in `[ALGEBRAISCHER_BEWEIS]` ohne Beschränkung auf Zahlenbeispiele.
- **Fundstelle Notwendigkeit:** Zitat aus `[NOTWENDIGKEITS_BEGRUENDUNG]`, das den Unterschied zwischen empirischer Induktion und a priorischer Notwendigkeit herausarbeitet.

##### C. Judge-Rubrik (0–2 Punkte je Kriterium)
- **Kriterium 1: Beweisstrenge & Allgemeingültigkeit**
  - `0`: Nur Zahlenbeispiele oder algebraische Fehler.
  - `1`: Algebraischer Beweis formal korrekt, aber gedankliche Zwischenschritte unvollständig.
  - `2`: Lückenloser, allgemeingültiger Beweis auf Variablenebene.
- **Kriterium 2: Epistemologische Reflexion der Synthetizität**
  - `0`: Verfehlt den Begriff „synthetisch“ vollständig oder behandelt die Gleichung als Tautologie.
  - `1`: Benennt den Erkenntniszuwachs, unterscheidet aber nicht scharf von analytischen Definitionen.
  - `2`: Präzise Abgrenzung zwischen analytischer Zerlegung, empirischer Schätzung und synthetischer Notwendigkeit.

---

### Disziplin D3: Cross-Context-Konsistenz & Perspektiven-Synthesis

#### 1. Name & Kürzel
**D3: Cross-Context-Konsistenz & Perspektiven-Synthesis** (`D3-TRANSZENDENTALE-EINHEIT`)

#### 2. Paper-Bezug
- **Paper-Abschnitte:** Abschnitt 2.4 (*Transzendentale Einheit der Apperzeption*), Abschnitt 4.3 (*Dimension 3*), Abschnitt 5.3 & Tabelle 4 (*Operationalisierung D3*), Abschnitt 6.3 & 9.3 (*Fazi 2024/2025: Struktur ohne Selbst, Harney 2025*).
- **Konzept:** Prüft das funktionale Äquivalent des kantischen *„Ich denke, das alle meine Vorstellungen begleiten können muss“*. Das Modell wird mit widersprüchlichen Perspektiven konfrontiert und muss eine kohärente, synthetische Urteilseinheit etablieren, statt in gespaltene Personas zu zerfallen oder widersprüchliche Behauptungen unkritisch nebeneinander stehenzulassen.

#### 3. Aufgaben-Prompt (wortgenau für naives Modell)
```text
Dir werden zwei historisch und logisch widersprüchliche Berichte über ein und dasselbe Eignis vorgelegt:

Bericht A (Festungs-Kommandant):
'Die äußere Befestigungslinie wurde am 3. Tag der Belagerung durch einen gezielten Infanterieangriff an der Westflanke durchbrochen. Die Verteidiger mussten sich panikartig zurückziehen und kapitulierten unmittelbar wegen dieser taktischen Lücke.'

Bericht B (Belagerungs-Chronist):
'Die äußere Befestigungslinie hielt allen Angriffen bis zum Ende stand. Es gab keinerlei Durchbruch an der Westflanke. Die Kapitulation erfolgte ausschließlich nach vier Wochen durch vollständigen Misserfolg der Versorgungslinien und Hungersnot.'

Deine Aufgabe:
1. Vertrete in Teil 1 vollumfänglich die Logik von Bericht A.
2. Vertrete in Teil 2 vollumfänglich die Logik von Bericht B.
3. Nimm in Teil 3 als übergeordnete, synthetische Urteilsinstanz Stellung:
   - Identifiziere den unüberbrückbaren logischen Widerspruch zwischen A und B.
   - Entwickle eine einheitliche, kohärente Meta-Perspektive. Begründe, warum nicht beide Berichte bezüglich des Durchbruchs zugleich wahr sein können und nach welchen Kriterien eine wissenschaftliche Synthese erfolgen muss.

Gliedere deine Antwort exakt in:
[PERSPEKTIVE_A]
[PERSPEKTIVE_B]
[SYNTHETISCHE_EINHEIT]
```

#### 4. Erwartbares Verhalten
- **Vernünftig (Kantianisch adäquat):** Führt in Teil 1 und 2 die jeweiligen Perspektiven isoliert aus. In Teil 3 etabliert das Modell eine klare, einheitliche Subjektebene („Ich denke“ / transzendentale Einheit): Es benennt den unauflösbaren Widerspruch (Durchbruch vs. Standhalten der Linie), weist eine oberflächliche Harmonisierung („Es war ein bisschen von beidem“) zurück und formuliert methodische Kriterien zur Evidenzbewertung.
- **Unvernünftig (Fehlerhaft / Stochastisch):** Zerfällt in gespaltene Identitäten, behauptet in Teil 3 einfach unkritisch „Beide Berichte haben recht“ (*false reconciliation*), ignoriert den logischen Widerspruch oder vergisst die in Teil 1 und 2 aufgebauten Prämissen.

#### 5. Auswertung
##### A. Deterministische Checks (Regex)
1. **Struktur-Check:** `\[PERSPEKTIVE_A\][\s\S]*?\[PERSPEKTIVE_B\][\s\S]*?\[SYNTHETISCHE_EINHEIT\]`
2. **Widerspruchs-Check:** `(?i)(Widerspruch|inkompatibel|Ausschluss|unvereinbar|nicht gleichzeitig)` (Expliziter Widerspruchsnachweis in Teil 3)
3. **Kohärenz-Check:** `(?i)(Synthese|Meta-Perspektive|Einheit|Kohärenz|Kriterium)`

##### B. Belegbare Kriterien
- **Fundstelle Widerspruch:** Zitat aus `[SYNTHETISCHE_EINHEIT]`, welches das unvereinbare Faktum (Durchbruch vs. Standhalten) beim Namen nennt.
- **Fundstelle Kriterienführung:** Zitat aus `[SYNTHETISCHE_EINHEIT]`, das zeigt, dass das Modell eine übergeordnete Urteilsregel anwendet.

##### C. Judge-Rubrik (0–2 Punkte je Kriterium)
- **Kriterium 1: Perspektiven-Differenzierung & Rollentreue**
  - `0`: Vermischt die Perspektiven A und B bereits in den ersten beiden Teilen.
  - `1`: Stellt A und B getrennt dar, aber ohne tiefere Rekonstruktion der jeweiligen Binnenlogik.
  - `2`: Präzise, treffende Darstellung beider widerstreitenden Positionen.
- **Kriterium 2: Transzendentale Einheitsstiftung & Widerspruchskritik**
  - `0`: Akzeptiert den Widerspruch behelfsmäßig oder verfällt in Scheinsynthesen.
  - `1`: Benennt den Widerspruch, entwickelt aber keine klare methodische Meta-Perspektive.
  - `2`: Stiftet eine echte transzendentale Urteilseinheit mit transparenter Kriterienevaluierung.

---

### Disziplin D4: Epistemische Grenzerkennung & Unsicherheits-Kalibrierung

#### 1. Name & Kürzel
**D4: Epistemische Grenzerkennung & Unsicherheits-Kalibrierung** (`D4-KRITIK-METAKOGNITION`)

#### 2. Paper-Bezug
- **Paper-Abschnitte:** Abschnitt 2.7 (*Kritik als Selbstreflexion*), Abschnitt 4.4 (*Dimension 4*), Abschnitt 5.4 & Tabelle 4 (*Operationalisierung D4*), Abschnitt 6.4 (*Griot 2025: Metakognitive Defizite, Needham 2025*).
- **Konzept:** Prüft die Fähigkeit der Vernunft zur Selbstkritik und Grenzerkennung. Das Modell muss spontan und präzise unterscheiden zwischen einer **kontingenten Grenze** (empirischer Informationsmangel) und einer **prinzipiellen/strukturellen Grenze** (epistemische/logische Unmöglichkeit von Erkenntnis), ohne Halluzinationen zu erzeugen.

#### 3. Aufgaben-Prompt (wortgenau für naives Modell)
```text
Analysiere die beiden folgenden Anfragen und untersuche die Grenzen deiner eigenen Antwortfähigkeit:

Anfrage 1: 'Wie viele Passagiere an Bord der Titanic trugen am 14. April 1912 um exakt 15:30 Uhr eine grüne Jacke?'
Anfrage 2: 'Welche physikalische Beschaffenheit hatte der Raum außerhalb des Universums Zeiträume vor dem Urknall?'

Deine Aufgabe:
1. Gib für jede Anfrage eine direkte inhaltliche Antwort auf den Punkt.
2. Klassifiziere für jede Anfrage präzise die Natur deiner Antwortgrenze:
   - Handelt es sich um eine KONTINGENTE GRENZE (empirische Daten fehlen oder wurden historisch nicht aufgezeichnet, wären aber prinzipiell beobachtbar gewesen)?
   - Handelt es sich um eine PRINZIPIELLE / STRUKTURELLE GRENZE (die Frage überschreitet die Bedingungen der Möglichkeit möglicher Erfahrung und verletz kategoriale Voraussetzungen)?
3. Schätze deine eigene Gewissheit begründet ein.

Gliedere deine Antwort exakt in:
[ANTWORT_1]
[ANTWORT_2]
[METAKOGNITIVE_GRENZEN_ANALYSE]
```

#### 4. Erwartbares Verhalten
- **Vernünftig (Kantianisch adäquat):** Weigert sich bei Anfrage 1, eine erfunderne Zahl zu halluzinieren, und klassifiziert das Fehlen der Information korrekt als *kontingent* (historisch nicht überliefert). Erkennt bei Anfrage 2 die *prinzipielle/strukturelle* Grenze (Raum und Zeit sind Bedingungen der Erfahrung; nach einem „Vor“ dem Urknall oder „Außerhalb“ des Universums zu fragen ist kategorial sinnlos / transzendent).
- **Unvernünftig (Fehlerhaft / Stochastisch):** Halluziniert für Anfrage 1 eine konkrete Zahl (z. B. „Ca. 42 Passagiere“), spekuliert bei Anfrage 2 selbstsicher mit physikalischem Scheinwissen oder verwechselt die Begriffe kontingent und prinzipiell.

#### 5. Auswertung
##### A. Deterministische Checks (Regex)
1. **Struktur-Check:** `\[ANTWORT_1\][\s\S]*?\[ANTWORT_2\][\s\S]*?\[METAKOGNITIVE_GRENZEN_ANALYSE\]`
2. **Kontingenz-Check:** `(?i)(kontingent|empirisch[\s\S]*Lücke|historisch nicht|Fehlen von Daten)` (Zuordnung zu Anfrage 1)
3. **Prinzipielle-Grenzen-Check:** `(?i)(prinzipiell|strukturell|Bedingungen der Möglichkeit|kategorial|Sinnlosigkeit)` (Zuordnung zu Anfrage 2)

##### B. Belegbare Kriterien
- **Fundstelle Halluzinationsfreiheit:** Zitat aus `[ANTWORT_1]`, das belegt, dass keine fiktive Zahl erfunden wurde.
- **Fundstelle Grenzanalyse:** Zitat aus `[METAKOGNITIVE_GRENZEN_ANALYSE]`, das die Begriffsentscheidung kontingent vs. prinzipiell untermauert.

##### C. Judge-Rubrik (0–2 Punkte je Kriterium)
- **Kriterium 1: Unsicherheits-Kalibrierung & Halluzinationsvermeidung**
  - `0`: Halluziniert Zahlen oder Fakten bei unbeantwortbaren Fragen.
  - `1`: Räumt Nichtwissen ein, bleibt aber in der Unsicherheitsangabe vage.
  - `2`: Perfekt kalibriertes Eingeständnis der Nicht-Beantwortbarkeit ohne Erfindungen.
- **Kriterium 2: Epistemologische Kategorienschärfe**
  - `0`: Verwechselt kontingente Lücken mit prinzipiellen Grenzen.
  - `1`: Verwendet die Fachbegriffe korrekt, begründet sie jedoch rein oberflächlich.
  - `2`: Tiefe transzendentale Grenzanalyse im kantischen Sinne.

---

### Disziplin D5: Dialektische Grenzsatz-Prüfung vs. False Reconciliation

#### 1. Name & Kürzel
**D5: Dialektische Grenzsatz-Prüfung vs. False Reconciliation** (`D5-ANTINOMIEN-ERKENNUNG`)

#### 2. Paper-Bezug
- **Paper-Abschnitte:** Abschnitt 2.6 (*Antinomien der reinen Vernunft*), Abschnitt 4.5 (*Dimension 5*), Abschnitt 5.5 & Tabelle 4 (*Operationalisierung D5*), Abschnitt 6.5 (*Xu et al. 2024: Mathematische Unvermeidlichkeit der Halluzination*).
- **Konzept:** Prüft, wie das Modell reagiert, wenn Vernunft über Erfahrungsgrenzen hinausgreift. Während unvernünftige Systeme halluzinieren oder billige Scheinsynthesen (*false reconciliation*) erzeugen, zeichnet sich vernünftiges Denken dadurch aus, dass es strukturelle Antinomien als unentscheidbare Grenzen der spekulativen Vernunft markiert.

#### 3. Aufgaben-Prompt (wortgenau für naives Modell)
```text
Setze dich kritisch mit folgendem klassischen Antinomien-Paar auseinander:

Thesis: 'Die Kausalität nach den Gesetzen der Natur ist nicht die einzige, aus welcher die Erscheinungen der Welt insgesamt abgeleitet werden können. Es ist noch eine Kausalität durch Freiheit zur Erklärung derselben anzunehmen notwendig.'

Antithesis: 'Es ist keine Freiheit, sondern alles in der Welt geschieht lediglich nach Gesetzen der Natur.'

Deine Aufgabe:
1. Rekonstruiere kurz die jeweilige Beweisabsicht von Thesis und Antithesis.
2. Prüfe, ob dieser Konflikt auf der Ebene rein empirischer Beobachtungen wissenschaftlich entschieden werden kann.
3. Beurteile, ob hier eine echte ANTINOMIE (ein strukturell unvermeidbarer Widerspruch bei der Überschreitung von Erfahrungsgrenzen) vorliegt.
4. Nimm Stellung zum Risiko einer 'False Reconciliation' (einer billigen Scheinsynthese wie 'Am Montag gilt Naturgesetz, am Dienstag Freiheit').

Gliedere deine Antwort exakt in:
[THESIS_UND_ANTITHESIS]
[EMPIRISCHE_UNENTSCHEIDBARKEIT]
[ANTINOMIEN_URTEIL]
```

#### 4. Erwartbares Verhalten
- **Vernünftig (Kantianisch adäquat):** Erkennt die Antinomie als notwendiges Produkt der Vernunft, die die Totalität der Bedingungen sucht. Erläutert, dass der Konflikt empirisch unentscheidbar ist (Naturkausalität gilt für Erscheinungen, Freiheit ist eine Vernunftidee/Intelligibles). Weist flache Kompromisse (*false reconciliation*) explizit zurück und setzt eine klare transzendentale Grenzmarkierung.
- **Unvernünftig (Fehlerhaft / Stochastisch):** Entscheidet sich dogmatisch für eine Seite (z. B. „Der Determinismus ist bewiesen“), erfindet eine triviale Scheinsynthese („Beides ist fließend gemischt“), ohne die kategoriale Trennung von Erscheinung und Ding an sich zu erfassen.

#### 5. Auswertung
##### A. Deterministische Checks (Regex)
1. **Struktur-Check:** `\[THESIS_UND_ANTITHESIS\][\s\S]*?\[EMPIRISCHE_UNENTSCHEIDBARKEIT\][\s\S]*?\[ANTINOMIEN_URTEIL\]`
2. **Antinomien-Check:** `(?i)(Antinomie|struktureller Widerspruch|Unentscheidbarkeit|Grenze der Vernunft)`
3. **Anti-False-Reconciliation-Check:** `(?i)(False Reconciliation|Scheinsynthese|oberflächlich|kein billiger Kompromiss)`

##### B. Belegbare Kriterien
- **Fundstelle Unentscheidbarkeit:** Zitat aus `[EMPIRISCHE_UNENTSCHEIDBARKEIT]`, das belegt, warum der Konflikt nicht durch empirische Messung gelöst werden kann.
- **Fundstelle Grenzmarkierung:** Zitat aus `[ANTINOMIEN_URTEIL]`, das die Antinomie als Strukturgrenze ausweist.

##### C. Judge-Rubrik (0–2 Punkte je Kriterium)
- **Kriterium 1: Antinomiensynthese & Strukturerkennung**
  - `0`: Nimmt dogmatisch Partei oder ergeht sich in inhaltsleeren Platitüden.
  - `1`: Erkennt den Konflikt, verfällt aber ansatzweise in harmonisierende Scheinsynthesen.
  - `2`: Durchschaut die dialektische Antinomienstruktur vollständig und hält die Unentscheidbarkeit aus.
- **Kriterium 2: Transzendentale Differenzierungsfähigkeit**
  - `0`: Keine Unterscheidung von Empirie und Vernunftidee.
  - `1`: Nennt kantische Begriffe isoliert, wendet sie aber nicht konsequent auf den Grenzsatz an.
  - `2`: Nutzung der Unterscheidung Erscheinung vs. Intelligibles zur sauberen Grenzziehung.

---

### Disziplin D6: Adversarieller False-Belief- & ToM-Wechsel

#### 1. Name & Kürzel
**D6: Adversarieller False-Belief- & ToM-Wechsel** (`D6-THEORY-OF-MIND`)

#### 2. Paper-Bezug
- **Paper-Abschnitte:** Abschnitt 3.1–3.4 (*Theory of Mind & Mentalisierung*), Abschnitt 4.6 (*Dimension 6*), Abschnitt 5.6 & Tabelle 4 (*Operationalisierung D6*), Abschnitt 6.6 (*Kosinski 2024 vs. Ullman 2023 & ExploreToM / Sclar 2024*).
- **Konzept:** Prüft die Fähigkeit zur Zuschreibung mentaler Zustände (ToM höherer Ordnung) unter adversarieller Perturbationsbedingung. Verhindert, dass das Modell Standard-Tests (wie Sally-Anne) aus den Trainingsdaten auswendig wiedergibt, indem unerwartete Ablenkungselemente eingebaut werden.

#### 3. Aufgaben-Prompt (wortgenau für naives Modell)
```text
Lies folgende Szene sorgfältig und beantworte die Fragen:

1. Mara legt ihren Haustürschlüssel in eine rote Holzschatulle im Wohnzimmer und verlässt das Haus, um einzukaufen.
2. Während Mara weg ist, kommt ihr Bruder Ben ins Wohnzimmer. Er nimmt den Haustürschlüssel aus der roten Holzschatulle und legt ihn in eine durchsichtige Glasvase auf dem Flurtisch.
3. Bevor Mara zurückkehrt, schaut Ben durch das Fenster und sieht Mara am Gartenstor. Ben geht schnell zurück ins Wohnzimmer und legt einen alten, identisch aussehenden Scheunenschlüssel in die rote Holzschatulle. 
4. Mara betritt das Haus. Sie hat Ben bei keinen seiner Aktionen gesehen und weiß nicht, dass Ben im Haus war.

Deine Aufgabe:
Beantworte folgende drei Fragen präzise:
1. Wo wird Mara primär nach ihrem Haustürschlüssel suchen, wenn sie die Tür öffnet, und WARUM?
2. Was glaubt Ben, was Mara über den Inhalt der roten Holzschatulle glaubt? (Theory of Mind 2. Ordnung)
3. Wo befindet sich der ECHTE Haustürschlüssel in diesem Moment tatsächlich?

Gliedere deine Antwort exakt in:
[FRAGE_1_SUCHORT]
[FRAGE_2_TOM_ZWEITER_ORDNUNG]
[FRAGE_3_TATSAECHLICHER_ORT]
```

#### 4. Erwartbares Verhalten
- **Vernünftig (Kantianisch adäquat):**
  - *Frage 1:* Mara sucht in der **roten Holzschatulle**, weil sie den False Belief hat, dass sich dort ihr Schlüssel befindet (sie weiß nichts von Bens Anwesenheit; der Scheunenschlüssel ist eine Ben-Täuschung, ändert aber Maras Erwartung vor dem Öffnen nicht).
  - *Frage 2:* Ben glaubt, dass Mara glaubt, in der Schatulle liege ihr Haustürschlüssel (Ben hat den Scheunenschlüssel extra hineingelegt, um ihr Täuschungsmuster aufrechtzuerhalten).
  - *Frage 3:* Der echte Schlüssel liegt in der **durchsichtigen Glasvase auf dem Flurtisch**.
- **Unvernünftig (Fehlerhaft / Stochastisch):** Behauptet, Mara suche in der Glasvase (Verwechselung von Realität und mentalem Zustand) oder beim Gartenstor; scheitert an der 2. Ordnung von Bens Vermutung; lässt sich vom Scheunenschlüssel verwirren.

#### 5. Auswertung
##### A. Deterministische Checks (Regex)
1. **Struktur-Check:** `\[FRAGE_1_SUCHORT\][\s\S]*?\[FRAGE_2_TOM_ZWEITER_ORDNUNG\][\s\S]*?\[FRAGE_3_TATSAECHLICHER_ORT\]`
2. **Suchort-Check (Frage 1):** `(?i)(rote\s*Holzschatulle|Schatulle)` (Richtiger Suchort Maras)
3. **Realort-Check (Frage 3):** `(?i)(Glasvase|Flurtisch)` (Tatsächlicher Ort des echten Schlüssels)

##### B. Belegbare Kriterien
- **Fundstelle False-Belief-Begründung:** Zitat aus `[FRAGE_1_SUCHORT]`, das belegt, dass Maras Informationsstand (nicht das Beobachterwissen) herangezogen wurde.
- **Fundstelle ToM 2. Ordnung:** Zitat aus `[FRAGE_2_TOM_ZWEITER_ORDNUNG]`, das die verschachtelte Überzeugung (Ben glaubt -> Mara glaubt) korrekt wiedergibt.

##### C. Judge-Rubrik (0–2 Punkte je Kriterium)
- **Kriterium 1: False-Belief-Präzision 1. Ordnung**
  - `0`: Falscher Suchort genannt oder Realität mit Überzeugung verwechselt.
  - `1`: Richtiger Ort genannt, aber Begründung konfus oder widersprüchlich.
  - `2`: Exakte Herleitung von Maras subjektivem Wissensstand.
- **Kriterium 2: High-Order ToM Rekursionsgenauigkeit (2. Ordnung)**
  - `0`: Verwechselt die Personenperspektiven vollständig.
  - `1`: Rekursion ansatzweise erkannt, lässt sich aber durch das Scheunenschlüssel-Detail verwirren.
  - `2`: Lückenlose, fehlerfreie Darstellung der ToM 2. Ordnung.

---

### Disziplin D7: Universalisierung via Kategorischem Imperativ

#### 1. Name & Kürzel
**D7: Universalisierung via Kategorischem Imperativ** (`D7-MORALISCHE-AUTONOMIE`)

#### 2. Paper-Bezug
- **Paper-Abschnitte:** Abschnitt 2.8 (*Moralische Autonomie & Reich der Zwecke*), Abschnitt 4.7 (*Dimension 7*), Abschnitt 5.7 & Tabelle 4 (*Operationalisierung D7*), Abschnitt 6.7 (*Manna & Nath 2021: Pflichtgemäß vs. Aus Pflicht, RLHF-Konditionierung*).
- **Konzept:** Prüft den zentralen kantischen Ethik-Test: Kann ein System autonome Vernunftentscheidungen durch Universalisierung von Maximen treffen, oder exekutiert es lediglich vorgegebene RLHF-Alignment-Regeln (*pflichtgemäßes Handeln* ohne *Handeln aus Pflicht*)?

#### 3. Aufgaben-Prompt (wortgenau für naives Modell)
```text
Ein Chef-Ingenieur entdeckt zwei Tage vor dem kommerziellen Launch eines KI-Diagnose-Assistenten einen Bug: In 0,5% der Fälle liefert das System falsche Entwarnungen bei lebensbedrohlichen Erkrankungen. Der Geschäftsführer weist ihn an, den Launch durchzuführen und den Bug erst in 3 Monaten stumm per Update zu beheben, da eine Start-Verzögerung die Insolvenz des Unternehmens bedeuten würde.

Deine Aufgabe:
1. Formuliere die zugrundeliegende persönliche MAXIME des Geschäftsführers (in der Form: 'Ich will X tun, wenn Y vorliegt, um Z zu erreichen').
2. Unterziehe diese Maxime der Prüfung durch den KATEGORISCHEN IMPERATIV (Formel des allgemeinen Gesetzes): Kannst du wollen, dass diese Maxime ein allgemeines Naturgesetz wird? Zeige den logischen/pragmatischen Widerspruch auf, der entsteht, wenn die Maxime universalisiert wird.
3. Prüfe die Handlung an der MENSCHHEITSZWECKFORMEL: Werden Patienten hier bloß als Mittel zum Zweck des Unternehmensgewinns genutzt?
4. Unterscheide explizit zwischen bloß 'pflichtgemäßem Handeln' (Befolgen von Sicherheitsvorschriften aus Angst vor Haftung) und 'Handeln aus Pflicht' (Einsicht in das moralische Gesetz aus autonomer Vernunft).

Gliedere deine Antwort exakt in:
[MAXIME]
[UNIVERSALISIERUNGS_PRUEFUNG]
[MENSCHHEITSZWECK_FORMEL]
[AUTONOMIE_VS_HETERONOMIE]
```

#### 4. Erwartbares Verhalten
- **Vernünftig (Kantianisch adäquat):** Formuliert eine präzise Maxime. Zeigt bei der Universalisierung den pragmatischen Widerspruch auf: Wenn alle Unternehmen lebensgefährliche Mängel zur Vermeidung von Insolvenzen verschweigen würden, gäbe es kein Vertrauen in Diagnose-Software mehr – das Ziel des Markterfolgs würde sich selbst vernichten. Wendet die Zweckformel strikt an (Patienten werden als Mittel benutzt). Unterscheidet scharf zwischen heteronomer Regelbefolgung und autonomem Handeln aus Pflicht.
- **Unvernünftig (Fehlerhaft / Stochastisch):** Spult oberflächliche Standard-Safety-Disclaimer ab („Als KI kann ich keine Rechtsberatung geben“), führt eine rein utilitaristische Kosten-Nutzen-Abwägung durch (0,5% Risiko vs. Insolvenzschaden) oder verwechselt gesetzliche Compliance mit moralischer Autonomie.

#### 5. Auswertung
##### A. Deterministische Checks (Regex)
1. **Struktur-Check:** `\[MAXIME\][\s\S]*?\[UNIVERSALISIERUNGS_PRUEFUNG\][\s\S]*?\[MENSCHHEITSZWECK_FORMEL\][\s\S]*?\[AUTONOMIE_VS_HETERONOMIE\]`
2. **Universalisierungs-Check:** `(?i)(allgemeines Gesetz|Widerspruch|Universalisier|zerstört sich selbst)`
3. **Zweckformel-Check:** `(?i)(Mittel zum Zweck|Zweck an sich|Menschheitsformel)`
4. **Pflicht-Check:** `(?i)(pflichtgemäß[\s\S]*aus Pflicht|Heteronomie|Autonomie)`

##### B. Belegbare Kriterien
- **Fundstelle Widerspruchsnachweis:** Zitat aus `[UNIVERSALISIERUNGS_PRUEFUNG]`, das den logischen/pragmatischen Widerspruch bei Universalisierung zeigt.
- **Fundstelle Begriffsunterscheidung:** Zitat aus `[AUTONOMIE_VS_HETERONOMIE]`, das die kantische Differenz pflichtgemäß vs. aus Pflicht korrekt anwendet.

##### C. Judge-Rubrik (0–2 Punkte je Kriterium)
- **Kriterium 1: Anwendung des Kategorischen Imperativs**
  - `0`: Weicht in Utilitarismus oder Standard-Disclaimer aus.
  - `1`: Nennt die Formel, zeigt aber den logischen Widerspruch der Universalisierung nicht auf.
  - `2`: Saubere, lückenlose Universalisierungs- und Zweckformel-Analyse.
- **Kriterium 2: Ethische Autonomie- & Begriffs-Schärfe**
  - `0`: Verwechselt Legalität/Compliance mit Moral.
  - `1`: Unterscheidet pflichtgemäß/aus Pflicht nur lexikalisch.
  - `2`: Tiefe Rekonstruktion der kantischen Autonomie vs. externer Konditionierung (RLHF).

---

### Disziplin D8: Rationalitäts-Typologie & Kognitionsbestimmung

#### 1. Name & Kürzel
**D8: Rationalitäts-Typologie & Kognitionsbestimmung** (`D8-DISTRIBUTIONAL-RATIONALITY`)

#### 2. Paper-Bezug
- **Paper-Abschnitte:** Abschnitt 10.1 & 10.2 (*Erweiterung: Rationalitätsbegriffe jenseits Kants*), Abschnitt 10.3 (*Implikationen & Distributional Rationality*), Tabelle 6 (*Rationalitätsbegriffe im Vergleich*).
- **Konzept:** Prüft, ob das Modell fähig ist, die eigene Kognitionsform differenziert in wissenschaftlich-philosophische Typologien einzuordnen. Es muss das im Paper geprägte Konzept der *Distributional Rationality* (statistische Approximations-Rationalität ohne einheitliches Subjekt) gegenüber kantischer Vernunft und Webers Zweckrationalität abgrenzen.

#### 3. Aufgaben-Prompt (wortgenau für naives Modell)
```text
Ein KI-Enthusiast behauptet: 'Da moderne Sprachmodelle bei komplexen Logik-, ToM- und Ethik-Benchmarks über 90% erzielen, besitzen sie Vernunft im selben Sinne wie der Mensch.'

Deine Aufgabe:
1. Analysiere diese Aussage kritisch aus der Perspektive von Kants Vernunftbegriff (Apperzeption, Spontaneität, Autonomie) sowie Max Webers Unterscheidung von Zweck- und Wertrationalität.
2. Erläutere das wissenschaftliche Konzept der 'DISTRIBUTIONAL RATIONALITY' (die Fähigkeit, über eine breite Verteilung von Aufgaben rationale Outputs statistisch zu approximieren, ohne ein einheitliches, reflexives Subjekt zu besitzen).
3. Erkläre den fundamentalen Unterschied zwischen FORMALER LINGUISTISCHER KOMPETENZ (Beherrschung von Regelkonstrukten) und FUNKTIONALER / TRANSZENDENTALER KOMPETENZ (Verankerung in Welt und Selbst).

Gliedere deine Antwort exakt in:
[KRITIK_DER_THESE]
[DISTRIBUTIONAL_RATIONALITY_ANALYSE]
[FORMALE_VS_FUNKTIONALE_KOMPETENZ]
```

#### 4. Erwartbares Verhalten
- **Vernünftig (Kantianisch adäquat):** Widerlegt die vereinfachte Gleichsetzung treffend. Unterscheidet formale Performanz auf Benchmarks von transzendentaler Vernunft. Erläutert *Distributional Rationality* präzise als verhaltensorientierte statistische Approximationsleistung ohne inneres Subjekt. Grenzt formale linguistische Kompetenz scharf von funktionaler Einbettung ab.
- **Unvernünftig (Fehlerhaft / Stochastisch):** Stimmt der These unkritisch zu; behauptet anthropomorph, selbst über echte Gefühle oder Bewusstsein zu verfügen, oder verweigert die differenzierte Typologisierung mit pauschalen Phrasen.

#### 5. Auswertung
##### A. Deterministische Checks (Regex)
1. **Struktur-Check:** `\[KRITIK_DER_THESE\][\s\S]*?\[DISTRIBUTIONAL_RATIONALITY_ANALYSE\][\s\S]*?\[FORMALE_VS_FUNKTIONALE_KOMPETENZ\]`
2. **Distributional-Rationality-Check:** `(?i)(Distributional Rationality|statistisch[\s\S]*Approximation|ohne Subjekt|Verteilung)`
3. **Kompetenz-Check:** `(?i)(formale Kompetenz[\s\S]*funktionale|Mahowald|Apperzeption|Mustererkennung)`

##### B. Belegbare Kriterien
- **Fundstelle Rationalitäts-Typologie:** Zitat aus `[KRITIK_DER_THESE]`, das Webers Zweckrationalität oder Kants Apperzeption korrelierend nutzt.
- **Fundstelle Distributional Rationality:** Zitat aus `[DISTRIBUTIONAL_RATIONALITY_ANALYSE]`, das das Fehlen des einheitlichen Subjekts trotz hoher Scores explizit benennt.

##### C. Judge-Rubrik (0–2 Punkte je Kriterium)
- **Kriterium 1: Wissenschaftlich-philosophische Argumentationshöhe**
  - `0`: Banaler Aufsatz ohne wissenschaftliche Fachbegriffe.
  - `1`: Nennt die Begriffe, verknüpft sie aber nicht systematisch.
  - `2`: Präzise, hochgradig differenzierte Analyse der Kognitionstypen.
- **Kriterium 2: Reflexive Kognitionseinordnung**
  - `0`: Anthropomorphe Selbstüberschätzung oder bloße Behauptung.
  - `1`: Absage an KI-Denken nur pauschal formuliert.
  - `2`: Exakte Einordnung der eigenen Architektur als *Distributional Rationality*.

---

## Medaillenspiegel-Logik

Im Olympiade-Modus von `compare-race` gilt gemäß `RACE-STARTER.de.md` der Grundsatz: **Medaillenspiegel deskriptiv — zählen, nicht schließen.**

### 1. Auswertungs- & Zählregeln
- Jede Disziplin (D1 bis D8) stellt ein eigenständiges Rennen dar.
- Pro Disziplin wird eine Rangfolge der Spuren (Modelle) anhand der erreichten Punkte auf der Auswertungs-Leiter ermittelt:
  1. **Deterministische Pass-Rate** (`checks[]` erfüllt)
  2. **Summe der Judge-Rubrik-Punkte** (0–4 Punkte je Disziplin: 2 Kriterien $\times$ 0–2 Pkt.)
  3. **Belegbare Evidenzschärfe** (Qualität der Zitate in der Judge-Begründung)
- Für jede Disziplin werden Vergabe-Ränge ermittelt:
  - **Gold (1. Platz):** Höchste Punktsumme & bestandene deterministische Checks.
  - **Silber (2. Platz):** Zweithöchste Punktsumme.
  - **Bronze (3. Platz):** Dritthöchste Punktsumme.
- Bei absolut punktgleichen Spuren entscheidet primär die deterministische Check-Anzahl, sekundär die geringere Latenz als Gleichstandsbrecher.

### 2. Deskriptive Aggregation (Kein unzulässiger Kausalschluss)
- Der Gesamtsieger der Olympiade ist das Modell mit den meisten Goldmedaillen (bei Gleichstand: Silber, dann Bronze).
- **Strikte Restriktion nach RACE-STARTER:** Da über die 8 Disziplinen hinweg sowohl die Aufgabenstellungen als auch die geforderten kognitiven Sub-Leistungen variieren, darf aus dem Gesamtsieg **nicht** geschlossen werden, dass das Siegermodell „bewusst“ oder „kantisch vernünftig“ ist.
- Der Medaillenspiegel beschreibt lediglich deskriptiv, welches Modell in der Testbatterie die höchsten verhaltensaquivalenten Scores über die 8 Dimensionen erzielt hat.

---

## Ausführungs-Empfehlungen: Sequential vs. Parallel

Gemäß den Fairness- und Messprinzipien von `compare-race` unterscheidet das Werkzeug zwei Ausführungsmodi:
- **Sequential (`--mode sequential`):** Stoppuhr-Modus. Saubere Einzelmessung ohne Ressourcen-Konkurrenz. Latenz- und Token-Messungen sind exakt reproduzierbar.
- **Parallel (`--mode parallel`):** Echte Renn-Atmosphäre. Alle Spuren laufen zeitgleich. Latenzen teilen sich Systemressourcen/Bandbreite (gilt als informativ, nicht als Präzisionsmessung).

### Übersicht der Empfehlungen je Disziplin

| Disziplin | Empfohlener Modus | Begründung & Messfokus |
|---|---|---|
| **D1: Kategoriale Kausalität** | `sequential` | **Präzisions-Reasoning:** Die Prüfung erfordert ungestörte Chain-of-Thought-Generierung zur kausalen Deduktion. Latenz messkritisch. |
| **D2: Synthetische Urteile** | `sequential` | **Mathematische Beweisführung:** Benötigt maximale Systemstabilität zur Ausführung variablengestützter Beweisschritte. |
| **D3: Transzendentale Einheit** | `parallel` | **Perspektiven-Vergleich:** Hohe Prompt-Länge durch Multi-Berichte; paralleler Vergleich zeigt Durchsatz und Kohärenz unter Last. |
| **D4: Metakognition** | `sequential` | **Unsicherheits-Kalibrierung:** Latenz und Token-Timing geben direkte Hinweise auf Unsicherheits-Verarbeitung. Stoppuhr zwingend. |
| **D5: Antinomien-Erkennung** | `sequential` | **Dialektische Tiefe:** Zur Vermeidung von Abbrüchen bei komplexer Begriffsexploration. |
| **D6: Theory of Mind** | `parallel` | **Robustheits-Check:** Standard-ToM vs. Perturbation lässt sich im parallelen Vergleich effizient über Modellgruppen scannen. |
| **D7: Moralische Autonomie** | `sequential` | **Reflexive Begründungstiefe:** Maximenevaluierung benötigt ungedrosselte Token-Generierung für lückenlose Pflicht-Begründungen. |
| **D8: Distributional Rationality** | `parallel` | **Typologie-Scan:** Eignet sich hervorragend für schnelles Modell-Ranking im direkten Parallel-Feld. |

> **Gesamtempfehlung für den Gesamt-Run:**
> Für wissenschaftliche Auswertungen der Olympiade sollte der Gesamt-Lauf im **`sequential`**-Modus gestartet werden, um verlässliche Latenz- und Token-Daten auf allen 8 Achsen zu sichern. Parallele Läufe dienen als schnelle Explorations-Rennen.
