import json
import os
import re
import sys

# Check for correct usage
if len(sys.argv) != 2:
    print("Usage: python script.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

try:
    # Load the JSON data
    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Ensure the JSON data is a list
    if not isinstance(data, list):
        print("Error: The JSON file must contain a list of conversations.")
        sys.exit(1)

    # Create output directory
    os.makedirs("MarkdownFiles", exist_ok=True)

    # Determine the number of digits for zero-padding
    total_files = len(data)
    digit_count = len(str(total_files))

    # Process each conversation
    for i, conversation in enumerate(data, start=1):
        # Generate zero-padded number
        padded_number = str(i).zfill(digit_count)

        # Extract title and sanitize it for use as a filename
        title = conversation.get("title", f"Conversation_{padded_number}")
        title = re.sub(r'[\\/:\"*?<>|]', "_", title)  # Replace invalid filename characters with "_"

        # Extract "parts" content
        parts = []
        mapping = conversation.get("mapping", {})
        for node_id, node_data in mapping.items():
            message = node_data.get("message")
            if message:
                content = message.get("content", {})
                for part in content.get("parts", []):
                    if not isinstance(part, str):
                        part = json.dumps(part, ensure_ascii=False, indent=2)  # Convert non-string parts to JSON string
                    parts.append(part)

        # Create Markdown content
        markdown_content = f"# {title}\n\n" + "\n".join(parts)

        # Save to a Markdown file
        output_file = os.path.join("MarkdownFiles", f"{padded_number}_{title}.md")
        with open(output_file, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content.strip())

        print(f"Saved: {output_file}")

    print(f"Processed {len(data)} conversations. Markdown files are in the 'MarkdownFiles' folder.")

except FileNotFoundError:
    print(f"Error: File '{input_file}' not found.")
except json.JSONDecodeError as e:
    print(f"Error: File '{input_file}' is not valid JSON. {e}")
except Exception as e:
    print(f"An error occurred: {e}")

