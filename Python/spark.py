from pyspark.sql import Row
from pyspark.sql.functions import size, first, last, countDistinct, col


genius = sqlContext.read.parquet('/user/big_pharmaceuta/genius/*')
youtube = sqlContext.read.parquet('/user/big_pharmaceuta/youtube/*')

genius_lyrics = genius.map(lambda x: Row(id2=x.id, length=len(x.lyrics)))
genius_new = sqlContext.createDataFrame(genius_lyrics)
genius_new.show()

all_stats = genius.join(youtube, genius.id == youtube.songid, 'inner')
all_stats = all_stats.join(genius_new, genius.id == genius_new.id2, 'inner')
all_stats.show()
all_stats.printSchema()
all_stats = all_stats.withColumn('like_per_view',col('likeCount')/col('viewCount')).withColumn('dislike_ratio',col('dislikeCount')/(col('dislikeCount')+ col('likeCount'))).withColumn('annotation_per_comment',col('annotation_count')/col('commentCount'))
all_stats_agg = all_stats.groupBy('primary_artist_name').agg({'like_per_view':'mean','dislike_ratio':'mean', 'annotation_per_comment':'mean', 'annotation_count':'sum', 'id':'count'})
all_stats_agg = all_stats_agg.withColumn('annotation_per_song', col('sum(annotation_count)')/col('count(id)'))

all_stats_agg.show()