import cookielib
import mechanize
from BeautifulSoup import BeautifulSoup
import html2text
import re

base_url='http://www.ruutu.fi'
media_cache_host="http://gatling.nelonenmedia.fi"

swfUrl = 'http://www.ruutu.fi/sites/all/modules/custom/ruutu_video/files/jwplayer/7.1.63.1/player.swf'

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Open some site, let's pick a random one, the first that pops in mind:
r = br.open(base_url)
html = r.read()

# Show the source
#print html
# or
#print br.response().read()

# or
#print br.response().info()

# Show the available forms
#for f in br.forms():
#    print f

br.select_form(nr=1)
br.form['name'] = 'juha.majuri@gmail.com'
br.form['pass'] = 'no243va'

# Login
br.submit()

#print br.response().read()

#r = br.open('http://www.ruutu.fi/urheilu/sm-liiga')
r = br.open('http://www.ruutu.fi/leffat')

#print br.response().read()

#all_game_links = [l for l in br.links(url_regex='/ohjelmat/sm-liiga/')]
all_game_links = [l for l in br.links(url_regex='/ohjelmat/elokuvat/')]
links_with_text = []

for game_link in all_game_links:
    if game_link.text:
        links_with_text.append(game_link)

for game_link in links_with_text:
    print game_link

program_link=links_with_text[7]
print program_link.url

program_url=base_url + program_link.url
print program_url
r = br.open(program_url)

p = re.compile('data-media-id="([0-9]*)')

tmp = br.response().read()

m = p.findall(tmp)

video_id = m[0]

media_cache_url = media_cache_host + "/media-xml-cache?type=video_clip&site=www.ruutu.fi&gRVBR=0&id=" + video_id

print media_cache_url

r = br.open(media_cache_url)

p = re.compile('<SourceFile>(.*)</SourceFile>')

m = p.findall(br.response().read())

print br.response().read()

print m[0]

