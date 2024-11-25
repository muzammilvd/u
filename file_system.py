import os

# Constants
BLOCK_SIZE = 128  # Each block has 128 bytes
DISK_SIZE = 1024  # Simulate a disk with 1024 blocks

# Simulate disk storage
disk = [""] * DISK_SIZE  # Empty blocks

# File Metadata Table: (filename, size, start_block)
file_table = {}


# Helper function to find free blocks
def find_free_blocks(size_in_bytes):
    num_blocks_needed = (size_in_bytes + BLOCK_SIZE - 1) // BLOCK_SIZE
    free_blocks = [i for i, block in enumerate(disk) if block == ""]
    if len(free_blocks) >= num_blocks_needed:
        return free_blocks[:num_blocks_needed]
    else:
        return []


# Create a file
def create_file(filename, content):
    if filename in file_table:
        print(f"File '{filename}' already exists.")
        return

    size = len(content)
    free_blocks = find_free_blocks(size)

    if not free_blocks:
        print("Not enough free blocks to store the file.")
        return

    # Write content to disk
    start_block = free_blocks[0]
    for i, block_num in enumerate(free_blocks):
        start = i * BLOCK_SIZE
        disk[block_num] = content[start : start + BLOCK_SIZE]

    # Store file metadata
    file_table[filename] = {
        "size": size,
        "start_block": start_block,
        "blocks": free_blocks,
    }
    print(f"File '{filename}' created successfully.")


# Read a file
def read_file(filename):
    if filename not in file_table:
        print(f"File '{filename}' not found.")
        return

    file_info = file_table[filename]
    blocks = file_info["blocks"]
    content = "".join(disk[block] for block in blocks)
    print(f"Content of '{filename}':\n{content}")


# Delete a file
def delete_file(filename):
    if filename not in file_table:
        print(f"File '{filename}' does not exist.")
        return

    # Free up disk blocks
    file_info = file_table[filename]
    blocks = file_info["blocks"]
    for block in blocks:
        disk[block] = ""

    # Remove file metadata
    del file_table[filename]
    print(f"File '{filename}' deleted successfully.")


# List all files
def list_files():
    if not file_table:
        print("No files found.")
    else:
        print("Files on disk:")
        for filename, metadata in file_table.items():
            print(
                f" - {filename} (Size: {metadata['size']} bytes, Blocks: {metadata['blocks']})"
            )


# Main menu
def main_menu():
    while True:
        print("\nFile System Simulation")
        print("1. Create File")
        print("2. Read File")
        print("3. Delete File")
        print("4. List Files")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            filename = input("Enter filename: ")
            content = input("Enter file content: ")
            create_file(filename, content)

        elif choice == "2":
            filename = input("Enter filename to read: ")
            read_file(filename)

        elif choice == "3":
            filename = input("Enter filename to delete: ")
            delete_file(filename)

        elif choice == "4":
            list_files()

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main_menu()
