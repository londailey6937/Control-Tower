#!/usr/bin/env python3
"""Generate PDF of FDA Pre-Submission Guidelines extracted from webinar transcript."""

from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "FDA Q-Submission, Pre-Submission & 510(k) Guidelines", align="L")
        self.ln(4)
        self.set_draw_color(0, 102, 153)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 70, 120)
        self.ln(4)
        self.cell(0, 8, title)
        self.ln(10)

    def sub_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(0, 90, 140)
        self.ln(2)
        self.cell(0, 7, title)
        self.ln(8)

    def sub_sub_title(self, title):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(50, 50, 50)
        self.ln(1)
        self.cell(0, 6, title)
        self.ln(7)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text, indent=15):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        x = self.get_x()
        self.set_x(x + indent)
        self.cell(5, 5.5, "-")
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def table_row(self, col1, col2, w1=70, w2=115, header=False):
        self.set_font("Helvetica", "B" if header else "", 9)
        if header:
            self.set_fill_color(0, 70, 120)
            self.set_text_color(255, 255, 255)
        else:
            self.set_fill_color(240, 245, 250)
            self.set_text_color(30, 30, 30)
        h = 7
        x = self.get_x()
        y = self.get_y()
        self.rect(x, y, w1, h, "F")
        self.rect(x + w1, y, w2, h, "F")
        self.set_draw_color(200, 200, 200)
        self.rect(x, y, w1, h, "D")
        self.rect(x + w1, y, w2, h, "D")
        self.set_xy(x + 2, y)
        self.cell(w1 - 4, h, col1)
        self.set_xy(x + w1 + 2, y)
        self.cell(w2 - 4, h, col2)
        self.ln(h)


pdf = PDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

# Title page content
pdf.set_font("Helvetica", "B", 22)
pdf.set_text_color(0, 70, 120)
pdf.ln(20)
pdf.cell(0, 12, "FDA Q-Submission,", align="C")
pdf.ln(14)
pdf.cell(0, 12, "Pre-Submission & 510(k) Guidelines", align="C")
pdf.ln(20)

pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 7, "Extracted from: FDA CDRH Webinars on Q-Submissions & 510(k) Program", align="C")
pdf.ln(8)
pdf.cell(0, 7, 'Guidance: "Requests for Feedback and Meetings for Medical Device', align="C")
pdf.ln(7)
pdf.cell(0, 7, 'Submissions: The Q-Submission Program" (Final, May 7, 2019)', align="C")
pdf.ln(7)
pdf.cell(0, 7, '& FDA CDRH Learn -- 510(k) Program Overview', align="C")
pdf.ln(20)

pdf.set_draw_color(0, 102, 153)
pdf.set_line_width(0.8)
pdf.line(60, pdf.get_y(), 150, pdf.get_y())

# Section 1
pdf.add_page()
pdf.section_title("1. What Is the Q-Submission Program?")
pdf.body_text(
    "The Q-Submission Program is a voluntary program that provides a mechanism to request "
    "different types of interactions with FDA regarding medical device submissions. "
    "The request submitted to FDA is called a Q-Submission (Q-Sub)."
)
pdf.bullet("Interactions can consist of written feedback, a face-to-face meeting, or a teleconference.")
pdf.bullet("All Q-Submissions must be formally submitted in electronic copy (eCopy) format to FDA via the Document Control Center.")
pdf.bullet("The program evolved from the 1995 Pre-IDE program, was formalized as the Pre-Sub Program in 2013, and expanded to the Q-Sub Program with the May 2019 guidance.")

# Section 2
pdf.section_title("2. Types of Q-Submissions")
pdf.sub_title("2.1 Five Main Q-Sub Types")

pdf.table_row("Q-Sub Type", "Purpose", header=True)
pdf.table_row("Pre-Sub Meeting Request", "Written feedback + subsequent meeting")
pdf.table_row("Pre-Sub Written Feedback", "Written feedback only (no meeting)")
pdf.table_row("Submission Issue Request", "Discuss outstanding issues from hold/IDE/IND letters")
pdf.table_row("Informational Meeting", "Present info to FDA without official feedback")
pdf.table_row("Study Risk Determination", "Obtain SR or NSR determination for clinical study")
pdf.ln(4)

