"""Generate a professional resume PDF for Lon Dailey in Chinese."""
from fpdf import FPDF

# Colors
DARK = (30, 30, 35)
BLUE = (25, 70, 170)
GRAY = (100, 100, 110)
RULE = (180, 180, 190)

FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"
FONT_NAME = "ARUNI"


class ResumeCN(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font(FONT_NAME, "", FONT_PATH)
        self.add_font(FONT_NAME, "B", FONT_PATH)
        self.add_font(FONT_NAME, "I", FONT_PATH)
        self.set_auto_page_break(auto=True, margin=20)

    def header_block(self):
        self.set_font(FONT_NAME, "B", 22)
        self.set_text_color(*DARK)
        self.cell(0, 10, "Lon Dailey", new_x="LMARGIN", new_y="NEXT", align="C")
        self.set_font(FONT_NAME, "", 10)
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
        self.set_font(FONT_NAME, "B", 13)
        self.set_text_color(*BLUE)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def para(self, text):
        self.set_font(FONT_NAME, "", 10)
        self.set_text_color(*DARK)
        self.multi_cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def bullet(self, text):
        self.set_font(FONT_NAME, "", 10)
        self.set_text_color(*DARK)
        x = self.l_margin
        self.set_x(x + 4)
        self.cell(4, 5, "-", new_x="END", new_y="TOP")
        self.multi_cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")

    def job_title(self, title):
        self.set_font(FONT_NAME, "B", 11)
        self.set_text_color(*DARK)
        self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")

    def job_meta(self, text):
        self.set_font(FONT_NAME, "I", 10)
        self.set_text_color(*GRAY)
        self.cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def skill_row(self, items):
        self.set_font(FONT_NAME, "", 10)
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
    pdf = ResumeCN()
    pdf.add_page()
    pdf.set_margin(18)

    # Header
    pdf.header_block()

    # Professional Summary
    pdf.section("\u804c\u4e1a\u6982\u8981")
    pdf.para(
        "\u7ecf\u9a8c\u4e30\u5bcc\u7684\u6280\u672f\u5199\u4f5c\u4eba\u5458\u3001"
        "\u51fa\u7248\u7269\u7ecf\u7406\u548c\u8f6f\u4ef6\u5f00\u53d1\u4eba\u5458\uff0c"
        "\u5728\u5de5\u7a0b\u548c\u534a\u5bfc\u4f53\u6280\u672f\u65b9\u9762\u62e5\u6709"
        "\u624e\u5b9e\u7684\u57fa\u7840\u3002\u5177\u5907\u5c06\u590d\u6742\u6280\u672f"
        "\u6982\u5ff5\u8f6c\u5316\u4e3a\u6e05\u6670\u3001\u4ee5\u7528\u6237\u4e3a\u4e2d"
        "\u5fc3\u7684\u6587\u6863\u7684\u5353\u8d8a\u80fd\u529b\u3002\u80cc\u666f\u5305"
        "\u62ec\u6280\u672f\u56e2\u961f\u9886\u5bfc\u3001\u5236\u9020\u73af\u5883\u4e2d"
        "\u7684\u5b9e\u9645\u5de5\u7a0b\u7ecf\u9a8c\u4ee5\u53ca\u8fd1\u671f\u7684\u8f6f"
        "\u4ef6\u5f00\u53d1\u9879\u76ee\u3002"
    )

    # Core Skills
    pdf.section("\u6838\u5fc3\u6280\u80fd")
    skills = [
        "\u6280\u672f\u5199\u4f5c\u4e0e\u6587\u6863\u7f16\u5236",
        "\u534a\u5bfc\u4f53\u884c\u4e1a\u4e13\u4e1a\u77e5\u8bc6",
        "\u6280\u672f\u51fa\u7248\u7269\u7ba1\u7406",
        "PLC \u7f16\u7a0b\u4e0e\u5de5\u4e1a\u63a7\u5236",
        "\u8f6f\u4ef6\u5f00\u53d1",
        "\u9879\u76ee\u7ba1\u7406\uff08\u7011\u5e03\u4e0e\u654f\u6377\uff09",
        "\u8de8\u804c\u80fd\u56e2\u961f\u9886\u5bfc",
        "\u6d41\u7a0b\u6539\u8fdb\u4e0e\u6587\u6863\u4f53\u7cfb",
        "\u786c\u4ef6/\u8f6f\u4ef6\u96c6\u6210",
    ]
    pdf.skill_row(skills)
    pdf.ln(1)

    # Professional Experience
    pdf.section("\u804c\u4e1a\u7ecf\u5386")

    # Job 1
    pdf.job_title("\u81ea\u96c7\u8f6f\u4ef6\u5f00\u53d1\u4eba\u5458")
    pdf.job_meta("510k Bridge\uff0c\u7279\u62c9\u534e\u5dde | 2025-2026")
    pdf.bullet("\u6839\u636e\u5ba2\u6237\u9700\u6c42\u5f00\u53d1\u5b9a\u5236\u8f6f\u4ef6\u89e3\u51b3\u65b9\u6848")
    pdf.bullet("\u8bbe\u8ba1\u5e76\u5b9e\u73b0\u4ee5\u53ef\u7528\u6027\u548c\u6027\u80fd\u4e3a\u91cd\u70b9\u7684\u5e94\u7528\u7a0b\u5e8f")
    pdf.bullet("\u7ba1\u7406\u4ece\u6982\u5ff5\u5230\u90e8\u7f72\u7684\u5b8c\u6574\u5f00\u53d1\u751f\u547d\u5468\u671f")
    pdf.ln(3)

    # Job 2
    pdf.job_title("\u6280\u672f\u51fa\u7248\u7269\u7ecf\u7406")
    pdf.job_meta("Cascade Microtech | 1998-2004")
    pdf.bullet("\u9886\u5bfc\u6280\u672f\u5199\u4f5c\u4eba\u5458\u548c\u8bbe\u8ba1\u7ed8\u56fe\u4eba\u5458\u56e2\u961f")
    pdf.bullet("\u76d1\u7763\u6280\u672f\u624b\u518c\u548c\u6587\u6863\u4f53\u7cfb\u7684\u521b\u5efa\u4e0e\u7ef4\u62a4")
    pdf.bullet("\u6539\u8fdb\u8de8\u90e8\u95e8\u7684\u6587\u6863\u5de5\u4f5c\u6d41\u7a0b\u548c\u8d28\u91cf\u6807\u51c6")
    pdf.ln(3)

    # Job 3
    pdf.job_title("\u6280\u672f\u5199\u4f5c\u4eba\u5458")
    pdf.job_meta("Cascade Microtech | 1994-1998")
    pdf.bullet("\u4e3a\u664b\u5706\u63a2\u9488\u548c\u534a\u5bfc\u4f53\u6d4b\u8bd5\u7cfb\u7edf\u7f16\u5199\u8be6\u7ec6\u6280\u672f\u6587\u6863")
    pdf.bullet("\u4e0e\u5de5\u7a0b\u56e2\u961f\u5408\u4f5c\u786e\u4fdd\u51c6\u786e\u6027\u548c\u6e05\u6670\u5ea6")
    pdf.bullet("\u7f16\u5199\u7528\u6237\u624b\u518c\u3001\u670d\u52a1\u6307\u5357\u548c\u57f9\u8bad\u6750\u6599")
    pdf.ln(3)

    # Job 4
    pdf.job_title("\u6280\u672f\u5199\u4f5c\u4eba\u5458\uff08\u5408\u540c/\u591a\u5bb6\u516c\u53f8\uff09")
    pdf.job_meta("Intel\u3001Cascade Microtech\u3001Lattice Semiconductor \u7b49 | 1990-1994")
    pdf.bullet("\u4e3a\u591a\u4e2a\u534a\u5bfc\u4f53\u7ec4\u7ec7\u521b\u5efa\u6280\u672f\u6587\u6863")
    pdf.bullet("\u8de8\u9879\u76ee\u6807\u51c6\u5316\u6587\u6863\u5b9e\u8df5")
    pdf.bullet("\u5728\u7d27\u8feb\u7684\u622a\u6b62\u65e5\u671f\u524d\u4ea4\u4ed8\u9ad8\u8d28\u91cf\u6750\u6599")
    pdf.ln(3)

    # Job 5
    pdf.job_title("\u73b0\u573a\u63a7\u5236\u5de5\u7a0b\u5e08")
    pdf.job_meta("Coe Manufacturing\uff0c\u4fc4\u52d2\u5188\u5dde Tigard | 1984-1990")
    pdf.bullet("\u5728\u80f6\u5408\u677f\u5236\u9020\u4e2d\u7f16\u7a0b\u548c\u7ef4\u62a4 PLC \u63a7\u5236\u673a\u68b0")
    pdf.bullet("\u6392\u9664\u6545\u969c\u5e76\u4f18\u5316\u5de5\u4e1a\u63a7\u5236\u7cfb\u7edf")
    pdf.bullet("\u63d0\u4f9b\u73b0\u573a\u6280\u672f\u652f\u6301\u548c\u7cfb\u7edf\u6539\u8fdb")
    pdf.ln(1)

    # Education
    pdf.section("\u6559\u80b2\u80cc\u666f")
    pdf.job_title("\u6280\u672f\u4f20\u64ad\u7406\u5b66\u5b66\u58eb")
    pdf.job_meta("Charter Oak College\uff0c\u7f8e\u56fd\u5eb7\u6d85\u72c4\u683c\u5dde New Britain | 2002")
    pdf.ln(2)
    pdf.job_title("\u786c\u4ef6/\u8f6f\u4ef6\u5de5\u7a0b\u526f\u5b66\u58eb")
    pdf.job_meta("Portland Community College\uff0c\u7f8e\u56fd\u4fc4\u52d2\u5188\u5dde Portland | 1984")
    pdf.ln(1)

    # Certifications
    pdf.section("\u8bc1\u4e66")
    pdf.job_title("\u9879\u76ee\u7ba1\u7406\u4e13\u4e1a\u4eba\u58eb (PMP)")
    pdf.job_meta("\u65af\u5766\u798f\u5927\u5b66 | 2000")
    pdf.bullet("\u63a2\u7d22\u4e86\u9879\u76ee\u7ba1\u7406\u77e5\u8bc6\u4f53\u7cfb (PMBOK) \u5b9a\u4e49\u7684\u57fa\u672c\u9879\u76ee\u7ba1\u7406\u5b9e\u8df5\u3001\u65b9\u6cd5\u3001\u5de5\u5177\u548c\u6280\u672f")
    pdf.bullet("\u83b7\u5f97\u4e86\u4f20\u7edf\u7011\u5e03\u548c\u654f\u6377\u9879\u76ee\u65b9\u6cd5\u8bba\u7684\u7ecf\u9a8c")
    pdf.bullet("\u5728\u4e0d\u540c\u7684\u6280\u672f\u548c\u5546\u4e1a\u73af\u5883\u4e2d\u5e94\u7528\u9879\u76ee\u7ba1\u7406\u539f\u5219")
    pdf.ln(1)

    # Additional Information
    pdf.section("\u5176\u4ed6\u4fe1\u606f")
    pdf.bullet("\u5728\u5de5\u7a0b\u4e0e\u5546\u4e1a\u6c9f\u901a\u4e4b\u95f4\u67b6\u8d77\u6865\u6881\u7684\u4e30\u5bcc\u7ecf\u9a8c")
    pdf.bullet("\u5f3a\u5927\u7684\u5206\u6790\u548c\u89e3\u51b3\u95ee\u9898\u7684\u80fd\u529b")
    pdf.bullet("\u9002\u5e94\u591a\u4e2a\u884c\u4e1a\uff0c\u5305\u62ec\u534a\u5bfc\u4f53\u5236\u9020\u548c\u5de5\u4e1a\u81ea\u52a8\u5316")
    pdf.ln(4)

    # Footer
    pdf.set_font(FONT_NAME, "I", 9)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 5, "\u63a8\u8350\u4eba\u4fe1\u606f\u5907\u7d22", new_x="LMARGIN", new_y="NEXT", align="C")

    out = "Lon_Dailey_Resume_CN.pdf"
    pdf.output(out)
    print(f"Resume saved: {out}")


if __name__ == "__main__":
    build()
