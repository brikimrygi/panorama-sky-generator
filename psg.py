#!/usr/bin/env python3
import sys
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HELP_TEXT = """========================================================================
PL: INSTRUKCJA INSTALACJI I URUCHOMIENIA SKRYPTU SKYBOX (psg.py)
========================================================================

Ten skrypt służy do automatycznej konwersji sferycznych panoramy 360° 
oraz płaskich, szerokich zdjęć panoramicznych na pojedyncze ściany 
sześcianu (skybox) oraz gotowe szablony siatek.

------------------------------------------------------------------------
1. WYMAGANIA SYSTEMOWE
------------------------------------------------------------------------
Aby uruchomić skrypt, na komputerze musi być zainstalowany Python 3.

* Windows i macOS:
  Pobierz i zainstaluj instalator ze strony: https://www.python.org/downloads/
  Ważne (Windows): Podczas instalacji upewnij się, że zaznaczona jest 
  opcja "Add Python to PATH" na samym dole pierwszego okna instalatora.

* Linux (Debian/Ubuntu):
  Otwórz terminal i zainstaluj pakiety wpisując:
  sudo apt update && sudo apt install python3 python3-pip

------------------------------------------------------------------------
2. INSTALACJA WYMAGANYCH BIBLIOTEK
------------------------------------------------------------------------
Skrypt wymaga dwóch zewnętrznych bibliotek (numpy i Pillow). 
Zainstalujesz je, wpisując w terminalu (lub Wierszu polecenia na Windows):

pip install numpy Pillow

------------------------------------------------------------------------
3. SPOSÓB URUCHOMIENIA I TRYBY
------------------------------------------------------------------------
Otwórz terminal lub wiersz poleceń, przejdź do folderu ze skryptem i wpisz:

python psg.py <nazwa_pliku> [rozmiar_sciany] [-sp|-st] [flagi_nf] [-raw|-final] [-np]

Dostępne parametry i tryby rzutowania:
  -sp, -spherical - (Zalecany dla płaskich, szerokich zdjęć) Tryb sferyczny.
                    Utrzymuje horyzont horyzontalnie prostym w grze i zapobiega 
                    jego wyginaniu w łuk.
  -st, -standard  - (Zalecany dla pełnych sfer 360°x180°) Tryb standardowy.
                    Poprawnie odwzorowuje niebo bezpośrednio nad graczem.

Flagi wyłączenia filtrów (No Filters):
  -nf             - Wyłącza filtry dla wszystkich ścian jednocześnie (czysty cubemap).
  -nft            - Wyłącza odwrócenie pionowe dla ściany TOP.
  -nfb            - Wyłącza obroty dla ściany BOTTOM.
  -nff            - Wyłącza połówkowe odbicie lustrzane dla ściany FRONT.
  -nfbk           - Wyłącza połówkowe odbicie lustrzane dla ściany BACK.
  -nfl            - Wyłącza tworzenie ściany LEFT z right (generuje czysty rzut).
  -nfr            - Wyłącza filtry dla ściany RIGHT.

Flagi optymalizacji i filtrów dodatkowych:
  -np, -nopinch   - (No Pinch) Włącza filtr usuwający efekt "wirówki" (Polar 
                    Coordinates pinch) w centralnym punkcie sufitu (sky_top) 
                    oraz podłogi (sky_bottom). Tworzy gładkie, jednolite przejście.
  -raw            - (Raw Mode) Generuje wyłącznie 6 pojedynczych ścian sky_*.png,
                    pomijając całkowicie tworzenie szablonów i siatek zbiorczych.
  -final, -f      - (Final Mode) Generuje wyłącznie plik końcowy starfield02.png,
                    pomijając pojedyncze kafelki i pozostałe siatki (operacje w pamięci).

Przykłady użycia:
- python psg.py panorama.jpg                    (Auto-wykrywanie, rozmiar 1024)
- python psg.py panorama.jpg 2048 -sp -np       (Cylindryczny z usunięciem wirówki, 2048)
- python psg.py panorama.jpg -st -final 2048    (Standardowy, tylko starfield02.png, 2048)

------------------------------------------------------------------------
4. GENEROWANE PLIKI WYJŚCIOWE
------------------------------------------------------------------------
Wszystkie pliki wyjściowe zapisywane są w automatycznie tworzonym
folderze "panorama-sky-generator" w bieżącym katalogu roboczym:

* sky_front.png, sky_back.png, sky_left.png, sky_right.png, sky_top.png, sky_bottom.png
  - Pojedyncze, wycięte ściany nieba (z nałożonymi korektami, pomijane w -final).
* skybox_grid_3x2.png - Szablon siatki 3x2 z oznaczeniami (pomijane w -raw, -final).
* skybox_strip_1x3.png - Pionowy pasek 1x3 (Top, Front, Bottom) (pomijane w -raw, -final).
* starfield02.png - Kompletny, pełny szablon siatki 3x2 bez napisów (pomijane w -raw).


========================================================================
EN: SKYBOX GENERATION SCRIPT (psg.py) - INSTALLATION & RUNNING GUIDE
========================================================================

This script is designed to automatically convert both 360° spherical 
panoramas and flat, wide panoramic images into individual cubemap 
faces (skybox) and pre-aligned layout sheets.

------------------------------------------------------------------------
1. SYSTEM REQUIREMENTS
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
2. INSTALLING REQUIRED LIBRARIES
------------------------------------------------------------------------
The script requires two external libraries (numpy and Pillow). 
Install them by typing the following command in your terminal 
(or Command Prompt on Windows):

pip install numpy Pillow

------------------------------------------------------------------------
3. HOW TO RUN AND PROJECTION MODES
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
4. GENERATED OUTPUT FILES
------------------------------------------------------------------------
All files are saved inside the automatically created folder
"panorama-sky-generator" in your current working directory:

* sky_front.png, sky_back.png, sky_left.png, sky_right.png, sky_top.png, sky_bottom.png
  - Individual, cropped skybox faces (skipped in -final).
* skybox_grid_3x2.png - A 3x2 grid template with labels and transparency (skipped in -raw, -final).
* skybox_strip_1x3.png - A vertical 1x3 strip layout (Top, Front, Bottom) (skipped in -raw, -final).
* starfield02.png - The final, complete 3x2 grid template without any labels (skipped in -raw).
"""

