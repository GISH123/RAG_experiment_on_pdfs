import re

def clean_requirements(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    cleaned_lines = []
    for line in lines:
        # Detect Windows-specific local file paths
        if "file:///" in line:
            # Extract the package name before '@'
            package_name = re.match(r"([\w\-]+)", line)
            if package_name:
                cleaned_lines.append(f"{package_name.group(1)}\n")
        else:
            cleaned_lines.append(line)

    # Write the cleaned requirements to a new file
    with open(output_file, 'w') as file:
        file.writelines(cleaned_lines)

    print(f"Cleaned requirements saved to {output_file}")

# Usage
clean_requirements("requirements.txt", "requirements_cleaned.txt")