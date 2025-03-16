import os

import subprocess


def get_available_args(exe_path):
    """Attempt to get available arguments from EXE using /? or read-me."""
    try:
        result = subprocess.run(f"{exe_path}?", shell=True, text=True, capture_output=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error checking {exe_path}: {e}")
        try:
            with open(exe_path.replace('.exe', '.txt'), 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if 'available arguments' in content.lower():
                    return extract_available_args(content)
        except FileNotFoundError:
            print(f"Read-me not found for {exe_path}")
    return []


def extract_available_args(readme_content):
    """Extract VST3 plugin version from read-me."""
    available = {}
    lines = readme_content.split('\n')
    for line in lines:
        if 'available arguments' in line.lower():
            parts = line.split()
            if len(parts) > 1 and '=' in parts[1]:
                arg = parts[1]
                version = next(part for part in parts if part.isdigit())
                available[arg] = f"vst3_{version}"
    return available


def main():
    script_dir = os.getcwd()
    installers = [f for f in os.listdir(script_dir) if f.endswith('.exe')]

    for exe_path in installers:
        print(f"Processing {exe_path}")
        try:
            args = get_available_args(exe_path)
            if not args:
                continue

            version = next(iter(args.values()), None)
            if not version:
                print(f"No supported argument found for {exe_path}. Skipping.")
                continue

            # Example command: install=vst3_123456, path=C:\Program Files\PlugInName
            cmd = f"start {version} /install={version}"

            print(f"Installing VST3 plugin with version: {version}")
            subprocess.run(cmd, shell=True)
        except Exception as e:
            print(f"Error processing {exe_path}: {e}")


if __name__ == "__main__":
    main()
