## Upload To S3 Directly From Browser

S3upload is a javascript library for directly uploading files from a web browser to AWS S3, using S3's multipart upload.

You can easily add progress bar to the upload via callbacks. 

## SET UP s3Upload

1. add s3upload.js in your page
2. Setup your S3 bucket, make sure your CORS settings for your S3 bucket looks similar to what is provided below (The PUT allowed method and the ETag exposed header are critical).


            <CORSConfiguration>
                <CORSRule>
                    <AllowedOrigin>https://*.yourdomain.com</AllowedOrigin>
                    <AllowedMethod>GET</AllowedMethod>
                    <AllowedMethod>PUT</AllowedMethod>
                    <AllowedMethod>POST</AllowedMethod>
                    <AllowedMethod>DELETE</AllowedMethod>
                    <MaxAgeSeconds>3000</MaxAgeSeconds>
                    <ExposeHeader>x-amz-server-side-encryption</ExposeHeader>
                    <ExposeHeader>x-amz-request-id</ExposeHeader>
                    <ExposeHeader>x-amz-id-2</ExposeHeader>
                    <AllowedHeader>*</AllowedHeader>
                </CORSRule>
            </CORSConfiguration>

3. Setup a signing handler (see url_signer.py) on your backend application. This will provide a signature for your multipart requests to s3. **s3upload.js** calls an AJAX call to this function and gets that signature. So you have to provide a url route that will serve the AJAX call.  

4. Now you can run the server and check after uploading files.

## Use s3Upload

            var s3upload = new S3Upload({
                        file_dom_selector: [ID OF HTML FILE HANDLER],
                        s3_folder : [S3_FOLDER_TO_PUT],
                        s3_sign_put_url: [S3_SIGN_URL],
                        s3_object_name : [NAME_OF_THE_FILE],
                        onProgress: function(percent, message) {
                            // On Progress CallBack
                        },
                        onFinishS3Put: function(url) {
                            // Success Callback
                        },
                        onError: function(status) {
                            // Failure Callback
                        }
                    });

- file_dom_selector : It is a html file input id.
- s3_folder : Name of the s3 folder inside bucket.
- s3_sign_put_url : This is the signer url that you have added in your backend app.
- onProgress : This callback is called when s3upload.js uploads a file, an percentage progress has been given.
- onFinishS3Put : This callback is called when s3upload.js finished a file upload.
- onError : This callback is called when s3upload.js finishes a file upload. 


