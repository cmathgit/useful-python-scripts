import json
import os

# Define input directory and output file paths
input_json_directory = 'Bible' # use https://github.com/aruljohn/Bible-kjv
output_html_file = 'bible.html' # push the entire bible to a <script> in HTML

# Function to convert JSON structure (assumed to be a dictionary for a single book)
# to desired JavaScript format
def convert_book_json_to_js(book_data):
    # Check if the input is actually a dictionary with the expected 'book' key
    if not isinstance(book_data, dict) or 'book' not in book_data:
        # Log an error or warning if the structure is unexpected
        print(f"Warning: Skipping item with unexpected format: {type(book_data)}")
        return None # Return None to indicate failure

    book_name = book_data['book']
    chapters = []
    # Check if 'chapters' key exists and is a list
    if 'chapters' in book_data and isinstance(book_data['chapters'], list):
        for chapter in book_data['chapters']:
            # Basic check for chapter structure
            if isinstance(chapter, dict) and 'chapter' in chapter and 'verses' in chapter and isinstance(chapter['verses'], list):
                try:
                    chapter_obj = {
                        "chapter": int(chapter["chapter"]),
                        "verses": [
                            {
                                "verse": int(verse["verse"]),
                                "text": verse["text"]
                            }
                            # Check verse structure before processing
                            for verse in chapter["verses"] if isinstance(verse, dict) and 'verse' in verse and 'text' in verse
                        ]
                    }
                    chapters.append(chapter_obj)
                except (ValueError, KeyError, TypeError) as e:
                     print(f"Warning: Skipping chapter/verse due to invalid data in book '{book_name}': {e}")
            else:
                print(f"Warning: Skipping chapter with unexpected format in book '{book_name}': {chapter}")
    else:
         print(f"Warning: 'chapters' key missing or not a list in book '{book_name}'")


    # Only return data if chapters were successfully processed
    if chapters:
        return {book_name: {"chapters": chapters}}
    else:
        print(f"Warning: No valid chapters found for book '{book_name}'. Skipping this book.")
        return None


# Consolidate all JSON data
consolidated_data = {}
# Check if the directory exists
if not os.path.isdir(input_json_directory):
    print(f"Error: Input directory not found at '{input_json_directory}'")
else:
    for json_file in os.listdir(input_json_directory):
        if json_file.endswith('.json'):
            file_path = os.path.join(input_json_directory, json_file)
            print(f"Processing file: {file_path}") # Added for debugging
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    input_data = json.load(file)

                    # Check if input_data is a list or a dictionary
                    if isinstance(input_data, list):
                        # If it's a list, process each item assuming it's a book dictionary
                        print(f"  File contains a list. Processing {len(input_data)} items.") # Debugging
                        for book_item in input_data:
                            js_data = convert_book_json_to_js(book_item)
                            if js_data: # Only update if conversion was successful
                                consolidated_data.update(js_data)
                    elif isinstance(input_data, dict):
                        # If it's a dictionary, process it directly
                        print("  File contains a dictionary. Processing directly.") # Debugging
                        js_data = convert_book_json_to_js(input_data)
                        if js_data: # Only update if conversion was successful
                            consolidated_data.update(js_data)
                    else:
                        # Handle cases where the root JSON element is neither list nor dict
                         print(f"Warning: Skipping file {json_file} - root element is not a list or dictionary.")

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from file {file_path}: {e}")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

# Write consolidated data to HTML file with JavaScript
if consolidated_data:
    try:
        with open(output_html_file, 'w', encoding='utf-8') as file:
            file.write("<html><head><title>Bible Data</title></head><body>\n")
            file.write("<script>\n")
            file.write("// --- !!! SIMULATED BIBLE DATA !!! ---\n")
            file.write("const simulatedBibleData = ")
            file.write(json.dumps(consolidated_data, ensure_ascii=False, indent=4))
            file.write(";\n")
            file.write("// --- End Simulated Data ---\n")
            file.write("</script>\n")
            file.write("</body></html>")

        print(f"Conversion complete. HTML file saved as '{output_html_file}'.")
    except IOError as e:
        print(f"Error writing HTML file '{output_html_file}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred while writing the HTML file: {e}")
else:
     print(f"No valid JSON data successfully processed from '{input_json_directory}'. Output file '{output_html_file}' not created or updated.")
