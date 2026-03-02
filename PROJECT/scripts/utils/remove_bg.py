from PIL import Image
import os

def remove_white_background(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        # If the pixel is very close to white, make it transparent
        # Threshold 240, 240, 240 to be safe
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(output_path, "PNG")
    print(f"[*] Background removed. Saved to: {output_path}")

if __name__ == "__main__":
    IN_LOGO = r"e:\Downloads\--ANTIGRAVITY store\IDE-optimus\IN\Layer-4.png"
    OUT_LOGO = r"e:\Downloads\--ANTIGRAVITY store\IDE-optimus\PROJECT\frontend\nexus-v2\public\assets\logo_transparent.png"
    
    os.makedirs(os.path.dirname(OUT_LOGO), exist_ok=True)
    remove_white_background(IN_LOGO, OUT_LOGO)
