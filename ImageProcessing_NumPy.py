from PIL import Image
import numpy as np

  
# open method used to open different extension image file
# Input the image 
im = Image.open("11.jpg") 

# detection of edges using numpy
class Edges():
    def apply(pixels: np.ndarray) -> np.ndarray:
        output=np.pad(pixels,pad_width=1)
        for i in range(pixels.shape[2]):
            
            # Choice of kernal
            kernel=np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])

            (iH, iW) = pixels.shape[:2]
            (kH, kW) = kernel.shape[:2]
            pad = (kW - 1) // 2

            #image = np.zeros((pixels.shape[0] + pad*2, pixels.shape[1] + pad*2))
            image=np.pad(pixels[:,:,i],pad_width=1)
            
            for y in np.arange(pad, iH + pad):
                for x in np.arange(pad,iW+pad):
                    roi = image[y - pad:y + pad + 1, x - pad:x + pad + 1]
                    k = (roi * kernel).sum()
                    image[y - pad, x - pad] = k
            
            #image = (image).astype("uint8")
            output[:,:,i+1]=image

            # returning only channel 1,2,3 since due to padding the extra channels were added
        return output[:,:,(1,2,3)]


class De_noise():
    def apply(pixels: np.ndarray) -> np.ndarray:
        output=np.pad(pixels,pad_width=1)
        for i in range(pixels.shape[2]):

            kernel=np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])

            (iH, iW) = pixels.shape[:2]
            (kH, kW) = kernel.shape[:2]
            pad = (kW - 1) // 2

            #image = np.zeros((pixels.shape[0] + pad*2, pixels.shape[1] + pad*2))
            image=np.pad(pixels[:,:,i],pad_width=1)
            for y in np.arange(pad, iH + pad):
                for x in np.arange(pad,iW+pad):
                    selectedPixels = image[y - pad:y + pad + 1, x - pad:x + pad + 1]
                    median=np.median(selectedPixels)
                    image[y - pad, x - pad] = median
            
            
            output[:,:,i+1]=image

            # returning only channel 1,2,3 since due to padding the extra channels were added
        return output[:,:,(1,2,3)]

# Normalize the image using the formula pixel -lowest(pixel)/highest(pixcel)-lowest(pixcel)
class Normalize():
    def apply(pixel: np.ndarray) -> np.ndarray:
        print("Normalize takes time so please wait for the result")
        for j in range(pixel.shape[1]):
            for i in range(pixel.shape[0]):
                #for Red Channel
                if (np.amax(pixel[:,:,0])!= np.amin(pixel[:,:,0])):
                    pixel[i,j,0]=255*(pixel[i,j,0]-np.amin(pixel[:,:,0]))/(np.amax(pixel[:,:,0])-np.amin(pixel[:,:,0]))
                #for Blue Channel
                if (np.amax(pixel[:,:,1])!=np.amin(pixel[:,:,1])):
                    pixel[i,j,1]=255*(pixel[i,j,1]-np.amin(pixel[:,:,1]))/(np.amax(pixel[:,:,1])-np.amin(pixel[:,:,1]))        
                #for Green Channel
                if (np.amax(pixel[:,:,2])!=np.amin(pixel[:,:,2])):
                    pixel[i,j,2]=255*(pixel[i,j,2]-np.amin(pixel[:,:,2]))/(np.amax(pixel[:,:,2])-np.amin(pixel[:,:,2]))
        
        return pixel

class Dilate():
    def apply(pixels: np.ndarray) -> np.ndarray:
        output=np.pad(pixels,pad_width=1)
        for i in range(pixels.shape[2]):
            # Creating Kernal
            kernel=np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])

            (iH, iW) = pixels.shape[:2]
            (kH, kW) = kernel.shape[:2]
            pad = (kW - 1) // 2

            image=np.pad(pixels[:,:,i],pad_width=1)            
            for y in np.arange(pad, iH + pad):
                for x in np.arange(pad,iW+pad):
                    roi = image[y - pad:y + pad + 1, x - pad:x + pad + 1]
                    k=np.amax(roi)
                    image[y - pad, x - pad] = k
            
            output[:,:,i+1]=image
        # returning only channel 1,2,3 since due to padding the extra channels were added
        return output[:,:,(1,2,3)] 

#convert the image into pixels
image=np.asarray(im, dtype=np.int16)

# Change the class to to call the respective filture
image=Dilate.apply(image)
# image=Edges.apply(image)    #uncomment to see the edge filter
#convert pixels to image
output=Image.fromarray(np.uint8(image))        
output
