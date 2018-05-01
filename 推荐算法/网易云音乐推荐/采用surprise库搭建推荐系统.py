import json
import surprise
import pickle
from surprise import Reader
from surprise import Dataset
from surprise import KNNBasic

#解析歌单json文件
def parse_song_line(in_line):
    data=json.loads(in_line)
    name = data['result']['name']
    tags = ",".join(data['result']['tags'])
    subscribed_count = data['result']['subscribedCount']
    #如果歌单的关注量少于100，则给予剔除
    if (subscribed_count<100):
        return False
    playlist_id = data['result']['id']
    song_info = ''
    songs = data['result']['tracks']
    for song in songs:
        try:
            song_info += "\t" + ":::".join(
                [str(song['id']), song['name'], song['artists'][0]['name'], str(song['popularity'])])
        except Exception:
            continue
    return name + "##" + tags + "##" + str(playlist_id) + "##" + str(subscribed_count) + song_info

def parse_file(in_file,out_file):
    out=open(out_file,'w',encoding='utf-8')
    for line in open(in_file,encoding='utf-8'):
        result=parse_song_line(line)
        if result:
            out.write(result.strip()+"\n")
    out.close()

parse_file('C:\\Users\\T\\Desktop\\python视频\\playlistdetail.all.json','C:\\Users\\T\\Desktop\\python视频\\163_music_playlist.txt')


#将数据转化成surprise支持的格式，即user item rating timestamp
def is_null(s):
    return len(s.split(",")) > 2

def parse_song_info(song_info):
    try:
        song_id, name, artist, popularity = song_info.split(":::")
        #设置时间戳都为1300000,这里时间不起作用
        return ",".join([song_id, "1.0", '1300000'])
    except Exception:
        return ""

def parse_playlist_line(in_line):
    try:
        contents = in_line.strip().split("\t")
        name, tags, playlist_id, subscribed_count = contents[0].split("##")
        songs_info = map(lambda x: playlist_id + "," + parse_song_info(x), contents[1:])
        songs_info = filter(is_null, songs_info)
        return "\n".join(songs_info)
    except Exception:
        return False

def parse_file(in_file, out_file):
    out = open(out_file, 'w',encoding='utf-8')
    for line in open(in_file,encoding='utf-8'):
        result = parse_playlist_line(line)
        if (result):
            out.write(result.strip() + "\n")
    out.close()

parse_file("C:\\Users\\T\\Desktop\\python视频\\163_music_playlist.txt", "C:\\Users\\T\\Desktop\\python视频\\163_music_suprise_format.txt")


#建立歌单id与歌单名字的映射、歌曲id与歌曲名字的映射
def parse_playlist_get_info(in_line, playlist_dic, song_dic):
    contents = in_line.strip().split("\t")
    name, tags, playlist_id, subscribed_count = contents[0].split("##")
    playlist_dic[playlist_id] = name
    for song in contents[1:]:
        try:
            song_id, song_name, artist, popularity = song.split(":::")
            song_dic[song_id] = song_name + "\t" + artist
        except:
            print("song format error")
            print(song + "\n")

def parse_file(in_file, out_playlist, out_song):
    # 从歌单id到歌单名称的映射字典
    playlist_dic = {}
    # 从歌曲id到歌曲名称的映射字典
    song_dic = {}
    for line in open(in_file,encoding='utf-8'):
        parse_playlist_get_info(line, playlist_dic, song_dic)
    # 把映射字典保存在二进制文件中
    pickle.dump(playlist_dic, open(out_playlist, "wb"))
    # 可以通过 playlist_dic = pickle.load(open("playlist.pkl","rb"))重新载入
    pickle.dump(song_dic, open(out_song, "wb"))

parse_file("C:\\Users\\T\\Desktop\\python视频\\163_music_playlist.txt", "C:\\Users\\T\\Desktop\\python视频\\playlist.pkl", "C:\\Users\\T\\Desktop\\python视频\\song.pkl")


#加载歌单id=>歌单名的映射
id_name_dic=pickle.load(open("C:\\Users\\T\\Desktop\\python视频\\playlist.pkl",'rb'))
#构建歌单名=>歌单id的映射
name_id_dic={}
for playlist_id in id_name_dic:
    name_id_dic[id_name_dic[playlist_id]]=playlist_id


#读取数据
#指定文件的格式
reader=Reader(line_format="user item rating timestamp",sep=',')
music_data=Dataset.load_from_file('C:\\Users\\T\\Desktop\\python视频\\163_music_suprise_format.txt',reader)
#将整个数据作为训练集
trainset=music_data.build_full_trainset()

#查看用户数量和物品数量
trainset.n_users
trainset.n_items

#训练协同过滤模型,这里采用用户协同过滤
algo=KNNBasic()
algo.train(trainset)

#计算第39个歌单的前10个近邻歌单
current_playlist_name=list(name_id_dic.keys())[39]
print(current_playlist_name)
current_playlist_id=name_id_dic[current_playlist_name]
print(current_playlist_id)
#映射到内部user_id
playlist_inner_id=algo.trainset.to_inner_uid(current_playlist_id)
#获取前10个近邻
playlist_neighbors=algo.get_neighbors(playlist_inner_id,k=10)
#将近邻映射回原来的id
playlist_neighbors=[algo.trainset.to_raw_uid(inner_id) for inner_id in playlist_neighbors]
#将歌单id映射回歌单名字
playlist_neighbors=[id_name_dic[id] for id in playlist_neighbors]
playlist_neighbors


#加载歌曲id=>歌曲名字映射文件
song_id_name_dic=pickle.load(open("C:\\Users\\T\\Desktop\\python视频\\song.pkl",'rb'))
#构建歌单名=>歌单id的映射
song_name_id_dic={}
for song_id in song_id_name_dic:
    song_name_id_dic[song_id_name_dic[song_id]]=song_id

#对用户进行推荐，这里选择4号用户
user_inner_id = 1
user_rating = trainset.ur[user_inner_id]
items = map(lambda x:x[0], user_rating)
for song in items:
    print(song_id_name_dic[trainset.to_raw_iid(song)])

#模型的保存和加载
surprise.dump.dump('C:\\Users\\T\\Desktop\\python视频\\recommendation.model',algo=algo)
algo=surprise.dump.load('C:\\Users\\T\\Desktop\\python视频\\recommendation.model')


