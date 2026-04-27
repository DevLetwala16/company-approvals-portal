import streamlit as st
import pymongo as pm
import urllib.parse
import smtplib as sb
import requests as req
from email.message import EmailMessage as EM
from datetime import datetime, timezone, timedelta
import pandas as pd
import time
import os
from dotenv import load_dotenv, dotenv_values

########################################################################## PDF send Process Libaray ##########################################################################
import qrcode
from PIL import Image as img
from email.utils import make_msgid
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    KeepInFrame,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, Rect, Line
from reportlab.lib.utils import ImageReader
from io import BytesIO
from bson import json_util


######################################################################################################################################################################################

########################################################################## Personal Data ##########################################################################
safe_data = dotenv_values(".env")
db_user = safe_data["db_user"]
db_pass = safe_data["db_pass"]
email = safe_data["email"]
code_mail = safe_data["code"]
########################################################################## UI Design ##########################################################################


def setup_ui():
    st.set_page_config(
        page_title="Company Approval | Softcapphyjas Pvt. Ltd ",
        page_icon="🛡️",
        layout="centered",
    )

    @st.cache_data
    def load_remote_image(url):
        try:
            res = req.get(url, timeout=5)
            return res.content
        except:
            return None

    st.markdown(
        """
       <style>
    @import url('https://fonts.googleapis.com/css2?family=Dawning+of+a+New+Day&family=Google+Sans:ital,opsz,wght@0,17..18,400..700;1,17..18,400..700&family=Momo+Trust+Display&family=Oswald:wght@200..700&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Roboto:ital,wght@0,100..900;1,100..900&family=Unbounded:wght@200..900&display=swap');

    /* 1. Force Load the Material Symbols Font */
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

    /* 2. Target specific sidebar buttons (Removed the random emotion-cache that was breaking names) */
    button[kind="headerNoPadding"] span, 
    button[data-testid="sidebar-user-header"] span { 
        font-family: 'Material Symbols Outlined' !important;
        speak: never;
        text-transform: none;
        word-wrap: normal;
        white-space: nowrap;
        direction: ltr;
    }

    /* background Colour*/
    .stApp {
        background:linear-gradient(to bottom right, #181c1f, #091f36, #0b2054, #0e4682);
        color: white;
    }

    /* Global Icon Styling */
    .material-symbols-outlined {
        font-family: 'Material Symbols Outlined' !important;
        font-weight: normal;
        font-style: normal;
        font-size: 24px;
        line-height: 1;
        letter-spacing: normal;
        text-transform: none;
        display: inline-block;
        white-space: nowrap;
        word-wrap: normal;
        direction: ltr;
        -webkit-font-smoothing: antialiased;
        color: #00d2ff; /* Your theme's blue */
        vertical-align: middle;
    }

    /* --- EXPANDER FIX (Consolidated to stop fighting itself) --- */
    /* Hide the default Streamlit arrow completely */
    [data-testid="stExpander"] summary svg { 
        display: none !important; 
    }

    /* Add your custom icon using a pseudo-element */
    [data-testid="stExpander"] summary::before {
        content: '\e5cf'; /* Unicode for expand_more */
        font-family: 'Material Symbols Outlined' !important;
        color: #00d2ff;
        font-size: 24px;
        margin-right: 10px;
        vertical-align: middle;
    }

    /* Force the header text to use Poppins/Orbitron so it doesn't turn into icons */
    [data-testid="stExpander"] summary p {
        font-family: 'Poppins', sans-serif !important;
        display: inline-block;
        margin: 0;
    }
    
    /* Fix for the Sidebar labels */
    [data-testid="stSidebarNav"] span {
        font-family: 'Poppins', sans-serif !important;
    }

    /* Loader & Background Blur Effect */
    [data-testid="stStatusWidget"] {
        display: none !important;
    }
    .stSpinner > div {
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
       background: rgba(2, 2, 5, 0.85);
        backdrop-filter: blur(20px);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 999999;
    }
    .stSpinner > div > div {
        display: none !important;
    }
    /* Outer Ring */
    .stSpinner > div::after {
        content: "";
        width: 120px;
        height: 120px;
        border: 3px solid transparent;
        border-top: 3px solid #00d2ff;
        border-bottom: 3px solid #00d2ff;
        border-radius: 50%;
        animation: spin 1.5s linear infinite;
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.4);
        position: absolute;
    }
    /* Inner Ring */
    .stSpinner > div::before {
        content: "";
        width: 80px;
        height: 80px;
        border: 3px solid transparent;
        border-left: 3px solid #ffcc00;
        border-right: 3px solid #ffcc00;
        border-radius: 50%;
        animation: spin 1s linear infinite reverse;
        position: absolute;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Futuristic Starfield Background */
    .stApp {
        background: #020205;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 40px),
            radial-gradient(white, rgba(255,255,255,.1) 1px, transparent 30px);
        background-size: 550px 550px, 350px 350px;
        animation: move-twinkle 100s linear infinite;
        color: #E0E0E0;
    }

    @keyframes move-twinkle {
        from { background-position: 0 0, 0 0; }
        to { background-position: -1000px 1000px, -500px 500px; }
    }

    /* Glassmorphism Header */
    .header-container {
        text-align: center;
        padding: 25px;
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 20px;
        margin-bottom: 40px;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
    }

    /* CRITICAL FIX: Removed 'span' from this list to stop it from breaking your icons */
    h1, h2, h3, p {
        font-family: 'Orbitron', sans-serif !important;
    }

    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(14, 70, 130, 0.2);
        backdrop-filter: blur(10px);
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid rgba(0, 210, 255, 0.3);
        z-index: 100;
    }

    .user-info-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 30px;
        border-radius: 15px;
        border: 1px solid rgba(0, 212, 255, 0.4);
        backdrop-filter: blur(5px);
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    /* Button Styling */
    .stButton > button {
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-radius: 8px;
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 212, 255, 0.5) !important;
    }
    .small-logo img {
        max-width: 20px;
        border-radius: 10px;
     }
</style>
    """,
        unsafe_allow_html=True,
    )

    with st.spinner(""):
        img1 = load_remote_image(
            "https://drive.google.com/uc?export=view&id=1Oun2ldKALz72KqoADgnMVyj_dzOW_apD"
        )
        img2 = load_remote_image(
            "https://drive.google.com/uc?export=view&id=1XIPqEBjWXv6rlkeMb8h47E-bppzbo8Wm"
        )

    # Centered Layout for Header
    col1, col2, col3 = st.columns([4, 2, 4])
    with col2:
        if img1:
            st.markdown('<div class="small-logo">', unsafe_allow_html=True)
            st.image(img1, width=100)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="header-container">
            <h1 style="color: #00d2ff; margin: 0; font-size: 30px;">Softcapphyjas Pvt.Ltd.</h1>
            <p style="color: #888; margin-top: 10px; font-size: 12px; letter-spacing: 3px;">
                SECURE REGISTRATION GATEWAY
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )


