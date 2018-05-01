import multiprocessing
import gensim
from random import shuffle
import pickle

#将每个歌单的歌曲转化为序列
def parse_playlist_get_sequence(in_line, playlist_sequence):
	song_sequence = []
	contents = in_line.strip().split("\t")
	#解析歌单序列
	for song in contents[1:]:
		try:
			song_id, song_name, artist, popularity = song.split(":::")
			song_sequence.append(song_id)
		except:
			print("song format error")
			print(song+"\n")
    #由于歌单的歌曲其实是无序的，因此，这里对每个歌单进行随机打乱
	for i in range(len(song_sequence)):
		shuffle(song_sequence)
		playlist_sequence.append(song_sequence)

#训练song2vec模型
def train_song2vec(in_file, out_file):
	#所有歌单序列
	playlist_sequence = []
	#遍历所有歌单
	for line in open(in_file,encoding='utf-8'):
		parse_playlist_get_sequence(line, playlist_sequence)
	#使用word2vec训练
	cores = multiprocessing.cpu_count()
	print("using all "+str(cores)+" cores")
	print("Training word2vec model...")
    #设置每个歌曲的向量长度为150，窗口大小为7，出现次数少于3的歌曲给予剔除
	model = gensim.models.Word2Vec(sentences=playlist_sequence, size=150, min_count=3, window=7, workers=cores)
	print("Saving model...")
	model.save(out_file)

#开始训练模型
train_song2vec('C:\\Users\\T\\Desktop\\python视频\\163_music_playlist.txt','C:\\Users\\T\\Desktop\\python视频\\song2vec.model')

#加载模型
model=gensim.models.Word2Vec.load('C:\\Users\\T\\Desktop\\python视频\\song2vec.model')

#加载歌曲id=>歌曲名字映射文件
song_id_name_dict=pickle.load(open('C:\\Users\\T\\Desktop\\python视频\\song.pkl','rb'))

#从1000到1500每隔50取一首歌，然后计算每首歌最相似的歌曲
song_id_list = list(song_id_name_dict.keys())[1000:1500:50]
for song_id in song_id_list:
    result_song_list = model.most_similar(song_id)
    print(song_id, song_id_name_dict[song_id])
    print("\n相似歌曲 和 相似度 分别为:")
    for song in result_song_list:
        print("\t", song_id_name_dict[song[0]], song[1])