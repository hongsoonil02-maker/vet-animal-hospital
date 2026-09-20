import os
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "C:\\Windows\\Fonts\\malgun.ttf"
FONT_BOLD_PATH = "C:\\Windows\\Fonts\\malgunbd.ttf"

def get_font(size, bold=False):
    path = FONT_BOLD_PATH if bold else FONT_PATH
    return ImageFont.truetype(path, size)

def render_scene_image(scene_data, scene_num, total_scenes=7, output_path="frame.png"):
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), color=(10, 25, 47)) # #0A192F Dark Navy
    draw = ImageDraw.Draw(img)

    # Top accent line
    draw.rectangle([(0, 0), (width, 8)], fill=(16, 185, 129)) # Emerald accent line

    # Top brand bar
    font_brand = get_font(20, bold=True)
    draw.text((80, 40), "주식회사 삼원팜텍  |  SAMWON PHARMTECH", font=font_brand, fill=(16, 185, 129))
    draw.text((1250, 40), "S-NACF 한일사료 임가공(월 18,000톤) 맞춤형 제안", font=get_font(20, bold=False), fill=(148, 163, 184))

    # Divider
    draw.line([(80, 80), (width - 80, 80)], fill=(30, 58, 138), width=2)

    # Scene Tag Pill
    tag_font = get_font(18, bold=True)
    tag_text = scene_data["header_tag"]
    draw.rounded_rectangle([(80, 110), (380, 150)], radius=12, fill=(6, 78, 59), outline=(16, 185, 129), width=2)
    draw.text((96, 118), tag_text, font=tag_font, fill=(236, 253, 245))

    # Headline
    hl_font = get_font(42, bold=True)
    draw.text((80, 175), scene_data["headline"], font=hl_font, fill=(255, 255, 255))

    # Subheadline
    sub_font = get_font(24, bold=False)
    draw.text((80, 240), scene_data["subheadline"], font=sub_font, fill=(52, 211, 153))

    # Main Card Box (Navy Slate Box)
    card_top = 300
    card_bottom = 850
    draw.rounded_rectangle([(80, card_top), (width - 80, card_bottom)], radius=20, fill=(15, 32, 67), outline=(30, 58, 138), width=3)

    # Bullets inside card
    bullet_font = get_font(26, bold=False)
    bullet_bold_font = get_font(28, bold=True)
    
    start_y = card_top + 45
    bullets = scene_data["bullets"]
    
    for idx, bullet in enumerate(bullets):
        by = start_y + idx * 85
        # Bullet marker
        draw.rounded_rectangle([(120, by + 8), (136, by + 24)], radius=4, fill=(16, 185, 129))
        draw.text((160, by), bullet, font=bullet_font, fill=(241, 245, 249))

    # Highlight Banner at Bottom of Card
    draw.rounded_rectangle([(110, 740), (width - 110, 820)], radius=12, fill=(6, 78, 59), outline=(16, 185, 129), width=2)
    hi_font = get_font(24, bold=True)
    draw.text((140, 762), "★  " + scene_data["highlight"], font=hi_font, fill=(255, 255, 255))

    # Bottom Footer
    draw.line([(80, 990), (width - 80, 990)], fill=(30, 58, 138), width=1)
    footer_font = get_font(18, bold=False)
    draw.text((80, 1015), "(주)삼원팜텍 대표이사 김한호  |  충북 옥천 테크노밸리 본사 및 공장  |  국가 조달청 관납 전국 총판", font=footer_font, fill=(148, 163, 184))
    draw.text((1700, 1015), f"Scene {scene_num:02d} / {total_scenes:02d}", font=get_font(20, bold=True), fill=(16, 185, 129))

    img.save(output_path, quality=95)
    print(f"Generated frame: {output_path}")

def generate_all_frames():
    from generate_audio import SCENES
    out_dir = r"C:\Users\master\vet_animal_hospital\s_project\frames"
    os.makedirs(out_dir, exist_ok=True)
    for i, scene in enumerate(SCENES, start=1):
        out_path = os.path.join(out_dir, f"scene_{i:02d}.png")
        render_scene_image(scene, i, len(SCENES), out_path)

if __name__ == "__main__":
    generate_all_frames()