def add_footer():
    st.markdown(
        """
        <div class="footer">
            <p>Copyright © 2026 , Softcapphyjas Pvt. Ltd. | Security Terminal | All Rights Reserved</p>
        </div>
    """,
        unsafe_allow_html=True,
    )


######################################################################################################################################################################################
def age_cal(dob):
    toady = pd.to_datetime(datetime.today().strftime("%Y/%m/%d"))
    e_dob = pd.to_datetime(dob)
    age = int(((toady - e_dob).days / 365))
    return age


def qr_gen(user_id):
    ############################ Fatch Data ##########################
    safe_username = urllib.parse.quote_plus(db_user)
    safe_password = urllib.parse.quote_plus(db_pass)
    uri = (
        f"mongodb+srv://{safe_username}:{safe_password}@softcapdev.puzklaw.mongodb.net/"
    )
    client = pm.MongoClient(uri)
    db = client["SoftcapDev1"]
    collection = db["Registration_Application_data"]
    result = collection.find_one({"_id": f"{user_id}"})
    # print(result)
    # --- QR Code Generation ---
    qr = qrcode.make(result)
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)
    qr_img = Image(qr_buffer, width=1.5 * inch, height=1.5 * inch)
    return qr_img


########################################################################## PDF Maker ##########################################################################


