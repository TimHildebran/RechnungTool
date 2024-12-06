import streamlit as st
import os
from datetime import date
from utils import generate_invoice_number, save_invoice_as_pdf

# Setze den absoluten Pfad des Zielordners
INVOICE_DIRECTORY = "/Users/timhildebrand/TomCode"

# Titel der Anwendung
st.title("Rechnungstool für watches24.com")

# 1. Daten des Käufers abfragen
st.header("Kundendaten")
name = st.text_input("Name des Käufers?")
address = st.text_area("Adresse des Käufers?")
watch_model = st.text_input("Uhrenmodell?")
reference_number = st.text_input("Referenznummer der Uhr?")
serial_number = st.text_input("Seriennummer der Uhr?")
price = st.number_input("Kaufpreis der Uhr (nur die Zahl)?", min_value=0)

# Option für Versand
shipping = st.checkbox("Fällt Versand an?")
shipping_text = "zuzüglich Versand" if shipping else ""

# Zahlungsart auswählen
st.header("Zahlungsart")
payment_method = st.radio(
    "Wählen Sie eine Zahlungsart:",
    ["Überweisung", "Bar", "EC-Karte", "Kreditkarte", "Chrono24"]
)

# Zusätzliche Angaben für Zahlungsart
payment_details = ""
if payment_method == "Überweisung":
    payment_details = (
        "bitte an:\n"
        "Andreas Hildebrand | watches24.com\n"
        "IBAN: DE 18 7015 0000 0031 2111 47\n"
        "BIC: SSKMDEMMXXX"
    )
elif payment_method == "Chrono24":
    checkout_number = st.text_input("Bitte die Checkout-Nummer eingeben:")
    if checkout_number:
        payment_details = f"ist die Bezahlung erfolgt, die passende Checkoutnummer ist: {checkout_number}"

# 2. Rechnung erstellen
if st.button("Rechnung erstellen"):
    try:
        # Verzeichnis prüfen
        if not os.path.exists(INVOICE_DIRECTORY):
            os.makedirs(INVOICE_DIRECTORY)

        # Rechnungsnummer generieren
        invoice_number = generate_invoice_number(INVOICE_DIRECTORY)
        current_date = date.today().strftime("%d.%m.%Y")

        # Rechnungstext erstellen
        invoice_text = f"""
        Rechnungsnummer: {invoice_number}

        {name}
        {address}

        Mit diesem Schreiben erwirbt {name} von watches24.com vertreten durch
        Andreas Hildebrand, Ottostr. 5, 80333 München
        Tel 089/123 64 70 Mobil 0175/55 55 55 3

        Eine orig. Armbanduhr von {watch_model}.
        Die Referenznummer der Uhr ist {reference_number}.
        Die Seriennummer von der Uhr ist folgende {serial_number}.

        Andreas Hildebrand bestätigt hiermit uneingeschränkt die Originalität der hier verkauften {watch_model}.

        {name} bezahlt für die Uhr den Preis von {price} Euro {shipping_text}. Per {payment_method}
        {payment_details}.
        
        Die Uhr wird nach § 25 Umsatzsteuergesetz (Differenzbesteuerung Sonderregelung) verkauft.
        Die Mwst kann nicht ausgewiesen werden.

        Vielen Dank für Ihr Vertrauen.
        München, {current_date}
        Andreas Hildebrand


        P.S. Sind Sie mit meinem Service zufrieden? Bitte bewerten Sie mich auf Google+ oder auf Facebook.
        """

        # Dateiname mit Rechnungsnummer
        filename = f"{invoice_number}_Rechnung.pdf"
        pdf_path = save_invoice_as_pdf(invoice_text, f"{INVOICE_DIRECTORY}/{filename}")
        st.success(f"Rechnung wurde erfolgreich erstellt: {pdf_path}")

        # Download-Button für die Rechnung
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Rechnung herunterladen",
                data=pdf_file,
                file_name=filename,
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"Fehler bei der Rechnungserstellung: {e}")
