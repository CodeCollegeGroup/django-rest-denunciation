FROM python:3

ENV PYTHONUNBUFFERED 1
ENV EMAIL_ADDRESS somemail@gmail.com
ENV EMAIL_PWD password
ENV CC_TEST_REPORTER_ID 20ba1fe10b612e336a3fa714f2963cd91da674b14e8930f3df48e57b58cce15a

RUN mkdir -p /home/django_rest_denunciation/django_rest_denunciation/tests_coverage
WORKDIR /home/django_rest_denunciation/django_rest_denunciation

ADD requirements.txt ..
RUN pip install -r ../requirements.txt
