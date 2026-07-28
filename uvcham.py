"""Version: 1.30594.20260120
Win32:
    (a) x86: XP SP3 or above; CPU supports SSE2 instruction set or above
    (b) x64: Win7 or above
"""
import sys, ctypes, os.path

"""
************************************************************************
* Uvcham_enum (optional)                                               *
* ----> Uvcham_open                                                    *
* ----> enum resolutions, set resolution, set exposure time, etc       *
* ----> Uvcham_start                                                   *
* ----> callback for image and events                                  *
* ----> Uvcham_close                                                   *
************************************************************************
"""
UVCHAM_MAX                 = 16

UVCHAM_FLIPHORZ            = 0x00000002    # flip horizontal
UVCHAM_FLIPVERT            = 0x00000003    # flip vertical
UVCHAM_AEXPOTARGET         = 0x00000004    # exposure compensation
UVCHAM_DENOISE             = 0x00000005    # denoise
UVCHAM_WBROILEFT           = 0x00000006    # white balance mode roi: left
UVCHAM_WBROIWIDTH          = 0x00000007    # white balance mode roi: width, width >= UVCHAM_WBROI_WIDTH_MIN
UVCHAM_WBROITOP            = 0x00000008    # white balance mode roi: top
UVCHAM_WBROIHEIGHT         = 0x0000000a    # white balance mode roi: height, height >= UVCHAM_WBROI_HEIGHT_MIN
UVCHAM_YEAR                = 0x0000000b    # firmware version: year
UVCHAM_MONTH               = 0x0000000c    # firmware version: month
UVCHAM_DAY                 = 0x0000000d    # firmware version: day
UVCHAM_WBMODE              = 0x00000010    # white balance mode: 0 = manual, 1 = auto, 2 = roi
UVCHAM_EXPOTIME            = 0x00000011    # exposure time
UVCHAM_AEXPO               = 0x00000013    # auto exposure: 0 = manual, 1 = auto
UVCHAM_SHARPNESS           = 0x00000016
UVCHAM_SATURATION          = 0x00000017
UVCHAM_GAMMA               = 0x00000018
UVCHAM_CONTRAST            = 0x00000019
UVCHAM_BRIGHTNESS          = 0x0000001a
UVCHAM_HZ                  = 0x0000001b    # 0 -> 60HZ AC;  1 -> 50Hz AC;  2 -> DC
UVCHAM_WBRED               = 0x0000001c    # white balance: R/G/B gain
UVCHAM_WBGREEN             = 0x0000001d    # white balance: R/G/B gain
UVCHAM_WBBLUE              = 0x0000001e    # white balance: R/G/B gain
UVCHAM_HUE                 = 0x0000001f
UVCHAM_CHROME              = 0x00000020    # color(0)/grey(1)
UVCHAM_AFPOSITION          = 0x00000021    # auto focus sensor board positon, now is 0~854
UVCHAM_AFMODE              = 0x00000022    # auto focus mode (0:manul focus; 1:auto focus; 2:once focus; 3:Conjugate calibration)
UVCHAM_AFZONE              = 0x00000023    # auto focus zone index
                                           #    the whole resolution is divided in w * h zones:
                                           #        w = max & 0xff
                                           #        h = (max >> 8) & 0xff
                                           #    then:
                                           #        zone row:    value / w
                                           #        zone column: value % w
                                           #
UVCHAM_AFFEEDBACK          = 0x00000024    # auto focus information feedback
                                           #    0: unknown
                                           #    1: focused
                                           #    2: focusing
                                           #    3: defocuse (out of focus)
                                           #    4: up (workbench move up)
                                           #    5: down (workbench move down)
                                           #
UVCHAM_AFPOSITION_ABSOLUTE = 0x00000025    # absolute auto focus sensor board positon: -5400um~10600um(-5.4mm~10.6mm); range only
UVCHAM_PAUSE               = 0x00000026    # pause
UVCHAM_SN                  = 0x00000027    # serial number
UVCHAM_BPS                 = 0x00000032    # bitrate: Mbps
UVCHAM_LIGHT_ADJUSTMENT    = 0x00000033    # light source brightness adjustment
UVCHAM_ZOOM                = 0x00000034    # SET only
UVCHAM_USER                = 0x00000035    # User
UVCHAM_EF_MODE             = 0x00000036
UVCHAM_EF_FL               = 0x00000037
UVCHAM_EF_APERTURE_MIN_MAX = 0x00000038
UVCHAM_EF_APERTURE_CUR     = 0x00000039
UVCHAM_EF_FOCUS_CUR        = 0x0000003a
UVCHAM_EF_FOCUS_MAX        = 0x0000003b
UVCHAM_EF_LENS_ID          = 0x0000003c
UVCHAM_EF_AFMF             = 0x0000003d
UVCHAM_EF_WD_ENABLE        = 0x0000003e
UVCHAM_EF_WD_NEAR          = 0x0000003f
UVCHAM_EF_WD_FAR           = 0x00000040
UVCHAM_TEMP                = 0x00000042    # temp/tint mode: color temperature
UVCHAM_TINT                = 0x00000043    # temp/tint mode: tint
UVCHAM_AGAIN               = 0x00000084    # analog gain
UVCHAM_NEGATIVE            = 0x00000085    # negative film
UVCHAM_REALTIME            = 0x00000086    # realtime: 1 => ON, 0 => OFF
UVCHAM_FORMAT              = 0x000000fe    # output format: 0 => BGR888, 1 => BGRA8888, 2 => RGB888, 3 => RGBA8888; default: 0
                                           # Can be changed only when camera is not running.
                                           #
