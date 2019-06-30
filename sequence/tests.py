import json
from datetime import datetime, timedelta

from rest_framework.test import APITestCase

from .serializers import ShortSequenceSerializer, LongSequenceSerializer
from sequence.models import ShortSequence, LongSequence, Tikee


class ShortSequenceTestCase(APITestCase):

    def setUp(self):
        self.tikee = Tikee.objects.create(tikee_id = "tikeeid1")
        self.shortseq =  ShortSequence.objects.create(name = "shortseq1", start = datetime.now(), interval = 10, duration = 6, tikee_id = self.tikee)
        self.shortseq2 =  ShortSequence.objects.create(name = "shortseq2", start = datetime.now() + timedelta(hours = 2), interval = 10, duration = 6, tikee_id = self.tikee)


    def test_get_tikee(self):
        response = self.client.get('/short_sequences/{}/'.format(self.tikee.tikee_id), format='json')
        self.assertEqual(response.status_code, 200)
        
        serializer_data = json.dumps(ShortSequenceSerializer(instance=self.shortseq).data)
        serializer_data2 = json.dumps(ShortSequenceSerializer(instance=self.shortseq2).data)
        serializer_data = [json.loads(serializer_data), json.loads(serializer_data2)]
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data)

    def test_get_shortsequence(self):
        response = self.client.get('/short_sequences/{}/'.format(self.shortseq.id), format='json')
        self.assertEqual(response.status_code, 200)
        
        serializer_data = json.dumps(ShortSequenceSerializer(instance=self.shortseq).data)
        serializer_data = json.loads(serializer_data)
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data)

    def test_create_shortsequence(self):
        response = self.client.post('/short_sequences/', {"name" : "shortseq3", "start" : "2019-01-01 12:00", "interval" : 10, "duration" : 6, "tikee_id" : "tikeeid1"})
        self.assertEqual(201, response.status_code)

        #test overlap
        response = self.client.post('/short_sequences/', {"name" : "shortseq4", "start" : "2019-01-01 12:05", "interval" : 10, "duration" : 6, "tikee_id" : "tikeeid1"})
        self.assertEqual(400, response.status_code)

        #test negative interval
        response = self.client.post('/short_sequences/', {"name" : "shortseq4", "start" : "2019-01-01 14:00", "interval" : -10, "duration" : 6, "tikee_id" : "tikeeid1"})
        self.assertEqual(400, response.status_code)

    def test_update_shortsequence(self):
        response = self.client.put('/short_sequences/{}/'.format(self.shortseq.id), {"name" : "nameshortseq1", "start" : "2019-01-01 16:00", "interval" : 10, "duration" : 6, "tikee_id" : "tikeeid1"})
        self.assertEqual(200, response.status_code)
        response_data = json.loads(response.content)

        shortseq_updated = ShortSequence.objects.get(id=self.shortseq.id)
        self.assertEqual(response_data.get("name"), shortseq_updated.name)

    def test_delete_shortsequence(self):
        response = self.client.delete('/short_sequences/{}/'.format(self.shortseq.id))
        self.assertEqual(204, response.status_code)

        self.assertFalse(ShortSequence.objects.filter(id=1).exists())

class LongSequenceTestCase(APITestCase):

    def setUp(self):
        self.tikee = Tikee.objects.create(tikee_id = "tikeeid2")
        self.longseq =  LongSequence.objects.create(name = "longseq1", start = datetime.now(), end = datetime.now()+ timedelta(days=1), tikee_id = self.tikee)
        self.longseq2 =  LongSequence.objects.create(name = "longseq2", start = datetime.now() + timedelta(days = 3), end = datetime.now()+ timedelta(days=4), tikee_id = self.tikee)


    def test_get_tikee(self):
        response = self.client.get('/long_sequences/{}/'.format(self.tikee.tikee_id), format='json')
        self.assertEqual(response.status_code, 200)

        serializer_data = json.dumps(LongSequenceSerializer(instance=self.longseq).data)
        serializer_data2 = json.dumps(LongSequenceSerializer(instance=self.longseq2).data)
        serializer_data = [json.loads(serializer_data), json.loads(serializer_data2)]
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data)

    def test_get_longsequence(self):
        response = self.client.get('/long_sequences/{}/'.format(self.longseq.id), format='json')
        self.assertEqual(response.status_code, 200)
        
        serializer_data = json.dumps(LongSequenceSerializer(instance=self.longseq).data)
        serializer_data = json.loads(serializer_data)
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data)

    def test_create_longsequence(self):
        response = self.client.post('/long_sequences/', {"name" : "longseq3", "start" : "2019-01-01 12:00", "end" : "2019-01-01 12:10", "tikee_id" : "tikeeid2"})
        self.assertEqual(201, response.status_code)

        #test overlap
        response = self.client.post('/long_sequences/', {"name" : "longseq4", "start" : "2019-01-01 12:05", "end" : "2019-01-01 12:10", "tikee_id" : "tikeeid2"})
        self.assertEqual(400, response.status_code)

        #test end < start
        response = self.client.post('/long_sequences/', {"name" : "longseq4", "start" : "2019-01-01 14:00", "end" : "2019-01-01 11:50", "tikee_id" : "tikeeid2"})
        self.assertEqual(400, response.status_code)

    def test_update_longsequence(self):
        response = self.client.put('/long_sequences/{}/'.format(self.longseq.id), {"name" : "newlongseq1", "start" : "2019-01-01 16:00", "end" : "2019-01-01 16:10", "tikee_id" : "tikeeid2"})
        self.assertEqual(200, response.status_code)
        response_data = json.loads(response.content)

        longseq_updated = LongSequence.objects.get(id=self.longseq.id)
        self.assertEqual(response_data.get("name"), longseq_updated.name)

    def test_delete_longsequence(self):
        response = self.client.delete('/long_sequences/{}/'.format(self.longseq.id))
        self.assertEqual(204, response.status_code)

        self.assertFalse(LongSequence.objects.filter(id=1).exists())