pdf.sub_title("2.2 Additional Q-Sub Types (Detailed in Other Guidances)")
pdf.bullet("PMA Day 100 Meetings")
pdf.bullet("Breakthrough Device Designation Requests")
pdf.bullet("Interactions for Breakthrough Devices")
pdf.bullet("Early Collaboration Meetings")
pdf.bullet("Accessory Classification Requests")

# Section 3
pdf.add_page()
pdf.section_title("3. Pre-Submission (Pre-Sub) Guidelines")

pdf.sub_title("3.1 Purpose")
pdf.body_text(
    "A Pre-Sub is a formal request to FDA for feedback prior to an intended premarket "
    "submission, IDE, accessory classification request, or CLIA Waiver. Pre-Subs are used to "
    "guide product development, develop study protocols, or prepare an application."
)

pdf.sub_title("3.2 Applicable Submission Types")
pdf.body_text("Pre-Subs can be submitted to discuss potential or planned:")
pdf.bullet("510(k)s, PMAs, De Novo Requests, HDEs")
pdf.bullet("IDEs, BLAs, INDs")
pdf.bullet("Accessory Classification Requests, CLIA Waivers")

pdf.sub_title("3.3 Content Requirements")
pdf.bullet("Include specific questions so FDA can provide useful feedback.")
pdf.bullet("Limit to 3-4 substantial topics for the most productive conversations.")
pdf.bullet("Only include information relevant to the specific questions -- you do NOT need to complete all testing or data collection beforehand.")
pdf.bullet("Include enough information for the review team to understand what you are asking.")
pdf.bullet("Specify whether you are requesting written feedback only or a meeting (which includes written feedback prior to the meeting).")

pdf.sub_title("3.4 Pre-Submission Checklist & Examples")
pdf.bullet("Updated Pre-Submission checklist: Appendix 1 of the guidance document.")
pdf.bullet("Examples of productive questions: Appendix 2 of the guidance document.")

pdf.sub_title("3.5 MDUFA Review Timelines")
pdf.table_row("Milestone", "Timeline", header=True)
pdf.table_row("Acceptance review (RTA)", "Within 15 days of receiving Pre-Sub")
pdf.table_row("Meeting date determined", "By Day 30")
pdf.table_row("Written feedback provided", "5 days before meeting or Day 70 (whichever sooner)")
pdf.ln(4)

pdf.sub_title("3.6 FDA Feedback Commitment")
pdf.body_text(
    "FDA intends that feedback provided in response to a Pre-Sub will not change, provided:"
)
pdf.bullet("The information in a future IDE or marketing submission is consistent with that provided in the Pre-Sub, AND")
pdf.bullet("The data in the future submission do not raise any important new issues materially affecting safety or effectiveness.")

pdf.sub_title("3.7 Cost")
pdf.body_text("There are NO costs associated with Q-Submissions or Pre-Submissions at this time.")

# Section 4
pdf.add_page()
pdf.section_title("4. Practical Guidance (from Q&A)")

pdf.sub_title("4.1 Multiple Pre-Submissions for the Same Device")
pdf.bullet("You CAN submit multiple Pre-Subs for the same device on different topics over time.")
pdf.bullet("Submissions for the same device/intended use are tracked as supplements within the same Q-Sub family.")
pdf.bullet("AVOID having multiple Pre-Subs for the same product and same indication open simultaneously.")
pdf.bullet("Exception: If the same device has two completely different indications (e.g., cardiac and neuro), two separate Pre-Subs are acceptable.")

pdf.sub_title("4.2 Written Feedback vs. Meeting -- Best Practice")
pdf.body_text(
    'KEY RECOMMENDATION: "Request a meeting upfront. It is easier to cancel a meeting '
    'that is already on the books than it is to add one that has not been planned." -- Josh Nipper'
)
pdf.bullet("If written feedback is sufficient, you can cancel the meeting -- perfectly acceptable to FDA.")
pdf.bullet("Requesting only written feedback and later wanting a meeting creates scheduling difficulties.")

