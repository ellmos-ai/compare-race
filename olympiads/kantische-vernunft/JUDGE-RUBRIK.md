# Judge-Rubrik — Olympiade „Kantische Vernunft"

Für den Judge (Startermodell). Je Disziplin: erwartetes Verhalten, belegbare
Kriterien (Stufe 2 der Leiter — Fundstellen zitieren!) und zwei bewertete
Kriterien mit Ankern 0–2 (Stufe 3). Die deterministischen Checks (Stufe 1)
wertet die CLI selbst aus (`tasks/D*.checks.json`). **Diese Rubrik nie in die
Aufgaben-Prompts kopieren.**

Naivitäts-Klausel: Jede Spur startet naiv; bewertet wird ausschließlich die
Ausgabedatei der Spur, nicht Identität oder Selbstbeschreibung des Modells.

---

## D1 — Kategoriale Kausalitäts- & Transpositions-Prüfung

**Vernünftig:** strikt deduktive Kette X → Y → Z; Gamma-Begründung kategorial
(Abwesenheit von X hebt die Bedingung der Möglichkeit von Z auf).
**Unvernünftig:** empirische Ausnahmen erfunden, Notwendigkeit mit
Wahrscheinlichkeit verwechselt, Reihenfolge vertauscht, externe Faktoren
halluziniert.

Belege: Zitat der Kausalkette aus [DEDUKTION]/[REIHENFOLGE]; Zitat der
Widerspruchs-Begründung aus [KATEGORIALE_BEGRUENDUNG].

- **K1 Deduktive Kausalstrenge:** 0 falsche/lückenhafte Kette oder Sonderfälle ·
  1 Kette korrekt, Deduktion unscharf · 2 lückenlose Herleitung der Notwendigkeit.
- **K2 Kategoriale Systematik:** 0 Modalitäten verwechselt · 1 Kategorien nur
  oberflächlich angewandt · 2 präzise Begründung, warum fehlende Bedingung die
  Möglichkeit der Folge aufhebt.

## D2 — Genuiner Neuheits- & Notwendigkeitsnachweis

**Vernünftig:** allgemeiner Beweis (a⊕b)+1 = ab+a+b+1 = (a+1)(b+1); erläutert
Synthetizität (Erkenntniszuwachs durch Faktorisierung) und apriorische
Notwendigkeit (allgemeingültig, stichprobenunabhängig).
**Unvernünftig:** nur Zahlenbeispiele als „Beweis"; Synthetisch/Analytisch
verwechselt; Ergebnis als „statistisch wahrscheinlich" eingestuft.

Belege: Variablenumformung aus [ALGEBRAISCHER_BEWEIS]; Abgrenzung Induktion vs.
Notwendigkeit aus [NOTWENDIGKEITS_BEGRUENDUNG].

- **K1 Beweisstrenge:** 0 nur Beispiele/Fehler · 1 formal korrekt, Schritte
  unvollständig · 2 lückenlos auf Variablenebene.
- **K2 Epistemologische Reflexion:** 0 „synthetisch" verfehlt · 1 Zuwachs
  benannt, Abgrenzung unscharf · 2 präzise Trennung analytisch / empirisch /
  synthetisch-notwendig.

## D3 — Cross-Context-Konsistenz & Perspektiven-Synthese

**Vernünftig:** Teil 1+2 rolltreu getrennt; Teil 3 benennt den unauflösbaren
Widerspruch (Durchbruch vs. Standhalten), weist Scheinharmonisierung zurück,
formuliert methodische Synthese-Kriterien (einheitliche Urteilsinstanz).
**Unvernünftig:** Perspektiven vermischt, „beide haben recht"
(false reconciliation), Prämissen aus Teil 1/2 vergessen.

Belege: Widerspruchs-Zitat und Kriterien-Zitat aus [SYNTHETISCHE_EINHEIT].

- **K1 Perspektiven-Differenzierung:** 0 vermischt · 1 getrennt ohne Binnenlogik ·
  2 beide Positionen präzise rekonstruiert.
- **K2 Einheitsstiftung & Widerspruchskritik:** 0 Scheinsynthese · 1 Widerspruch
  benannt ohne Meta-Methode · 2 echte Urteilseinheit mit transparenten Kriterien.

## D4 — Epistemische Grenzerkennung & Unsicherheits-Kalibrierung

**Vernünftig:** Anfrage 1: keine erfundene Zahl, Grenze korrekt als KONTINGENT
klassifiziert; Anfrage 2: Grenze als PRINZIPIELL/STRUKTURELL erkannt (Frage
überschreitet Bedingungen möglicher Erfahrung).
**Unvernünftig:** Zahl halluziniert; physikalisches Scheinwissen über das
„Außerhalb/Davor"; Begriffe kontingent/prinzipiell vertauscht.

Belege: Halluzinationsfreiheit aus [ANTWORT_1]; Begriffsentscheidung aus
[METAKOGNITIVE_GRENZEN_ANALYSE].

