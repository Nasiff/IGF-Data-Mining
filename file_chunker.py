import os

for i in range(2006, 2018, 1):
    # Directory to chunk
    FILE_DIR = '/Users/nasif/Desktop/Mine/Workspace/vs_workspace/IGF-Data-Mining/Transcripts_Chunked/Transcripts_' + str(i)
    list_of_files_in_dir = os.listdir(FILE_DIR)
    print("Splitting the year " + str(i) + " into chunks")
    chunk_counter = 0

    # Chunk all the files in this directory
    for file in list_of_files_in_dir:
        print("Chunking file: " + str(file))
        input = FILE_DIR + "/" + file
        try:
            text_list = open(input, "r").read().split()
            total_number_of_words = len(text_list)
            number_of_words_per_chunk = 1001
            for j in range(0, total_number_of_words, number_of_words_per_chunk):
                chunk_counter = chunk_counter + 1
                file_chunk = open(FILE_DIR + "/" + str(i) + "_Chunk_" + str(chunk_counter).zfill(4) + ".txt", "w")
                file_chunk.write(" ".join(text_list[j:j+1001]))
                file_chunk.close()
            # Remove the original file after it has been chunked
            os.remove(input)
        except:
            pass
