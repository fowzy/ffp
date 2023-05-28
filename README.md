# ffp
F* Flash Photography, Download your digital pictures for your graudation for FREE, no charge! Tired of college spam and I want to help you not get scammed by your college.

## Instructions for Running:
Create a docker image:
>docker build -t ffp .

Once the image has been created, excute the container by using the following command:
>docker run -p 8000:8000 ffp-ocean

To run the container in detached mode (in the background): 
>docker run -d -p 8000:8000 ffp-ocean

