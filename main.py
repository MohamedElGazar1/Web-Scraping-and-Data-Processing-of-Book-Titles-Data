import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "db_books.csv"


def process_chunk(chunk):
    start_time = time.time()
    summary_stats = chunk.describe()
    missing_values = chunk.isnull().sum()
    end_time = time.time()

    # Print or do further analysis based on your requirements
    print("Summary Statistics:")
    print(summary_stats)

    print("\nMissing Values:")
    print(missing_values)
    print(f"Chunk processed in {end_time - start_time:.2f} seconds")


def load_data_with_chunksize(file_path, chunk_size):
    start_time = time.time()
    chunks = []
    for x in pd.read_csv(file_path, chunksize=chunk_size):
        process_chunk(x)  # Process each chunk
        chunks.append(x)
    df = pd.concat(chunks, ignore_index=True)
    end_time = time.time()
    return end_time - start_time


chunk_sizes_to_test = [10, 50, 100, 200, 1000]

best_chunk_size = None
best_time_taken = float('inf')

for chunk_size in chunk_sizes_to_test:
    time_taken = load_data_with_chunksize(file_path, chunk_size)
    print(f"Chunk Size: {chunk_size}, Time Taken: {time_taken:.4f} seconds")
    if time_taken < best_time_taken:
        best_chunk_size = chunk_size
        best_time_taken = time_taken

print(f"\nBest Chunk Size: {best_chunk_size}, Best Time Taken: {best_time_taken:.4f} seconds")

chunk_list = []
for chunk in pd.read_csv(file_path, chunksize=best_chunk_size):
    chunk_list.append(chunk)

df1 = pd.concat(chunk_list)

# Add this part to visualize the most frequent languages
def visualize_most_frequent_languages(df):
    """
    Visualizes the most frequent languages in the 'Language' column of the DataFrame.
    """
    language_counts = df['Language'].value_counts()

    # Create a bar plot for the most frequent languages
    plt.figure(figsize=(10, 6))
    sns.barplot(x=language_counts.index, y=language_counts.values, palette='viridis')
    plt.title("Most Frequent Languages in db_books.csv")
    plt.xlabel("Language")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.show()

# Visualize the most frequent languages in df1
visualize_most_frequent_languages(df1)

# Web scraping to get book titles
response = requests.get("http://books.toscrape.com")
soup = BeautifulSoup(response.content)

titles = soup.find_all("h3")

with open('book_titles.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Title page'])
    for title in titles:
        csv_writer.writerow([title.text.strip()])

print("Data has been saved to book_titles.csv file.")

# Combine the data from db_books.csv and book_titles.csv
df2 = pd.read_csv("book_titles.csv")
df1 = pd.DataFrame({'Title page': df1['Title']})
result = pd.concat([df1, df2], ignore_index=True)
result.to_csv("output.csv", index=False)
print("Data has been saved to output.csv file.")