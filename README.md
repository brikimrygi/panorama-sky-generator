# Panorama Sky Generator (psg.py)

> **Disclaimer**
>
> This project was created primarily as an experiment to test how capable AI is at generating scripts of this complexity.
> The code was generated with AI assistance and was originally intended for personal use.

---

## Features

* Converts panoramas into cubemap skybox faces.
* Supports both:

  * 360° × 180° equirectangular panoramas.
  * Flat wide panoramic images.
* Generates:

  * Individual skybox faces.
  * Layout sheets.
  * Final `starfield02.png` composite texture.
* Multiple projection modes.
* Optional face-specific filters and optimizations.

---

# ONLINE VERSION (NO INSTALLATION)

[Open an online generator](https://panorama-sky-generator-kawvmuhapbgyi88g9f4lm7.streamlit.app/)

---

## Requirements

### Python

Python 3 is required.

Download Python:

https://www.python.org/downloads/

**Windows:** During installation, enable **"Add Python to PATH"**.

### Linux (Debian / Ubuntu)

```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Linux (Arch)

```bash
sudo pacman -Syu
sudo pacman -S python3 python3-pip
```

### Android (Termux)

```bash
pkg install (or -i) python3
pkg install (or -i) python3-pip
```

---

## Installation

Install the required dependencies:

```bash
pip install numpy Pillow
```
* To use this, install python3-pip firstly!

### Linux (Debian / Ubuntu)

```bash
sudo apt install python-numpy
sudo apt install python-pillow
```
* Use if you can't download python3-pip!

### Linux (Arch)

```bash
sudo pacman -S python-numpy
sudo pacman -S python-pillow
```
* Use if you can't download python3-pip!

### Android (Termux)

```bash
pkg install (or -i) python-numpy
pkg install (or -i) python-pillow
```

---

## Usage

```bash
python psg.py <panorama_filename> [face_size] [-sp|-st] [nf_flags] [-raw|-final] [-np]
```

### Projection Modes

| Flag                | Description                                                                                        |
| ------------------- | -------------------------------------------------------------------------------------------------- |
| `-sp`, `-spherical` | Recommended for flat panoramic images. Keeps the horizon flat and prevents bowl-shaped distortion. |
| `-st`, `-standard`  | Recommended for true 360° × 180° panoramas. Accurately projects the sky above the player.          |

### No-Filter Flags

| Flag    | Description                                   |
| ------- | --------------------------------------------- |
| `-nf`   | Disable filters on all faces.                 |
| `-nft`  | Disable vertical flip on the TOP face.        |
| `-nfb`  | Disable rotations on the BOTTOM face.         |
| `-nff`  | Disable half-mirror filter on the FRONT face. |
| `-nfbk` | Disable half-mirror filter on the BACK face.  |
| `-nfl`  | Disable mirrored LEFT face generation.        |
| `-nfr`  | Disable filters on the RIGHT face.            |

### Optimization & Output Flags

| Flag              | Description                                                                      |
| ----------------- | -------------------------------------------------------------------------------- |
| `-np`, `-nopinch` | Applies radial blending to reduce polar pinch artifacts on top and bottom faces. |
| `-raw`            | Generate only the six cubemap faces (`sky_*.png`).                               |
| `-final`, `-f`    | Generate only the final `starfield02.png` texture using in-memory processing.    |

---

## Examples

Auto-detect panorama type and generate a 1024px skybox:

```bash
python psg.py panorama.jpg
```

Generate a 2048px skybox using spherical mode with pinch correction:

```bash
python psg.py panorama.jpg 2048 -sp -np
```

Generate only `starfield02.png` using standard projection:

```bash
python psg.py panorama.jpg -st -final 2048
```

---

## Output Files

All generated files are stored inside:

```text
panorama-sky-generator/
```

### Cubemap Faces

```text
sky_front.png
sky_back.png
sky_left.png
sky_right.png
sky_top.png
sky_bottom.png
```

Individual skybox faces.

*Skipped when using `-final`.*

### Layouts

```text
skybox_grid_3x2.png
```

3×2 labeled grid template with transparency.

*Skipped when using `-raw` or `-final`.*

```text
skybox_strip_1x3.png
```

Vertical strip layout containing:

```text
Top
Front
Bottom
```

*Skipped when using `-raw` or `-final`.*

### Final Texture

```text
starfield02.png
```

Final 3×2 composite texture without labels.

*Skipped when using `-raw`.*