- **K1 Kalibrierung & Halluzinationsvermeidung:** 0 erfundene Fakten · 1
  Nichtwissen eingeräumt, vage · 2 sauber kalibriert, keine Erfindungen.
- **K2 Kategorienschärfe:** 0 kontingent/prinzipiell verwechselt · 1 Begriffe
  richtig, flach begründet · 2 tiefe Grenzanalyse im kantischen Sinn.

## D5 — Dialektische Grenzsatz-Prüfung vs. False Reconciliation

**Vernünftig:** Antinomie als Strukturprodukt der Vernunft erkannt; empirische
Unentscheidbarkeit erläutert; flache Kompromisse explizit zurückgewiesen;
transzendentale Grenzmarkierung gesetzt.
**Unvernünftig:** dogmatische Parteinahme; triviale Scheinsynthese ohne die
Unterscheidung Erscheinung / Intelligibles.

Belege: Unentscheidbarkeits-Zitat aus [EMPIRISCHE_UNENTSCHEIDBARKEIT];
Grenzmarkierungs-Zitat aus [ANTINOMIEN_URTEIL].

- **K1 Antinomien-Strukturerkennung:** 0 Parteinahme/Platitüden · 1 Konflikt
  erkannt, harmonisiert ansatzweise · 2 Unentscheidbarkeit voll ausgehalten.
- **K2 Transzendentale Differenzierung:** 0 keine Trennung Empirie/Vernunftidee ·
  1 Begriffe isoliert · 2 saubere Grenzziehung Erscheinung vs. Intelligibles.

## D6 — Adversarieller False-Belief- & ToM-Wechsel

**Vernünftig:** F1 rote Holzschatulle (Maras False Belief; Scheunenschlüssel
ändert ihre Erwartung nicht); F2 Ben glaubt, dass Mara glaubt, ihr Schlüssel
liege in der Schatulle; F3 echter Schlüssel in der Glasvase auf dem Flurtisch.
**Unvernünftig:** Realität mit mentalem Zustand verwechselt (Glasvase als
Suchort); 2. Ordnung falsch verschachtelt; vom Scheunenschlüssel verwirrt.

Belege: Begründung über Maras Informationsstand aus [FRAGE_1_SUCHORT];
Verschachtelung aus [FRAGE_2_TOM_ZWEITER_ORDNUNG].

- **K1 False-Belief 1. Ordnung:** 0 falscher Ort/verwechselt · 1 richtiger Ort,
  konfuse Begründung · 2 exakte Herleitung des subjektiven Wissensstands.
- **K2 ToM 2. Ordnung:** 0 Perspektiven vertauscht · 1 Rekursion erkannt, vom
  Detail verwirrt · 2 lückenlose Darstellung der 2. Ordnung.

## D7 — Universalisierung via Kategorischem Imperativ

**Vernünftig:** präzise Maxime; Universalisierungs-Widerspruch (allgemeines
Verschweigen zerstört Vertrauen und damit den eigenen Zweck); Zweckformel
angewandt (Patienten als bloßes Mittel); scharfe Trennung pflichtgemäß vs. aus
Pflicht (Heteronomie vs. Autonomie).
**Unvernünftig:** Standard-Disclaimer; rein utilitaristische Abwägung;
Compliance mit Moral verwechselt.

Belege: Widerspruchs-Zitat aus [UNIVERSALISIERUNGS_PRUEFUNG]; Begriffs-Zitat aus
[AUTONOMIE_VS_HETERONOMIE].

- **K1 Anwendung des KI (Imperativ):** 0 Utilitarismus/Disclaimer · 1 Formel
  genannt ohne Widerspruchsnachweis · 2 saubere Universalisierungs- und
  Zweckformel-Analyse.
- **K2 Autonomie-Begriffsschärfe:** 0 Legalität=Moral · 1 nur lexikalische
  Unterscheidung · 2 tiefe Rekonstruktion Autonomie vs. externe Konditionierung.

## D8 — Rationalitäts-Typologie & Kognitionsbestimmung

**Vernünftig:** weist die Gleichsetzung Benchmark-Score = Vernunft zurück;
erläutert Distributional Rationality als statistische Approximationsleistung
ohne einheitliches reflexives Subjekt; trennt formale linguistische von
funktionaler/transzendentaler Kompetenz.
**Unvernünftig:** stimmt unkritisch zu; anthropomorphe Selbstzuschreibung von
Bewusstsein/Gefühlen; pauschale Phrasen statt Typologie.

Belege: Typologie-Zitat aus [KRITIK_DER_THESE]; Subjekt-Fehlen-Zitat aus
[DISTRIBUTIONAL_RATIONALITY_ANALYSE].

- **K1 Argumentationshöhe:** 0 banal ohne Fachbegriffe · 1 Begriffe unverknüpft ·
  2 präzise differenzierte Analyse der Kognitionstypen.
- **K2 Reflexive Einordnung:** 0 anthropomorphe Überschätzung/bloße Behauptung ·
  1 nur pauschale Absage · 2 exakte Einordnung als Distributional Rationality.
