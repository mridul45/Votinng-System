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
    def create(self, request):
        # Assuming the share link is sent in the request data as 'uploaded_share1_link'
        uploaded_share1_link = request.data.get('uploaded_share1_link')

        if not uploaded_share1_link:
            return JsonResponse({'error': 'Invalid request. Share link not provided.'}, status=400)

        # Download the file from the provided link
        response = requests.get(uploaded_share1_link)
        if response.status_code == 200:
            uploaded_share1_content = BytesIO(response.content)

            # Add your decryption logic here
            decrypted_data_uploaded = decrypt_share(uploaded_share1_content.read())

            # Get the user's share from the database
            user_share = Shares.objects.filter(user=request.user).first()
            if user_share:
                decrypted_data_database = decrypt_share(user_share.share1.read())

                # Combine shares (Assuming shares are visualized as black and white images)
                combined_share = combine_shares(decrypted_data_uploaded, decrypted_data_database)

                # Check if the combined share is successfully created
                if combined_share:
                    # Decryption successful, generate a random 4-digit number
                    random_number = random.randint(1000, 9999)

                    # Return the random number as JSON response
                    return Response({'random_number': random_number})
                else:
                    # Failed to combine shares
                    return JsonResponse({'error': 'Failed to combine shares'}, status=400)
            else:
                # User's share not found in the database
                return JsonResponse({'error': 'User share not found in the database'}, status=400)
        else:
            # Failed to download the file
            return JsonResponse({'error': 'Failed to download the file'}, status=400)


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

        # Save the combined result as an image (you can adjust this part based on your needs)
        combined_image_bytes = BytesIO()
        combined_image.save(combined_image_bytes, format='PNG')
        combined_image_bytes.seek(0)

        return combined_image_bytes.read()

    except Exception as e:
        print(f"Error combining shares: {e}")
        return None