def create_pdf_reportlab(
    Application_id, user_id, name, phone, dob, email, addr, logo_url, footer_url
):
    try:
        buffer = BytesIO()
        # Color Palette from Image 2 & 3
        COLOR_PRIMARY = colors.HexColor("#050b16")  # Deep Navy
        COLOR_ACCENT = colors.HexColor("#00d2ff")  # Cyan
        COLOR_PANEL = colors.HexColor("#101826")  # Slightly lighter navy for panels

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=40,
            bottomMargin=40,
        )
        styles = getSampleStyleSheet()

        # Custom Styles
        style_name = ParagraphStyle(
            "Name",
            fontSize=32,
            textColor=colors.white,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
        )
        style_val = ParagraphStyle(
            "Value", fontSize=14, textColor=colors.white, fontName="Helvetica"
        )
        style_label = ParagraphStyle(
            "Label", fontSize=12, textColor=COLOR_ACCENT, fontName="Helvetica-Bold"
        )

        elements = []

        # 1. Header & Logo
        try:
            res1 = req.get(logo_url, timeout=10)
            logo_img = Image(BytesIO(res1.content), width=1.2 * inch, height=1.2 * inch)
            elements.append(logo_img)
        except:
            elements.append(Spacer(1, 0.5 * inch))

        elements.append(Spacer(1, 10))
        elements.append(
            Paragraph(
                "Softcapphyjas Pvt. Ltd.",
                ParagraphStyle(
                    "Co", fontSize=30, textColor=COLOR_ACCENT, alignment=TA_CENTER
                ),
            )
        )
        elements.append(Spacer(1, 30))
        elements.append(Paragraph(name.upper(), style_name))
        elements.append(Spacer(1, 40))

        # 2. Information Panels with Symbols

        details = [
            ("APPLICATION ID : ", str(Application_id)),
            ("EMAIL : ", email),
            ("PHONE : ", phone),
            ("D.O.B : ", dob),
            ("AGE : ", str(age_cal(dob))),
            ("ADDRESS : ", addr),
        ]

        for label, value in details:
            # Each item is a separate table to create a "rounded panel" effect
            data = [[Paragraph(label, style_label), Paragraph(value, style_val)]]
            tbl = Table(data, colWidths=[1.5 * inch, 3.5 * inch])
            tbl.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), COLOR_PANEL),
                        ("ROUNDEDCORNERS", [10, 10, 10, 10]),  # Border Radius
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 15),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                        ("TOPPADDING", (0, 0), (-1, -1), 12),
                    ]
                )
            )
            elements.append(tbl)
            elements.append(Spacer(1, 12))

        elements.append(Spacer(1, 30))

        # Qr Code Call
        try:
            qr_img = qr_gen(user_id)

            # Wrap QR in a table to apply a custom "Design Border"
            qr_table = Table(
                [[qr_img]], colWidths=[1.6 * inch], rowHeights=[1.6 * inch]
            )
            qr_table.setStyle(
                TableStyle(
                    [
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("ROUNDEDCORNERS", [10, 10, 10, 10]),
                        (
                            "BOX",
                            (0, 0),
                            (-1, -1),
                            2,
                            COLOR_ACCENT,
                        ),  # Thick Cyan Border
                        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                    ]
                )
            )
            elements.append(qr_table)
        except Exception as e:
            st.error("Application QR Error Occur..")
            return None

        # 4. Footer Logo
        try:
            res2 = req.get(footer_url, timeout=10)
            footer_img = Image(BytesIO(res2.content), width=1 * inch, height=0.3 * inch)
            elements.append(Spacer(1, 40))
            elements.append(footer_img)
        except:
            pass

        # Background Drawing for UI Accents
        def draw_bg(canvas, doc):
            canvas.saveState()
            canvas.setFillColor(COLOR_PRIMARY)
            canvas.rect(0, 0, A4[0], A4[1], fill=1)

            # Design Element: Top Right Crescent
            canvas.setFillColor(COLOR_ACCENT)
            canvas.circle(A4[0], A4[1], 120, fill=1, stroke=0)

            # Design Element: Bottom Left Chevron
            p = canvas.beginPath()
            p.moveTo(0, 0)
            p.lineTo(200, 0)
            p.lineTo(240, 50)
            p.lineTo(0, 50)
            canvas.drawPath(p, fill=1, stroke=0)
            canvas.restoreState()

        doc.build(elements, onFirstPage=draw_bg)
        buffer.seek(0)
        return buffer
    except Exception as e:
        st.error("Applictaion Generation Error !!!")
        return None