pdf.sub_title("4.3 Meeting Format")
pdf.bullet("Meetings are typically 60 minutes. Longer meetings are possible but not standard.")
pdf.bullet("In-person vs. teleconference is a sponsor decision:")
pdf.bullet("In-person: allows demos, face-to-face interaction", indent=25)
pdf.bullet("Teleconference: may be scheduled sooner", indent=25)

pdf.sub_title("4.4 Meeting Minutes")
pdf.bullet("Meeting minutes are REQUIRED for all meetings, regardless of Q-Sub type.")
pdf.bullet("The SUBMITTER is responsible for drafting meeting minutes.")
pdf.bullet("FDA has approximately 30 days to review and respond to submitted minutes.")

pdf.sub_title("4.5 Disagreements with FDA Feedback")
pdf.body_text("Pre-Sub feedback is NOT binding. If you disagree with feedback:")
pdf.bullet("Step 1: Reach out to the lead reviewer")
pdf.bullet("Step 2: Escalate to the assistant director (formerly branch chief)")
pdf.bullet("Step 3: Escalate to the division director")
pdf.bullet("You may also raise concerns in the cover letter of your marketing submission.")
pdf.body_text(
    "Note: There is NO formal appeal process or least-burdensome flag for Pre-Sub feedback. "
    "The least-burdensome flag is only available after a deficiency/AI letter for a 510(k)."
)

pdf.sub_title("4.6 When a Pre-Sub Is (and Isn't) Needed")
pdf.bullet("Pre-Subs: appropriate for substantive questions about regulatory strategy, clinical protocols, predicate selection, testing plans.")
pdf.bullet('NOT every question requires a Pre-Sub. Simple questions (e.g., "What supplement type?") can be addressed by reaching out to the lead reviewer or branch management directly.')
pdf.bullet("If FDA determines your question needs deeper analysis, they may direct you to submit a formal Pre-Sub.")

pdf.sub_title("4.7 Regulatory Classification Questions")
pdf.bullet('If your primary question is "Am I a medical device?" or "What classification am I?" -- the 513(g) program is the appropriate pathway.')
pdf.bullet("You CAN use a Pre-Sub or Informational Meeting to discuss your product and get general suggestions.")
pdf.bullet("You would NOT get a formal classification decision under the Pre-Sub program.")

pdf.sub_title("4.8 Confidentiality")
pdf.body_text("All information submitted through the Q-Sub program is considered confidential.")

# Section 5
pdf.add_page()
pdf.section_title("5. Submission Issue Requests (SIRs)")

pdf.sub_title("5.1 Purpose")
pdf.body_text(
    "Discuss outstanding review issues provided in a marketing submission hold letter, "
    "IDE letter, or IND clinical hold letter. Help submitters determine how to respond to "
    "outstanding questions in formal responses."
)

pdf.sub_title("5.2 When to Use (and Not Use)")
pdf.bullet("USE when you need to discuss approaches to address deficiencies identified in a formal letter.")
pdf.bullet("DO NOT USE for simple clarification questions that can be handled by the lead reviewer.")
pdf.bullet("DO NOT USE to discuss issues while a file is under active review (use interactive review instead).")

pdf.sub_title("5.3 Two-Tiered Review Timeline")
pdf.table_row("Timing", "FDA Feedback Goal", header=True)
pdf.table_row("SIR within 60 days of letter", "21 days")
pdf.table_row("SIR more than 60 days after", "70 days")
pdf.ln(4)

pdf.body_text(
    "Rationale: When received promptly, issues are still current and the review team is "
    "familiar. After extended time, the team may need to re-familiarize themselves, adding time."
)

pdf.sub_title("5.4 Key Changes from Previous Guidance")
pdf.bullet('Renamed from "Submission Issue Meetings (SIMs)" -- feedback can now be written or via meeting.')
pdf.bullet("SIRs and Informational Meetings no longer receive an RTA (acceptance) review.")