UVCHAM_CODEC               = 0x01000000    # codec:
                                           #    Can be changed only when camera is not running.
                                           #    To get the number of the supported codec, use: Uvcham_range(h, UVCHAM_CODEC, nullptr, &num, nullptr)
                                           #
UVCHAM_CODEC_FOURCC        = 0x02000000    # to get fourcc of the nth codec, use: Uvcham_get(h, UVCHAM_CODEC_FOURCC | n, &fourcc), such as MAKEFOURCC('M', 'J', 'P', 'G')
UVCHAM_RES                 = 0x10000000    # resolution:
                                           #    Can be changed only when camera is not running.
                                           #    To get the number of the supported resolution, use: Uvcham_range(h, UVCHAM_RES, nullptr, &num, nullptr)
                                           #
UVCHAM_WIDTH               = 0x40000000    # to get the nth width, use: Uvcham_get(h, UVCHAM_WIDTH | n, &width)
UVCHAM_HEIGHT              = 0x80000000

"""
********************************************************************
* How to enum the resolutions:                                     *
*     res = cam_.range(UVCHAM_RES)                                 *
*     for i in range(0, res[0] + 1):                               *
*         width = cam_.get(UVCHAM_WIDTH | i)                       *
*         height = cam_.get(UVHSAM_HEIGHT | i)                     *
*         print('{}: {} x {}\n'.format(i, width, height))          *
********************************************************************

********************************************************************
* "Direct Mode" vs "Pull Mode"                                     *
* (1) Direct Mode:                                                 *
*     (a) cam_.start(h, pFrameBuffer, ...)                         *
*     (b) pros: simple, slightly more efficient                    *
* (2) Pull Mode:                                                   *
*     (a) cam_.start(h, None, ...)                                 *
*     (b) use cam_.pull(h, pFrameBuffer) to pull image             *
*     (c) pros: never frame confusion                              *
********************************************************************

********************************************************************
* How to test whether the camera supports auto focus:              *
*     try:                                                         *
*         val = cam_.get(UVCHAM_AFZONE)                            *
*     except:                                                      *
*         // not supported                                         *
*     else:                                                        *
*         // no except, it supports                                *
********************************************************************
"""

# event
UVCHAM_EVENT_IMAGE         = 0x0001
UVCHAM_EVENT_DISCONNECT    = 0x0002    # camera disconnect
UVCHAM_EVENT_ERROR         = 0x0004    # error

UVCHAM_WBROI_WIDTH_MIN     = 48
UVCHAM_WBROI_HEIGHT_MIN    = 32