# Bezpieczne pobranie metod obracania i odbijania dla różnych wersji biblioteki Pillow
try:
    ROT_90_CW = Image.Transpose.ROTATE_270   # Obrót o 90 stopni w prawo (270 CCW)
    ROT_90_CCW = Image.Transpose.ROTATE_90   # Obrót o 90 stopni w lewo (90 CCW)
    ROT_180 = Image.Transpose.ROTATE_180     # Obrót o 180 stopni (do góry nogami)
    FLIP_LR = Image.Transpose.FLIP_LEFT_RIGHT # Lustrzane odbicie lewo-prawo
    FLIP_TB = Image.Transpose.FLIP_TOP_BOTTOM # Lustrzane odbicie góra-dół (pionowo)
except AttributeError:
    ROT_90_CW = Image.ROTATE_270
    ROT_90_CCW = Image.ROTATE_90
    ROT_180 = Image.ROTATE_180
    FLIP_LR = Image.FLIP_LEFT_RIGHT
    FLIP_TB = Image.FLIP_TOP_BOTTOM

def project_face(img_array, face, face_size, selected_mode, no_pinch=False):
    h_pano, w_pano, channels = img_array.shape
    u, v = np.meshgrid(np.linspace(-1, 1, face_size), np.linspace(-1, 1, face_size))
    
    if face == 'front':
        x = np.ones_like(u)
        y = -u
        z = -v
    elif face == 'back':
        x = -np.ones_like(u)
        y = u
        z = -v
    elif face == 'left':
        x = u
        y = np.ones_like(u)
        z = -v
    elif face == 'right':
        x = -u
        y = -np.ones_like(u)
        z = -v
    elif face == 'top':
        x = u
        y = -v
        z = np.ones_like(u)
    elif face == 'bottom':
        x = u
        y = v
        z = -np.ones_like(u)
        
    aspect = w_pano / h_pano
    
    if selected_mode == "standard":
        # 1. Rzutowanie standardowe (dla pełnych panoram 360x180)
        r = np.sqrt(x**2 + y**2 + z**2)
        theta = np.arctan2(y, x)
        phi = np.arcsin(z / r)
        
        px = ((theta + np.pi) / (2 * np.pi)) * (w_pano - 1)
        py = ((np.pi / 2 - phi) / np.pi) * (h_pano - 1)
    else:
        # 2. Rzutowanie sferyczno-cylindryczne (dla płaskich panoram szerokokątnych - prosty horyzont)
        theta = np.arctan2(y, x)
        d = np.sqrt(x**2 + y**2)
        d_safe = np.where(d < 1e-5, 1e-5, d)
        v_ratio = z / d_safe
        
        px = ((theta + np.pi) / (2 * np.pi)) * (w_pano - 1)
        v_scale = aspect / 2.0
        py = (0.5 - (v_ratio * v_scale / 2.0)) * (h_pano - 1)
        
    # Bezpieczne przycinanie współrzędnych
    px = np.clip(np.round(px).astype(int), 0, w_pano - 1)
    py = np.clip(np.round(py).astype(int), 0, h_pano - 1)
    
    # Filtr usuwający efekt "wirówki" na biegunach (top/bottom) poprzez płynne rozmycie radialne do średniego koloru tła
    if no_pinch and (face in ['top', 'bottom']):
        if face == 'top':
            avg_color = np.mean(img_array[0, :, :], axis=0) # Średni kolor nieba (góra)
        else:
            avg_color = np.mean(img_array[-1, :, :], axis=0) # Średni kolor ziemi (dół)
            
        # Wyznaczamy odległość od środka kafelka (0 w środku, do ok. 1.41 na rogach)
        d_center = np.sqrt(u**2 + v**2)
        
        # Promień blendowania (d < 0.5 oznacza centralny obszar kafelka)
        blend_radius = 0.5
        alpha = np.clip(d_center / blend_radius, 0.0, 1.0)
        alpha_3d = np.expand_dims(alpha, axis=-1)
        
        sampled_pixels = img_array[py, px]
        blended_pixels = (alpha_3d * sampled_pixels + (1.0 - alpha_3d) * avg_color).astype(np.uint8)
        return blended_pixels
    else:
        return img_array[py, px]

