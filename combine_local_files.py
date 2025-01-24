import os
import logging
import mimetypes
import argparse

# Configure logging
logging.basicConfig(
    filename="file_combiner.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def is_text_file(file_path):
    """
    Checks if a file is a text file based on its MIME type.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file is a text file, False otherwise.
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type is not None and mime_type.startswith("text")


def combine_files(directory_path, output_file, script_name):
    """
    Combines the content of all text files in a directory into a single output file.
    Adds the filename before each file's content and skips the script's own file.

    Args:
        directory_path (str): The path to the directory containing the files.
        output_file (str): The path to the output file.
        script_name (str): The name of the script file to exclude.
    """
    try:
        logging.info(f"Starting to combine files in directory: {directory_path}")

        # Check if the directory exists
        if not os.path.isdir(directory_path):
            logging.error(f"The directory {directory_path} does not exist.")
            return

        combined_content = []

        # Iterate through all files in the directory
        for file_name in sorted(
            os.listdir(directory_path)
        ):  # Sort for consistent order
            file_path = os.path.join(directory_path, file_name)

            # Skip the script's own file and non-text files
            if (
                file_name == script_name
                or not os.path.isfile(file_path)
                or not is_text_file(file_path)
            ):
                logging.info(f"Skipping file: {file_name}")
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    file_content = file.read()
                    combined_content.append(f"--- Start of file: {file_name} ---\n")
                    combined_content.append(file_content)
                    combined_content.append(f"--- End of file: {file_name} ---\n")
                    logging.info(f"Successfully read {file_name}")
            except Exception as e:
                logging.error(f"Error reading {file_name}: {e}")

        # Write the combined content to the output file
        try:
            with open(output_file, "w", encoding="utf-8") as output:
                output.write("\n".join(combined_content))
            logging.info(f"Successfully wrote combined content to {output_file}")
        except Exception as e:
            logging.error(f"Error writing to output file {output_file}: {e}")

    except Exception as e:
        logging.critical(f"Unexpected error: {e}")


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Combine text files from a directory into a single file."
    )
    parser.add_argument(
        "directory",
        type=str,
        nargs="?",
        default=".",
        help="The directory containing the files to combine (default: current directory)",
    )
    parser.add_argument(
        "output",
        type=str,
        nargs="?",
        default="combine_local_files_output.txt",
        help="The output file to write the combined content to (default: combine_local_files_output.txt)",
    )

    args = parser.parse_args()

    # Get the name of the current script
    script_name = os.path.basename(__file__)

    # Run the file combiner
    combine_files(args.directory, args.output, script_name)
