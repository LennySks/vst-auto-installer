import customtkinter
import glob
import os


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.directories = []
        self.checkboxes = []  # Store checkboxes

        self.title("VST Installer")
        self.geometry("600x600")
        self.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(self, text="Select the directories where the VST plugins are located")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        # Frame for directory list
        self.list_frame = customtkinter.CTkFrame(self)
        self.list_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        self.list_frame.grid_columnconfigure(0, weight=1)

        # Add Directory button
        self.add_button = customtkinter.CTkButton(self, text="+ Add Directory", command=self.button_callback,
                                                  fg_color="green")
        self.add_button.grid(row=2, column=0, padx=5, pady=5)

        # Install button
        self.install_button = customtkinter.CTkButton(self, text="Install", command=self.install_callback)
        self.install_button.grid(row=3, column=0, padx=10, pady=10, columnspan=2, sticky="ew")

    def button_callback(self):
        filename = customtkinter.filedialog.askdirectory()
        if filename and filename not in self.directories:
            self.directories.append(filename)
            self.add_directory_entry(filename)

    def add_directory_entry(self, directory):
        row = len(self.directories)
        entry = customtkinter.CTkEntry(self.list_frame, width=10)
        entry.insert(0, directory)
        entry.configure(state="disabled")
        entry.grid(row=row, column=0, padx=5, pady=2, sticky="ew")

        remove_button = customtkinter.CTkButton(self.list_frame, text="X", fg_color="red",
                                                command=lambda: self.remove_directory(directory, entry, remove_button))
        remove_button.grid(row=row, column=1, padx=5, pady=2)

    def remove_directory(self, directory, entry, button):
        if directory in self.directories:
            self.directories.remove(directory)
            entry.destroy()
            button.destroy()

    def is_installer(self, filename):
        """Filter only valid installers."""
        filename_lower = filename.lower()
        installer_keywords = ["setup", "install", "update", "vst"]
        exclude_keywords = ["keygen", "patcher", "crack", "r2r", "serial", "fix", "license"]

        parent_folder = os.path.basename(os.path.dirname(filename)).lower()

        if any(keyword in filename_lower for keyword in installer_keywords) and not any(
                keyword in filename_lower or keyword in parent_folder for keyword in exclude_keywords
        ):
            return True
        return False

    def install_callback(self):
        found_installers = []
        for directory in self.directories:
            if os.path.isdir(directory):
                files = glob.glob(f"{directory}/**/*.exe", recursive=True)
                valid_installers = [file for file in files if self.is_installer(file)]
                found_installers.extend(valid_installers)

        if found_installers:
            self.show_installer_selection(found_installers)

    def show_installer_selection(self, installers):
        """Open a new window to let the user select installers."""
        self.checkbox_window = customtkinter.CTkToplevel(self)
        self.checkbox_window.title("Select Installers")
        self.checkbox_window.geometry("500x500")

        self.checkbox_frame = customtkinter.CTkFrame(self.checkbox_window)
        self.checkbox_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.checkboxes = []
        for installer in installers:
            var = customtkinter.BooleanVar()
            checkbox = customtkinter.CTkCheckBox(self.checkbox_frame, text=os.path.basename(installer), variable=var)
            checkbox.pack(anchor="w", padx=5, pady=2)
            self.checkboxes.append((var, installer))

        install_button = customtkinter.CTkButton(self.checkbox_window, text="Install Selected",
                                                 command=self.process_selected_installers)
        install_button.pack(pady=10)

    def process_selected_installers(self):
        """Get selected installers and print them."""
        selected_installers = [installer for var, installer in self.checkboxes if var.get()]
        print("Selected installers:", selected_installers)
        # TODO: For every installer, run it and use pyautogui to automate process (Check chosen format vst2, vst3 ... )


if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    app = App()
    app.mainloop()
