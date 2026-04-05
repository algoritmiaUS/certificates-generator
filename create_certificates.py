import argparse
import csv
import os
import re
import subprocess
from dotenv import load_dotenv

import img2pdf
from tqdm import tqdm

load_dotenv()

DATE = os.environ["DATE"]
COMPETITION_DATE = os.environ["COMPETITION_DATE"]
TEMPLATE_PATH = os.getenv("TEMPLATE_PATH", "./templates/{name}.svg")
FONT_PATH = os.getenv("FONT_PATH", "./fonts/Baskervville-Regular.ttf")
FONT_NAME = os.getenv("FONT_NAME", "Baskervville")
CSV_FILE_PATH = os.getenv("CSV_FILE_PATH", "./data/participants.csv")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./out/")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "{prefix}_" + DATE + "_{name}.pdf")

PARTICIPANT_ACHIEVEMENT = "haber participado"
WINNERS_ACHIEVEMENTS = (
    "obtener la medalla de oro",
    "obtener la medalla de plata",
    "obtener la medalla de bronce",
)

LOG_PATH = f"./{DATE}_certificates.log"

img2pdf.logger.disabled = True


def generate_certificate(
    name: str,
    output_path: str,
    template: str,
    achievement: str,
    stdout=subprocess.DEVNULL,
):
    """Generate certificate with the given name and achievement."""

    tmp_svg_path = output_path + ".tmp"
    tmp_png_path = output_path + ".png"

    with open(tmp_svg_path, "w", encoding="utf-8") as tmp:
        tmp.write(
            template.replace("[Nombre del destinatario]", name)
            .replace("[logro alcanzado]", achievement)
            .replace("[fecha competicion]", COMPETITION_DATE)
        )

    subprocess.call(
        args=[
            "resvg",
            tmp_svg_path,
            tmp_png_path,
            "--use-font-file",
            FONT_PATH,
            "--font-family",
            FONT_NAME,
        ],
        stdout=stdout,
    )

    os.remove(tmp_svg_path)
    with open(tmp_png_path, "rb") as png_file, open(output_path, "wb") as output_file:
        output_file.write(img2pdf.convert(png_file))

    os.remove(tmp_png_path)


def sign_certificate(file_path: str, signer_id: str, stdout=subprocess.DEVNULL):
    """Sign the .pdf certificate with the given file path."""

    res = subprocess.call(
        args=[
            "autofirmacommandline",
            "sign",
            "-i",
            file_path,
            "-o",
            file_path.replace(".pdf", "_signed.pdf"),
            "-filter",
            f"subject.contains:{signer_id};nonexpired:",
        ],
        stdout=stdout,
    )

    if res != 0:
        raise Exception(f"Error signing {file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--template",
        help="Template name (i.e., 'demo' for ./templates/demo.svg)",
        default="demo",
    )
    parser.add_argument(
        "-s",
        "--signerid",
        help="Signer ID (DNI/NIE) to sign the certificates",
    )
    args = parser.parse_args()
    template = args.template
    signer_id = args.signerid

    with open(LOG_PATH, "w") as stdout:
        output_dir = os.path.dirname(OUTPUT_PATH)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        template_path = TEMPLATE_PATH.format(name=template)
        with open(template_path, encoding="utf-8") as template_file:
            template = template_file.read()

        with open(CSV_FILE_PATH, encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            rows = list(reader)

        for row in tqdm(rows, desc="Generating certificates"):
            name = row.get("name", "").strip()
            if not name:
                print(f"Falta nombre de: {row.get('email', '')}")
                continue

            position = str(row.get("position", "")).strip()

            if position == "1":
                prefix = "1"
                achievement = WINNERS_ACHIEVEMENTS[0]
            elif position == "2":
                prefix = "2"
                achievement = WINNERS_ACHIEVEMENTS[1]
            elif position == "3":
                prefix = "3"
                achievement = WINNERS_ACHIEVEMENTS[2]
            else:
                prefix = "0"
                achievement = PARTICIPANT_ACHIEVEMENT

            kebab_name = re.sub(r"\W+", "-", name.casefold()).strip("-")
            output_path = OUTPUT_PATH.format(prefix=prefix, name=kebab_name)

            generate_certificate(
                name=name,
                output_path=output_path,
                template=template,
                achievement=achievement,
                stdout=stdout,
            )

        if signer_id is not None:
            for elem in tqdm(list(os.scandir(OUTPUT_DIR)), desc="Signing certificates"):
                if (
                    elem.is_file()
                    and elem.name.endswith(".pdf")
                    and not elem.name.endswith("_signed.pdf")
                ):
                    sign_certificate(os.path.abspath(elem.path), signer_id)
                    os.remove(elem.path)
