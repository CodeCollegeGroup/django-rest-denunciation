FROM python:3

ENV PYTHONUNBUFFERED 1
ENV EMAIL_ADDRESS somemail@gmail.com
ENV EMAIL_PWD password
ENV CC_TEST_REPORTER_ID 4b469c4090b87b620c88dedd8caa5c8a4447966868d2cc4aa2553b702c7f85d4

RUN mkdir -p /home/django_rest_denunciation/django_rest_denunciation/tests_coverage
WORKDIR /home/django_rest_denunciation/django_rest_denunciation

ADD requirements.txt ..
RUN pip install -r ../requirements.txt