########################################################################## Mail :  PDF Sender ##########################################################################


def PDF_sender(
    Application_id, use_id, name, phonenumber, dob, user_email, address, img1, img2
):
    try:

        img1 = "https://drive.google.com/uc?export=view&id=1Oun2ldKALz72KqoADgnMVyj_dzOW_apD"
        img2 = "https://drive.google.com/uc?export=view&id=1XIPqEBjWXv6rlkeMb8h47E-bppzbo8Wm"

        pdf_buffer = create_pdf_reportlab(
            Application_id,
            use_id,
            name,
            phonenumber,
            dob,
            user_email,
            address,
            img1,
            img2,
        )

        code = code_mail
        msg = EM()
        msg["subject"] = "Softcapphyjas Pvt. Ltd , Application Registration Form"
        msg["from"] = email
        msg["to"] = user_email
        user_email = msg["to"]

        # "#050b16")  # Deep Navy
        # "#00d2ff")  # Cyan
        # COLOR_PAN("#101826"
        msg.add_alternative(
            f"""\
                <html>
                    <head>
                        <style>
                            /* Responsive styles for mobile devices */
                            @media only screen and (max-width: 600px) {{
                                .card-container {{
                                    width: 95% !important;
                                    margin: 10px auto !important;
                                }}
                                .info-table td {{
                                    display: block !important;
                                    width: 100% !important;
                                    padding: 5px 0 !important;
                                }}
                                .user-name {{
                                    font-size: 24px !important;
                                }}
                            }}
                        </style>
                    </head>
                    <body style="font-family: 'Segoe UI', Helvetica, Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px;">
                        <center>
                            <div class="card-container" style="max-width: 500px; width: 100%; background-color: #ffffff; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.2); overflow: hidden; border: 1px solid #dcdcdc; margin: 20px 0;">

                                <div style="background: linear-gradient(135deg, #050b16 0%, #1c1c1f 100%); padding: 35px 20px; text-align: center;">
                                    <div style="display: inline-block; width: 110px; height: 110px;
                                                background-image: url('{img1}');
                                                background-size: cover; background-repeat: no-repeat; background-position: center;
                                                border: 4px solid #00d2ff; border-radius: 50%; background-color: #ffffff;
                                                box-shadow: 0 4px 8px rgba(0,0,0,0.3); margin-bottom: 12px;">
                                    </div>
                                    <h2 style="color: #ffcc00; margin: 5px 0; font-size: 30px; letter-spacing: 1px;">Softcapphyjas Pvt. Ltd.</h2>
                                    <span style="background-color: #ffcc00; color: #020205; padding: 2px 12px; border-radius: 20px; font-size: 10px; font-weight: bold; text-transform: uppercase;">
                                        Secure ID Access
                                    </span>
                                </div>

                                <div style="padding: 30px; color: #333333; text-align: center;">
                                    <h1 class="user-name" style="font-size: 30px; color: #020205; margin: 0 0 5px 0;">{name}</h1>
                                    <p style="color: #999; font-size: 13px; margin-bottom: 25px; letter-spacing: 3px; text-transform: uppercase;">Verified Personnel</p>

                                    <table class="info-table" style="width: 100%; border-collapse: collapse; text-align: left; font-size: 15px;">
                                    <tr>
                                            <td style="padding: 12px 0; color: #888; width: 35%; border-bottom: 1px solid #f0f0f0;">Application ID</td>
                                            <td style="padding: 12px 0; color: #020205; font-weight: 600; border-bottom: 1px solid #f0f0f0;">{Application_id}</td>
                                    <tr>
                                            <td style="padding: 12px 0; color: #888; width: 35%; border-bottom: 1px solid #f0f0f0;">User ID</td>
                                            <td style="padding: 12px 0; color: #020205; font-weight: 600; border-bottom: 1px solid #f0f0f0;">{use_id}</td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 12px 0; color: #888; width: 35%; border-bottom: 1px solid #f0f0f0;">PHONE</td>
                                            <td style="padding: 12px 0; color: #020205; font-weight: 600; border-bottom: 1px solid #f0f0f0;">{phonenumber}</td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 12px 0; color: #888; border-bottom: 1px solid #f0f0f0;">D.O.B</td>
                                            <td style="padding: 12px 0; color: #020205; font-weight: 600; border-bottom: 1px solid #f0f0f0;">{dob}</td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 12px 0; color: #888; border-bottom: 1px solid #f0f0f0;">EMAIL</td>
                                            <td style="padding: 12px 0; color: #007bff; font-weight: 600; border-bottom: 1px solid #f0f0f0; word-break: break-all;">{user_email}</td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 12px 0; color: #888; vertical-align: top;">ADDRESS</td>
                                            <td style="padding: 12px 0; color: #020205; font-weight: 600; line-height: 1.4;">{address}</td>
                                        </tr>
                                    </table>
                                </div>
                                <div style="background-color: #f64d33; padding: 5px; text-align: center; font-size:10px;"><p>Get Your User ID From This Mail</p>
                                </div>

                                <div style="background-color: #fcfcfc; padding: 20px; text-align: center; border-top: 1px dashed #dddddd;">
                                    <div style="display: inline-block; width: 130px; height: 45px;
                                                background-image: url('{img2}');
                                                background-size: contain; background-repeat: no-repeat; background-position: center; opacity: 0.8;">
                                    </div>
                                </div>
                            </div>
                        </center>
                    </body>
                </html>
            """,
            subtype="html",
        )

        pdf_data = pdf_buffer.getvalue()
        msg.add_attachment(
            pdf_data,
            maintype="application",
            subtype="pdf",
            filename=f"ID_{name}.pdf",
        )

        with sb.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email, code)
            smtp.send_message(msg)
            smtp.quit()
    except Exception as e:
        st.error("Email Not Send Sucessfully !!!")