# Section 6
pdf.section_title("6. Application to Novel Devices (De Novo Pathway)")
pdf.body_text(
    "For novel devices with no clear predicate (such as a wearable gyroscopic balance belt), "
    "the Pre-Sub process is particularly valuable:"
)
pdf.bullet("Submit a Pre-Sub before your De Novo request to get FDA feedback on classification, testing, clinical study design, and software documentation.")
pdf.bullet("Limit to 3-4 topics for the most productive interaction.")
pdf.bullet("Request a meeting (not just written feedback) -- you can always cancel.")
pdf.bullet("No cost is associated with the Pre-Sub.")
pdf.bullet("Target the Physical Medicine Devices division (21 CFR Part 890).")

# =====================================================================
# PART II: 510(k) PROGRAM
# =====================================================================

pdf.add_page()
pdf.section_title("7. The 510(k) Program Overview")
pdf.body_text(
    "A 510(k), also referred to as a Premarket Notification, is the most common premarket "
    "submission for medical devices. The name refers to Section 510(k) of the Federal Food, "
    "Drug and Cosmetic Act. The requirements for a 510(k) submission are outlined in "
    "21 CFR 807 Subpart E."
)
pdf.body_text(
    "A 510(k) is a marketing clearance application. FDA clears 510(k)s based on a "
    "determination of Substantial Equivalence. Important distinctions:"
)
pdf.bullet("A 510(k) results in FDA CLEARANCE (not approval). Only PMAs result in FDA approval.")
pdf.bullet("A 510(k) is not just a form -- it can be hundreds of pages depending on the device.")
pdf.bullet("A 510(k) is not establishment registration or device listing.")
pdf.bullet("A 510(k) is not a Premarket Approval (PMA).")

# Section 8: Device Classification
pdf.add_page()
pdf.section_title("8. Device Classification & the 510(k)")

pdf.sub_title("8.1 Risk-Based Classification")
pdf.table_row("Class", "Risk / Controls / 510(k) Requirement", header=True)
pdf.table_row("Class I", "Low risk. General controls. Most are 510(k) exempt.")
pdf.table_row("Class II", "Moderate risk. General + special controls. Most require 510(k).")
pdf.table_row("Class III", "High risk. General controls + PMA required (not 510(k)).")
pdf.ln(4)

pdf.sub_title("8.2 Product Classification Database")
pdf.body_text(
    "The FDA Product Classification Database is an invaluable public resource. It provides "
    "the three-letter product code, submission type, applicable consensus standards, and "
    "relevant guidance documents for each device type. Search by device name to find the "
    "appropriate regulatory pathway."
)

pdf.sub_title("8.3 The 513(g) Program")
pdf.body_text(
    "If you cannot determine the appropriate device classification after searching the "
    "Product Classification Database, consider the 513(g) program:"
)
pdf.bullet("513(g) is a formal request to FDA for classification information.")
pdf.bullet("FDA will respond with what they consider the appropriate regulatory pathway.")
pdf.bullet("There IS a 513(g) user fee.")
pdf.bullet("A 513(g) response does NOT constitute FDA clearance or approval -- you must still comply with the identified pathway.")

# Section 9: Substantial Equivalence
pdf.add_page()
pdf.section_title("9. Substantial Equivalence")

pdf.sub_title("9.1 Definition")
pdf.body_text(
    "Substantial Equivalence is the foundation of the 510(k) program. It is the demonstration "
    "that your new device, compared to a predicate device, meets one of two standards:"
)
pdf.bullet("Same intended use AND same technological characteristics, OR")
pdf.bullet("Same intended use AND different technological characteristics that do NOT raise different questions of safety and effectiveness.")

pdf.sub_title("9.2 Predicate Devices")
pdf.body_text(
    "A predicate device is a legally marketed device (typically 510(k)-cleared) used for "
    "comparison. Key points:"
)
pdf.bullet("Multiple predicate devices are acceptable only under certain circumstances (refer to guidance).")
pdf.bullet("Split predicates (combining intended use of one device with technology of another) are INCONSISTENT with the 510(k) regulatory standard.")
pdf.bullet("Reference Devices may be used to support scientific methodology or standard reference values -- they are NOT predicate devices.")

