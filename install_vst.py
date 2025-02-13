import os

import pyautogui
import subprocess
import time

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")


def find_and_click(image_name, confidence=0.8):
    """Find an image on the screen and click it if found."""
    image_path = os.path.join(IMAGES_DIR, image_name)
    location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)

    if location:
        pyautogui.click(location)
        print(f"Clicked {image_name}")
        time.sleep(1)  # Add a small delay to avoid misclicks
        return True
    return False


def install_vst(executable_path):
    print(f"Attempting to install {executable_path}")
    process = subprocess.Popen([executable_path], shell=True)

    while process.poll() is None:
        # Step 1: Agree to terms (if exists)
        find_and_click("agree.png")

        # Step 2: Click "Next" (loop in case there are multiple next steps)
        while find_and_click("next.png"):
            pass

        # Step 3: Select VST3 checkbox (optional, adjust if user can choose formats)
        # find_and_click("checkmark_vst3_1.png")
        # or
        # find_and_click("checkmark_vst3_2.png")
        find_and_click("text_vst3_1.png")

        # Step 4: Click next button
        find_and_click("next_btn_1.png")

        # Step 5: Wait for install to complete
        print("Waiting for installation to complete...")

        # Step 6: Click "Finish" button when installation is done
        while not find_and_click("finish.png"):
            time.sleep(1)

        print("Installation complete.")
        break

# Check for agreement
# Check for next button
# Check for chosen formats and choose them (checkboxes)
# Wait until installation is finished
# Check if finish button is available
# On positive result, execute next exe
