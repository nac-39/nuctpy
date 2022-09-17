import nuctpy

announcement = nuctpy.Announcement()

SITE_ID = "<site_id>"
print(announcement.site(SITE_ID))
print(announcement.user())
print(announcement.motd())
