# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    depends_on = ( 
        ("events", "0001_initial.py"),
    )
    def forwards(self, orm):
        
        # Adding field 'Profile.market'
        db.add_column('profiles_profile', 'market', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Market'], null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Profile.market'
        db.delete_column('profiles_profile', 'market_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'events.market': {
            'Meta': {'object_name': 'Market'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'US/Eastern'", 'max_length': '50'})
        },
        'invites.invite': {
            'Meta': {'object_name': 'Invite'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'approved_invite'", 'null': 'True', 'to': "orm['auth.User']"}),
            'approved_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'explanation': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite_code': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'invitee': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'inviter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_invite'", 'to': "orm['auth.User']"}),
            'rejected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'used': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'profiles.profile': {
            'Meta': {'object_name': 'Profile'},
            'aim_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'collapse_size': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'email_public': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'gtalk_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'invite_used': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['invites.Invite']", 'null': 'True'}),
            'ip_signup': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'last_events_view': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_post': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_profile_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_view': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'market': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Market']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'photo_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'profile_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'show_images': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '150', 'blank': 'True'})
        }
    }

    complete_apps = ['profiles']
