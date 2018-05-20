FROM python:3

ENV PYTHONUNBUFFERED 1
ENV EMAIL_ADDRESS somemail@gmail.com
ENV EMAIL_PWD password
ENV CC_TEST_REPORTER_ID 470f0048de804cd1cdf906abea8112369c3d25dcd3f453c7dc62bd532f8869d9

RUN mkdir -p /home/CodeCollege/code_college/tests_coverage
WORKDIR /home/CodeCollege/code_college

ADD requirements.txt ..
RUN pip install -r ../requirements.txt
