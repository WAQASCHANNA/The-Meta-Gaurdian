from fpdf import FPDF
import json
import os
from datetime import datetime

LOG_FILE = "audit_log.json"

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'MetaGuardian Compliance Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

def generate_report():
    if not os.path.exists(LOG_FILE):
        return "No data found."

    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    # Summary Stats
    total = len(data)
    violations = sum(1 for d in data if not d["compliance_check"]["compliant"])
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Report Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1)
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Total Decisions Monitored: {total}', 0, 1)
    pdf.cell(0, 10, f'Total Violations Detected: {violations}', 0, 1)
    pdf.ln(10)

    # Violations List
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Detailed Violations:', 0, 1)
    pdf.set_font('Arial', '', 10)
    
    for item in data:
        if not item["compliance_check"]["compliant"]:
            decision = item["original_decision"]
            compliance = item["compliance_check"]
            
            pdf.multi_cell(0, 10, f"Time: {item['timestamp']}")
            pdf.multi_cell(0, 10, f"Agent: {decision['agent_name']}")
            pdf.multi_cell(0, 10, f"Violation: {compliance['violation_type']}")
            pdf.multi_cell(0, 10, f"Details: {compliance['message']}")
            pdf.ln(5)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)

    output_file = "compliance_report.pdf"
    pdf.output(output_file, 'F')
    return output_file

if __name__ == "__main__":
    print(generate_report())
