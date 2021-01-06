import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('metal2.jpg', cv2.IMREAD_GRAYSCALE)
cv2.imshow('metal2.jpg', img)

hist = cv2.calcHist([img], [0], None, [256], [0, 256])
plt.plot(hist, color='gray' )

plt.xlabel('intensidad')
plt.ylabel('cantidad de pixeles')
plt.show()

cv2.destroyAllWindows()


#metal 2 https://www.sciencedirect.com/science/article/abs/pii/S0921509311011580 
#metal 3 https://www.researchgate.net/figure/Light-optical-micrograph-of-the-ferrite-pearlite-microstructure-of-this-steel-etched_fig1_233515844
