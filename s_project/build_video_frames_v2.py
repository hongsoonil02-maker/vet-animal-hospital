import os
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "C:\\Windows\\Fonts\\malgun.ttf"
FONT_BOLD_PATH = "C:\\Windows\\Fonts\\malgunbd.ttf"

def get_font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD_PATH if bold else FONT_PATH, size)

ASSETS_DIR = r"C:\Users\master\vet_animal_hospital\s_project\assets"

SCENE_IMAGES = {
    1: os.path.join(ASSETS_DIR, "grain_market_volatility_1789881820210.jpg"),
    2: os.path.join(ASSETS_DIR, "premix_product_packaging_1789881875376.jpg"),
    3: os.path.join(ASSETS_DIR, "chart_cost_comparison.png"),
    4: os.path.join(ASSETS_DIR, "micro_capsule_science_1789881698716.jpg"),
    5: os.path.join(ASSETS_DIR, "feed_production_line_1789881658069.jpg"),
    6: os.path.join(ASSETS_DIR, "healthy_livestock_farm_1789881676601.jpg"),
    7: os.path.join(ASSETS_DIR, "company_factory_panorama_1789881641339.jpg"),
}

MASCOT_PATH = os.path.join(ASSETS_DIR, "bio_livestock_mascot_1789881785483.jpg")

def render_vivid_scene_frame(scene_data, scene_num, total_scenes=7, output_path="frame.png"):
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), color=(10, 25, 47)) # Dark Navy
    draw = ImageDraw.Draw(img)

    # Top emerald line
    draw.rectangle([(0, 0), (width, 8)], fill=(16, 185, 129))

    # Top brand bar
    draw.text((70, 35), "주식회사 삼원팜텍  |  SAMWON PHARMTECH", font=get_font(20, bold=True), fill=(16, 185, 129))
    draw.text((1200, 35), "S-NACF 한일사료 임가공(월 18,000톤) 맞춤형 제안", font=get_font(18), fill=(148, 163, 184))
    draw.line([(70, 75), (width - 70, 75)], fill=(30, 58, 138), width=2)

    # ---------------- LEFT COLUMN: Text & Bullets (Width: 980px) ----------------
    # Scene Tag Pill
    draw.rounded_rectangle([(70, 95), (380, 135)], radius=10, fill=(6, 78, 59), outline=(16, 185, 129), width=2)
    draw.text((85, 103), scene_data["header_tag"], font=get_font(16, bold=True), fill=(236, 253, 245))

    # Headline & Subheadline
    draw.text((70, 150), scene_data["headline"], font=get_font(34, bold=True), fill=(255, 255, 255))
    draw.text((70, 205), scene_data["subheadline"], font=get_font(20), fill=(52, 211, 153))

    # Left Main Card Box
    card_top = 250
    card_bottom = 850
    card_w = 950
    draw.rounded_rectangle([(70, card_top), (70 + card_w, card_bottom)], radius=16, fill=(15, 32, 67), outline=(30, 58, 138), width=2)

    # Bullets
    bullets = scene_data["bullets"]
    start_y = card_top + 35
    for idx, bullet in enumerate(bullets[:4]): # Max 4 bullets
        by = start_y + idx * 88
        # Bullet marker
        draw.rounded_rectangle([(105, by + 6), (120, by + 22)], radius=4, fill=(16, 185, 129))
        
        # Split bullet text if too long
        if len(bullet) > 34:
            b1 = bullet[:34]
            b2 = bullet[34:]
            draw.text((140, by), b1, font=get_font(21, bold=True), fill=(241, 245, 249))
            draw.text((140, by + 28), b2, font=get_font(18), fill=(203, 213, 225))
        else:
            draw.text((140, by + 2), bullet, font=get_font(21, bold=True), fill=(241, 245, 249))

    # Highlight Banner at Bottom of Left Card
    draw.rounded_rectangle([(90, 755), (70 + card_w - 20, 830)], radius=10, fill=(6, 78, 59), outline=(16, 185, 129), width=2)
    draw.text((115, 775), "★  " + scene_data["highlight"], font=get_font(19, bold=True), fill=(255, 255, 255))

    # ---------------- RIGHT COLUMN: Image / Graphic / Photo (Width: 780px) ----------------
    img_x = 1060
    img_y = 110
    img_w = 790
    img_h = 740
    
    photo_path = SCENE_IMAGES.get(scene_num)
    if photo_path and os.path.exists(photo_path):
        try:
            with Image.open(photo_path) as p_img:
                # Resize keeping aspect ratio or fit
                p_resized = p_img.resize((img_w, img_h), Image.Resampling.LANCZOS)
                img.paste(p_resized, (img_x, img_y))
                
                # Draw elegant frame around photo
                draw.rectangle([(img_x, img_y), (img_x + img_w, img_y + img_h)], outline=(16, 185, 129), width=3)
        except Exception as e:
            print(f"Error loading {photo_path}: {e}")

    # Special Mascot Overlay on Scene 01 and Scene 07
    if scene_num in [1, 7] and os.path.exists(MASCOT_PATH):
        try:
            with Image.open(MASCOT_PATH) as m_img:
                m_size = 230
                m_resized = m_img.resize((m_size, m_size), Image.Resampling.LANCZOS)
                # Paste at bottom right corner of photo
                mx = img_x + img_w - m_size - 15
                my = img_y + img_h - m_size - 15
                img.paste(m_resized, (mx, my))
                draw.rectangle([(mx, my), (mx + m_size, my + m_size)], outline=(52, 211, 153), width=3)
        except Exception as e:
            print(f"Mascot error: {e}")

    # Bottom Footer Bar
    draw.line([(70, 990), (width - 70, 990)], fill=(30, 58, 138), width=1)
    draw.text((70, 1015), "(주)삼원팜텍 대표이사 김한호  |  충북 옥천 테크노밸리 본사 및 공장  |  국가 조달청 관납 전국 총판", font=get_font(18), fill=(148, 163, 184))
    draw.text((1700, 1015), f"Scene {scene_num:02d} / {total_scenes:02d}", font=get_font(20, bold=True), fill=(16, 185, 129))

    img.save(output_path, quality=95)
    print(f"Rendered vivid frame: {output_path}")

def main():
    from generate_audio import SCENES
    out_dir = r"C:\Users\master\vet_animal_hospital\s_project\frames"
    os.makedirs(out_dir, exist_ok=True)
    for i, scene in enumerate(SCENES, start=1):
        out_path = os.path.join(out_dir, f"scene_{i:02d}.png")
        render_vivid_scene_frame(scene, i, len(SCENES), out_path)

if __name__ == "__main__":
    main()
