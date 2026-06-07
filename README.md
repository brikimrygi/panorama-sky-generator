
- DISCLAIMER:
THIS CODE IS FULLY AI MADE! I PERSONALLY DON'T LIKE USING AI FOR CODING, BUT I JUST WANTED TO SEE IS AI REALLY GOOD AT MAKING SCRIPTS LIKE THIS ONE! I MADE THIS FOR ONLY PERSONAL USAGE!

========================================================================
EN: SKYBOX GENERATION SCRIPT (psg.py) - INSTALLATION & RUNNING GUIDE
========================================================================

This script is designed to automatically convert both 360° spherical
panoramas and flat, wide panoramic images into individual cubemap
faces (skybox) and pre-aligned layout sheets.

------------------------------------------------------------------------
1. **SYSTEM REQUIREMENTS**
------------------------------------------------------------------------
To run the script, Python 3 must be installed on your computer.

* Windows & macOS:
  Download and install Python from: https://www.python.org/downloads/
  Important (Windows): During installation, make sure to check the
  "Add Python to PATH" box at the bottom of the first setup window.

* Linux (Debian/Ubuntu):
  Open a terminal and install the required packages by running:
  sudo apt update && sudo apt install python3 python3-pip

------------------------------------------------------------------------
2. **INSTALLING REQUIRED LIBRARIES**
------------------------------------------------------------------------
The script requires two external libraries (numpy and Pillow).
Install them by typing the following command in your terminal
(or Command Prompt on Windows):

pip install numpy Pillow

------------------------------------------------------------------------
3. **HOW TO RUN AND PROJECTION MODES**
------------------------------------------------------------------------
Open a terminal / command prompt, navigate to the folder containing
the script, and run:

python psg.py <panorama_filename> [face_size] [-sp|-st] [nf_flags] [-raw|-final] [-np]

Available projection modes:
  -sp, -spherical - (Recommended for flat, wide photos) Spherical mode.
                    Keeps the horizon perfectly flat in-game and prevents
                    it from bending into a bowl shape.
  -st, -standard  - (Recommended for true 360°x180° panoramas) Standard mode.
                    Accurately projects the sky directly above the player.

No-Filter Flags:
  -nf             - Disables filters on all faces at once (pure raw cubemap).
  -nft            - Disables vertical flip on the TOP face.
  -nfb            - Disables rotations on the BOTTOM face.
  -nff            - Disables half-mirror filter on the FRONT face.
  -nfbk           - Disables half-mirror filter on the BACK face.
  -nfl            - Disables generating LEFT face as a right-mirror (pure render).
  -nfr            - Disables filters on the RIGHT face.

Optimization & Extra Filter Flags:
  -np, -nopinch   - (No Pinch) Enables a radial blending filter at the center
                    of sky_top and sky_bottom to completely remove the ugly
                    "vortex/pinch" effect (Polar Coordinates convergence).
  -raw            - (Raw Mode) Generates only the 6 individual face files (sky_*.png),
                    completely skipping the creation of layouts and composite grids.
  -final, -f      - (Final Mode) Generates only the final starfield02.png composite grid,
                    skipping individual faces and auxiliary grids (in-memory processing).

Examples of usage:
- python psg.py panorama.jpg                   (Auto-detection, size 1024)
- python psg.py panorama.jpg 2048 -sp -np      (Spherical mode with pinch removal, 2048)
- python psg.py panorama.jpg -st -final 2048   (Standard mode, starfield02.png only, 2048)

------------------------------------------------------------------------
4. **GENERATED OUTPUT FILES**
------------------------------------------------------------------------
All files are saved inside the automatically created folder
"panorama-sky-generator" in your current working directory:

* sky_front.png, sky_back.png, sky_left.png, sky_right.png, sky_top.png, sky_bottom.png
  - Individual, cropped skybox faces (skipped in -final).
* skybox_grid_3x2.png - A 3x2 grid template with labels and transparency (skipped in -raw, -final).
* skybox_strip_1x3.png - A vertical 1x3 strip layout (Top, Front, Bottom) (skipped in -raw, -final).
* starfield02.png - The final, complete 3x2 grid template without any labels (skipped in -raw).
