# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    depends_on = (
        ("invites", "0002_auto__chg_field_invite_approved_on.py"),
        )

    def forwards(self, orm):
        
        # Adding model 'Profile'
        db.create_table('profiles_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('ip_signup', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('new_message', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_view', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_post', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_profile_update', self.gf('django.db.models.fields.DateTimeField')()),
            ('profile_views', self.gf('django.db.models.fields.IntegerField')()),
            ('last_events_view', self.gf('django.db.models.fields.DateTimeField')()),
            ('banned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('aim_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('gchat_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=150)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=2500)),
            ('email_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('security_answer', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('show_images', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('photo_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('profiles', ['Profile'])


    def backwards(self, orm):
        
        # Deleting model 'Profile'
        db.delete_table('profiles_profile')


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
        'profiles.profile': {
            'Meta': {'object_name': 'Profile'},
            'aim_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'banned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'email_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gchat_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '2500'}),
            'ip_signup': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'last_events_view': ('django.db.models.fields.DateTimeField', [], {}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {}),
            'last_post': ('django.db.models.fields.DateTimeField', [], {}),
            'last_profile_update': ('django.db.models.fields.DateTimeField', [], {}),
            'last_view': ('django.db.models.fields.DateTimeField', [], {}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'new_message': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'photo_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'profile_views': ('django.db.models.fields.IntegerField', [], {}),
            'security_answer': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'show_images': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '150'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['profiles']
