import boto3
import face_recognition
import pickle
import cv2
import csv
import os

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')
output_bucket = 'serverlesspresso-output-us-west-1'

table_name = 'cse546-serverlesspresso-dynamodb'
id_key = 'name'

# Function to read the 'encoding' file
file = open("encoding", "rb")
known_face_encodings = pickle.load(file)


def face_recognition_handler(event, context):
    # Get the bucket name and key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    download_path = os.path.join("/tmp", key)
    # Read the video file from S3
    s3.download_file(Bucket=bucket_name, Filename=download_path, Key=key)
    video_capture = cv2.VideoCapture(download_path)

    process_this_frame = True
    face_recognized = False

    while not face_recognized:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Only process every other frame of video to save time
        if process_this_frame:

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(
                    known_face_encodings['encoding'], face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:

                    first_match_index = matches.index(True)
                    video_capture.release()
                    response = dynamodb.get_item(
                        TableName=table_name,
                        Key={
                            id_key: {
                                'S': known_face_encodings['name'][first_match_index]
                            }
                        }
                    )

                    # Process the data here...
                    data = response['Item']

                    csv_file = key.split('.')[0] + '.csv'
                    upload_path_csv = os.path.join("/tmp", csv_file)

                    # Open the CSV file for writing
                    with open(upload_path_csv, 'w') as file:

                        # Create a CSV writer object
                        writer = csv.writer(file)

                        # Write the header row
                        writer.writerow(
                            [data['name']['S'], data['major']['S'], data['year']['S']])

                    response = s3.upload_file(
                        Filename=upload_path_csv,
                        Bucket=output_bucket,
                        Key=csv_file
                    )

                    face_recognized = True
                    break

        process_this_frame = not process_this_frame
