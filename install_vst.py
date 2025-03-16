import os
import time
import subprocess
import pyautogui

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")


def find_and_click(image_name, confidence=0.85, grayscale=True):
    """Find an image on the screen and click it if found."""
    image_path = os.path.join(IMAGES_DIR, image_name)
    location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence, grayscale=grayscale)

    if location:
        pyautogui.click(location)
        print(f"Clicked {image_name}")
        time.sleep(1)  # Delay to avoid misclicks
        return True
    return False


def install_vst(executable_path):
    print(f"Attempting to install {executable_path}")
    process = subprocess.Popen([executable_path], shell=True)
    time.sleep(5)  # Wait for installer to open

    while process.poll() is None:  # While the installer is still running
        # Step 1: Agree to terms (if applicable)
        # find_and_click("buttons/accept_agreement.png")
        # find_and_click("buttons/agree_btn.png")

        # Step 2: Click "Next" (loop in case there are multiple steps)
        next_buttons = ["buttons/next_btn_1.png", "buttons/next_btn_2.png", "buttons/next_btn_r2r.png"]
        for next_button in next_buttons:
            while find_and_click(next_button):
                pass

        # Step 3: Check if VST3 is selected
        if not find_and_click("checked_vst3_1.png"):  # If already checked, don't click
            find_and_click("checkmark_vst3_1.png")  # Check the box if not checked

        # Step 4: Click "Next" to proceed with installation
        for next_button in next_buttons:
            find_and_click(next_button)

        # Step 5: Wait for installation to complete
        print("Waiting for installation to complete...")
        time.sleep(5)  # Adjust time as needed

        # Step 6: Click "Finish" button when installation is done
        while not find_and_click("buttons/finish_btn.png"):
            time.sleep(1)

        print("Installation complete.")
        break  # Exit loop once installation is done