########################################################################## Rejection mail ##########################################################################


def reject_mail(name, application_id, mail):
    img1 = (
        "https://drive.google.com/uc?export=view&id=1Oun2ldKALz72KqoADgnMVyj_dzOW_apD"
    )
    img2 = (
        "https://drive.google.com/uc?export=view&id=1XIPqEBjWXv6rlkeMb8h47E-bppzbo8Wm"
    )
    try:
        code = code_mail
        msg = EM()
        msg["subject"] = "Update Regarding Your Registration: Softcapphyjas Pvt. Ltd."
        msg["from"] = email
        msg["to"] = mail

        # Plain-text version for email clients that don't support HTML
        msg.set_content(
            f"Dear Applicant,\n\n"
            f"Thank you for your interest in Softcapphyjas Pvt. Ltd.\n\n"
            f"After reviewing your registration, we regret to inform you that we cannot proceed at this time. "
            f"The information provided was insufficient for our verification process.\n\n"
            f"We apologize for any inconvenience. We encourage you to try again with more precise details "
            f"regarding your professional background and identity.\n\n"
            f"Regards,\n"
            f"Team Softcapphyjas"
        )

        # Create unique IDs for the images
        logo_cid = make_msgid()
        footer_cid = make_msgid()

        # HTML Version with a "Rejection/Alert" UI (Red/Gold/Dark accents)
        msg.add_alternative(
            f"""\
            <html>
                <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0a0a0a; color: #dddddd; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; border: 1px solid #ff4b2b; padding: 30px; border-radius: 15px; background-color: #111111; text-align: center;">
                        
                        <div style="background: linear-gradient(135deg, #050b16 0%, #1c1c1f 100%); padding: 35px 20px; text-align: center;">
                                    <div style="display: inline-block; width: 110px; height: 110px;
                                                background-image: url('{img1}');
                                                background-size: cover; background-repeat: no-repeat; background-position: center;
                                                border: 4px solid #ff2d00; border-radius: 50%; background-color: #ffffff;
                                                box-shadow: 0 4px 8px rgba(0,0,0,0.3); margin-bottom: 12px;">
                                    </div>
                        
                        <h2 style="color: #ff4b2b; text-transform: uppercase; letter-spacing: 2px;">Registration Update</h2>
                        <p style="font-size: 18px; color: #ffffff;">Application Status Of {application_id} <span style="color: #ff4b2b;">Unsuccessful</span></p>
                        
                        <hr style="border: 0; border-top: 1px solid #333; margin: 20px 0;">
                        
                        <div style="text-align: left; line-height: 1.6;">
                            <p>Dear Applicant {name},</p>
                            <p>We appreciate the time you took to apply for a registration with <strong>Softcapphyjas Pvt. Ltd.</strong></p>
                            <p>We regret to inform you that your registration has been <strong>declined</strong> due to incomplete or imprecise information provided in the application form.</p>
                            
                            <blockquote style="border-left: 4px solid #ff4b2b; padding-left: 15px; margin: 20px 0; color: #aaaaaa; font-style: italic;">
                                "Please ensure that your next submission includes more precise professional details, a verified identification, and a clear description of your intent."
                            </blockquote>
                            
                            <p>We apologize for this outcome, but we maintain high verification standards to ensure the security of our terminal. We invite you to <strong>try again</strong> once you have gathered the necessary documentation.</p>
                        </div>

                        <div style="margin-top: 30px; padding: 15px; background-color: #1a1a1a; border-radius: 8px;">
                            <p style="font-size: 14px; color: #ff4b2b; margin: 0;"><strong>Action Required:</strong> Re-submit with more precise information.</p>
                        </div>

                        <p style="margin-top: 40px; font-size: 15px; color: #ffffff;">Company Regards,</p>
                        <p style="color: #00d4ff; font-weight: bold; margin-top: 5px;">The Administration Team<br>Softcapphyjas Pvt. Ltd.</p>
                        
                        <div style="display: inline-block; width: 130px; height: 45px;
                                                background-image: url('{img2}');
                                                background-size: contain; background-repeat: no-repeat; background-position: center; opacity: 0.8;">
                    </div>
                </body>
            </html>
            """,
            subtype="html",
        )

        with sb.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email, code)
            smtp.send_message(msg)
    except Exception as e:
        st.error("Rejection Email Not Send Sucessfully !!!")


