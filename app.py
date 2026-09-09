
import streamlit as st
from io import BytesIO
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth

st.set_page_config(page_title="Bariatric Insurance Navigator", page_icon="🩺", layout="wide")

PAYER_DEFAULTS = {
    "Aetna": {
        "policy": "Clinical Policy Bulletin 0157 - Obesity Surgery",
        "supervised_required": "Yes",
        "duration": "12 visits",
        "consecutive": "No",
        "through_auth": "Unknown",
        "time_window": "Within 2 years",
        "weight_gain": "Not specified",
        "net_gain": "Not specified",
        "obesity_history": "History of unsuccessful weight loss",
        "lmn": "Unknown",
        "lmn_pcp": "Unknown",
        "psych": "Yes",
        "nutrition": "Unknown",
        "psych_window": "Not specified",
        "cardiology": "Unknown",
        "pulmonary": "Unknown",
        "pcp": "Unknown",
        "egd": "Unknown",
        "sleep": "Unknown",
        "nicotine": "Unknown",
        "support": "Unknown",
        "logs": "Unknown",
        "notes": (
            "Aetna policy requires 12+ behavioral intervention sessions on separate dates, "
            "with nutrition, physical activity, and behavioral modification components. "
            "Member-specific bariatric benefit/exclusion must still be verified."
        )
    },
    "UnitedHealthcare": {
        "policy": "Plan-specific UHC bariatric medical policy",
        "supervised_required": "Unknown",
        "duration": "Unknown",
        "consecutive": "Unknown",
        "through_auth": "Unknown",
        "time_window": "Unknown",
        "weight_gain": "Unknown",
        "net_gain": "Unknown",
        "obesity_history": "Unknown",
        "lmn": "Unknown",
        "lmn_pcp": "Unknown",
        "psych": "Unknown",
        "nutrition": "Unknown",
        "psych_window": "Unknown",
        "cardiology": "Unknown",
        "pulmonary": "Unknown",
        "pcp": "Unknown",
        "egd": "Unknown",
        "sleep": "Unknown",
        "nicotine": "Unknown",
        "support": "Unknown",
        "logs": "Unknown",
        "notes": "Verify the member-specific plan and current UHC policy."
    },
    "BCBS Arizona / AZ Blue": {
        "policy": "Plan-specific AZ Blue / BCBS bariatric policy",
        "supervised_required": "Unknown",
        "duration": "Unknown",
        "consecutive": "Unknown",
        "through_auth": "Unknown",
        "time_window": "Unknown",
        "weight_gain": "Unknown",
        "net_gain": "Unknown",
        "obesity_history": "Unknown",
        "lmn": "Unknown",
        "lmn_pcp": "Unknown",
        "psych": "Unknown",
        "nutrition": "Unknown",
        "psych_window": "Unknown",
        "cardiology": "Unknown",
        "pulmonary": "Unknown",
        "pcp": "Unknown",
        "egd": "Unknown",
        "sleep": "Unknown",
        "nicotine": "Unknown",
        "support": "Unknown",
        "logs": "Unknown",
        "notes": "Requirements may vary by product and plan. Verify the applicable policy/guideline."
    },
    "Arizona Complete Health (Centene)": {
        "policy": "CP.MP.37 - Bariatric Surgery",
        "supervised_required": "No",
        "duration": "Not required",
        "consecutive": "Not specified",
        "through_auth": "Not specified",
        "time_window": "Not specified",
        "weight_gain": "Not specified",
        "net_gain": "Not specified",
        "obesity_history": "Not specified",
        "lmn": "Not specified",
        "lmn_pcp": "Not specified",
        "psych": "Yes",
        "nutrition": "Yes",
        "psych_window": "6 months",
        "cardiology": "Not specified",
        "pulmonary": "Not specified",
        "pcp": "Yes",
        "egd": "Unknown",
        "sleep": "Not specified",
        "nicotine": "Not specified",
        "support": "Not specified",
        "logs": "Not specified",
        "notes": (
            "CP.MP.37, last revision 09/25. Initial bariatric surgery requires both medical-history "
            "and preoperative-evaluation criteria. Adults age >18: BMI >=35 kg/m2 for all other "
            "ethnicities or >=32.5 kg/m2 for South Asian, Southeast Asian, and East Asian adults "
            "when LAGB, LSG, RYGB, SADI/SADI-S, or BPD-DS/BPD-GRDS is requested. Adults with "
            "BMI >=30 and <35 kg/m2 for all other ethnicities, or >=27.5 and <32.5 kg/m2 for the "
            "listed Asian groups, may qualify when one of those procedures is requested and there "
            "is type 2 diabetes OR a listed obesity-related comorbidity that has not improved despite "
            "nonsurgical weight-loss methods. Listed comorbidities include hypertension, dyslipidemia, "
            "OSA, obesity-hypoventilation/Pickwickian syndrome, NAFLD/NASH, pseudotumor cerebri, CAD, "
            "GERD, asthma, venous stasis disease, bone/joint disease, obesity-related disqualification "
            "from another specialty surgery, chronic kidney disease, infertility, PCOS, atrial "
            "fibrillation, and heart failure. For age <18, LSG or RYGB may qualify with BMI >=35 kg/m2 "
            "or 120% of the 95th percentile, whichever is lower. Within six months of scheduled surgery, "
            "all are required: medical evaluation from a physician other than the surgeon, preferably "
            "the PCP, including recommendation for bariatric surgery and medical clearance; nutritional "
            "evaluation by a qualified provider; and age-appropriate psychiatry/psychology consultation "
            "confirming candidacy and adequate management of mental health disorders. The current initial "
            "surgery criteria do not specify a mandatory supervised weight-loss visit duration. "
            "Repeat/revisional surgery has separate criteria, including meeting initial criteria again "
            "for certain revisions/conversions, prior surgery at least two years earlier, less than 50% "
            "excess-body-weight loss from the initial procedure, timing after eroded-band removal when "
            "applicable, documented postoperative nutrition/exercise compliance, and provider explanation "
            "of why the prior procedure failed. The policy also separately identifies procedures with "
            "inadequate evidence and procedures considered not medically necessary. Member-specific "
            "benefit coverage and exclusions still require verification."
        )
    },
    "Medicare": {
        "policy": "CMS / applicable MAC bariatric coverage criteria",
        "supervised_required": "Unknown",
        "duration": "Unknown",
        "consecutive": "Unknown",
        "through_auth": "Unknown",
        "time_window": "Unknown",
        "weight_gain": "Unknown",
        "net_gain": "Unknown",
        "obesity_history": "Unknown",
        "lmn": "Unknown",
        "lmn_pcp": "Unknown",
        "psych": "Unknown",
        "nutrition": "Unknown",
        "psych_window": "Unknown",
        "cardiology": "Unknown",
        "pulmonary": "Unknown",
        "pcp": "Unknown",
        "egd": "Unknown",
        "sleep": "Unknown",
        "nicotine": "Unknown",
        "support": "Unknown",
        "logs": "Unknown",
        "notes": "Verify applicable Medicare national and local/MAC documentation requirements."
    },
    "Other / Custom": {
        "policy": "Manual payer criteria",
        "supervised_required": "Unknown",
        "duration": "Unknown",
        "consecutive": "Unknown",
        "through_auth": "Unknown",
        "time_window": "Unknown",
        "weight_gain": "Unknown",
        "net_gain": "Unknown",
        "obesity_history": "Unknown",
        "lmn": "Unknown",
        "lmn_pcp": "Unknown",
        "psych": "Unknown",
        "nutrition": "Unknown",
        "psych_window": "Unknown",
        "cardiology": "Unknown",
        "pulmonary": "Unknown",
        "pcp": "Unknown",
        "egd": "Unknown",
        "sleep": "Unknown",
        "nicotine": "Unknown",
        "support": "Unknown",
        "logs": "Unknown",
        "notes": ""
    }
}

