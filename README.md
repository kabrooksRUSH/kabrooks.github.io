# Eigenfaces
Eigenfaces is an approach to facial recognition that aims to extract the most important features of a face image using Principal Component Analysis (PCA). The Eigenfaces approach has the ability to represent facial images more efficiently than storing a full size image. Many people consider Eigenfaces to be the first 'working' facial recognition technology.

## Approach
To start, we need a data set of **M x N** face images. The 'mean face' is then computed by taking the average of each pixel across the dataset. We then subtract the 'mean face' from all the images in our dataset. All the images are then rasterized into  **D** dimensional vectors where **D = M * N**. With all of our rasterized images, we form a new **D x L** matrix **A** where L is the number of images in our data set. We then perform PCA on the matrix **A** to get the matricies **U**, **S**, and **V** (Click here for more information on PCA). We then make a **D x r** matrix **U'** where **U'** is the concatenation of the first **r** column vectors of **U** that correspond with the largest eigenvalues. The column vectors of **U'** span our 'face space' and are called 'eigenfaces'. We can then project a rasterized input image **x** into our face space by doing matrix multiplication **U'^T * x**. The result of this matrix multiplication is often called **alpha**.

## My Results
In my experimentation I used the Extended Yale Face Database B data set. This set of images includes 15 subjects making 11 different facial expressions. Some subjects are wearing glasses and some are not.
![Tiled faces, subject 1](https://drive.google.com/uc?id=1b6zNXZ6CiFO9uE7hOxvAStnAkt3mKH6N)

The images shown below are the first 3 basis vectors for our face space. The images don't have any real usefulness to human eyes but they are interesting to look at.
| Basis Vector 1 | Basis Vector 2 | Basis Vector 3|
| :--------------------: | :----------------------: | :---------------------: |
| ![basis vector 1](https://drive.google.com/uc?id=1D5Lckla1gCqDA56DRYwkzhVJiNfmTvto) | ![basis vector 2](https://drive.google.com/uc?id=1CMBOA262uQwu6eEHLCHoZSs3bNpUMbFE) | ![basis vector 3](https://drive.google.com/uc?id=1WO4QUCAl6vIiBkNtMPjnyP6BEpdFL4Pt) |

Once we project an input image into our face space we can transform it back by left multiplying **alpha** by **U'**. This brings **alpha** back into our original **D** dimensional vector which we can reshape into the original image size of **M x N**. Keep in mind that when we create **alpha** we lose some information about the image so when we bring it back into our **D** dimensional space it will not be the same exact image. Below are the results of approximating the first image of subject 1.
| Original Image |
| :---------------------------: |
| ![Original Image](https://drive.google.com/uc?id=1kfxD4JzNajXWcA9yGLwkPqU6myqOiNRI) |

| Approximation r=5 | Approximation r=10 | Approximation r=100|
| :-----------: | :-----------: | :-----------: |
| ![Approximation r=5](https://drive.google.com/uc?id=1uhWC657uiWYkOlZRIx90rIpjTmJB2eq3) | ![approximation r=10](https://drive.google.com/uc?id=1el_P8BNB536BppOXNETrYtcqkR2Q7hj8) | ![approximation r=100](https://drive.google.com/uc?id=1aFXBL8xixNPHBYy4nG5JgG-Yb-S0chNZ) |

## Limitations
There are a few assumptions we have for our data that have an impact on how useful the Eigenfaces approach is in real world application. The first and most notable assumption is that all input images have the same pixel resolution and the eyes and mouths of the faces are in the same position. This limitation prevents Eigenfaces from being a solid approach to finding a face within a larger image. The second big limitation with Eigenfaces is that the lighting on the faces used in our data set has significant impact on how well face images can be approximated in face space. The Eigenfaces approach also has issues approximating faces with glasses or faces that have a different facial expressions. The Fisherfaces approach to facial reconition aims to address these shortcomings.

I will soon be publishing a blog like this one showcasing an extension of Eigenfaces called Fisherfaces.