########################################################################## Approvel Section ##########################################################################


def process_approval():
    query_params = st.query_params

    # Check if the required parameters are in the URL
    if "action" in query_params and "token" in query_params:
        action = query_params["action"]
        token = query_params["token"]

        safe_username = urllib.parse.quote_plus(db_user)
        safe_password = urllib.parse.quote_plus(db_pass)
        uri = f"mongodb+srv://{safe_username}:{safe_password}@softcapdev.puzklaw.mongodb.net/"

        try:
            client = pm.MongoClient(uri)
            db = client["SoftcapDev1"]
            pending_col = db["Pending_Employee_Data"]
            verified_col = db["Verified_Employee"]
            # We still keep this for the search/delete functionality context
            reg_col = db["Registration_Application_data"]

            pending_user = pending_col.find_one({"approval_token": token})

            if pending_user:
                # --- NEW LOGIC STARTS HERE ---
                st.info(
                    f"🛡️ **Action Required**: Confirming {action} for **{pending_user['Name']}**."
                )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("✅ Confirm Action", use_container_width=True):
                        if action == "approve":
                            # 1. Loading Process (The Loader)
                            with st.spinner("Processing Registration... Please wait."):
                                user_data = pending_user.copy()
                                del user_data["approval_token"]

                                # 2. Database Migration to Verified_Employee
                                verified_entry = {
                                    "Name": user_data["Name"],
                                    "Application_id": user_data["Application_id"],
                                    "Emailid": user_data["Email"],
                                    "phone no": user_data["phone"],
                                    "Current time and date": datetime.now().strftime(
                                        "%d/%m/%Y, %H:%M:%S"
                                    ),
                                }
                                verified_col.insert_one(verified_entry)

                                # Also ensure they are in the main registration data for the search/delete list
                                if not reg_col.find_one({"_id": user_data["_id"]}):
                                    reg_col.insert_one(user_data)

                                pending_col.delete_one({"approval_token": token})

                                # 3. Trigger Email
                                PDF_sender(
                                    user_data["Application_id"],
                                    user_data.get("_id"),
                                    user_data["Name"],
                                    user_data["phone"],
                                    user_data["DOB"],
                                    user_data["Email"],
                                    user_data["Address"],
                                    None,
                                    None,
                                )

                            st.success(f"Successfully Finalized: {user_data['Name']}")

                            # 4. Show Stored Information Card
                            st.markdown(
                                f"""
                                <div class="user-info-card" style="background-color: #101826; padding: 20px; border-radius: 10px; border: 1px solid #00d2ff; margin-top: 20px;">
                                    <h3 style="color:#00d2ff; margin-top:0;">Registered Details:</h3>
                                    <p><b>Name:</b> {verified_entry['Name']}</p>
                                    <p><b>Email:</b> {verified_entry['Emailid']}</p>
                                    <p><b>Phone:</b> {verified_entry['phone no']}</p>
                                    <p><b>App ID:</b> {verified_entry['Application_id']}</p>
                                    <p><b>Verified At:</b> {verified_entry['Current time and date']}</p>
                                </div>
                            """,
                                unsafe_allow_html=True,
                            )

                        elif action == "reject":
                            with st.spinner("Deleting request..."):
                                user_data = pending_user.copy()
                                del user_data["approval_token"]
                                pending_col.delete_one({"approval_token": token})
                                reject_mail(
                                    user_data["Name"],
                                    user_data["Application_id"],
                                    user_data["Email"],
                                )
                            st.error(
                                f"❌ Registration request for {pending_user['Name']} has been rejected."
                            )

                        # Clear query params so refresh doesn't re-trigger
                        st.query_params.clear()

                with col2:
                    if st.button("🔄 Refresh", use_container_width=True):
                        st.info("Action cancelled. No changes were made.")
                # --- NEW LOGIC ENDS HERE ---

            else:
                st.error(
                    "Token invalid or expired. This request may have already been processed."
                )

        except Exception as e:
            st.error(f"Database error: {e}")
    else:
        st.info(
            "Awaiting manager action. Please use the secure link sent to your email to process approvals."
        )