def generate_skybox(panorama_path, face_size=1024, mode="auto", nf_top=False, nf_bottom=False, nf_front=False, nf_back=False, nf_left=False, nf_right=False, no_pinch=False, raw_mode=False, final_mode=False):
    if not os.path.exists(panorama_path):
        print(f"Błąd: Nie znaleziono pliku '{panorama_path}'.")
        sys.exit(1)
        
    try:
        img = Image.open(panorama_path).convert('RGB')
        img_array = np.array(img)
        
        # Zmieniona kolejność: 'right' przed 'left'
        faces = ['front', 'back', 'right', 'left', 'top', 'bottom']
        generated_images = {}
        
        print(f"Konwertowanie: {os.path.basename(panorama_path)}")
        print(f"Rozdzielczość wyjściowa ścian: {face_size}x{face_size}px")
        
        h_pano, w_pano, _ = img_array.shape
        aspect = w_pano / h_pano
        
        # Określenie ostatecznego trybu rzutowania
        selected_mode = "auto"
        if mode == "standard":
            selected_mode = "standard"
            print(" -> Tryb rzutowania wymuszony przez flagę: STANDARD (-st)")
        elif mode == "spherical":
            selected_mode = "spherical"
            print(" -> Tryb rzutowania wymuszony przez flagę: SPHERICAL (-sp)")
        else:
            # Tryb automatyczny na podstawie proporcji obrazu
            if 1.95 <= aspect <= 2.05:
                selected_mode = "standard"
                print(f" -> Auto-wykrywanie (proporcje {aspect:.2f}:1): Tryb STANDARD (standardowy)")
            else:
                selected_mode = "spherical"
                print(f" -> Auto-wykrywanie (proporcje {aspect:.2f}:1): Tryb SPHERICAL (sferyczny)")
        
        # Przygotowanie folderu wyjściowego "panorama-sky-generator"
        output_dir = os.path.join(os.getcwd(), "panorama-sky-generator")
        if not os.path.exists(output_dir):
            print(f" -> Tworzenie folderu wyjściowego: {output_dir}")
            os.makedirs(output_dir)
        
        # 1. Generowanie i zapisywanie pojedynczych ścian
        for face in faces:
            if face == 'left' and not nf_left:
                # Ściana left powstaje przez poziome odbicie gotowej ściany right
                print(" -> Tworzenie ściany left jako odbitej poziomo ściany right...")
                face_image = generated_images['right'].transpose(FLIP_LR)
            else:
                if face == 'left':
                    print(" -> Generowanie czystej ściany left (wyłączony filtr)...")
                elif face == 'right' and nf_right:
                    print(" -> Generowanie czystej ściany right (wyłączony filtr)...")
                # Pozostałe ściany są projektowane na podstawie wybranego trybu
                face_data = project_face(img_array, face, face_size, selected_mode, no_pinch)
                face_image = Image.fromarray(face_data)
            
            # Warunkowe nakładanie filtrów
            if not nf_top or not nf_bottom or not nf_front or not nf_back or not nf_left or not nf_right:
                # Modyfikacje dla ściany top (odwrócenie pionowe)
                if face == 'top' and not nf_top:
                    print(" -> Odwracanie ściany top pionowo (globalnie)...")
                    face_image = face_image.transpose(FLIP_TB)
                    
                # Modyfikacje dla ściany bottom (obrót do góry nogami - 180 stopni)
                elif face == 'bottom' and not nf_bottom:
                    print(" -> Obracanie ściany bottom do góry nogami (180 stopni, globalnie)...")
                    face_image = face_image.transpose(ROT_180)
                    
                # Lustrzane odbicie prawej połowy na lewą dla ściany przód (sky_front) (bez obracania)
                elif face == 'front' and not nf_front:
                    print(" -> Lustrzane odbijanie prawej połowy ściany front na lewą stronę...")
                    right_half = face_image.crop((face_size // 2, 0, face_size, face_size))
                    mirrored_left = right_half.transpose(FLIP_LR)
                    face_image.paste(mirrored_left, (0, 0))
                    
                # Lustrzane odbicie lewej połowy na prawą dla ściany tyłu (sky_back)
                elif face == 'back' and not nf_back:
                    print(" -> Lustrzane odbijanie lewej połowy ściany back na prawą stronę...")
                    left_half = face_image.crop((0, 0, face_size // 2, face_size))
                    mirrored_right = left_half.transpose(FLIP_LR)
                    face_image.paste(mirrored_right, (face_size // 2, 0))
            else:
                print(f" -> Generowanie czystej ściany {face} (tryb NO FILTERS)...")
                
            # Zapisujemy kopię wygenerowanego obrazu do pamięci RAM
            generated_images[face] = face_image.copy()
            
            # Dodatkowy obrót o 90 stopni w prawo stosowany wyłącznie przy zapisie pojedynczego pliku bottom
            if face == 'bottom' and not nf_bottom:
                print(" -> Obracanie ściany bottom o 90 stopni w prawo (dla pliku)...")
                face_image = face_image.transpose(ROT_90_CW)
                
            # Zapisywanie pojedynczego pliku pomijamy w trybie FINAL
            if not final_mode:
                output_path = os.path.join(output_dir, f"sky_{face}.png")
                face_image.save(output_path)
            
        # W trybie RAW pomijamy generowanie szablonów siatek
        if raw_mode:
            print(f"\nGotowe! Wygenerowano pojedyncze ściany (tryb RAW) w folderze: {output_dir}")
            return

        # Szablon 1: Siatka 3x2 w oryginalnym układzie użytkownika (RGBA z przezroczystością)
        # Pomijane w trybie FINAL
        if not final_mode:
            print(" -> Tworzenie szablonu siatki 3x2 z przezroczystością i napisami (skybox_grid_3x2.png)...")
            grid_3x2 = Image.new('RGBA', (face_size * 3, face_size * 2), (0, 0, 0, 0))
            grid_3x2.paste(generated_images['back'].convert('RGBA'), (face_size * 2, 0))
            grid_3x2.paste(generated_images['left'].convert('RGBA'), (0, face_size))
            grid_3x2.paste(generated_images['right'].convert('RGBA'), (face_size * 2, face_size))
            
            draw = ImageDraw.Draw(grid_3x2)
            try:
                font = ImageFont.load_default(size=int(face_size * 0.08))
            except TypeError:
                font = ImageFont.load_default()
                
            red_color = (255, 0, 0, 255)
            center_bottom = (face_size // 2, face_size // 2)
            center_top = (face_size + face_size // 2, face_size // 2)
            center_front = (face_size + face_size // 2, face_size + face_size // 2)
            
            draw.text(center_bottom, "bottom", fill=red_color, font=font, anchor="mm")
            draw.text(center_top, "top", fill=red_color, font=font, anchor="mm")
            draw.text(center_front, "front", fill=red_color, font=font, anchor="mm")
            grid_3x2.save(os.path.join(output_dir, "skybox_grid_3x2.png"), "PNG")
        
        # Szablon 2: Pionowy pasek 1x3 (Szerokość: face_size, Wysokość: 3 * face_size)
        # Generowany w pamięci zawsze (potrzebny do starfield02.png), ale zapisywany tylko gdy nie final_mode
        strip_1x3 = Image.new('RGB', (face_size, face_size * 3))
        
        # 1. SKY_TOP: Wklejona bezpośrednio z pamięci
        strip_1x3.paste(generated_images['top'], (0, 0))
        
        # 2. SKY_FRONT: Wklejenje na pozycję (0, face_size)
        strip_1x3.paste(generated_images['front'], (0, face_size))
        
        # 3. SKY_BOTTOM: Wklejenie na pozycję (0, face_size * 2) z pamięci, obrócona o 90 stopni CW (jeśli nie nf_bottom)
        sky_bottom_rotated = generated_images['bottom']
        if not nf_bottom:
            sky_bottom_rotated = sky_bottom_rotated.transpose(ROT_90_CW)
        strip_1x3.paste(sky_bottom_rotated, (0, face_size * 2))
        
        # 4. Lustrzane odbicie lewej połowy ściany bottom na prawą stronę (tylko, jeśli nie ma wyłączonego bottom filter)
        if not nf_bottom:
            left_half_bottom = strip_1x3.crop((0, face_size * 2, face_size // 2, face_size * 3))
            mirrored_right_bottom = left_half_bottom.transpose(FLIP_LR)
            strip_1x3.paste(mirrored_right_bottom, (face_size // 2, face_size * 2))
        
        if not final_mode:
            print(" -> Tworzenie pionowego szablonu 1x3 (skybox_strip_1x3.png)...")
            strip_1x3.save(os.path.join(output_dir, "skybox_strip_1x3.png"))
        
        print(" -> Tworzenie KOŃCOWEGO, PEŁNEGO szablonu siatki 3x2 (starfield02.png)...")
        # Szablon 3: Pełna siatka 3x2 bez napisów i przezroczystości
        starfield02 = Image.new('RGB', (face_size * 3, face_size * 2))
        
        # Wycinanie przetworzonych elementów bezpośrednio z gotowego szablonu 1x3 w pamięci RAM
        top_from_1x3 = strip_1x3.crop((0, 0, face_size, face_size))
        front_from_1x3 = strip_1x3.crop((0, face_size, face_size, face_size * 2))
        bottom_from_1x3 = strip_1x3.crop((0, face_size * 2, face_size, face_size * 3))
        
        # Układanie siatki 3x2 z przeniesionymi elementami
        # Rząd 1: Bottom (ze strip_1x3) | Top (ze strip_1x3) | Back (oryginalna)
        starfield02.paste(bottom_from_1x3, (0, 0))
        starfield02.paste(top_from_1x3, (face_size, 0))
        starfield02.paste(generated_images['back'], (face_size * 2, 0))
        
        # Rząd 2: Left (odbity od right) | Front (ze strip_1x3) | Right (oryginalna)
        starfield02.paste(generated_images['left'], (0, face_size))
        starfield02.paste(front_from_1x3, (face_size, face_size))
        starfield02.paste(generated_images['right'], (face_size * 2, face_size))
        
        starfield02.save(os.path.join(output_dir, "starfield02.png"))
        
        print(f"\nGotowe! Wszystkie pliki zostały wygenerowane w folderze: {output_dir}")
        
    except Exception as e:
        print(f"Wystąpił błąd podczas generowania skyboxa: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Obsługa flagi pomocy przed standardowym sprawdzeniem argumentów
    if len(sys.argv) >= 2 and sys.argv[1].lower() in ["-help", "--help", "-h", "--h"]:
        print(HELP_TEXT)
        sys.exit(0)

    if len(sys.argv) < 2:
        print("Użycie: psg <nazwa_pliku_lub_sciezka.png> [rozmiar_sciany] [-sp|-st] [-nf] [-nft] [-nfb] [-nff] [-nfbk] [-nfl] [-nfr] [-np] [-raw|-final] lub psg -help")
        sys.exit(1)
        
    input_path = sys.argv[1]
    size = 1024
    mode = "auto"
    raw_mode = False
    final_mode = False
    no_pinch = False
    
    nf_top = False
    nf_bottom = False
    nf_front = False
    nf_back = False
    nf_left = False
    nf_right = False
    
    for arg in sys.argv[2:]:
        arg_lower = arg.lower()
        if arg_lower in ["-sp", "--sp", "-spherical", "--spherical"]:
            mode = "spherical"
        elif arg_lower in ["-st", "--st", "-standard", "--standard"]:
            mode = "standard"
        elif arg_lower in ["-nf", "--nf", "-nofilters"]:
            nf_top = nf_bottom = nf_front = nf_back = nf_left = nf_right = True
        elif arg_lower in ["-nft", "--nft", "-nofiltertop"]:
            nf_top = True
        elif arg_lower in ["-nfb", "--nfb", "-nofilterbottom"]:
            nf_bottom = True
        elif arg_lower in ["-nff", "--nff", "-nofilterfront"]:
            nf_front = True
        elif arg_lower in ["-nfbk", "--nfbk", "-nofilterback"]:
            nf_back = True
        elif arg_lower in ["-nfl", "--nfl", "-nofilterleft"]:
            nf_left = True
        elif arg_lower in ["-nfr", "--nfr", "-nofilterright"]:
            nf_right = True
        elif arg_lower in ["-np", "--np", "-nopinch"]:
            no_pinch = True
        elif arg_lower in ["-raw", "--raw"]:
            raw_mode = True
        elif arg_lower in ["-final", "--final", "-f", "--f"]:
            final_mode = True
        else:
            try:
                size = int(arg)
            except ValueError:
                print(f"Błąd: Niepoprawny argument '{arg}'. Dozwolone flagi: -sp, -st, -nf, -np, -raw, -final lub rozmiar.")
                sys.exit(1)
                
    generate_skybox(input_path, size, mode, nf_top, nf_bottom, nf_front, nf_back, nf_left, nf_right, no_pinch, raw_mode, final_mode)