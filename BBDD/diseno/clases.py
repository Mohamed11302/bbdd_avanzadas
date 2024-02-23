from datetime import datetime

class dates:
    def __init__(self, date_id, year, month, day, hour, min, sec):
        self.date_id = date_id
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.min = min
        self.sec = sec

class Video:
    def __init__(self, video_id, title, statistics_id, category_id, duration, default_audio_language, type, tags=[]):
        self.video_id = video_id
        self.title = title
        self.statistics_id = statistics_id
        self.category_id = category_id
        self.duration = duration
        self.default_audio_language = default_audio_language
        self.type = type
        self.tags = tags

class Channel:
    def __init__(self, channel_id, name, statistics_id, language, country):
        self.channel_id = channel_id
        self.name = name
        self.statistics_id = statistics_id
        self.language = language
        self.country = country
    
class VideoStatistics:
    def __init__(self, stats_id, view_count, like_count, comment_count):
        self.stats_id = stats_id
        self.view_count = view_count
        self.like_count = like_count
        self.comment_count = comment_count

class ChannelStatistics:
    def __init__(self, stats_id, subscribers, view_count, num_videos):
        self.stats_id = stats_id
        self.subscribers = subscribers
        self.view_count = view_count
        self.num_videos = num_videos

class VideoStats:
    def __init__(self, stats_id, dates, video, channel):
        self.stats_id = stats_id
        self.dates = dates
        self.video = video
        self.channel = channel

class ChannelStats:
    def __init__(self, stats_id, dates, channel):
        self.stats_id = stats_id
        self.dates = dates
        self.channel = channel

    def get_stats_id(self):
        return self.stats_id

    def get_date(self):
        return self.dates

    def get_channel(self):
        return self.channel

    def set_stats_id(self, stats_id):
        self.stats_id = stats_id

    def set_date(self, dates):
        self.dates = dates

    def set_channel(self, channel):
        self.channel = channel


def create_date_from_csv(row, df, column_date, column_identifier):
    date_time_obj = datetime.strptime(row[column_date], '%Y-%m-%dT%H:%M:%SZ')
    date_id = row[column_identifier] + "_" + row[column_date]
    return dates(date_id, date_time_obj.year, date_time_obj.month, date_time_obj.day, date_time_obj.hour, date_time_obj.minute, date_time_obj.second)

def create_video_from_csv(row):
    tags = row['tags'].strip("[]").split(", ")
    return Video(row['id'], row['title'], str(row['id'])+"_statistics", row['categoryId'], row['duration'], row['defaultAudioLanguage'], row['type'], tags)

def create_channel_from_csv(row):
    return Channel(row['id'], row['name'], row['id'], row['language'], row['country'])

def create_video_statistics_from_csv(row):
    return VideoStatistics(str(row['id'])+"_statistics", row['viewCount'], row['likeCount'], row['commentCount'])

def create_channel_statistics_from_csv(row):
    return ChannelStatistics(row['id'], row['subscribers'], row['viewcount'], row['numvideos'])

def create_video_stats_from_csv(row, video, channel, dates):
    return VideoStats(row['id'], dates, video, channel)

def create_channel_stats_from_csv(row, channel, dates):
    return ChannelStats(row['id'], dates, channel)