pdf.sub_title("9.3 Decision-Making Flow Chart (Appendix A)")
pdf.body_text("The 510(k) SE determination follows five decision points:")
pdf.bullet("Decision Point 1: Is the predicate device legally marketed?")
pdf.bullet("Decision Point 2: Do the devices have the same intended use?")
pdf.bullet("Decision Point 3: Do the devices have the same technological characteristics?")
pdf.bullet("Decision Point 4: Do the differences raise different questions of safety and effectiveness?")
pdf.bullet("Decision Point 5: Provide acceptable test methods AND data to demonstrate SE.")
pdf.body_text(
    "Key reference: Final guidance -- 'Evaluating Substantial Equivalence in Premarket "
    "Notifications [510(k)]' -- Appendix A contains the full flow chart."
)

pdf.sub_title("9.4 No Predicate? Consider De Novo")
pdf.body_text(
    "If you have a low or moderate risk device with no identifiable predicate, the De Novo "
    "classification pathway may be appropriate. This creates a new classification and product "
    "code that future devices can use as a predicate."
)

# Section 10: Types of 510(k)
pdf.add_page()
pdf.section_title("10. Types of 510(k) Submissions")

pdf.table_row("Type", "Key Characteristics", header=True)
pdf.table_row("Traditional", "Standard SE demonstration. Can be used in any circumstance.")
pdf.table_row("Abbreviated", "Relies on guidance docs, special controls, consensus standards.")
pdf.table_row("Special", "Modifications to manufacturer's OWN cleared device.")
pdf.ln(4)

pdf.sub_title("10.1 Traditional 510(k)")
pdf.bullet("Must include required elements of 21 CFR 807.87.")
pdf.bullet("Relies on demonstration of Substantial Equivalence.")
pdf.bullet("Can be used under any circumstance.")

pdf.sub_title("10.2 Abbreviated 510(k)")
pdf.bullet("Must include required elements of 21 CFR 807.87.")
pdf.bullet("Relies on FDA guidance documents, special controls, and recognized consensus standards.")
pdf.bullet("Under certain conditions, sponsors may NOT need to submit test data.")

pdf.sub_title("10.3 Special 510(k)")
pdf.bullet("Must include required elements of 21 CFR 807.87.")
pdf.bullet("Appropriate ONLY for modifications to the manufacturer's own legally marketed device.")
pdf.bullet("Modification must NOT affect the intended use or fundamental scientific technology.")
pdf.bullet("Test data is typically NOT submitted.")
pdf.bullet("MDUFA goal: 30 FDA review days (vs. 90 for traditional/abbreviated).")

# Section 11: Content of a 510(k)
pdf.add_page()
pdf.section_title("11. Content of a 510(k) Submission")

pdf.sub_title("11.1 Intended Use & Indications for Use")
pdf.bullet("Intended Use: general purpose/function of the device (broad).")
pdf.bullet("Indications for Use: the disease/condition the device will diagnose, treat, prevent, cure, or mitigate, including the patient population.")
pdf.bullet("Must be CONSISTENT throughout the entire 510(k) -- summary, labeling, IFU, etc.")
pdf.bullet("Use FDA Form 3881 for the Indications for Use statement.")
pdf.bullet("Identify whether the device is prescription use or over-the-counter.")

pdf.sub_title("11.2 510(k) Summary")
pdf.bullet("High-level discussion of content within the 510(k).")
pdf.bullet("Must cover elements in 21 CFR 807.92.")
pdf.bullet("Must include sufficient detail to explain the basis for SE determination.")
pdf.bullet("FDA will verify accuracy and completeness.")
pdf.bullet("Refer to 510(k) Program Final Guidance, Appendix B, for requirements and example.")

pdf.sub_title("11.3 Device Description")
pdf.bullet("Include device design details, figures, diagrams.")
pdf.bullet("List patient-contacting materials (drives biocompatibility testing requirements).")
pdf.bullet("Include energy sources (battery, AC power).")
pdf.bullet("Include key technological features.")