def select_with_default(label, options, default):
    idx = options.index(default) if default in options else 0
    return st.selectbox(label, options, index=idx)


def _pdf_safe(value):
    if value is None:
        return ""
    return str(value).replace("–", "-").replace("—", "-").replace("≥", ">=").replace("²", "2")


def _wrap_text(c, text, x, y, max_width, font="Helvetica", size=8, leading=10):
    """Draw wrapped text and return the next y position."""
    text = _pdf_safe(text)
    words = text.split()
    line = ""
    for word in words:
        trial = word if not line else line + " " + word
        if stringWidth(trial, font, size) <= max_width:
            line = trial
        else:
            c.setFont(font, size)
            c.drawString(x, y, line)
            y -= leading
            line = word
    if line:
        c.setFont(font, size)
        c.drawString(x, y, line)
        y -= leading
    return y


def build_chart_pdf(data):
    """
    One-page bariatric insurance criteria summary modeled after the clinic's
    existing criteria checklist. This is generated in memory for Streamlit download.
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    margin = 0.42 * inch
    left = margin
    right = width - margin
    y = height - 0.42 * inch

    # Header
    c.setFont("Helvetica-Bold", 13)
    c.drawString(left, y, "BARIATRIC INSURANCE CRITERIA")
    c.setFont("Helvetica", 8)
    c.drawRightString(right, y, f"Verified: {_pdf_safe(data.get('verification_date', ''))}")
    y -= 16

    c.setLineWidth(0.8)
    c.line(left, y, right, y)
    y -= 14

    # Patient / insurance identifiers
    c.setFont("Helvetica-Bold", 8)
    c.drawString(left, y, "Patient / Chart:")
    c.setFont("Helvetica", 8)
    c.drawString(left + 72, y, _pdf_safe(data.get("patient_label", ""))[:38])

    c.setFont("Helvetica-Bold", 8)
    c.drawString(310, y, "Payer:")
    c.setFont("Helvetica", 8)
    c.drawString(345, y, _pdf_safe(data.get("payer", ""))[:30])
    y -= 12

    c.setFont("Helvetica-Bold", 8)
    c.drawString(left, y, "Plan:")
    c.setFont("Helvetica", 8)
    c.drawString(left + 32, y, _pdf_safe(data.get("plan_name", ""))[:45])

    c.setFont("Helvetica-Bold", 8)
    c.drawString(310, y, "Member ID:")
    c.setFont("Helvetica", 8)
    c.drawString(365, y, _pdf_safe(data.get("member_id", ""))[:28])
    y -= 12

    c.setFont("Helvetica-Bold", 8)
    c.drawString(left, y, "Group #:")
    c.setFont("Helvetica", 8)
    c.drawString(left + 45, y, _pdf_safe(data.get("group_number", ""))[:30])

    c.setFont("Helvetica-Bold", 8)
    c.drawString(310, y, "Policy / Guideline:")
    c.setFont("Helvetica", 8)
    c.drawString(392, y, _pdf_safe(data.get("policy_number", ""))[:27])
    y -= 15

    # Benefit verification box
    c.setFillGray(0.92)
    c.rect(left, y - 13, right-left, 15, fill=1, stroke=0)
    c.setFillGray(0)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left + 4, y - 9, "BENEFIT VERIFICATION")
    y -= 23

    benefit_line = (
        f"Benefit verified: {data.get('benefit_verified')}    "
        f"Exclusion: {data.get('exclusion')}    "
        f"Prior auth: {data.get('prior_auth')}    "
        f"COE / facility restriction: {data.get('coe')}"
    )
    c.setFont("Helvetica", 8)
    c.drawString(left, y, _pdf_safe(benefit_line))
    y -= 12

    ref_line = (
        f"Rep: {data.get('rep_name') or ''}    "
        f"Reference #: {data.get('reference') or ''}    "
        f"Auth phone: {data.get('auth_phone') or ''}"
    )
    y = _wrap_text(c, ref_line, left, y, right-left, size=8, leading=10)

    plan_lines = [
        f"Plan type: {data.get('plan_type') or ''}    State: {data.get('state') or ''}    Employer/group: {data.get('employer_group') or ''}",
        f"Auth portal/vendor: {data.get('auth_portal') or ''}    Facility/network restriction: {data.get('facility_note') or ''}",
        f"Deductible/remaining: {data.get('deductible') or ''}    Coinsurance: {data.get('coinsurance') or ''}    OOP max/remaining: {data.get('oop') or ''}",
        f"Policy effective/review: {data.get('policy_effective') or ''}"
    ]
    for plan_line in plan_lines:
        y = _wrap_text(c, plan_line, left, y, right-left, size=7.4, leading=9)
    y -= 2

    # Main criteria heading
    c.setFillGray(0.92)
    c.rect(left, y - 13, right-left, 15, fill=1, stroke=0)
    c.setFillGray(0)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left + 4, y - 9, "CRITERIA")
    y -= 23

    lines = [
        ("Supervised / medically managed weight-loss program", data.get("supervised")),
        ("Required duration / visits", data.get("duration")),
        ("Visits consecutive", data.get("consecutive")),
        ("Continue visits until authorization submitted", data.get("through_auth")),
        ("Program timing window", data.get("time_window")),
        ("Weight gain allowed during program", data.get("weight_gain")),
        ("Net weight gain allowed", data.get("net_gain")),
        ("Required weight / obesity history", data.get("obesity_history")),
        ("Letter of Medical Necessity required", data.get("lmn")),
        ("LMN must be from PCP", data.get("lmn_pcp")),
    ]

    c.setFont("Helvetica", 8)
    for label, value in lines:
        c.setFont("Helvetica-Bold", 8)
        c.drawString(left, y, _pdf_safe(label) + ":")
        c.setFont("Helvetica", 8)
        value_x = left + min(235, stringWidth(_pdf_safe(label) + ": ", "Helvetica-Bold", 8) + 5)
        c.drawString(value_x, y, _pdf_safe(value))
        y -= 10

    # Two-column lower section
    y -= 2
    column_gap = 18
    col_w = (right-left-column_gap)/2
    x1 = left
    x2 = left + col_w + column_gap
    top_y = y

    def section_header(x, yy, title, w):
        c.setFillGray(0.92)
        c.rect(x, yy - 13, w, 15, fill=1, stroke=0)
        c.setFillGray(0)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x + 4, yy - 9, title)
        return yy - 22

    y1 = section_header(x1, top_y, "CLEARANCES / TESTING", col_w)
    left_items = [
        ("Psych evaluation", data.get("psych")),
        ("Nutritional evaluation", data.get("nutrition")),
        ("Psych validity", data.get("psych_window")),
        ("Cardiology clearance", data.get("cardiology")),
        ("Pulmonology clearance", data.get("pulmonary")),
        ("PCP clearance", data.get("pcp")),
        ("EGD", data.get("egd")),
        ("Sleep study", data.get("sleep")),
        ("Nicotine test", data.get("nicotine")),
        ("EKG", data.get("ekg")),
        ("Chest X-ray", data.get("chest_xray")),
        ("Support group", data.get("support")),
        ("Food / exercise logs", data.get("logs")),
    ]
    for label, value in left_items:
        c.setFont("Helvetica-Bold", 7.6)
        c.drawString(x1, y1, _pdf_safe(label) + ":")
        c.setFont("Helvetica", 7.6)
        c.drawRightString(x1 + col_w, y1, _pdf_safe(value))
        y1 -= 10

    y2 = section_header(x2, top_y, "LABS", col_w)

    labs = data.get("labs") or []
    c.setFont("Helvetica-Bold", 7.6)
    c.drawString(x2, y2, "Required labs:")
    y2 -= 10
    if labs:
        for lab in labs:
            y2 = _wrap_text(c, "• " + lab, x2, y2, col_w, size=7.6, leading=9)
    else:
        c.setFont("Helvetica", 7.6)
        c.drawString(x2, y2, "None documented / unknown")
        y2 -= 10

    y = min(y1, y2) - 7

    # Notes
    if y < 115:
        c.showPage()
        y = height - 0.5 * inch

    c.setFillGray(0.92)
    c.rect(left, y - 13, right-left, 15, fill=1, stroke=0)
    c.setFillGray(0)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left + 4, y - 9, "NOTES")
    y -= 23

    note_text = " | ".join(
        [x for x in [
            data.get("benefit_notes", ""),
            data.get("criteria_notes", "")
        ] if x]
    )
    if not note_text:
        note_text = "No additional notes."
    y = _wrap_text(c, note_text, left, y, right-left, size=7.5, leading=9)

    c.setFont("Helvetica-Oblique", 6.7)
    footer = (
        "Pre-consult insurance requirement summary. Coverage is subject to the member-specific benefit plan "
        "and current payer policy. Verify requirements before authorization."
    )
    _wrap_text(c, footer, left, 34, right-left, font="Helvetica-Oblique", size=6.7, leading=8)

    c.save()
    buffer.seek(0)
    return buffer.getvalue()


# -----------------------------
# Demo / navigation shell
# -----------------------------
if "workflow_page" not in st.session_state:
    st.session_state.workflow_page = "Home"

if "insurance_data" not in st.session_state:
    st.session_state.insurance_data = {}

st.warning(
    "PROTOTYPE DEMO — DO NOT ENTER PHI. Use only fictional/test information until this application "
    "is reviewed and deployed in a Banner-approved environment."
)

with st.sidebar:
    st.markdown("### Bariatric Insurance Navigator")
    st.caption("Prototype demonstration")
    st.markdown(f"**Current screen:** {st.session_state.workflow_page}")
    st.divider()
    if st.button("Home", use_container_width=True):
        st.session_state.workflow_page = "Home"
        st.rerun()
    if st.button("Insurance Information", use_container_width=True):
        st.session_state.workflow_page = "Insurance Information"
        st.rerun()
    if st.session_state.get("insurance_data"):
        if st.button("Pre-Consult Requirements", use_container_width=True):
            st.session_state.workflow_page = "Pre-Consult Requirements"
            st.rerun()
    st.divider()
    st.caption("For demonstration only. Member-specific benefit verification is still required.")

if st.session_state.workflow_page == "Home":
    st.title("Bariatric Insurance Navigator")
    st.caption("Pre-consult insurance benefit, payer criteria, and bariatric program requirements")

    st.markdown(
        """
        ### Purpose
        This prototype is designed to standardize the information staff gather **before a bariatric consult**.
        It brings benefit verification, payer criteria, program standards, consult talking points, and a
        chart-ready PDF into one workflow.

        **Current prototype capabilities**
        - Capture bariatric benefit and authorization information
        - Review payer-specific bariatric requirements
        - Keep payer requirements distinguishable from bariatric program standards
        - Generate patient-facing consult talking points
        - Create a one-page chart PDF
        """
    )

    st.info(
        "This demo does not connect directly to payer portals, the EHR, or Banner systems. "
        "It is intended for workflow review and IT/security evaluation."
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Start Blank Demo →", type="primary", use_container_width=True):
            st.session_state.insurance_data = {}
            st.session_state.workflow_page = "Insurance Information"
            st.rerun()

    with c2:
        if st.button("Open Sample Test Case", use_container_width=True):
            st.session_state.insurance_data = {
                "patient_label": "TEST-001",
                "payer": "Arizona Complete Health (Centene)",
                "plan_name": "Demo Medicaid Plan",
                "state": "AZ",
                "member_id": "TEST-MEMBER-001",
                "group_number": "TEST-GROUP",
                "plan_type": "Medicaid",
                "employer_group": "Demo / Test Only",
                "benefit_verified": "Yes",
                "exclusion": "No",
                "prior_auth": "Yes",
                "coe": "Unknown",
                "rep_name": "Demo Representative",
                "reference": "DEMO-REF-001",
                "verification_date": date.today(),
                "auth_phone": "Test only",
                "auth_portal": "Test only",
                "facility_note": "",
                "deductible": "N/A - demo",
                "coinsurance": "N/A - demo",
                "oop": "N/A - demo",
                "benefit_notes": "Fictional sample case for demonstration. Do not use for patient care."
            }
            st.session_state.workflow_page = "Pre-Consult Requirements"
            st.rerun()

    st.divider()
    st.markdown("### Suggested Banner review")
    st.write(
        "Use the sample case to review the workflow without entering patient information. "
        "For production use, hosting, authentication, security, audit logging, data retention, and EHR integration "
        "should be reviewed with Banner IT/security/compliance."
    )

elif st.session_state.workflow_page == "Insurance Information":
    st.title("Bariatric Insurance Navigator")
    st.caption("Step 1 of 2 — Insurance Information")
    if st.button("← Back to Home"):
        st.session_state.workflow_page = "Home"
        st.rerun()

    st.info(
        "Use fictional/test information in this demo. This screen documents benefit and plan information "
        "gathered before the patient's bariatric consult."
    )
    st.subheader("Insurance Information")

    c1, c2, c3 = st.columns(3)

    with c1:
        patient_label = st.text_input("Patient label / test ID", placeholder="TEST-001")
        payer = st.selectbox("Insurance company", list(PAYER_DEFAULTS.keys()))
        plan_name = st.text_input("Plan name")
        state = st.text_input("State", value="AZ")

    with c2:
        member_id = st.text_input("Member ID / test member ID")
        group_number = st.text_input("Group number")
        plan_type = st.selectbox(
            "Plan type",
            ["Unknown", "Commercial", "HMO", "PPO", "EPO", "Exchange",
             "Medicare", "Medicare Advantage", "Medicaid", "Other"]
        )
        employer_group = st.text_input("Employer / group name")

    with c3:
        benefit_verified = st.selectbox("Bariatric benefit verified?", ["Unknown", "Yes", "No"])
        exclusion = st.selectbox("Bariatric surgery exclusion?", ["Unknown", "No", "Yes"])
        prior_auth = st.selectbox("Prior authorization required?", ["Unknown", "Yes", "No"])
        coe = st.selectbox("Center of Excellence / facility restriction?", ["Unknown", "No", "Yes"])

    st.markdown("### Benefit Verification Details")
    d1, d2, d3 = st.columns(3)

    with d1:
        rep_name = st.text_input("Representative name")
        reference = st.text_input("Call / chat reference #")
        verification_date = st.date_input("Verification date")

    with d2:
        auth_phone = st.text_input("Authorization phone")
        auth_portal = st.text_input("Authorization portal / vendor")
        facility_note = st.text_input("Facility / network restriction")

    with d3:
        deductible = st.text_input("Deductible / remaining")
        coinsurance = st.text_input("Coinsurance")
        oop = st.text_input("Out-of-pocket max / remaining")

    benefit_notes = st.text_area("Benefit notes", height=100)

    st.divider()
    if st.button("Continue to Pre-Consult Requirements →", type="primary", use_container_width=True):
        st.session_state.insurance_data = {
            "patient_label": patient_label,
            "payer": payer,
            "plan_name": plan_name,
            "state": state,
            "member_id": member_id,
            "group_number": group_number,
            "plan_type": plan_type,
            "employer_group": employer_group,
            "benefit_verified": benefit_verified,
            "exclusion": exclusion,
            "prior_auth": prior_auth,
            "coe": coe,
            "rep_name": rep_name,
            "reference": reference,
            "verification_date": verification_date,
            "auth_phone": auth_phone,
            "auth_portal": auth_portal,
            "facility_note": facility_note,
            "deductible": deductible,
            "coinsurance": coinsurance,
            "oop": oop,
            "benefit_notes": benefit_notes,
        }
        st.session_state.workflow_page = "Pre-Consult Requirements"
        st.rerun()

elif st.session_state.workflow_page == "Pre-Consult Requirements":
    st.title("Bariatric Insurance Navigator")
    st.caption("Step 2 of 2 — Pre-Consult Requirements")

    if st.button("← Back to Insurance Information", use_container_width=True):
        st.session_state.workflow_page = "Insurance Information"
        st.rerun()

    saved = st.session_state.get("insurance_data", {})
    if not saved:
        st.warning("Please complete Insurance Information first.")
        if st.button("Go to Insurance Information", type="primary"):
            st.session_state.workflow_page = "Insurance Information"
            st.rerun()
        st.stop()

    patient_label = saved.get("patient_label", "")
    payer = saved.get("payer", "Aetna")
    plan_name = saved.get("plan_name", "")
    state = saved.get("state", "AZ")
    member_id = saved.get("member_id", "")
    group_number = saved.get("group_number", "")
    plan_type = saved.get("plan_type", "Unknown")
    employer_group = saved.get("employer_group", "")
    benefit_verified = saved.get("benefit_verified", "Unknown")
    exclusion = saved.get("exclusion", "Unknown")
    prior_auth = saved.get("prior_auth", "Unknown")
    coe = saved.get("coe", "Unknown")
    rep_name = saved.get("rep_name", "")
    reference = saved.get("reference", "")
    verification_date = saved.get("verification_date", date.today())
    auth_phone = saved.get("auth_phone", "")
    auth_portal = saved.get("auth_portal", "")
    facility_note = saved.get("facility_note", "")
    deductible = saved.get("deductible", "")
    coinsurance = saved.get("coinsurance", "")
    oop = saved.get("oop", "")
    benefit_notes = saved.get("benefit_notes", "")

    d = PAYER_DEFAULTS[payer]

    st.subheader(f"Pre-Consult Bariatric Requirements — {payer}")
    st.caption(
        "Document the insurance requirements here before the patient's first visit. "
        "These are requirements to communicate to the patient — not completion tracking."
    )

    st.markdown(f"**Policy / source:** {d['policy']}")

    left, right = st.columns(2)

    with left:
        st.markdown("### Medical Weight-Loss / Visit Requirements")
        supervised = select_with_default(
            "Is a supervised / medically managed weight-loss program required?",
            ["Unknown", "No", "Yes"], d["supervised_required"]
        )
        duration = select_with_default(
            "Required duration / number of visits",
            ["Unknown", "Not required", "3 months", "4 months", "6 months",
             "12 months", "90 days", "12 visits", "Other"], d["duration"]
        )
        consecutive = select_with_default(
            "Do visits need to be consecutive?",
            ["Unknown", "No", "Yes", "Not specified"], d["consecutive"]
        )
        through_auth = select_with_default(
            "Must visits continue until authorization is submitted?",
            ["Unknown", "No", "Yes", "Not specified"], d["through_auth"]
        )
        time_window = select_with_default(
            "When must the visits/program occur?",
            ["Unknown", "Not specified", "Within 6 months", "Within 12 months",
             "Within 2 years", "Within 3 years", "Within 5 years", "Other"], d["time_window"]
        )
        weight_gain = select_with_default(
            "Can the patient gain weight during the program?",
            ["Unknown", "No", "Yes", "Not specified"], d["weight_gain"]
        )
        net_gain = select_with_default(
            "Is net weight gain allowed?",
            ["Unknown", "No", "Yes", "Not specified"], d["net_gain"]
        )
        obesity_history = st.text_input(
            "Required weight / obesity history",
            value=d["obesity_history"]
        )

        st.markdown("### Letter / Documentation Requirements")
        lmn = select_with_default(
            "Letter of Medical Necessity required?",
            ["Unknown", "No", "Yes", "Not specified"], d["lmn"]
        )
        lmn_pcp = select_with_default(
            "If required, must the LMN come from PCP?",
            ["Unknown", "No", "Yes", "Not specified"], d["lmn_pcp"]
        )

    with right:
        st.markdown("### Evaluations / Clearances")
        psych = select_with_default(
            "Psychological / behavioral health evaluation required?",
            ["Unknown", "No", "Yes", "Not specified"], d["psych"]
        )
        nutrition = select_with_default(
            "Nutritional evaluation required?",
            ["Unknown", "No", "Yes", "Not specified"], d.get("nutrition", "Unknown")
        )
        psych_window = select_with_default(
            "Psych evaluation validity window",
            ["Unknown", "Not specified", "6 months", "12 months", "Other"], d["psych_window"]
        )
        cardiology = select_with_default(
            "Cardiology clearance required?",
            ["Unknown", "No", "Yes", "Conditional", "Not specified"], d["cardiology"]
        )
        pulmonary = select_with_default(
            "Pulmonology clearance required?",
            ["Unknown", "No", "Yes", "Conditional", "Not specified"], d["pulmonary"]
        )
        pcp_default = d["pcp"] if d["pcp"] in ["Yes", "Conditional"] else "Program Standard"
        pcp = select_with_default(
            "PCP clearance required?",
            ["Unknown", "No", "Yes", "Conditional", "Program Standard", "Not specified"], pcp_default
        )

        st.markdown("### Testing / Other Requirements")
        egd_default = d["egd"] if d["egd"] in ["Yes", "Conditional"] else "Program Standard"
        egd = select_with_default(
            "EGD required?",
            ["Unknown", "No", "Yes", "Conditional", "Program Standard", "Not specified"], egd_default
        )
        sleep = select_with_default(
            "Sleep study required?",
            ["Unknown", "No", "Yes", "Conditional", "Not specified"], d["sleep"]
        )
        nicotine = select_with_default(
            "Nicotine test required?",
            ["Unknown", "No", "Yes", "Conditional", "Not specified"], d["nicotine"]
        )
        ekg = st.selectbox(
            "EKG required?",
            ["Program Standard", "Unknown", "No", "Yes", "Conditional", "Not specified"]
        )
        chest_xray = st.selectbox(
            "Chest X-ray required?",
            ["Program Standard", "Unknown", "No", "Yes", "Conditional", "Not specified"]
        )
        support = select_with_default(
            "Support group required?",
            ["Unknown", "No", "Yes", "Not specified"], d["support"]
        )
        logs = select_with_default(
            "Food / exercise logs required?",
            ["Unknown", "No", "Yes", "Not specified"], d["logs"]
        )

        labs = st.multiselect(
            "Required labs",
            [
                "Preop labs - CBC CMP — Program Standard",
                "TSH / T4",
                "A1C / glucose if diabetic",
                "Calcium", "Iron", "Folic acid", "Vitamin D", "Potassium",
                "Vitamin A", "Vitamin B1", "Vitamin B12", "Lipid panel", "Other"
            ],
            default=["Preop labs - CBC CMP — Program Standard"]
        )



    st.markdown("### Policy / Call Notes")
    policy_number = st.text_input("Policy / guideline number", value=d["policy"])
    policy_effective = st.text_input("Policy effective / review date")
    criteria_notes = st.text_area("Additional insurance criteria / notes", value=d["notes"], height=120)

    st.divider()
    st.markdown("## What to Communicate at the Consult")
    st.caption("This section turns the gathered insurance requirements into patient-facing talking points.")

    talking_points = []

    if benefit_verified == "Yes":
        talking_points.append("Bariatric surgery benefit was verified for the plan.")
    elif benefit_verified == "No":
        talking_points.append("Bariatric surgery benefit was not verified / is not covered based on current verification.")
    else:
        talking_points.append("Bariatric benefit still needs verification.")

    if exclusion == "Yes":
        talking_points.append("The plan has a bariatric surgery exclusion.")
    elif exclusion == "No":
        talking_points.append("No bariatric surgery exclusion was identified during verification.")

    if supervised == "Yes":
        detail = f"The insurance requires a supervised weight-loss program: {duration}."
        if consecutive not in ["Unknown", "Not specified"]:
            detail += f" Consecutive visits required: {consecutive}."
        if time_window not in ["Unknown", "Not specified"]:
            detail += f" Timing: {time_window}."
        talking_points.append(detail)
    elif supervised == "No":
        talking_points.append("The insurance does not require a supervised weight-loss program based on current verification.")

    if psych == "Yes":
        text = "A psychological / behavioral health evaluation is required."
        if psych_window not in ["Unknown", "Not specified"]:
            text += f" It is valid for {psych_window}."
        talking_points.append(text)

    if nutrition == "Yes":
        talking_points.append("A nutritional evaluation is required.")

    for label, value in [
        ("Cardiology clearance", cardiology),
        ("Pulmonology clearance", pulmonary),
        ("PCP clearance", pcp),
        ("Sleep study", sleep),
        ("Nicotine testing", nicotine),
        ("Support group", support),
        ("Food / exercise logs", logs),
    ]:
        if value == "Yes":
            talking_points.append(f"{label} is required.")
        elif value == "Conditional":
            talking_points.append(f"{label} may be required depending on clinical/plan criteria.")

    if labs:
        talking_points.append("Required labs: " + ", ".join(labs) + ".")

    for label, value in [
        ("EGD", egd),
        ("EKG", ekg),
        ("Chest X-ray", chest_xray),
    ]:
        if value == "Program Standard":
            talking_points.append(f"{label} is required by the bariatric program.")

    specialty_required_by_insurance = any(
        value in ["Yes", "Conditional"] for value in [cardiology, pulmonary]
    )
    if pcp == "Program Standard" and not specialty_required_by_insurance:
        talking_points.append(
            "PCP clearance is required by the bariatric program because no insurance-required specialty clearance is identified."
        )

    if coe == "Yes":
        talking_points.append("The plan has a Center of Excellence and/or facility restriction.")
    if prior_auth == "Yes":
        talking_points.append("Prior authorization is required.")

    for i, point in enumerate(talking_points, 1):
        st.write(f"{i}. {point}")

    patient_message = "\n".join([f"• {p}" for p in talking_points])
    st.text_area(
        "Consult communication summary",
        value=patient_message,
        height=220,
        help="Copy this into the consult workflow or use it as the insurance-requirement discussion guide."
    )

    st.divider()
    st.markdown("## Chart PDF")
    st.caption(
        "Create a one-page insurance criteria document similar to the clinic checklist "
        "for placement in the patient's chart."
    )

    pdf_data = {
        "patient_label": patient_label,
        "payer": payer,
        "plan_name": plan_name,
        "member_id": member_id,
        "group_number": group_number,
        "plan_type": plan_type,
        "state": state,
        "employer_group": employer_group,
        "benefit_verified": benefit_verified,
        "exclusion": exclusion,
        "prior_auth": prior_auth,
        "coe": coe,
        "rep_name": rep_name,
        "reference": reference,
        "verification_date": verification_date.strftime("%m/%d/%Y"),
        "auth_phone": auth_phone,
        "auth_portal": auth_portal,
        "facility_note": facility_note,
        "deductible": deductible,
        "coinsurance": coinsurance,
        "oop": oop,
        "benefit_notes": benefit_notes,
        "supervised": supervised,
        "duration": duration,
        "consecutive": consecutive,
        "through_auth": through_auth,
        "time_window": time_window,
        "weight_gain": weight_gain,
        "net_gain": net_gain,
        "obesity_history": obesity_history,
        "lmn": lmn,
        "lmn_pcp": lmn_pcp,
        "psych": psych,
        "nutrition": nutrition,
        "psych_window": psych_window,
        "cardiology": cardiology,
        "pulmonary": pulmonary,
        "pcp": pcp,
        "egd": egd,
        "sleep": sleep,
        "nicotine": nicotine,
        "ekg": ekg,
        "chest_xray": chest_xray,
        "support": support,
        "logs": logs,
        "labs": labs,
        "policy_number": policy_number,
        "policy_effective": policy_effective,
        "criteria_notes": criteria_notes,
    }

    pdf_bytes = build_chart_pdf(pdf_data)
    filename_label = patient_label.strip().replace(" ", "_") if patient_label.strip() else "patient"
    st.download_button(
        "Create / Download Chart PDF",
        data=pdf_bytes,
        file_name=f"{filename_label}_bariatric_insurance_criteria.pdf",
        mime="application/pdf",
        use_container_width=True
    )


else:
    st.session_state.workflow_page = "Home"
    st.rerun()
