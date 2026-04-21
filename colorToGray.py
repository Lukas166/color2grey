from PIL import Image # library untuk load dan save gambar

# Fungsi membaca gambar dan mengubah ke list pixel RGB
def load_image(filename):
    img = Image.open(filename).convert("RGB")
    width, height = img.size
    pixels = list(img.getdata())
    return img, width, height, pixels

# Fungsi menyimpan hasil grayscale
def save_image(width, height, pixels, filename):
    new_img = Image.new("RGB", (width, height))
    new_img.putdata(pixels)
    new_img.save(filename)

# Averaging
def grayscale_averaging(pixels):
    result = []
    for r, g, b in pixels:
        gray = (r + g + b) // 3
        result.append((gray, gray, gray))
    return result

# Luminosity (Weighting)
def grayscale_weighting(pixels):
    result = []
    for r, g, b in pixels:
        gray = int(0.299*r + 0.587*g + 0.114*b)
        result.append((gray, gray, gray))
    return result

# Desaturation
def grayscale_desaturation(pixels):
    result = []
    for r, g, b in pixels:
        gray = (max(r, g, b) + min(r, g, b)) // 2
        result.append((gray, gray, gray))
    return result

# Single channel (Red)
def grayscale_single_channel(pixels):
    return [(r, r, r) for r, g, b in pixels]

# Decomposition (Max)
def grayscale_decomposition_max(pixels):
    return [(max(r, g, b),)*3 for r, g, b in pixels]

# Decomposition (Min)
def grayscale_decomposition_min(pixels):
    return [(min(r, g, b),)*3 for r, g, b in pixels]

# main
filename = "image.png" # Ubah sesuai nama dan format file gambar

img, width, height, pixels = load_image(filename)

while True:
    print("\nMENU GRAYSCALE")
    print("1. Averaging")
    print("2. Luminosity (Weighting)")
    print("3. Desaturation")
    print("4. Single Channel (Red)")
    print("5. Decomposition (Max)")
    print("6. Decomposition (Min)")
    print("0. Keluar")

    choice = input("Pilih metode: ")

    if choice == "1":
        result = grayscale_averaging(pixels)
        out = "avg.png"
    elif choice == "2":
        result = grayscale_weighting(pixels)
        out = "luminosity.png"
    elif choice == "3":
        result = grayscale_desaturation(pixels)
        out = "desaturation.png"
    elif choice == "4":
        result = grayscale_single_channel(pixels)
        out = "red.png"
    elif choice == "5":
        result = grayscale_decomposition_max(pixels)
        out = "max.png"
    elif choice == "6":
        result = grayscale_decomposition_min(pixels)
        out = "min.png"
    elif choice == "0":
        print("Program selesai")
        break
    else:
        print("Pilihan tidak valid")
        continue

    save_image(width, height, result, out)
    print(f"Hasil disimpan sebagai {out}")