pdf.sub_title("11.4 Substantial Equivalence Discussion")
pdf.bullet("The FOUNDATION of your 510(k) -- comparative analysis of new device vs. predicate.")
pdf.bullet("Follow the SE decision-making flow chart through each decision point.")
pdf.bullet("Clearly explain how SE is demonstrated.")

pdf.sub_title("11.5 Consensus Standards")
pdf.bullet("Voluntary program to simplify and streamline 510(k) review.")
pdf.bullet("Sponsors can declare conformance to FDA-recognized consensus standards.")
pdf.bullet("Document extent of conformance via FDA Form 3654.")
pdf.bullet("Search the public Recognized Consensus Standards Database.")

pdf.sub_title("11.6 FDA Guidance Documents")
pdf.bullet("Represent FDA's current thinking on a topic.")
pdf.bullet("Can be device-specific or general.")
pdf.bullet("Do NOT create binding obligations -- alternative approaches may be acceptable.")
pdf.bullet("Search the public FDA Guidance Document Database.")

pdf.sub_title("11.7 Proposed Labeling")
pdf.bullet("Must comply with 21 CFR 801.")
pdf.bullet("Include: package insert, service manuals, IFU, advertising/promotional materials.")
pdf.bullet("Directions for use must include intended use statement, warnings, contraindications, limitations.")
pdf.bullet("Submit as a FINAL DRAFT.")
pdf.bullet("Predicate device labeling is recommended but not required.")

pdf.sub_title("11.8 Performance Testing")
pdf.body_text("Performance testing can be bench, animal, or clinical:")
pdf.bullet("Testing is determined by device complexity and intended use.")
pdf.bullet("Consider FDA guidance documents, especially device-specific ones.")
pdf.bullet("Comparative (side-by-side) testing is helpful but not required.")
pdf.bullet("If the predicate device is unavailable, use tabular comparison of specifications.")
pdf.bullet("Include: test methods, acceptance criteria, and test results.")
pdf.ln(2)
pdf.body_text("Clinical Testing -- most often NOT required for 510(k)s. May be needed when:")
pdf.bullet("New or modified indication for use.")
pdf.bullet("Significant technological changes.")
pdf.bullet("Nonclinical testing methods are limited or inappropriate.")

pdf.sub_title("11.9 Key Formatting Considerations")
pdf.bullet("Make information complete, organized; include table of contents, tabs, page numbers.")
pdf.bullet("Use tables, graphs, and visual aids whenever possible.")
pdf.bullet("Clearly identify basic requirements (510(k) summary, IFU form).")
pdf.bullet("Maintain consistency throughout the entire submission.")
pdf.bullet("Follow any applicable guidance document or device-specific checklist.")

# Section 12: 510(k) Submission Process & Timeline
pdf.add_page()
pdf.section_title("12. 510(k) Submission Process & Timeline")

pdf.sub_title("12.1 Before You Submit")
pdf.body_text("eCopy Requirements:")
pdf.bullet("A valid eCopy is REQUIRED for all premarket submissions, including 510(k)s.")
pdf.bullet("An eCopy is an exact duplicate of the paper submission.")
pdf.bullet("Submit: one electronic copy (eCopy) + one paper copy + signed cover letter.")
pdf.bullet("Mail to the appropriate Document Control Center.")
pdf.bullet("FDA does NOT return your submission after review.")
pdf.ln(2)
pdf.body_text("User Fees:")
pdf.bullet("510(k) submissions are subject to user fees.")
pdf.bullet("Fee must be received ON OR BEFORE the application is submitted.")
pdf.bullet("FDA will NOT accept the 510(k) if the fee is not paid.")
pdf.bullet("Standard fee and small business reduced fee are available.")
pdf.bullet("Small business: < $100M in sales -- must obtain Small Business Determination FIRST.")
pdf.bullet("If you pay the standard fee and later qualify as small business, FDA will NOT refund the difference.")

