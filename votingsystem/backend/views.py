from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializes import *
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import requests
from io import BytesIO
import random
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class CandidateViewSet(viewsets.ViewSet):

    def list(self,request):

        candidates = Candidate.objects.all()
        serializer = CandidateSerializer(candidates,many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CandidateCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class VoterViewset(viewsets.ViewSet):

    def list(self,request):

        voter = Voter.objects.all()
        serializer = VoterSerializer(voter,many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = VoterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ElectionViewSet(viewsets.ViewSet):

    def list(self,request):

        elections = Election.objects.all()
        serializer = ElectionSerializer(elections,many=True)

        return Response(serializer.data)
    

    def create(self, request):
        serializer = ElectionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserSignupViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = UserSignupSerializer(data=request.data)
        
        if serializer.is_valid():
        # Create a new user
            user = User.objects.create_user(
                username=serializer.validated_data['name'],
                password=serializer.validated_data['password'],
                email = serializer.validated_data['email']
            )

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    


class VotedViewset(viewsets.ViewSet):

    def list(self,request):

        votes = Voted.objects.all()
        serializer = VotedSerializer(votes,many=True)

        return Response(serializer.data)
    

    def create(self, request):
        serializer = VotedSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ShareViewset(viewsets.ViewSet):

    def list(self,request):

        shares = Shares.objects.all()
        serializer = ShareSerializer(shares,many=True)

        return Response(serializer.data)
    

class ShareUploadViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        image_url = request.data.get('uploaded_share1_link')

        if not image_url:
            return Response({'error': 'Invalid request. Share data not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Download the image from the URL
            response = requests.get(image_url)
            response.raise_for_status()
            binary_data = response.content
        except Exception as e:
            return Response({'error': f'Failed to download image from the URL. {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Now 'binary_data' contains the binary image data
        iv = secrets.token_bytes(16)
        uploaded_share1_content = BytesIO(binary_data)

        # Add your decryption logic here
        decrypted_data_uploaded = decrypt_share(uploaded_share1_content.read(), iv)

        try:
            # Get the latest user's share from the database
            user_share = Shares.objects.latest('id')
        except ObjectDoesNotExist:
            return Response({'error': 'User share not found in the database'}, status=status.HTTP_400_BAD_REQUEST)

        decrypted_data_database = decrypt_share(user_share.share1.read(), iv)

        # Combine shares (Assuming shares are visualized as black and white images)
        combined_share = combine_shares(decrypted_data_uploaded, decrypted_data_database)

        # Check if the combined share is successfully created
        if combined_share:
            # Decryption successful, generate a random 4-digit number
            random_number = random.randint(1000, 9999)

            # Save the combined share to the database
            user_share.share_combined = combined_share
            user_share.save()

            # Return the random number as JSON response
            return Response({'random_number': random_number})
        else:
            # Failed to combine shares
            return Response({'error': 'Failed to combine shares'}, status=status.HTTP_400_BAD_REQUEST)

def combine_shares(share1, share2):
    try:
        # Convert shares to PIL Images
        share1_image = Image.open(BytesIO(share1))
        share2_image = Image.open(BytesIO(share2))

        # Ensure both images have the same size
        if share1_image.size != share2_image.size:
            raise ValueError("Shares must have the same dimensions")

        # Create an image for the combined result
        combined_image = Image.new('1', share1_image.size)
        draw_combined = ImageDraw.Draw(combined_image)

        # Iterate over pixels and combine shares
        for x in range(combined_image.width):
            for y in range(combined_image.height):
                pixel_share1 = share1_image.getpixel((x, y))
                pixel_share2 = share2_image.getpixel((x, y))

                # If both pixels are black or white, set the combined pixel to white; otherwise, set it to black
                combined_pixel = 0 if pixel_share1 == pixel_share2 else 1

                draw_combined.point((x, y), fill=combined_pixel)

        # Save the combined result as binary data
        combined_image_bytes = BytesIO()
        combined_image.save(combined_image_bytes, format='PNG')
        combined_image_bytes.seek(0)

        return combined_image_bytes.read()

    except Exception as e:
        print(f"Error combining shares: {e}")
        return None