def TDIBWIDTHBYTES(bits):
    return ((bits + 31) // 32 * 4)

class UvchamDevice:
    def __init__(self, displayname, id):
        self.displayname = displayname   # display name
        self.id = id                     # unique and opaque id of a connected camera, for Uvcham_open

class HRESULTException(OSError):
    def __init__(self, hr):
        OSError.__init__(self, None, ctypes.FormatError(hr).strip(), None, hr)
        self.hr = hr

class Uvcham:
    class __Device(ctypes.Structure):
        _fields_ = [('displayname', ctypes.c_wchar * 128), # display name
                    ('id', ctypes.c_wchar * 128)]          # unique and opaque id of a connected camera, for Uvcham_open

    __CALLBACK = ctypes.WINFUNCTYPE(None, ctypes.c_uint, ctypes.py_object)
    __lib = None

    @staticmethod
    def __errcheck(result, fun, args):
        if result < 0:
            raise HRESULTException(result)
        return args

    @staticmethod
    def __convertStr(x):
        if isinstance(x, str):
            return x
        else:
            return x.decode('ascii')

    @classmethod
    def Version(cls):
        """get the version of this dll, which is: 1.30594.20260120"""
        cls.__initlib()
        return cls.__lib.Uvcham_version()

    @staticmethod
    def __convertDevice(a):
        return UvchamDevice(__class__.__convertStr(a.displayname), __class__.__convertStr(a.id))

    @classmethod
    def enum(cls):
        """enumerate the cameras that are currently connected to computer"""
        cls.__initlib()
        a = (cls.__Device * UVCHAM_MAX)()
        n = cls.__lib.Uvcham_enum(a)
        arr = []
        for i in range(0, n):
            arr.append(cls.__convertDevice(a[i]))
        return arr

    def __init__(self, h):
        """the object of Uvcham must be obtained by classmethod Open, it cannot be obtained by obj = uvcham.Uvcham()"""
        self.__h = h
        self.__fun = None
        self.__ctx = None
        self.__cb = None

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __nonzero__(self):
        return self.__h is not None

    def __bool__(self):
        return self.__h is not None

    @classmethod
    def open(cls, camId):
        """the object of Uvcham must be obtained by classmethod Open, it cannot be obtained by obj = uvcham.Uvcham()"""
        cls.__initlib()
        h = cls.__lib.Uvcham_open(camId)
        if h is None:
            return None
        return __class__(h)

    def close(self):
        if self.__h:
            self.__lib.Uvcham_close(self.__h)
            self.__h = None

    @staticmethod
    def __tcallbackFun(nEvent, ctx):
        if ctx:
            ctx.__callbackFun(nEvent)

    def __callbackFun(self, nEvent):
        if self.__fun:
            self.__fun(nEvent, self.__ctx)

    def start(self, buf, fun, ctx):
        self.__fun = fun
        self.__ctx = ctx
        self.__cb = __class__.__CALLBACK(__class__.__tcallbackFun)
        self.__lib.Uvcham_start(self.__h, buf, self.__cb, ctypes.py_object(self))

    def stop(self):
        self.__lib.Uvcham_stop(self.__h)

    def pull(self, buf):
        self.__lib.Uvcham_pull(self.__h, buf)

    def put(self, nId, val):
        """nId: UVCHAM_XXXX"""
        self.__lib.Uvcham_put(self.__h, ctypes.c_uint(nId), ctypes.c_int(val))

    def record(self, filePath):
        """
        (filePath == None) means to stop record.
        support file extension: *.asf, *.mp4, *.mkv
        """
        self.__lib.Uvcham_record(self.__h, filePath)

    def get(self, nId):
        x = ctypes.c_int(0)
        self.__lib.Uvcham_get(self.__h, ctypes.c_uint(nId), ctypes.byref(x))
        return x.value

    def range(self, nId):
        nMin = ctypes.c_int(0)
        nMax = ctypes.c_int(0)
        nDef = ctypes.c_int(0)
        self.__lib.Uvcham_range(self.__h, ctypes.c_uint(nId), ctypes.byref(nMin), ctypes.byref(nMax), ctypes.byref(nDef))
        return (nMin.value, nMax.value, nDef.value)

    @classmethod
    def __initlib(cls):
        if cls.__lib is None:
            try: # Firstly try to load the library in the directory where this file is located
                dir = os.path.dirname(os.path.realpath(__file__))
                cls.__lib = ctypes.windll.LoadLibrary(os.path.join(dir, 'uvcham.dll'))
            except OSError:
                pass

            if cls.__lib is None:
                cls.__lib = ctypes.windll.LoadLibrary('uvcham.dll')

            cls.__lib.Uvcham_version.restype = ctypes.c_wchar_p
            cls.__lib.Uvcham_version.argtypes = None
            cls.__lib.Uvcham_enum.restype = ctypes.c_uint
            cls.__lib.Uvcham_enum.argtypes = [cls.__Device * UVCHAM_MAX]
            cls.__lib.Uvcham_open.restype = ctypes.c_void_p
            cls.__lib.Uvcham_open.argtypes = [ctypes.c_wchar_p]
            cls.__lib.Uvcham_start.restype = ctypes.c_int
            cls.__lib.Uvcham_start.argtypes = [ctypes.c_void_p, ctypes.c_char_p, cls.__CALLBACK, ctypes.py_object]
            cls.__lib.Uvcham_start.errcheck = cls.__errcheck
            cls.__lib.Uvcham_stop.restype = ctypes.c_int
            cls.__lib.Uvcham_stop.argtypes = [ctypes.c_void_p]
            cls.__lib.Uvcham_stop.errcheck = cls.__errcheck
            cls.__lib.Uvcham_close.restype = None
            cls.__lib.Uvcham_close.argtypes = [ctypes.c_void_p]
            cls.__lib.Uvcham_put.restype = ctypes.c_int
            cls.__lib.Uvcham_put.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_int]
            cls.__lib.Uvcham_put.errcheck = cls.__errcheck
            cls.__lib.Uvcham_get.restype = ctypes.c_int
            cls.__lib.Uvcham_get.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_int)]
            cls.__lib.Uvcham_get.errcheck = cls.__errcheck
            cls.__lib.Uvcham_range.restype = ctypes.c_int
            cls.__lib.Uvcham_range.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
            cls.__lib.Uvcham_range.errcheck = cls.__errcheck
            cls.__lib.Uvcham_pull.restype = ctypes.c_int
            cls.__lib.Uvcham_pull.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
            cls.__lib.Uvcham_pull.errcheck = cls.__errcheck
            cls.__lib.Uvcham_record.restype = ctypes.c_int
            cls.__lib.Uvcham_record.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
            cls.__lib.Uvcham_record.errcheck = cls.__errcheck