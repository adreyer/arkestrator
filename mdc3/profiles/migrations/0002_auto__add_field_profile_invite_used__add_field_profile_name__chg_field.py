# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Profile.invite_used'
        db.add_column('profiles_profile', 'invite_used', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['invites.Invite'], null=True), keep_default=False)

        # Adding field 'Profile.name'
        db.add_column('profiles_profile', 'name', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True), keep_default=False)

        # Changing field 'Profile.email_public'
        db.alter_column('profiles_profile', 'email_public', self.gf('django.db.models.fields.EmailField')(max_length=75))


    def backwards(self, orm):
        
        # Deleting field 'Profile.invite_used'
        db.delete_column('profiles_profile', 'invite_used_id')

        # Deleting field 'Profile.name'
        db.delete_column('profiles_profile', 'name')

        # Changing field 'Profile.email_public'
        db.alter_column('profiles_profile', 'email_public', self.gf('django.db.models.fields.BooleanField')())


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
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
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'invites.invite': {
            'Meta': {'object_name': 'Invite'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'approved_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'explanation': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite_code': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'invitee': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'inviter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'used': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'profiles.profile': {
            'Meta': {'object_name': 'Profile'},
            'aim_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'banned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'email_public': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'gchat_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '2500', 'blank': 'True'}),
            'invite_used': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['invites.Invite']", 'null': 'True'}),
            'ip_signup': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'last_events_view': ('django.db.models.fields.DateTimeField', [], {}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {}),
            'last_post': ('django.db.models.fields.DateTimeField', [], {}),
            'last_profile_update': ('django.db.models.fields.DateTimeField', [], {}),
            'last_view': ('django.db.models.fields.DateTimeField', [], {}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'new_message': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'photo_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'profile_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'security_answer': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'show_images': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '150', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['profiles']
