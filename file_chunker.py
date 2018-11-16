import os

for i in range(2015, 2016, 1):
    FILE_DIR = '/Users/User/Desktop/Mine/Workspace/vs_workspace/IGF_Mining/Transcripts_Zip/Transcripts_Chunked/Transcripts_' + str(i)
    list_of_files_in_dir = os.listdir(FILE_DIR)
    # print (list_of_files_in_dir)
    print("Splitting the year " + str(i) + " into chunks")
    chunk_counter = 0
    for file in list_of_files_in_dir:
        print("Chunking file: " + str(file))
        input = FILE_DIR + "/" + file
        try:
            text_list = open(input, "r").read().split()
            total_number_of_words = len(text_list)
            number_of_words_per_chunk = 1001
            # print(file + " " + str(total_number_of_words))
            for j in range(0, total_number_of_words, number_of_words_per_chunk):
                chunk_counter = chunk_counter + 1
                file_chunk = open(FILE_DIR + "/" + str(i) + "_chunk_alt" + str(chunk_counter) + ".txt", "w")
                file_chunk.write(" ".join(text_list[j:j+1001]))
                file_chunk.close()
            os.remove(input)
        except:
            pass
        
# FILE_DIR = "/Users/User/Desktop/Mine/Workspace/vs_workspace/IGF_Mining/test.txt"
# # list_of_files_in_dir = os.listdir(FILE_DIR)
# # print (list_of_files_in_dir)
# print("Splitting the year " + " into chunks")
# print("Chunking file: test")
# input = FILE_DIR
# try:
#     text_list = open(input, "r").read().split()
#     total_number_of_words = len(text_list)
#     number_of_words_per_chunk = 1000
#     print(str(total_number_of_words))
#     chunk_counter = 0
#     for j in range(0, total_number_of_words, number_of_words_per_chunk):
#         chunk_counter = chunk_counter + 1
#         file_chunk = open(FILE_DIR +  "_chunk_" + str(chunk_counter) + ".txt", "w")
#         file_chunk.write(" ".join(text_list[j:j+1001]))
#         file_chunk.close()
#     os.remove(input)
# except FileNotFoundError:
#     print (FileNotFoundError)
