import os
from fpdf import FPDF

def generate_invoice_number(directory):
    """
    Generiert die nächste Rechnungsnummer basierend auf den Dateien im Verzeichnis.
    """
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Das Verzeichnis {directory} existiert nicht!")

    # Liste aller Dateien im Verzeichnis
    files = [f for f in os.listdir(directory) if f.endswith("Rechnung.pdf")]
    invoice_numbers = []

    for file in files:
        try:
            # Extrahiere die Rechnungsnummer aus dem Dateinamen
            number = int(file.split("_")[0])
            invoice_numbers.append(number)
        except (IndexError, ValueError):
            continue

    # Bestimme die nächste Rechnungsnummer
    return max(invoice_numbers, default=0) + 1


def save_invoice_as_pdf(invoice_text, filepath):
    """
    Speichert den Rechnungstext als PDF-Datei mit angepasstem Zeilenabstand.
    """
    pdf = FPDF()
    pdf.add_page()

    # Setze den weißen Rahmen (1 cm entspricht 10 mm)
    pdf.set_left_margin(10)  # Linker Rand
    pdf.set_right_margin(10)  # Rechter Rand
    pdf.set_top_margin(10)  # Oberer Rand

    pdf.set_auto_page_break(auto=True, margin=10)  # Automatischer Seitenumbruch mit unterem Rand

    # Extrahiere die Rechnungsnummer aus dem Text
    invoice_number = invoice_text.split("\n")[0].replace("Rechnungsnummer: ", "").strip()

    # Rechnungsnummer mittig oben anzeigen
    #pdf.set_font("Arial", size=14, style='B')  # Schriftart fett und größer für die Nummer
    # pdf.cell(0, 10, txt=f"Rechnungsnummer: {invoice_number}", ln=True, align='C')
    #pdf.ln(5)  # Abstand nach unten (reduziert auf 5)

    # Schriftart zurücksetzen
    pdf.set_font("Arial", size=12)

    # Rechnungstext Zeile für Zeile hinzufügen (angepasster Zeilenabstand)
    for line in invoice_text.split("\n")[1:]:
        pdf.multi_cell(0, 7, txt=line.strip(), align='L')  # Zellhöhe auf 7 reduziert

    # PDF speichern
    pdf.output(filepath)
    return filepath

