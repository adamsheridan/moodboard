from django.db import models
from django.db.models.signals import pre_save, post_save
from django.template.defaultfilters import slugify
from moodboard.slug import unique_slugify
import os, time, datetime
import urllib.request as urlr

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static/images/data/'))

'''
	Models
'''

class Board(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	date = models.DateField(default=datetime.date.today)
	slug = models.SlugField(blank=True)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id: #ensures slug is generated only on creation of record
			slug = self.name
			unique_slugify(self, slug)

		super(Board, self).save(*args, **kwargs)

class Image(models.Model):
	name = models.CharField(max_length=255)
	url_external = models.URLField(max_length=1024)
	url_internal = models.CharField(max_length=1024, blank=True)
	date = models.DateField(default=datetime.date.today)
	board = models.ForeignKey(Board)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		format = self.url_external.split('.')[-1]
		filename = str(round(time.time()*1000))
		self.url_internal = filename+'.'+format
		super(Image, self).save(*args, **kwargs)

class Comment(models.Model):
	name = models.CharField(max_length=255)
	comment = models.TextField()
	date = models.DateField(default=datetime.date.today)
	image = models.ForeignKey(Image)

	def __unicode__(self):
		return self.comment


'''
	Signals
'''

def download_image(sender, instance=True, **kwargs):
	model = Image.objects.get(pk=instance.pk)

	print('downloading image from: {0}'.format(instance.url_external))

	image = urlr.urlopen(model.url_external)
	filename = model.url_internal
	path = os.path.join(DATA_DIR, filename)
	output = open(path, 'wb')
	output.write(image.read())
	output.close()

post_save.connect(download_image, sender=Image)