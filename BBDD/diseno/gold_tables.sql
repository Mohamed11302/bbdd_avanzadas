CREATE TABLE IF NOT EXISTS gold.dates (
    date_id VARCHAR(255) PRIMARY KEY,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    hour INT NOT NULL,
    min INT NOT NULL,
    sec INT NOT NULL
);

CREATE TABLE IF NOT EXISTS gold.videostatistics(
    stats_id VARCHAR(255) PRIMARY KEY,
    view_count INT NOT NULL,
    like_count INT NOT NULL,
    comment_count INT NOT NULL
);

CREATE TABLE IF NOT EXISTS gold.channelstatistics(
    stats_id VARCHAR(255) PRIMARY KEY,
    subscribers INT NOT NULL,
    view_count INT NOT NULL,
    num_videos INT NOT NULL
);

CREATE TABLE IF NOT EXISTS gold.video(
    video_id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    statistics_id VARCHAR(255) NOT NULL,
    category_id INT NOT NULL,
    duration VARCHAR(255) NOT NULL,
    default_audio_language VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    FOREIGN KEY (statistics_id) REFERENCES gold.videostatistics(stats_id)
);

CREATE TABLE IF NOT EXISTS gold.channel (
    channel_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    statistics_id VARCHAR(255) NOT NULL,
    language VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    FOREIGN KEY (statistics_id) REFERENCES gold.channelstatistics(stats_id)
);

CREATE TABLE IF NOT EXISTS gold.fact_videostats (
    stats_id VARCHAR(255) PRIMARY KEY,
    date_id VARCHAR(255) NOT NULL,
    video_id VARCHAR(255) NOT NULL,
    channel_id VARCHAR(255) NOT NULL,
    FOREIGN KEY (date_id) REFERENCES gold.dates(date_id),
    FOREIGN KEY (video_id) REFERENCES gold.video(video_id),
    FOREIGN KEY (channel_id) REFERENCES gold.channel(channel_id)
);

CREATE TABLE IF NOT EXISTS gold.fact_channelstats (
    stats_id VARCHAR(255) PRIMARY KEY,
    date_id VARCHAR(255) NOT NULL,
    channel_id VARCHAR(255) NOT NULL,
    FOREIGN KEY (date_id) REFERENCES gold.dates(date_id),
    FOREIGN KEY (channel_id) REFERENCES gold.channel(channel_id)
);

CREATE TABLE IF NOT EXISTS gold.tag (
    tag_id SERIAL PRIMARY KEY,
    tag_name VARCHAR(255) NOT NULL,
    video_id VARCHAR(255) NOT NULL,
    FOREIGN KEY (video_id) REFERENCES gold.video(video_id)
);
