# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'WordFilter'
        db.create_table('bbking_wordfilter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('base_re', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('base_replace', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ignore_case', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('bbking', ['WordFilter'])


    def backwards(self, orm):
        
        # Deleting model 'WordFilter'
        db.delete_table('bbking_wordfilter')


    models = {
        'bbking.wordfilter': {
            'Meta': {'object_name': 'WordFilter'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'base_re': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'base_replace': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore_case': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['bbking']
