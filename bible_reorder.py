import json
import os
from collections import OrderedDict  # Import OrderedDict for explicit ordering

# Define input directory and output file paths
input_json_directory = 'Bible'
output_html_file = 'bible.html'

# --- KJV Book Order ---
# Define the canonical order of books in the KJV Bible
KJV_BOOK_ORDER = [
    # Old Testament
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth",
    "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon",
    "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi",
    # New Testament
    "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians",
    "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter",
    "1 John", "2 John", "3 John", "Jude", "Revelation"
]
# Create a set for quick lookups of expected books
KJV_BOOKS_SET = set(KJV_BOOK_ORDER)

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
                    # Sort verses numerically before creating chapter object
                    sorted_verses = sorted(chapter["verses"], key=lambda v: int(v.get("verse", 0)))

                    chapter_obj = {
                        "chapter": int(chapter["chapter"]),
                        "verses": [
                            {
                                "verse": int(verse["verse"]),
                                "text": verse["text"]
                            }
                            # Check verse structure before processing
                            for verse in sorted_verses if isinstance(verse, dict) and 'verse' in verse and 'text' in verse
                        ]
                    }
                    chapters.append(chapter_obj)
                except (ValueError, KeyError, TypeError) as e:
                     print(f"Warning: Skipping chapter/verse due to invalid data in book '{book_name}', chapter '{chapter.get('chapter', 'N/A')}': {e}")
            else:
                print(f"Warning: Skipping chapter with unexpected format in book '{book_name}': {chapter}")
    else:
         print(f"Warning: 'chapters' key missing or not a list in book '{book_name}'")

    # Sort chapters numerically before returning book data
    if chapters:
        chapters.sort(key=lambda c: c.get("chapter", 0))
        return {book_name: {"chapters": chapters}}
    else:
        print(f"Warning: No valid chapters found for book '{book_name}'. Skipping this book.")
        return None

# --- Main Processing Logic ---

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

                    books_in_file = []
                    # Check if input_data is a list or a dictionary
                    if isinstance(input_data, list):
                        # If it's a list, process each item assuming it's a book dictionary
                        print(f"  File contains a list. Processing {len(input_data)} items.") # Debugging
                        books_in_file = input_data
                    elif isinstance(input_data, dict):
                        # If it's a dictionary, treat it as a single book item
                        print("  File contains a dictionary. Processing directly.") # Debugging
                        books_in_file = [input_data]
                    else:
                        # Handle cases where the root JSON element is neither list nor dict
                         print(f"Warning: Skipping file {json_file} - root element is not a list or dictionary.")
                         continue # Skip to the next file

                    # Process each book found in the file
                    for book_item in books_in_file:
                         js_data = convert_book_json_to_js(book_item)
                         if js_data: # Only update if conversion was successful
                             # Check for duplicate book entries (optional but good practice)
                             book_name = list(js_data.keys())[0]
                             if book_name in consolidated_data:
                                 print(f"Warning: Duplicate data found for book '{book_name}' from file {json_file}. Overwriting previous data.")
                             consolidated_data.update(js_data)


            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from file {file_path}: {e}")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

# --- Reorder Consolidated Data ---
ordered_data = OrderedDict() # Use OrderedDict to preserve insertion order
processed_books = set()

print("\nReordering books according to KJV order...")
for book_name in KJV_BOOK_ORDER:
    if book_name in consolidated_data:
        ordered_data[book_name] = consolidated_data[book_name]
        processed_books.add(book_name)
        # print(f"  Added '{book_name}' to ordered data.") # Uncomment for verbose logging
    else:
        print(f"Warning: Book '{book_name}' from KJV order not found in the input JSON data.")

# Check for books found in JSON but not in KJV standard list
found_books = set(consolidated_data.keys())
extra_books = found_books - processed_books # Use set difference
if extra_books:
    print("\nWarning: The following books were found in the JSON data but are not in the standard KJV order list:")
    for book_name in sorted(list(extra_books)): # Sort alphabetically for consistent warning messages
        print(f"  - {book_name}")
        # Optionally, append these extra books to the end
        # ordered_data[book_name] = consolidated_data[book_name]

# --- Write Reordered Data to HTML ---
if ordered_data: # Check if we have any data to write after ordering
    print(f"\nWriting {len(ordered_data)} books to '{output_html_file}'...")
    try:
        with open(output_html_file, 'w', encoding='utf-8') as file:
            file.write("<html><head><title>Bible Data (KJV Order)</title></head><body>\n") # Updated title
            file.write("<script type=\"text/javascript\">\n") # Added type attribute
            file.write("// --- !!! BIBLE DATA (KJV ORDER) !!! ---\n") # Updated comment
            file.write("const simulatedBibleData = ")
            # Dump the ordered_data. json.dumps respects OrderedDict order.
            file.write(json.dumps(ordered_data, ensure_ascii=False, indent=4))
            file.write(";\n")
            file.write("// --- End Bible Data ---\n")
            file.write("</script>\n")
            # Optional: Add a message in the HTML body indicating completion or status
            file.write("<h1>Bible data loaded into JavaScript variable 'simulatedBibleData'.</h1>\n")
            file.write("</body></html>")

        print(f"Conversion and ordering complete. HTML file saved as '{output_html_file}'.")
    except IOError as e:
        print(f"Error writing HTML file '{output_html_file}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred while writing the HTML file: {e}")
else:
     # Updated message if no data was processed or found
     print(f"No valid JSON data found or processed according to KJV order from '{input_json_directory}'. Output file '{output_html_file}' not created or updated.")
