import argparse
import os
import re
import subprocess

import img2pdf
from tqdm import tqdm

DATE = "2024-10-18"  # YYYY-MM-DD format

TEMPLATE_PATH = "./templates/demo.svg"
FONT_PATH = "./fonts/Baskervville-Regular.ttf"
FONT_NAME = "Baskervville"
PARTICIPANTS_PATH = "./data/participants.csv"
WINNERS_PATH = "./data/winners.csv"
OUTPUT_PATH = "./out/" + DATE + "_{name}.pdf"

PARTICIPANT_ACHIEVEMENT = "haber participado"
WINNERS_ACHIEVEMENTS = (
    "obtener la medalla de oro",
    "obtener la medalla de plata",
    "obtener la medalla de bronce",
)


def generate_certificate(
    name: str,
    output_path: str,
    template: str,
    achievement: str,
):
    """Generate certificate with the given name and achievement."""

    tmp_svg_path = output_path + ".tmp"
    tmp_png_path = output_path + ".png"

    with open(tmp_svg_path, "w", encoding="utf-8") as tmp:
        tmp.write(
            template
            .replace("[Nombre del destinatario]", name)
            .replace("[logro alcanzado]", achievement)
        )

    subprocess.call([
        "resvg", tmp_svg_path, tmp_png_path,
        "--use-font-file", FONT_PATH,
        "--font-family", FONT_NAME,
    ])

    os.remove(tmp_svg_path)

    with open(tmp_png_path, "rb") as png_file, open(output_path, "wb") as ouptut_file:
        ouptut_file.write(img2pdf.convert(png_file))

    os.remove(tmp_png_path)


def sign_certificate(file_path: str, signer_id: str):
    """Sign the .pdf certificate with the given file path."""

    res = subprocess.call([
        "autofirmacommandline", "sign",
        "-i", file_path,
        "-o", file_path.replace(".pdf", "_signed.pdf"),
        "-filter", f"subject.contains:{signer_id};nonexpired:",
    ])

    if res != 0:
        raise Exception(f"Error signing {file_path}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--signerid",
        help="Signer ID (DNI/NIE) to sign the certificates",
    )
    args = parser.parse_args()
    signer_id = args.signerid

    output_dir = os.path.dirname(OUTPUT_PATH)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(TEMPLATE_PATH, encoding="utf-8") as template_file:
        template = template_file.read()

    with open(PARTICIPANTS_PATH, encoding="utf-8") as participants_file:
        participants = participants_file.read().splitlines()[1:]

    for name in tqdm(participants, desc="Generating certificates for participants"):
        kebab_name = re.sub(r"\W+", "-", name.strip().casefold())
        output_path = OUTPUT_PATH.format(name=kebab_name)
        generate_certificate(
            name=name,
            output_path=output_path,
            template=template,
            achievement=PARTICIPANT_ACHIEVEMENT,
        )

    with open(WINNERS_PATH, encoding="utf-8") as winners_file:
        winners = winners_file.read().splitlines()[1:]

    for name, achievement in zip(winners, WINNERS_ACHIEVEMENTS):
        kebab_name = re.sub(r"\W+", "-", name.strip().casefold())
        output_path = OUTPUT_PATH.format(name=kebab_name)
        generate_certificate(
            name=name,
            output_path=output_path,
            template=template,
            achievement=achievement,
        )

    if signer_id is not None:
        for elem in tqdm(os.scandir("./out"), desc="Signing certificates"):
            if elem.is_file() and elem.name.endswith(".pdf") and not elem.name.endswith("_signed.pdf"):
                sign_certificate(os.path.abspath(elem.path), signer_id)
                os.remove(elem.path)
