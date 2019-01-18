import ctypes

##so = ctypes.cdll.LoadLibrary('/Users/mental/Library/Developer/Xcode/DerivedData/pytest-fziufxvgpheflifmsljofyokeczf/Build/Products/Release/libpytest.dylib')
so = ctypes.cdll.LoadLibrary('/Users/mental/projects/other/pyobjc/pytest/libpytest.dylib')
so.echoWord.argtypes = [ctypes.POINTER(ctypes.c_char)] 
so.echoWord.restype = ctypes.c_char_p

so.getWord.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.c_int] 
so.getWord.restype = ctypes.c_int

## void *createNanoHippoDev()
so.createNanoHippoDev.restype = ctypes.c_void_p

## void destroyNanoHippoDev(void *obj)
so.destroyNanoHippoDev.argtypes =  [ctypes.c_void_p] 

## int openSerial(const char *serialDev)t 
so.openSerial.argtypes =  [ctypes.c_void_p,ctypes.c_char_p] 
so.openSerial.restype = ctypes.c_int

## int closeAll()
so.closeAll.restype = ctypes.c_int

## int SetWriteTimeInterval(int usleeps)
so.SetWriteTimeInterval.argtypes =  [ctypes.c_void_p,ctypes.c_int] 
so.SetWriteTimeInterval.restype = ctypes.c_int

## int WriteString(int port , const char* str )
so.WriteString.argtypes =  [ctypes.c_void_p,ctypes.c_int, ctypes.c_char_p] 
so.WriteString.restype = ctypes.c_int

## int WriteBytes(int port ,  const char* data , int len)
so.WriteBytes.argtypes =  [ctypes.c_void_p,ctypes.c_int, ctypes.c_char_p ,ctypes.c_int] 
so.WriteBytes.restype = ctypes.c_int

## int WriteStringBytes(int port , const char* str )
so.WriteStringBytes.argtypes =  [ctypes.c_void_p,ctypes.c_int, ctypes.c_char_p] 
so.WriteStringBytes.restype = ctypes.c_int

## void *readBuffer(int port)
so.readBuffer.argtypes =  [ctypes.c_void_p,ctypes.c_int] 
so.readBuffer.restype = ctypes.c_void_p

## const char* getStringFromBuffer(void *buffer)
so.getStringFromBuffer.argtypes =  [ctypes.c_void_p] 
so.getStringFromBuffer.restype = ctypes.c_char_p

## int getBufferLength( void *buffer)
so.getBufferLength.argtypes =  [ctypes.c_void_p] 
so.getBufferLength.restype = ctypes.c_int

## int getBytesFromBuffer(void *buffer , char* bytes , int length)
so.getBytesFromBuffer.argtypes =  [ctypes.c_void_p , ctypes.POINTER(ctypes.c_char) , ctypes.c_int] 
so.getBytesFromBuffer.restype = ctypes.c_int

## void destroyBuffer(void *buffer)
so.destroyBuffer.argtypes =  [ctypes.c_void_p] 

## const char * ReadChannels()
so.ReadChannels.argtypes =  [ctypes.c_void_p] 
so.ReadChannels.restype = ctypes.c_char_p

## const char * GetDetectString()
so.ReadChannels.argtypes =  [ctypes.c_void_p] 
so.GetDetectString.restype = ctypes.c_char_p

## void ClearBuffer(int port)
so.ClearBuffer.argtypes =  [ctypes.c_int] 

## int IsDataReady(int port)
so.IsDataReady.argtypes =  [ctypes.c_void_p,ctypes.c_int] 
so.IsDataReady.restype = ctypes.c_int

## int SetDetectString(const char* det)
so.SetDetectString.argtypes =  [ctypes.c_void_p,ctypes.c_char_p] 
so.SetDetectString.restype = ctypes.c_int

## int WaitDetect(int port, int timeout)
so.WaitDetect.argtypes =  [ctypes.c_void_p,ctypes.c_int,ctypes.c_int] 
so.WaitDetect.restype = ctypes.c_int

dev = so.createNanoHippoDev();
so.openSerial(dev,"/dev/cu.usbmodem14122")
so.WriteString(dev,-1,'hello world')

##
b = so.readBuffer(dev,-1)
if b!= 0:
    print so.getStringFromBuffer(b)
    so.destroyBuffer(b)
 
 
s = ctypes.create_string_buffer(b'\000' * 5)
  