#FROM --platform=linux/x86_64 python:3.9
FROM public.ecr.aws/lambda/python:3.9
# FROM amazon/aws-lambda-python:latest
# Copy function code
COPY requirements.txt .

# Install the function's dependencies using file requirements.txt
# from your project folder.

RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

ADD lambda_txt2img ./

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD ["txt2img.lambda_handler"]
