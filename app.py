from io import BytesIO
import streamlit as st
from PIL import Image

# Fungsi membaca gambar dan mengubah ke list pixel RGB
def load_image(file_obj, max_dim=2048):
	img = Image.open(file_obj).convert("RGB")
	width, height = img.size
	resized = False
	# Resize jika salah satu sisi lebih besar dari max_dim
	if width > max_dim or height > max_dim:
		scale = min(max_dim / width, max_dim / height)
		new_size = (int(width * scale), int(height * scale))
		img = img.resize(new_size, Image.LANCZOS)
		width, height = img.size
		resized = True
	pixels = list(img.getdata())
	return img, width, height, pixels, resized

# Fungsi membentuk kembali gambar dari list pixel RGB
def build_image(width, height, pixels):
	new_img = Image.new("RGB", (width, height))
	new_img.putdata(pixels)
	return new_img

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
		gray = int(0.299 * r + 0.587 * g + 0.114 * b)
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
	return [(max(r, g, b),) * 3 for r, g, b in pixels]

# Decomposition (Min)
def grayscale_decomposition_min(pixels):
	return [(min(r, g, b),) * 3 for r, g, b in pixels]

def get_methods():
	return {
		"Averaging": (
			grayscale_averaging,
			"Rata-rata dari nilai R, G, dan B.",
			"avg.png",
		),
		"Luminosity (Weighting)": (
			grayscale_weighting,
			"Memberi bobot lebih besar ke channel hijau.",
			"luminosity.png",
		),
		"Desaturation": (
			grayscale_desaturation,
			"Rata-rata dari nilai maksimal dan minimal RGB.",
			"desaturation.png",
		),
		"Single Channel (Red)": (
			grayscale_single_channel,
			"Mengambil hanya channel merah sebagai nilai grayscale.",
			"red.png",
		),
		"Decomposition (Max)": (
			grayscale_decomposition_max,
			"Mengambil nilai channel terbesar pada tiap pixel.",
			"max.png",
		),
		"Decomposition (Min)": (
			grayscale_decomposition_min,
			"Mengambil nilai channel terkecil pada tiap pixel.",
			"min.png",
		),
	}

def image_to_png_bytes(image):
	buffer = BytesIO()
	image.save(buffer, format="PNG")
	return buffer.getvalue()

def apply_selected_method(width, height, pixels, method_name, methods, progress_bar):
	method_func, description, filename = methods[method_name]

	progress_bar.progress(35, text="Mengubah pixel ke grayscale...")
	method_pixels = method_func(pixels)

	progress_bar.progress(70, text="Menyusun gambar hasil...")
	method_image = build_image(width, height, method_pixels)

	progress_bar.progress(90, text="Menyiapkan file download...")
	image_bytes = image_to_png_bytes(method_image)

	progress_bar.progress(100, text="Selesai")
	return method_image, image_bytes, description, filename

def render_basic_style():
	st.markdown(
		"""
		<style>
			.footer-custom {
				margin-top: 10rem;
				padding-top: 1rem;
				border-top: 1px solid rgba(224,224,224,0.3);
				text-align: center;
				color: #888;
				font-size: 1rem;
			}
			.stSelectbox > div[data-baseweb="select"] {
				width: 100% !important;
			}
			.stDownloadButton button {
				width: 100% !important;
			}
			.block-container {
				max-width: 1000px !important;
				margin-left: auto !important;
				margin-right: auto !important;
				padding-top: 2rem;
				padding-bottom: 2rem;
			}
			h1, h2, h3 {
				text-align: center;
			}
			div[data-testid="column"] .stDownloadButton {
				display: flex;
				justify-content: flex-end;
			}
		</style>
		""",
		unsafe_allow_html=True,
	)

def main():
	st.set_page_config(page_title="Grayscale Converter", layout="wide")
	render_basic_style()

	st.title("Konversi Gambar ke Grayscale")

	uploaded_file = st.file_uploader(
		"Upload file gambar", type=["png", "jpg", "jpeg", "bmp", "webp"]
	)

	methods = get_methods()
	method_names = list(methods.keys())

	control_col1, control_col2 = st.columns(2)
	with control_col1:
		selected_method = st.selectbox("Pilih metode grayscale", method_names)

	selected_description = methods[selected_method][1]
	download_data = b""
	download_filename = "hasil-grayscale.png"
	download_disabled = True
	original_image = None
	result_image = None

	if uploaded_file is not None:
		original_image, width, height, pixels, resized = load_image(uploaded_file)
		if resized:
			st.info(f"Gambar di-resize otomatis ke {width}x{height} piksel agar proses lebih stabil.")
		with st.spinner("Memproses gambar..."):
			progress_bar = st.progress(10, text="Membaca gambar...")
			(
				result_image,
				download_data,
				selected_description,
				download_filename,
			) = apply_selected_method(
				width,
				height,
				pixels,
				selected_method,
				methods,
				progress_bar,
			)
			progress_bar.empty()
		download_disabled = False

	with control_col2:
		st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
		st.download_button(
			label=f"Download {selected_method}",
			data=download_data,
			file_name=download_filename,
			mime="image/png",
			use_container_width=True,
			disabled=download_disabled,
			key=f"download-selected-{selected_method}",
		)

	if uploaded_file is None:
		return

	st.caption(selected_description)


	preview_col1, preview_col2 = st.columns(2)
	with preview_col1:
		st.caption("Gambar Asli")
		st.image(original_image, use_container_width=True)
	with preview_col2:
		st.caption(selected_method)
		st.image(result_image, use_container_width=True)

	# Footer
	st.markdown('<div class="footer-custom">Made by Lukas Austin | NPM 140810230011</div>', unsafe_allow_html=True)

if __name__ == "__main__":
	main()
