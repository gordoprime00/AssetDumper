import os
import sys
import shlex
import shutil

extensions = {
	"images": [".png", ".jpg", ".jpeg", ".gif", ".webp", ".icns", ".ico", ".tiff", ".bmp", ".svg"],
	"audio": [".wav", ".mp3", ".m4a", ".aac", ".ogg", ".aiff", ".aif", ".caf", ".flac"],
	"videos": [".mp4", ".mov", ".m4v", ".webm"],
	"fonts": [".ttf", ".otf", ".woff", ".woff2"],
	"data": [".json", ".xml", ".plist", ".strings", ".stringsdict", ".txt", ".yaml", ".yml"]
}

print("AssetDumper 0.1.0")
print("Extract resources and assets from macOS applications.")
print()

app = input("Drag and drop a macOS app here: ").strip()

if app.startswith("'") and app.endswith("'"):
	app = app[1:-1]
elif app.startswith('"') and app.endswith('"'):
	app = app[1:-1]
else:
	try:
		parts = shlex.split(app)
		if len(parts) == 1:
			app = parts[0]
	except ValueError:
		pass

app = os.path.abspath(os.path.expanduser(app))

if not os.path.isdir(app) or not app.lower().endswith(".app"):
	print("Error: Invalid macOS application.")
	sys.exit(1)

name = os.path.splitext(os.path.basename(app))[0]

print(f"\nDetected application: {name}")
print("Supported assets: images, audio, videos, fonts, and data.")
input("\nPress enter to begin scanning...")

output = os.path.join(os.getcwd(), "AssetDumper")
os.makedirs(output, exist_ok=True)

destination = os.path.join(output, name)
number = 2

while os.path.exists(destination):
	destination = os.path.join(output, f"{name}_{number}")
	number += 1

os.makedirs(destination)

counts = {category: 0 for category in extensions}
errors = 0
total = 0

print("\nScanning application...\n")

for root, dirs, files in os.walk(app):
	for file in files:
		total += 1

		ext = os.path.splitext(file)[1].lower()
		source = os.path.join(root, file)

		category = None

		for folder, supported in extensions.items():
			if ext in supported:
				category = folder
				break

		if category:
			target_folder = os.path.join(destination, category)
			target = os.path.join(target_folder, file)

			try:
				os.makedirs(target_folder, exist_ok=True)

				if os.path.exists(target):
					base, extension = os.path.splitext(file)
					number = 2

					while os.path.exists(target):
						target = os.path.join(target_folder, f"{base}_{number}{extension}")
						number += 1

				shutil.copy2(source, target)
				counts[category] += 1

			except OSError:
				errors += 1

		sys.stdout.write(f"\rScanned {total} files | Extracted {sum(counts.values())}")
		sys.stdout.flush()

print("\n\nExtraction complete!\n")

for category, count in counts.items():
	print(f"{category.capitalize()}: {count}")

print(f"\nTotal extracted: {sum(counts.values())}")
print(f"Errors: {errors}")
print(f"\nOutput directory: {destination}")