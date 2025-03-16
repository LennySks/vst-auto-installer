# vst-auto-installer

Automate the process of installing audio plugins with option for every format.

## Functionality

- [x] Choose the location of plugin location(s) (Browser window)
- [x] Iterate over every file in folder _(one level deep)_
- [x] Check if the file is a valid plugin
- [ ] Install every plugin
  - [ ] Automated using pyautogui synchronously
  - [ ] _Check if the plugin was installed correctly_

### Design

- [x] Button to add new directory 
  - [x] This will create a disabled input field with the path and create a new button below the input field
- [x] Button to remove a directory 
- [x] Button to start the process (Install button)


### Workflow

- Installer opens
- pyautogui looks for accept_agreement or next buttons
  - If found, click
- Keep pressing next until you find checkboxes to check
  - If found, check if vst3 checkbox is checked already
  - If not, check the checkbox
- Press next button (assuming it is installing)
- Press finish when done installing.