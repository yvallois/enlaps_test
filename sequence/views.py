from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound, PermissionDenied
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from sequence.models import ShortSequence, LongSequence, XRequestId
from sequence.serializers import ShortSequenceSerializer, LongSequenceSerializer


def CheckXRequestId(request):
    req_id = request.META.get('X_Request_Id')
    if req_id:
        if XRequestId.objects.filter(name=req_id, date__gte = (datetime.now() - timedelta(hours=24))):
            raise PermissionDenied(detail='x_request_id too recent', code = PermissionDenied.status_code)
        x_request_id = XRequestId(name = req_id ,date = datetime.datetime.now())
        x_request_id.save()

class ShortSequenceList(APIView):
    """
    List all short sequences for the requested tikee.
    """
    throttle_classes = (AnonRateThrottle,)

    def get(self, request, tikee, format=None):
        CheckXRequestId(request)

        sequences = ShortSequence.objects.filter(tikee_id=tikee)
        serializer = ShortSequenceSerializer(sequences, many=True)
        return Response(serializer.data)
            

class LongSequenceList(APIView):
    """
    List all long sequences for the requested tikee.
    """
    throttle_classes = (AnonRateThrottle,)

    def get(self, request, tikee, format=None):
        CheckXRequestId(request)

        sequences = LongSequence.objects.filter(tikee_id=tikee)
        serializer = LongSequenceSerializer(sequences, many=True)
        return Response(serializer.data)

class ShortSequenceDetail(APIView):
    """
    Retrieve, update or delete a short sequence instance.
    """
    throttle_classes = (AnonRateThrottle,)

    def get_object(self, pk):
        try:
            return ShortSequence.objects.get(pk=pk)
        except ShortSequence.DoesNotExist:
            raise NotFound(detail='Not Found', code = NotFound.status_code)

    def get(self, request, pk):
        CheckXRequestId(request)
        sequence = self.get_object(pk)
        serializer = ShortSequenceSerializer(sequence)
        return Response(serializer.data)

    def put(self, request, pk):
        CheckXRequestId(request)
        sequence = self.get_object(pk)
        serializer = ShortSequenceSerializer(sequence, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        raise ParseError(detail='Bad Request', code = ParseError.status_code)

    def delete(self, request, pk):
        CheckXRequestId(request)
        sequence = self.get_object(pk)
        sequence.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LongSequenceDetail(APIView):
    """
    Retrieve, update or delete a long sequence instance.
    """
    throttle_classes = (AnonRateThrottle,)

    def get_object(self, pk):
        try:
            return LongSequence.objects.get(pk=pk)
        except LongSequence.DoesNotExist:
            raise NotFound(detail='Not Found', code = NotFound.status_code)

    def get(self, request, pk):
        CheckXRequestId(request)
        sequence = self.get_object(pk)
        serializer = LongSequenceSerializer(sequence)
        return Response(serializer.data)

    def put(self, request, pk):
        CheckXRequestId(request)
        sequence = self.get_object(pk)
        serializer = LongSequenceSerializer(sequence, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        raise ParseError(detail='Bad Request', code = ParseError.status_code)

    def delete(self, request, pk):
        CheckXRequestId(request)
        sequence = self.get_object(pk)
        sequence.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ShortSequenceCreate(APIView):
    """
    Create short sequence
    """
    throttle_classes = (AnonRateThrottle,)

    def post(self, request):
        CheckXRequestId(request)

        serializer = ShortSequenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ParseError(detail='Bad Request', code = ParseError.status_code)


class LongSequenceCreate(APIView):
    """
    Create long sequence
    """
    throttle_classes = (AnonRateThrottle,)

    def post(self, request):
        CheckXRequestId(request)

        serializer = LongSequenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ParseError(detail='Bad Request', code = ParseError.status_code)
