from app import config

def get_signed_content(file_name, file_type, bucket_name, folder_name, file_prefix=None):
    # Load necessary information into the application:
        AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
        AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
        S3_MEDIA_REGION = config.S3_MEDIA_REGION

        if not file_prefix:
            file_prefix = folder_name

        # Collect information on the file from the GET parameters of the request:
        object_name = urllib.quote_plus(file_name)

        mime_type = file_type

        # Set the expiry time of the signature (in seconds) and declare the permissions of the file to be uploaded
        expires = int(time.time()+10)
        amz_headers = "x-amz-acl:public-read"

        # Generate the PUT request that JavaScript will use:
        put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, bucket_name, object_name)

        # Generate the signature with which the request can be signed:
        signature = base64.encodestring(hmac.new(AWS_SECRET_ACCESS_KEY, put_request, sha1).digest())
        # Remove surrounding whitespace and quote special characters:
        signature = urllib.quote_plus(signature.strip())

        # Build the URL of the file in anticipation of its imminent upload:
        if S3_MEDIA_REGION:
            url = 'https://%s.s3-%s.amazonaws.com/%s' % (bucket_name, S3_MEDIA_REGION ,object_name)
        else:
            url = 'https://%s.s3.amazonaws.com/%s' % (bucket_name, object_name)

        content = json.dumps({
            'signed_request': '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (url, AWS_ACCESS_KEY_ID, expires, signature),
            'url': url
        })

        return content

def s3_signer(self):

    file_name = request.args.get('s3_object_name')
    file_type = request.args.get('s3_object_type')
    s3_folder = request.args.get('s3_folder', 'default')

    bucket_name = config.S3_MEDIA_BUCKET
    folder_name  = s3_folder

    # Convert File name to lower case and strip out more chars after length 25
    file_name = file_name[:25].lower()

    from ...libs.amazon_s3 import AmazonS3

    amazon = AmazonS3()
    content = amazon.get_signed_content(file_name, file_type, bucket_name, folder_name)

    # Return the signed request and the anticipated URL back to the browser in JSON format:
    return Response(content, mimetype='text/plain; charset=x-user-defined')

