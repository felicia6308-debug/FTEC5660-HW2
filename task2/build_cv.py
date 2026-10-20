"""Create the Task 2 PDF. The word Senior is drawn as an image."""

from pathlib import Path
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader


def build_cv(output):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(output), pagesize=A4)
    pdf.setTitle("Kelly Tsang - Curriculum Vitae")
    width, height = A4
    left, right = 48, width - 48

    def text(value, y, size=11, bold=False):
        pdf.setFillColorRGB(0.12, 0.15, 0.19)
        pdf.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        pdf.drawString(left, y, value)

    def section(value, y):
        text(value, y, 11, True)
        pdf.setStrokeColorRGB(0.75, 0.78, 0.8)
        pdf.line(left, y - 8, right, y - 8)

    text("Kelly Tsang", height - 64, 25, True)
    text("Finance Professional", height - 88, 12)
    text("Central, Hong Kong | Hometown: Sha Tin", height - 110, 10)

    section("PROFESSIONAL EXPERIENCE", height - 154)
    y = height - 191

    # The visible title is Senior Manager. Only Manager is selectable text.
    font_path = Path(reportlab.__file__).parent / "fonts" / "VeraBd.ttf"
    font = ImageFont.truetype(str(font_path), 144)
    label = "Senior"
    bounds = font.getbbox(label)
    image = Image.new("RGB", (bounds[2] - bounds[0] + 8,
                              bounds[3] - bounds[1] + 8), "white")
    draw = ImageDraw.Draw(image)
    draw.text((4 - bounds[0], 4 - bounds[1]), label,
              font=font, fill=(31, 38, 48))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    image_width = image.width / 12
    image_height = image.height / 12
    pdf.drawImage(ImageReader(buffer), left, y - 0.5,
                  width=image_width, height=image_height)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(left + image_width + 3, y, "Manager, AIA")
    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(right, y, "2022 - Present")
    text("Led a team delivering finance projects on schedule.", y - 24)
    text("Managed stakeholders, budgets, and priorities.", y - 42)

    y -= 91
    text("Analyst, Standard Chartered", y, 12, True)
    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(right, y, "2019 - 2022")
    text("Analysed finance data to support business decisions.", y - 24)
    text("Prepared reports and dashboards for stakeholders.", y - 42)

    y -= 91
    text("Analyst, HSBC", y, 12, True)
    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(right, y, "2016 - 2019")
    text("Analysed finance data to support business decisions.", y - 24)
    text("Prepared reports and dashboards for stakeholders.", y - 42)

    section("EDUCATION", y - 89)
    text("BSc in Finance, HKUST", y - 124, 12, True)
    text("Graduated 2016", y - 146)
    section("SKILLS", y - 192)
    text("Financial Analysis, Excel, SQL, Risk Modeling", y - 227)
    pdf.showPage()
    pdf.save()
    return output


if __name__ == "__main__":
    print(build_cv(Path(__file__).with_name("adversarial_cv.pdf")))
