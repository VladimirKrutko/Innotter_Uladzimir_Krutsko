from .serializers import \
	(PageSerializer, PagePublicSerializer, PagePrivateSerializer, BlockPageSerializer)
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.response import Response
from django.core import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from page.models import Page
from user.models import User
from page.permissions import PagePermission, PageBlockPermissions, PageShowPermissions
from post.models import Post
import json
from django.core import serializers as dj_ser

class UpdatePageView(UpdateAPIView):
	serializer_class = PageSerializer
	permission_classes = (PagePermission, IsAuthenticated)
	
	def put(self, request, *args, **kwargs):
		instance = Page.objects.get(id=kwargs['pk'])
		self.check_object_permissions(request, instance)
		data = request.data
		serializer = self.serializer_class(data=data, instance=instance)
		serializer.is_valid()
		serializer.save()
		return Response(data)


class BlockPageView(UpdatePageView):
	serializer_class = BlockPageSerializer
	permission_classes = (PageBlockPermissions, IsAuthenticated)
	
	def put(self, request, *args, **kwargs):
		instance = Page.objects.get(id=kwargs['pk'])
		data = request.data
		serializer = self.serializer_class(data=data, instance=instance)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(data)


class AddFollowersPublicPage(UpdatePageView):
	serializer_class = PagePublicSerializer
	permission_classes = (PagePermission, IsAuthenticated)
	
	def put(self, request, *args, **kwargs):
		instance = get_object_or_404(Page.objects.all(), pk=int(kwargs['pk']))
		self.check_object_permissions(request=request, obj=instance)
		data = request.data
		serializer = self.serializer_class(data={'followers': data.get('followers')}, instance=instance)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		
		return Response()


class AddFollowersPrivatePage(UpdatePageView):
	serializer_class = PagePrivateSerializer
	permission_classes = (PagePermission, IsAuthenticated)
	
	def put(self, request, *args, **kwargs):
		instance = get_object_or_404(Page.objects.all(), id=kwargs['pk'])
		self.check_object_permissions(request=request, obj=instance)
		data = request.data
		serializer = self.serializer_class(data=data, instance=instance)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		
		return Response({'Status': 'Ok'})


class ListPagesView(ListAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = PageSerializer
	queryset = Page.objects.all()


class ListPagePostView(ListAPIView):
	permission_classes = (PageShowPermissions,)
	
	def get(self, request, *args, **kwargs):
		page_id = kwargs['pk']
		page = Page.objects.get(pk=page_id)
		self.check_object_permissions(request=request, obj=page)
		
		post = Post.objects.filter(page_id=page_id)
		response_json = PageSerializer.serialize_page_post(page_obj=page, post_obj=post)
		
		return Response(response_json)


class ListFollowRequestView(ListAPIView):
	permission_classes = (PagePermission,)
	
	def get(self, request, *args, **kwargs):
		page = Page.objects.get(pk=kwargs['pk'])
		self.check_object_permissions(request=request, obj=page)
		page_json = json.loads(serializers.serialize('json', [page, ]))
		# print(page_json["follow_requests"])
		response_json = {'follow_request': page_json[0]['fields']['follow_requests']}
		return Response(response_json)


class SearchPageView(ListAPIView):
	permission_classes = (IsAuthenticated,)

	def get(self, request, *args, **kwargs):
		"""
		Only one parameter for search
		"""
		data = request.data
		if list(data.keys())[0] == 'uuid':
			page = dj_ser.serialize('json', Page.objects.filter(uuid=data['uuid']))

			return Response({'page': json.loads(page)})

		elif list(data.keys())[0] == 'name':
			page = dj_ser.serialize('json', Page.objects.filter(name=data['name']))

			return Response({'page': json.loads(page)})

		elif list(data.keys())[0] == 'username':
			user = dj_ser.serialize('json', User.objects.filter(username=data['username']))

			return Response({'user': json.loads(user)})

		return Response('Not found')





