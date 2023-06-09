FROM Python:3.10
EXPOSE 5000
WORKDIR /backend
RUN pip install flask
COPY .  .
CMD ["flask","run","-host","0.0.0.0"]