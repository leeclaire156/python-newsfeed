def format_date(date):
  return date.strftime('%m/%d/%y') #strftime converts datetime object into a string

# Tests the format_date function with today's date, can be ran with `python app/utils/filters.py` in the terminal
# from datetime import datetime
# print(format_date(datetime.now()))

# formats urls on posts to just include the only the domain name (e.g. google.com as opposed to https://www.google.com/... etc)
def format_url(url):
  return url.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0].split('?')[0]

# Tests the format_url function with the following url, can be ran with `python app/utils/filters.py` in the terminal
# print(format_url('http://google.com/test/'))
# print(format_url('https://www.google.com?q=test'))

def format_plural(amount, word):
  if amount != 1:
    return word + 's'

  return word

# should return cats/dogs if its more than 1 count and just cat/dog if its 1 count
# print(format_plural(2, 'cat'))
# print(format_plural(1, 'dog'))