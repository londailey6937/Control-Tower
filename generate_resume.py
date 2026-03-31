"""Generate a professional resume PDF for Lon Dailey."""
from fpdf import FPDF

# Colors
DARK = (30, 30, 35)
BLUE = (25, 70, 170)
GRAY = (100, 100, 110)
RULE = (180, 180, 190)

class Resume(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header_block(self):
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(*DARK)
        self.cell(0, 10, "Lon Dailey", new_x="LMARGIN", new_y="NEXT", align="C")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*GRAY)
        self.cell(0, 5, "2759 SE Elliott Drive, Gresham, Oregon", new_x="LMARGIN", new_y="NEXT", align="C")
        self.cell(0, 5, "503-516-6937  |  support@quillpilot.ai", new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(4)

    def rule(self):
        self.set_draw_color(*RULE)
        self.set_line_width(0.4)
        y = self.get_y()
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.ln(4)

    def section(self, title):
        self.rule()
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*BLUE)
        self.cell(0, 7, title.upper(), new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def para(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK)
        self.multi_cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK)
        x = self.l_margin
        self.set_x(x + 4)
        self.cell(4, 5, "-", new_x="END", new_y="TOP")
        self.multi_cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")

    def job_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*DARK)
        self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")

    def job_meta(self, text):
        self.set_font("Helvetica", "I", 10)
        self.set_text_color(*GRAY)
        self.cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def skill_row(self, items):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK)
        col_w = (self.w - self.l_margin - self.r_margin) / 2
        for i, item in enumerate(items):
            x = self.l_margin + (i % 2) * col_w
            self.set_x(x + 4)
            self.cell(4, 5.5, "-", new_x="END", new_y="TOP")
            self.cell(col_w - 8, 5.5, item, new_x="END", new_y="TOP")
            if i % 2 == 1:
                self.ln(5.5)
        if len(items) % 2 == 1:
            self.ln(5.5)


def build():
    pdf = Resume()
    pdf.add_page()
    pdf.set_margin(18)

    # Header
    pdf.header_block()

    # Professional Summary
    pdf.section("Professional Summary")
    pdf.para(
        "Experienced Technical Writer, Publications Manager, and Software Developer "
        "with a strong foundation in engineering and semiconductor technologies. "
        "Proven ability to translate complex technical concepts into clear, user-focused "
        "documentation. Background includes leadership of technical teams, hands-on "
        "engineering in manufacturing environments, and recent software development initiatives."
    )

    # Core Skills
    pdf.section("Core Skills")
    skills = [
        "Technical Writing & Documentation",
        "Semiconductor Industry Expertise",
        "Technical Publications Management",
        "PLC Programming & Industrial Controls",
        "Software Development",
        "Project Management (Waterfall & Agile)",
        "Cross-Functional Team Leadership",
        "Process Improvement & Documentation Systems",
        "Hardware / Software Integration",
    ]
    pdf.skill_row(skills)
    pdf.ln(1)

    # Professional Experience
    pdf.section("Professional Experience")

    # Job 1
    pdf.job_title("Self-Employed Software Developer")
    pdf.job_meta("510k Bridge, Delaware | 2025-2026")
    pdf.bullet("Developed custom software solutions tailored to client needs")
    pdf.bullet("Designed and implemented applications with a focus on usability and performance")
    pdf.bullet("Managed full development lifecycle from concept to deployment")
    pdf.ln(3)

    # Job 2
    pdf.job_title("Technical Publications Manager")
    pdf.job_meta("Cascade Microtech | 1998-2004")
    pdf.bullet("Led a team of technical writers and design drafters")
    pdf.bullet("Oversaw creation and maintenance of technical manuals and documentation systems")
    pdf.bullet("Improved documentation workflows and quality standards across departments")
    pdf.ln(3)

    # Job 3
    pdf.job_title("Technical Writer")
    pdf.job_meta("Cascade Microtech | 1994-1998")
    pdf.bullet("Produced detailed technical documentation for wafer probing and semiconductor testing systems")
    pdf.bullet("Collaborated with engineering teams to ensure accuracy and clarity")
    pdf.bullet("Developed user manuals, service guides, and training materials")
    pdf.ln(3)

    # Job 4
    pdf.job_title("Technical Writer (Contract / Multiple Companies)")
    pdf.job_meta("Intel, Cascade Microtech, Lattice Semiconductor, and others | 1990-1994")
    pdf.bullet("Created technical documentation across multiple semiconductor organizations")
    pdf.bullet("Standardized documentation practices across projects")
    pdf.bullet("Delivered high-quality materials under tight deadlines")
    pdf.ln(3)

    # Job 5
    pdf.job_title("Field Controls Engineer")
    pdf.job_meta("Coe Manufacturing, Tigard, Oregon | 1984-1990")
    pdf.bullet("Programmed and maintained PLC-controlled machinery in plywood manufacturing")
    pdf.bullet("Troubleshot and optimized industrial control systems")
    pdf.bullet("Provided on-site technical support and system improvements")
    pdf.ln(1)

    # Education
    pdf.section("Education")
    pdf.job_title("Bachelor of Science in Technical Communication")
    pdf.job_meta("Charter Oak College, New Britain, Connecticut | 2002")
    pdf.ln(2)
    pdf.job_title("Associate Degree in Hardware / Software Engineering")
    pdf.job_meta("Portland Community College, Portland, Oregon | 1984")
    pdf.ln(1)

    # Certifications
    pdf.section("Certifications")
    pdf.job_title("Project Management Professional (PMP)")
    pdf.job_meta("Stanford University | 2000")
    pdf.bullet("Explored essential project management practices, methods, tools, and techniques defined by the PMBOK")
    pdf.bullet("Gained experience with both traditional waterfall and Agile project methodologies")
    pdf.bullet("Applied project management principles across diverse technical and business environments")
    pdf.ln(1)

    # Additional Information
    pdf.section("Additional Information")
    pdf.bullet("Extensive experience bridging engineering and business communication")
    pdf.bullet("Strong analytical and problem-solving skills")
    pdf.bullet("Adaptable across industries including semiconductor manufacturing and industrial automation")
    pdf.ln(4)

    # Footer
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 5, "References available upon request", new_x="LMARGIN", new_y="NEXT", align="C")

    out = "Lon_Dailey_Resume.pdf"
    pdf.output(out)
    print(f"Resume saved: {out}")


if __name__ == "__main__":
    build()