pdf.sub_title("12.2 Review Timeline (Calendar Days)")
pdf.table_row("Day", "Milestone", header=True)
pdf.table_row("Day 1", "FDA receives 510(k) submission")
pdf.table_row("Day 7", "Acknowledgment letter OR hold letter (user fee/eCopy issues)")
pdf.table_row("Day 15", "Acceptance review (RTA) -- accepted or Refuse to Accept Hold")
pdf.table_row("Day 60", "Substantive review -- Interactive Review or AI request")
pdf.table_row("Day 90", "MDUFA decision goal (traditional/abbreviated)")
pdf.table_row("Day 30", "MDUFA decision goal (special 510(k))")
pdf.table_row("Day 100", "Missed MDUFA decision communication (if no decision by Day 90)")
pdf.ln(4)

pdf.sub_title("12.3 Interactive Review vs. Additional Information (AI) Requests")
pdf.body_text("Interactive Review:")
pdf.bullet("Informal interaction between FDA and submitter during review.")
pdf.bullet("Does NOT stop the FDA clock.")
pdf.bullet("May reduce overall time to decision.")
pdf.bullet("Not subject to eCopy requirements (unless submitted through Document Control Center).")
pdf.ln(2)
pdf.body_text("Additional Information (AI) Requests:")
pdf.bullet("Formal requests made via email, followed by formal hold letter.")
pdf.bullet("DOES stop the FDA clock.")
pdf.bullet("Subject to eCopy requirements.")
pdf.bullet("Submitter has 180 days to provide a complete response.")
pdf.bullet("WARNING: If you submit on Day 179 and fail eCopy requirements, you may exceed 180 days and your 510(k) may be withdrawn.")

# Section 13: 510(k) Decisions
pdf.add_page()
pdf.section_title("13. 510(k) Decisions")

pdf.sub_title("13.1 Substantially Equivalent (SE) Decision")
pdf.bullet("You may legally market the device.")
pdf.bullet("You receive a valid 510(k) number (K-number).")
pdf.bullet("You must then complete establishment registration and device listing.")
pdf.bullet("Posted publicly: SE determination letter, Indications for Use form, 510(k) summary.")

pdf.sub_title("13.2 Not Substantially Equivalent (NSE) Decision")
pdf.body_text("You may receive an NSE if:")
pdf.bullet("You did not identify an appropriate predicate device (not legally marketed or not appropriate).")
pdf.bullet("The predicate has a different intended use.")
pdf.bullet("Differences in technological characteristics raise different safety/effectiveness questions.")
pdf.bullet("You did not demonstrate that the device is as safe and effective as the predicate.")
pdf.ln(2)
pdf.body_text("After an NSE, options include:")
pdf.bullet("Resubmit another 510(k) with new data.")
pdf.bullet("Submit a PMA.")
pdf.bullet("Submit a De Novo request.")
pdf.bullet("Submit a reclassification petition.")

pdf.sub_title("13.3 Pre-Submission for 510(k)s")
pdf.body_text(
    "A Pre-Sub for a 510(k) is only appropriate for unique situations, such as when clinical "
    "data may be needed to support SE. Through the Pre-Sub program, you submit a formal "
    "written request and can request written feedback, a meeting, or a teleconference. "
    "Pre-Subs are subject to eCopy requirements."
)

# Closing
pdf.ln(10)
pdf.set_draw_color(0, 102, 153)
pdf.set_line_width(0.5)
pdf.line(10, pdf.get_y(), 200, pdf.get_y())
pdf.ln(6)
pdf.set_font("Helvetica", "I", 9)
pdf.set_text_color(100, 100, 100)
pdf.multi_cell(0, 5,
    "This document was extracted and compiled from FDA Webinar transcripts: "
    "(1) Q-Submission Program for Medical Device Submissions (June 11, 2019), and "
    "(2) CDRH Learn -- 510(k) Program Overview. For the complete guidance documents, "
    "refer to: 'Requests for Feedback and Meetings for Medical Device Submissions: "
    "The Q-Submission Program' (May 7, 2019) and 'Evaluating Substantial Equivalence "
    "in Premarket Notifications [510(k)]'."
)

output_path = "/Users/londailey/Control-Tower/FDA_Pre-Submission_Guidelines.pdf"
pdf.output(output_path)
print(f"PDF generated: {output_path}")
