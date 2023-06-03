import re

TAGS_PATTERN = re.compile(r"#([\w]+)")
MENTIONS_PATTERN = re.compile(r"@([\w]+)")

def get_mentions_and_tags(tweet):
    tags = TAGS_PATTERN.findall(tweet)
    mentions = MENTIONS_PATTERN.findall(tweet)
    return tags, mentions