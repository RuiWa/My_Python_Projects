import pydicom
import pylab

# 导入图片
ds = pydicom.read_file('D:\JupyterNotebook Files\HQZ 904754\MIP00001.dcm')

# 打印相关属性
print(ds.dir())
print(ds.PatientAge,ds.PatientBirthDate,ds.PatientID,ds.PatientName)
print(ds.data_element('PatientID'))
pixel_bytes = ds.PixelData
pix = ds.pixel_array
print(pix.shape)

# 显示图片
pylab.imshow(pix,cmap=pylab.cm.bone)
pylab.show()
