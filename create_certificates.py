
import os
import re
import subprocess


DATE = "2024-10-18"  # YYYY-MM-DD format

TEMPLATE_PATH = "./templates/demo.svg"
FONT_PATH = "./fonts/Baskervville-Regular.ttf"
FONT_NAME = "Baskervville"
PARTICIPANTS_PATH = "./data/participants.csv"
WINNERS_PATH = "./data/winners.csv"
OUTPUT_PATH = "./out/" + DATE + "_{name}.png"

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

    tmp_file = output_path + ".tmp"

    with open(tmp_file, "w", encoding="utf-8") as tmp:
        tmp.write(
            template
            .replace("[Nombre del destinatario]", name)
            .replace("[logro alcanzado]", achievement)
        )

    subprocess.call([
        "resvg", tmp_file, output_path,
        "--use-font-file", FONT_PATH,
        "--font-family", FONT_NAME,
    ])

    os.remove(tmp_file)


if __name__ == "__main__":

    output_dir = os.path.dirname(OUTPUT_PATH)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(TEMPLATE_PATH, encoding="utf-8") as template_file:
        template = template_file.read()

    with open(PARTICIPANTS_PATH, encoding="utf-8") as participants_file:
        participants = participants_file.read().splitlines()[1:]

    for name in participants:
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
