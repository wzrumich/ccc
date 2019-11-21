# Generated by Django 2.2.1 on 2019-06-16 16:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('version', models.CharField(default='', max_length=13)),
                ('firstgame', models.CharField(default='', max_length=13)),
                ('secondgame', models.CharField(default='', max_length=13)),
                ('thirdgame', models.CharField(default='', max_length=13)),
                ('totalearning', models.FloatField(default=0)),
                ('experimentearning', models.FloatField(default=0)),
                ('startedstudy', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedstudy', models.DateTimeField(default=django.utils.timezone.now)),
                ('optout', models.BooleanField(default=0)),
                ('postpone', models.BooleanField(default=0)),
                ('age', models.IntegerField(default=-1)),
                ('gender', models.CharField(default='', max_length=127)),
                ('emailsperday', models.CharField(default='', max_length=25)),
                ('ownpc', models.BooleanField(default=0)),
                ('ownsmartphone', models.BooleanField(default=0)),
                ('ownpda', models.BooleanField(default=0)),
                ('ownotherdevice', models.BooleanField(default=0)),
                ('otherdevice', models.CharField(default='', max_length=255)),
                ('internetuse', models.CharField(default='', max_length=25)),
                ('fullname', models.CharField(default='', max_length=255)),
                ('street', models.CharField(default='', max_length=255)),
                ('city', models.CharField(default='', max_length=255)),
                ('state', models.CharField(default='', max_length=255)),
                ('zipcode', models.CharField(default='', max_length=255)),
                ('yearsofeduction', models.CharField(default='', max_length=127)),
                ('ethnicity', models.CharField(default='', max_length=127)),
                ('maritalstatus', models.CharField(default='', max_length=127)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question1', models.IntegerField(default=-1)),
                ('question2', models.IntegerField(default=-1)),
                ('question3', models.IntegerField(default=-1)),
                ('question4', models.IntegerField(default=-1)),
                ('correct1', models.IntegerField(default=-1)),
                ('correct2', models.IntegerField(default=-1)),
                ('correct3', models.IntegerField(default=-1)),
                ('correct4', models.IntegerField(default=-1)),
                ('questionclicked1', models.IntegerField(default=-1)),
                ('questionclicked2', models.IntegerField(default=-1)),
                ('questionclicked3', models.IntegerField(default=-1)),
                ('questionclicked4', models.IntegerField(default=-1)),
                ('questionrightclicked1', models.IntegerField(default=-1)),
                ('questionrightclicked2', models.IntegerField(default=-1)),
                ('questionrightclicked3', models.IntegerField(default=-1)),
                ('questionrightclicked4', models.IntegerField(default=-1)),
                ('questionhovered1', models.IntegerField(default=-1)),
                ('questionhovered2', models.IntegerField(default=-1)),
                ('questionhovered3', models.IntegerField(default=-1)),
                ('questionhovered4', models.IntegerField(default=-1)),
                ('questionhoveredseconds1', models.FloatField(default=-1)),
                ('questionhoveredseconds2', models.FloatField(default=-1)),
                ('questionhoveredseconds3', models.FloatField(default=-1)),
                ('questionhoveredseconds4', models.FloatField(default=-1)),
                ('started', models.DateTimeField(default=django.utils.timezone.now)),
                ('finished', models.DateTimeField(default=django.utils.timezone.now)),
                ('startedquestion1', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedquestion1', models.DateTimeField(default=django.utils.timezone.now)),
                ('startedquestion2', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedquestion2', models.DateTimeField(default=django.utils.timezone.now)),
                ('startedquestion3', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedquestion3', models.DateTimeField(default=django.utils.timezone.now)),
                ('startedquestion4', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedquestion4', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.User')),
            ],
        ),
        migrations.CreateModel(
            name='Thankyou',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pretestComment', models.TextField(blank=True, null=True)),
                ('trainingComment', models.TextField(blank=True, null=True)),
                ('gamesComment', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.User')),
            ],
        ),
        migrations.CreateModel(
            name='Pretest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question1', models.IntegerField(default=-1)),
                ('question2', models.IntegerField(default=-1)),
                ('question3', models.IntegerField(default=-1)),
                ('question4', models.IntegerField(default=-1)),
                ('question5', models.IntegerField(default=-1)),
                ('question6', models.IntegerField(default=-1)),
                ('question7', models.IntegerField(default=-1)),
                ('correct1', models.IntegerField(default=-1)),
                ('correct2', models.IntegerField(default=-1)),
                ('correct3', models.IntegerField(default=-1)),
                ('correct4', models.IntegerField(default=-1)),
                ('correct5', models.IntegerField(default=-1)),
                ('correct6', models.IntegerField(default=-1)),
                ('correct7', models.IntegerField(default=-1)),
                ('questionclicked1', models.IntegerField(default=-1)),
                ('questionclicked2', models.IntegerField(default=-1)),
                ('questionclicked3', models.IntegerField(default=-1)),
                ('questionclicked4', models.IntegerField(default=-1)),
                ('questionclicked5', models.IntegerField(default=-1)),
                ('questionclicked6', models.IntegerField(default=-1)),
                ('questionclicked7', models.IntegerField(default=-1)),
                ('questionrightclicked1', models.IntegerField(default=-1)),
                ('questionrightclicked2', models.IntegerField(default=-1)),
                ('questionrightclicked3', models.IntegerField(default=-1)),
                ('questionrightclicked4', models.IntegerField(default=-1)),
                ('questionrightclicked5', models.IntegerField(default=-1)),
                ('questionrightclicked6', models.IntegerField(default=-1)),
                ('questionrightclicked7', models.IntegerField(default=-1)),
                ('questionhovered1', models.IntegerField(default=-1)),
                ('questionhovered2', models.IntegerField(default=-1)),
                ('questionhovered3', models.IntegerField(default=-1)),
                ('questionhovered4', models.IntegerField(default=-1)),
                ('questionhovered5', models.IntegerField(default=-1)),
                ('questionhovered6', models.IntegerField(default=-1)),
                ('questionhovered7', models.IntegerField(default=-1)),
                ('questionhoveredseconds1', models.FloatField(default=-1)),
                ('questionhoveredseconds2', models.FloatField(default=-1)),
                ('questionhoveredseconds3', models.FloatField(default=-1)),
                ('questionhoveredseconds4', models.FloatField(default=-1)),
                ('questionhoveredseconds5', models.FloatField(default=-1)),
                ('questionhoveredseconds6', models.FloatField(default=-1)),
                ('questionhoveredseconds7', models.FloatField(default=-1)),
                ('startedquestion1', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedquestion1', models.DateTimeField(default=django.utils.timezone.now)),
                ('startedquestion2', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedquestion2', models.DateTimeField(default=django.utils.timezone.now)),
                ('startedquestion3', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedquestion3', models.DateTimeField(default=django.utils.timezone.now)),
                ('startedquestion4', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedquestion4', models.DateTimeField(default=django.utils.timezone.now)),
                ('startedquestion5', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedquestion5', models.DateTimeField(default=django.utils.timezone.now)),
                ('startedquestion6', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedquestion6', models.DateTimeField(default=django.utils.timezone.now)),
                ('startedquestion7', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedquestion7', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.User')),
            ],
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invested', models.IntegerField(default=-1)),
                ('returned0', models.IntegerField(default=-1)),
                ('returned1', models.IntegerField(default=-1)),
                ('returned2', models.IntegerField(default=-1)),
                ('returned3', models.IntegerField(default=-1)),
                ('returned4', models.IntegerField(default=-1)),
                ('returned5', models.IntegerField(default=-1)),
                ('otherreturned', models.IntegerField(default=-1)),
                ('otherinvested', models.IntegerField(default=-1)),
                ('points', models.IntegerField(default=-1)),
                ('startedinvested', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedinvested', models.DateTimeField(default=django.utils.timezone.now)),
                ('startedreturned0', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedreturned0', models.DateTimeField(default=django.utils.timezone.now)),
                ('startedreturned1', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedreturned1', models.DateTimeField(default=django.utils.timezone.now)),
                ('startedreturned2', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedreturned2', models.DateTimeField(default=django.utils.timezone.now)),
                ('startedreturned3', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedreturned3', models.DateTimeField(default=django.utils.timezone.now)),
                ('startedreturned4', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedreturned4', models.DateTimeField(default=django.utils.timezone.now)),
                ('startedreturned5', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedreturned5', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('otheruser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='otherreturned_set', to='games.User')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.User')),
            ],
        ),
        migrations.CreateModel(
            name='HoltLaury',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decision', models.IntegerField(default=0)),
                ('option1', models.BooleanField(default=0)),
                ('option2', models.BooleanField(default=0)),
                ('option3', models.BooleanField(default=0)),
                ('option4', models.BooleanField(default=0)),
                ('option5', models.BooleanField(default=0)),
                ('option6', models.BooleanField(default=0)),
                ('option7', models.BooleanField(default=0)),
                ('option8', models.BooleanField(default=0)),
                ('option9', models.BooleanField(default=0)),
                ('option10', models.BooleanField(default=0)),
                ('die1', models.IntegerField(default=0)),
                ('die2', models.IntegerField(default=0)),
                ('die3', models.IntegerField(default=0)),
                ('die4', models.IntegerField(default=0)),
                ('die5', models.IntegerField(default=0)),
                ('die6', models.IntegerField(default=0)),
                ('die7', models.IntegerField(default=0)),
                ('die8', models.IntegerField(default=0)),
                ('die9', models.IntegerField(default=0)),
                ('die10', models.IntegerField(default=0)),
                ('points', models.FloatField(default=0)),
                ('originalPoints', models.FloatField(default=0)),
                ('willingness', models.FloatField(default=0)),
                ('willingnessRand', models.FloatField(default=16)),
                ('started', models.DateTimeField(default=django.utils.timezone.now)),
                ('finished', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.User')),
            ],
        ),
        migrations.CreateModel(
            name='Gamble',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chosen', models.IntegerField(default=0)),
                ('coin1', models.BooleanField(default=0)),
                ('coin2', models.BooleanField(default=0)),
                ('coin3', models.BooleanField(default=0)),
                ('coin4', models.BooleanField(default=0)),
                ('coin5', models.BooleanField(default=0)),
                ('coin6', models.BooleanField(default=0)),
                ('coin7', models.BooleanField(default=0)),
                ('coin8', models.BooleanField(default=0)),
                ('coin9', models.BooleanField(default=0)),
                ('points', models.FloatField(default=0)),
                ('originalPoints', models.FloatField(default=0)),
                ('willingness', models.FloatField(default=0)),
                ('willingnessRand', models.FloatField(default=16)),
                ('started', models.DateTimeField(default=django.utils.timezone.now)),
                ('finished', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.User')),
            ],
        ),
    ]