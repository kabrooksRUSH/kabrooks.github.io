# Eigenfaces
Eigenfaces is an approach to facial recognition that aims to extract the most important features of a face image using Principal Component Analysis (PCA). The Eigenfaces approach has the ability to represent facial images more efficiently than storing a full size image. Many people consider Eigenfaces to be the first 'working' facial recognition technology.

## Approach
To start, we need a data set of **M x N** face images. The 'mean face' is then computed by taking the average of each pixel across the dataset. We then subtract the 'mean face' from all the images in our dataset. All the images are then rasterized into  **D** dimensional vectors where **D = M * N**. With all of our rasterized images, we form a new **D x L** matrix **A** where L is the number of images in our data set. We then perform PCA on the matrix **A** to get the matricies **U**, **S**, and **V** (Click here for more information on PCA). We then make a **D x r** matrix **U'** where **U'** is the concatenation of the first **r** column vectors of **U** that correspond with the largest eigenvalues. The column vectors of **U'** span our 'face space' and are called 'eigenfaces'. We can project a rasterized input image **x** into our face space by doing matrix multiplication **U'^T * x**.

## My Results
In my experimentation I used the Extended Yale Face Database B data set. This set of images includes 15 subjects making 11 different facial expressions. Some subjects are wearing glasses and some are not.

## Limitations
There are a few assumptions we have for our data that have an impact on how useful the Eigenfaces approach is in real world application. The first and most notable assumption is that all input images have the same pixel resolution and the eyes and mouths of the faces are in the same position. This limitation prevents Eigenfaces from being a solid approach to finding a face within a larger image. The second big limitation with Eigenfaces is that the lighting on the faces used in our data set has significant impact on how well face images can be reapproximated in face space. The Eigenfaces approach also has issues reapproximating faces with glasses or faces that have a different facial expressions.

Soon I will be publishing a blog like this one showcasing an extension of Eigenfaces called Fisherfaces.