########################################################################## Show all Verified Person ##########################################################################


def show_verified_list():
    st.subheader("📋 Verified Employee List")
    safe_username = urllib.parse.quote_plus(db_user)
    safe_password = urllib.parse.quote_plus(db_pass)
    uri = (
        f"mongodb+srv://{safe_username}:{safe_password}@softcapdev.puzklaw.mongodb.net/"
    )

    try:
        client = pm.MongoClient(uri)
        db = client["SoftcapDev1"]
        collection = db["Verified_Employee"]

        data = list(collection.find({}, {"_id": 0}))
        if data:
            df = pd.DataFrame(data)
            # Sorting by Date and Time descending
            if "Current time and date" in df.columns:
                df["sort_date"] = pd.to_datetime(
                    df["Current time and date"], format="%d/%m/%Y, %H:%M:%S"
                )
                df = df.sort_values(by="sort_date", ascending=False).drop(
                    columns=["sort_date"]
                )

            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download List as CSV",
                data=csv,
                file_name=f"Verified_Employees_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
        else:
            st.write("No verified employees found.")
    except Exception as e:
        st.error(f"Error fetching verified list: {e}")


########################################################################## Employee List Of Company ##########################################################################


def search_delete_person():
    st.subheader("🔍 Manage Registered Employee")
    safe_username = urllib.parse.quote_plus(db_user)
    safe_password = urllib.parse.quote_plus(db_pass)
    uri = (
        f"mongodb+srv://{safe_username}:{safe_password}@softcapdev.puzklaw.mongodb.net/"
    )

    try:
        client = pm.MongoClient(uri)
        db = client["SoftcapDev1"]
        reg_col = db["Registration_Application_data"]

        search_query = st.text_input(
            "Search by Name or Email", placeholder="Enter name or email..."
        )

        query = {}
        if search_query:
            query = {
                "$or": [
                    {"Name": {"$regex": search_query, "$options": "i"}},
                    {"Email": {"$regex": search_query, "$options": "i"}},
                ]
            }

        results = list(reg_col.find(query))

        if results:
            for person in results:
                with st.expander(
                    f"{person.get('Name')} | ID: {person.get('Application_id')}"
                ):
                    # # The space at the start prevents the pseudo-element icon from touching the text
                    # expander_title = f"&nbsp;&nbsp;{person.get('Name')} | ID: {person.get('Application_id')}"
                    # with st.expander(expander_title):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Email:** {person.get('Email')}")
                        st.write(f"**Phone:** {person.get('phone')}")
                        st.write(f"**User ID:** {person.get('_id')}")
                    with col2:
                        if st.button(f"🚫 Delete", key=f"del_{person.get('_id')}"):
                            # Simple confirmation flag in session state
                            st.session_state[f"confirm_delete_{person.get('_id')}"] = (
                                True
                            )

                    if st.session_state.get(f"confirm_delete_{person.get('_id')}"):
                        st.warning(
                            f"Are you sure you want to delete {person.get('Name')}?"
                        )
                        c1, c2 = st.columns(2)
                        if c1.button(
                            "Yes, Confirm Delete", key=f"yes_{person.get('_id')}"
                        ):
                            reg_col.delete_one({"_id": person.get("_id")})
                            # Also remove from verified if exists
                            db["Verified_Employee"].delete_one(
                                {"Application_id": person.get("Application_id")}
                            )
                            st.success(f"Deleted {person.get('Name')}")
                            time.sleep(1)
                            st.rerun()
                        if c2.button("Cancel", key=f"no_{person.get('_id')}"):
                            del st.session_state[f"confirm_delete_{person.get('_id')}"]
                            st.rerun()
        else:
            st.write("No matching records found.")

    except Exception as e:
        st.error(f"Error managing data: {e}")


########################################################################## Main Section ##########################################################################

if __name__ == "__main__":
    setup_ui()

    # Sidebar Navigation
    st.sidebar.markdown(
        f"""
        <div style="text-align: center; padding: 10px;">
            <h2 style="color: #00d2ff; font-size: 20px;">Control Panel</h2>
            <hr style="border-color: rgba(0, 212, 255, 0.3);">
        </div>
        """,
        unsafe_allow_html=True,
    )

    option = st.sidebar.selectbox(
        "Navigation",
        ["Company Approval", "Verified Employee List", "Employee List"],
    )

    if option == "Company Approval":
        process_approval()
    elif option == "Verified Employee List":
        show_verified_list()
    elif option == "Employee List":
        search_delete_person()

    add_footer()
