import re

def validate_search(dist, checkin, checkout):

    if dist is None or len(dist.strip()) > 200:
        return False

    date_matcher = re.compile(r"(\d+-\d+-\d+)")

    if checkin is not None and checkin != "" and not date_matcher.match(checkin):
        return False

    if checkout is not None and checkout != "" and not date_matcher.match(checkout):
        return False

    return True
