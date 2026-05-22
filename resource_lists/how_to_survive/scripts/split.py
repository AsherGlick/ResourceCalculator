import os

def split_file_by_bytes(input_file_path, output_dir="output_segments"):
    # Target HEX value directly as a byte literal
    delimiter = b'your_value'
    
    os.makedirs(output_dir, exist_ok=True)
    
    with open(input_file_path, 'rb') as f:
        file_content = f.read()
    
    # Split the binary content by the byte sequence
    chunks = file_content.split(delimiter)
    
    file_count = 0
    for index, chunk in enumerate(chunks):
        # Ignore empty slice if the file starts exactly with the delimiter
        if index == 0 and len(chunk) == 0:
            continue
            
        # Reconstruct content by prepending the byte delimiter to split segments
        if index == 0:
            segment_data = chunk
        else:
            segment_data = delimiter + chunk
            
        if not segment_data:
            continue
            
        output_filename = os.path.join(output_dir, f"segment_{file_count}.dds")
        
        with open(output_filename, 'wb') as out_f:
            out_f.write(segment_data)
            
        print(f"Saved: {output_filename} ({len(segment_data)} bytes)")
        file_count += 1

# --- Configuration ---
INPUT_FILE = "your_input_file.ext"  # Replace with your actual file path

# Run the function
split_file_by_bytes(INPUT_FILE)
