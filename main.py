import customtkinter


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.directories = []
        self.entry_widgets = []

        self.title("VST Installer")
        self.geometry("600x600")
        self.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(self, text="Select the directories where the VST plugins are located")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        # Create frame to center input and button
        self.list_frame = customtkinter.CTkFrame(self)
        self.list_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        self.list_frame.grid_columnconfigure(0, weight=1)  # Make input expand

        # Add button
        self.add_button = customtkinter.CTkButton(self, text="+ Add Directory", command=self.button_callback,
                                                  fg_color="green", hover_color="gray", width=30)
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
        row = len(self.directories)  # Get next row index

        # Create a read-only entry field
        entry = customtkinter.CTkEntry(self.list_frame, width=10)
        entry.insert(0, directory)
        entry.configure(state="disabled")  # Make it read-only
        entry.grid(row=row, column=0, padx=5, pady=2, sticky="ew")

        # Create a remove button
        remove_button = customtkinter.CTkButton(self.list_frame, text="X", fg_color="red",
                                                hover_color="gray", width=30,
                                                command=lambda: self.remove_directory(directory, entry, remove_button))
        remove_button.grid(row=row, column=1, padx=5, pady=2)

        # Store entry widgets for deletion
        self.entry_widgets.append((entry, remove_button))

    def remove_directory(self, directory, entry, button):
        if directory in self.directories:
            self.directories.remove(directory)
            entry.destroy()
            button.destroy()

    def install_callback(self):
        for directory in self.directories:
            print(f"Installing VST plugins from {directory}")


if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    app = App()
    app.mainloop()
