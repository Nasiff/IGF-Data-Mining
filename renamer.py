import os

for i in range(2006, 2018, 1):
    path = '/Users/User/Desktop/Mine/Workspace/vs_workspace/IGF_Mining/Transcripts_Chunked_Test/Chunked_' + str(i)
    print ("Renaming transcripts from the year " + str(i))
    for filename in os.listdir(path):
        prefix = filename[0:11]
        postfix = filename[11:-4]
        zero_filled = postfix.zfill(4)
        os.rename(path + "/" + filename, path + "/" + prefix + zero_filled + ".txt")

# for i in range(2011, 2012, 1):
#     path = '/Users/User/Desktop/Mine/Workspace/vs_workspace/IGF_Mining/Transcripts_Chunked_Test/Chunked_' + str(i)
#     num = 1229
#     for filename in os.listdir(path):
#         if "alt" in filename:
#             num = num + 1
#             prefix = filename[0:11]
#             postfix = num
#             os.rename(path + "/" + filename, path + "/" + prefix + str(postfix) + ".txt")