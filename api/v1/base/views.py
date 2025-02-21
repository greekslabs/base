from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import NotFound, APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from api.v1.base.functions import generate_serializer_errors, create_response_data



class BaseRecordApiView(APIView):
    model = None
    serializer_class = None
    resource_name = None
    language = None
    alt_txt = None
    custom_order = None

    def post_record(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            if serializer.is_valid():
                # Set created_by and updated_by fields
                kwargs = {
                    'created_by': request.user,
                    'updated_by': request.user,
                }
                serializer.save(**kwargs)
                response_data = create_response_data(
                    status.HTTP_200_OK,
                    'Created',
                    serializer.data,
                    '',
                    f'{self.resource_name.capitalize()} successfully created'
                )
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = create_response_data(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    'Error',
                    '',
                    generate_serializer_errors(serializer.errors),
                    "Invalid data. Please check the provided data."
                )
                return Response(response_data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            response_data = create_response_data(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                'Error',
                '',
                str(e),
                f'An error occurred while creating the {self.resource_name}.',
            )
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        """Retrieve the base queryset, can be overridden in subclasses."""
        return self.model.objects.filter(is_deleted=False)

    def get_records(self, request):
        try:
            queryset = self.get_queryset()  # Call the get_queryset method

            # Apply any custom ordering
            queryset = queryset.order_by('-created_at') if not self.custom_order else queryset.order_by('custom_order')

            serialized = self.serializer_class(queryset, many=True, context={'request': request})  # Serialize the data
            data = serialized.data
            response_data = create_response_data(
                status.HTTP_200_OK,
                'Retrieve',
                data,
                '',
                f'Retrieve all {self.resource_name} details',
            )
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = create_response_data(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                'Error',
                '',
                str(e),
                f'An error occurred while retrieving {self.resource_name} details',
            )
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_object(self, request, pk):
        try:
            obj = self.model.objects.get(pk=pk, is_deleted=False)
            return obj
        except ObjectDoesNotExist:
            raise NotFound(f'{self.resource_name} with pk {pk} does not exist or has been deleted.')

    def get_record(self, request, pk):
        try:
            record = self.get_object(request, pk)
            serialized = self.serializer_class(record, context={'request': request})
            response_data = create_response_data(
                status.HTTP_200_OK,
                'Retrieve',
                serialized.data,
                '',
                f'Retrieve selected {self.resource_name} details'
            )
            return Response(response_data, status=status.HTTP_200_OK)
        except NotFound as e:
            response_data = create_response_data(
                status.HTTP_404_NOT_FOUND,
                'Error',
                '',
                str(e),
                str(e)
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except APIException as e:
            response_data = create_response_data(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                'Error',
                '',
                str(e),
                f'An error occurred while retrieving {self.resource_name}.',
            )
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put_record(self, request, pk):
        try:
            record = self.get_object(request, pk)
            serializer = self.serializer_class(record, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(updated_by=request.user)
                response_data = create_response_data(
                    status.HTTP_200_OK,
                    'Replaced',
                    serializer.data,
                    '',
                    f'Replaced selected {self.resource_name} details',
                )
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = create_response_data(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    'Error',
                    '',
                    generate_serializer_errors(serializer.errors),
                    'Invalid data. Please check the provided data.',
                )
                return Response(response_data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except ObjectDoesNotExist:
            response_data = create_response_data(
                status.HTTP_404_NOT_FOUND,
                'Error',
                '',
                'The resource was not found!',
                'Something went wrong',
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response_data = create_response_data(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                'Error',
                '',
                str(e),
                f'An error occurred while modifying the {self.resource_name}.',
            )
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch_record(self, request, pk):
        try:
            record = self.get_object(request, pk)
            serializer = self.serializer_class(record, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save(updated_by=request.user)
                response_data = create_response_data(
                    status.HTTP_200_OK,
                    'Updated',
                    serializer.data,
                    '',
                    f'Updated selected {self.resource_name} details',
                )
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = create_response_data(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    'Error',
                    '',
                    generate_serializer_errors(serializer.errors),
                    'Invalid data. Please check the provided data.',
                )
                return Response(response_data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except ObjectDoesNotExist:
            response_data = create_response_data(
                status.HTTP_404_NOT_FOUND,
                'Error',
                '',
                'The resource was not found!',
                'Something went wrong',
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response_data = create_response_data(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                'Error',
                '',
                str(e),
                f'An error occurred while updating the {self.resource_name}.',
            )
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_record(self, request, pk):
        try:
            record = self.get_object(request, pk)
            # Mark as deleted and update deletion metadata
            record.is_deleted = True
            record.deleted_by = request.user
            record.deleted_at = timezone.now()  # Use timezone-aware timestamp
            record.save()  # Commit the changes

            # Successful deletion response
            response_data = create_response_data(
                status.HTTP_200_OK,
                'Deleted',
                'Entire record and associated data are deleted successfully',
                '',
                'Deleted successfully',
            )
            return Response(response_data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            # Object not found response
            response_data = create_response_data(
                status.HTTP_404_NOT_FOUND,
                'Error',
                '',
                'The resource was not found!',
                'Something went wrong',
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Internal server error response
            response_data = create_response_data(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                'Error',
                '',
                str(e),
                f'An error occurred while deleting the {self.resource_name}.',
            )
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_filter_by_user(self, request):
        """Retrieve records filtered by the logged-in user."""
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        response_data = create_response_data(
            status.HTTP_200_OK,
            'Retrieve',
            serializer.data,
            '',
            f'Retrieve all {self.resource_name} details for user'
        )
        return Response(response_data, status=status.HTTP_200_OK)




