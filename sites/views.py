from datetime import datetime

from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sites.serializers import VisitAddSerializer


class ListVisits(APIView):
    """
    Output for all existing or suitable visits, using max and min date to avoid
    too many duplicates (for "From", for "To, for "From and To")

    """
    def get(self, request):
        queryset = cache.keys('*')
        domains = []
        # max and min available date
        start, end = datetime(1, 1, 1), datetime(9999, 12, 31)
        # rewrite them if custom 'from' and 'to' exist
        if 'from' in request.query_params:
            start = datetime.fromtimestamp(int(request.query_params['from']))
        if 'to' in request.query_params:
            end = datetime.fromtimestamp(int(request.query_params['to']))
        for key in queryset:
            if start <= cache.get(key) <= end:
                domains.append(key)
        return Response({'domains': sorted(domains), 'status': 'ok'},
                        status=status.HTTP_200_OK)


class AddVisits(APIView):
    """
    Add new visits with passing link list (Json or Form-Data format), delete
    prefixes, paths and parameters if they exist. Check is it a links
    (all links have dots).
    """
    def post(self, request):
        serializer = VisitAddSerializer(data=dict(request.data))
        now = datetime.now()
        if serializer.is_valid():
            links = serializer.data.get('links')
            for link in links:
                link = link.removeprefix('https://').removeprefix('http://')
                link = link.split('/', maxsplit=1)[0]
                link = link.split('?', maxsplit=1)[0]
                if '.' not in link:
                    return Response(
                        {'status': f'Object < {link} > is not a link'},
                        status=status.HTTP_400_BAD_REQUEST)
                cache.set(link, now)
            return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
        return Response({'status': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
