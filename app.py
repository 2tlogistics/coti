import streamlit as st
from fpdf import FPDF
import json
from datetime import datetime


# Sample product prices in JSON format
product_prices = json.dumps({
    "EN 590 - MT": 590.0,
    "JET A1 - BBL": 99.0,
    "UREA46 - MT": 20.0
})

# Load product prices
prices = json.loads(product_prices)

# Initialize session state for items
if 'items' not in st.session_state:
    st.session_state['items'] = []  # Ensure this is a list

# Function to generate PDF
class PDF(FPDF):
    def header(self):
        # Insert logo
        self.image('logo.png', 10, 8, 33)
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'SOFT CORPORATE OFFER',0, 1, 'C')
        self.cell(0, 10, txt=f"SCO Nro. 2025-{datetime.now().strftime('%Y%m%d%H%M%S')}",ln=True, align="R")
        if self.page_no() > 1:
            self.ln(20)  # Add 5 lines of space for pages after the first one

    def footer(self):
        # Go to 1.5 cm from bottom
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        # Contact information
        self.set_y(-10)
        self.cell(0, 10, '440 Cobia St, Houston, Texas | jtoledo@2tlogistics.us | https://2tlogistics.us', 0, 0, 'C')

def generate_pdf(contact_name, email, company_name, items, incoterm, delivery_to):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    # Add date and time aligned to the right with the same font size
    pdf.cell(0, 5, txt=f"Quotation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='R')

    # Add additional information below the date
    pdf.set_font("Arial", 'B', size=10)
    pdf.cell(0, 5, txt="2T INVESTMENTS HOLDING GROUP", ln=True, align='R')
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 5, txt="440 Cobia St. Houston, Texas,USA.", ln=True, align='R')
    #pdf.cell(0, 5, txt="3383, Javier Prado Avenue,", ln=True, align='R')
    #pdf.cell(0, 5, txt="San Borja District,", ln=True, align='R')
    #pdf.cell(0, 5, txt="Lima, Peru", ln=True, align='R')
    pdf.cell(0, 5, txt="Intl.Phone: +58-412-927-2908", ln=True, align='R')
    pdf.cell(0, 5, txt="E-mail: jtoledo@2tlogistics.us", ln=True, align='R')
    pdf.cell(0, 5, txt="URL: https://2tlogistics.us", ln=True, align='R')

    # Add contact details with line spacing of 1
    pdf.ln(15)  # Add three lines of space
    pdf.cell(200, 5, txt=f"Contact Name: {contact_name}", ln=True)
    pdf.cell(200, 5, txt=f"Email: {email}", ln=True)
    pdf.cell(200, 5, txt=f"Company Name: {company_name}", ln=True)

    pdf.ln(10)  # Add two lines of space

    # Read content from cuerpo.txt
    with open('cuerpo.txt', 'r', encoding='utf-8') as file:
        cuerpo_content = file.read()

    # Add content from cuerpo.txt
    pdf.multi_cell(0, 5, cuerpo_content.encode('latin-1', 'replace').decode('latin-1'))

    pdf.ln(10)  # Add two lines of space

    # Add items in a table
    pdf.cell(200, 5, txt="Items:", ln=True)
    pdf.cell(50, 5, txt="Product", border=1)
    pdf.cell(50, 5, txt="Quantity", border=1)
    pdf.cell(50, 5, txt="Total", border=1, ln=True)
    total_amount = 0
    for item in items:
        product, quantity = item
        price = prices[product]
        total = price * quantity
        total_amount += total
        pdf.cell(50, 5, txt=product.encode('latin-1', 'replace').decode('latin-1'), border=1)
        pdf.cell(50, 5, txt=str(quantity), border=1)
        pdf.cell(50, 5, txt=f"${total:.2f}", border=1, ln=True)

    pdf.cell(50, 5, txt="", border=0)
    pdf.cell(50, 5, txt="Total Amount", border=1)
    pdf.set_font("Arial", 'B', size=10)
    pdf.cell(50, 5, txt=f"${total_amount:.2f}", border=1, ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.ln(10)
    # Add total amount in text
    pdf.cell(200, 5, txt=f"TOTAL AMOUNT*: US${total_amount:.2f}", ln=True)

    # Add Incoterm and Delivery To information
    pdf.cell(200, 5, txt=f"INCOTERM: {incoterm}", ln=True)
    pdf.cell(200, 5, txt=f"DELIVERY TO: {delivery_to}", ln=True)
    # Add additional lines
    pdf.cell(200, 5, txt="ORIGIN: Non-Sanctioned Country.", ln=True)
    pdf.cell(200, 5, txt="QUALITY: Export quality.", ln=True)
    pdf.cell(200, 5, txt="CONTRACT: 12 MONTHS", ln=True)
    pdf.cell(200, 5, txt="CURRENCY: USD ($)", ln=True)
    pdf.cell(200, 5, txt="INSPECTIONS: SGS, Intertek, Veritas or Equivalent", ln=True)
    pdf.cell(200, 5, txt="PAYMENT PROCEDURES: SEE PROCEDURE.", ln=True)
    pdf.cell(200, 5, txt="OFFER VALID FOR: 07 DAYS.", ln=True)
    pdf.set_font("Arial", size=5)
    pdf.cell(200, 5, txt="*PRICES SUBJECT TO VARIATIONS IN THE FUEL MARKET.", ln=True)
    pdf.set_font("Arial", size=10)

    # Add signature image and details
    pdf.image('signature.png', x=10, y=pdf.get_y() + 5, w=40)  # Adjust the position and size as needed
    pdf.ln(20)  # Add space for the signature image
    pdf.cell(200, 5, txt="Jorge Toledo", ln=True)
    pdf.cell(200, 5, txt="CEO", ln=True)
    pdf.cell(200, 5, txt="2Tlogistics", ln=True)
    pdf.image('seal.png', x=40, y=pdf.get_y() - 21, w=30)
    pdf.ln(20)

    # Read content from the appropriate file based on the selected Incoterm
    if incoterm == "CIF":
        with open('cif.txt', 'r', encoding='utf-8') as file:
            incoterm_content = file.read()
    else:
        with open('fob.txt', 'r', encoding='utf-8') as file:
            incoterm_content = file.read()

    # Add Incoterm content
    pdf.multi_cell(0, 5, incoterm_content.encode('latin-1', 'replace').decode('latin-1'))

    # Save PDF to a file

    now = datetime.now()
    pdf_file_name = f"COT-{company_name}{now.strftime('%Y%m%d%H%M')}.pdf"
    pdf.output(pdf_file_name, 'F')
    return pdf_file_name
    # pdf_file_name = "quotation.pdf"
    # pdf.output(pdf_file_name, 'F')
    # return pdf_file_name

# Streamlit UI
st.title("Quotation Generator")

# Input contact details
contact_name = st.text_input("Contact Name")
email = st.text_input("Email")
company_name = st.text_input("Company Name")

# Input product and quantity
product = st.selectbox("Select Product", list(prices.keys()))
quantity = st.number_input("Quantity", min_value=1, value=1)

if st.button("Add Item"):
    # Ensure that 'items' is a list before appending
    if isinstance(st.session_state['items'], list):
        st.session_state['items'].append((product, quantity))  # Append item to the list
        st.success(f"Added {quantity} of {product}")
    else:
        st.error("Error: Items is not a list.")

# Display added items
if st.session_state['items']:  # Check if items is a list and not empty
    st.write("Items Added:")
    for item in st.session_state['items']:
        st.write(f"{item[0]} (x{item[1]})")

# Input Incoterm and Delivery To information
incoterm = st.radio("Select Incoterm", ("CIF", "FOB"))
delivery_to = st.text_input("Delivery To")

# Button to generate and download the quotation
if st.button("Generate Quotation"):
    pdf_file = generate_pdf(contact_name, email, company_name, st.session_state['items'], incoterm, delivery_to)
    with open(pdf_file, "rb") as f:
        st.download_button("Download Quotation", f, file_name=pdf_file)
