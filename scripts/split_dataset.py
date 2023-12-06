import os
import pandas as pd

def split_and_store(input_file, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Read the main dataset
    df = pd.read_csv(input_file)

    # Split the dataset into chunks of 10 rows each
    chunk_size = 10
    chunks = [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]

    # Save each chunk to a separate file in the output folder
    for i, chunk in enumerate(chunks):
        output_file = os.path.join(output_folder, f'chunk_{i + 1}.csv')
        chunk.to_csv(output_file, index=False)
        print(f"Saved {chunk_size} rows to {output_file}")

if __name__ == "__main__":
    # Specify the path to your main dataset and the output folder
    main_dataset_file = "/application_record.csv"
    output_folder = "Folder_A"

    # Call the function to split and store the dataset
    split_and_store(main_dataset_file, output_folder)
