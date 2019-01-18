

#import "CArmDL.h"


#define PORT_BASE 0


CArmDL::CArmDL()
{
    client = [[[DLClient alloc]init]retain];
    mId = 0;
    saveAllData = false;
    strcpy(libName, "NULL");
}

CArmDL::CArmDL(int mid)
{
    mId = mid;
    strcpy(libName, "NULL");
    saveAllData = false;
    client = [[[DLClient alloc]init]retain];
}

CArmDL::CArmDL(int mid, const char * sname)
{
    mId = mid;
    client = [[[DLClient alloc]init]retain];
    saveAllData = false;
    strcpy(libName, sname);
}

CArmDL::~CArmDL()
{
    if (client) {
        [client disconnect];
        [client release];
    }
}

int CArmDL::CreateTCPClient(const char* name, const char* ip, short port)
{
    NSLog(@"Create TCP Client: %s,%s,%d",name,ip,port);
    if((port < PORT_BASE || (int)port > 32768))
        return -1;
    client = (DLClient*)[[DLClient alloc] initWithIPPort:[NSString stringWithUTF8String:name] :[NSString stringWithUTF8String:ip] :port];
    return [client getConnectState];
}

int CArmDL::CreatZmqPub(const char * address)
{
    if (client) {
        return [client initZmqPub :address];
    }
    return -1;
}

//void CArmDL::updateConfig(float gain, float refVolt, float res, int flag, int unitConvert)
void CArmDL::updateConfig(int channel, float resdiv, float gain, float refVolt, float res, int flag, int unitConvert)
{
    //NSLog(@"update config %d,%f,%f,%f,%f,%d,%d",channel,resdiv,gain,refVolt,res,flag,unitConvert);
    if (channel<0 || channel>5)
        channel = 0;
    if(client)
    {
        saveAllData = (flag>0);
        [client updateConfig:channel :resdiv :gain :refVolt :res :flag :unitConvert];
    }
}

void CArmDL::updateCalFactor(int channel, float gain, float offset)
{
    //NSLog(@"update CAL factor %d,%f,%f",channel,gain,offset);
    if (channel<0 || channel>5)
        channel = 0;
    if(client)
    {
        [client updateCalFactor:channel :gain :offset];
    }
}

int CArmDL::setLogPath(const char* header,const char* filename)
{
    if (client) {
        [client setLogPath: header :filename];
    }
    return 0;
}

int CArmDL::SendString(char* szString)
{
    if (client) {
        return [client send:[NSString stringWithUTF8String:szString]];
    }
    return -99999;
}

int CArmDL::DetectString(char* szDetectString, int iTimeout)
{
    int r = 0;
    if (client)
    {
        SetDetectString(szDetectString);
        r = WaitForString(iTimeout);
    }
    else{
        r = -99999;
    }

    return r;
}

int CArmDL::SetDetectString(const char* detectString)
{
    int r = 0;
    [client setDetectString:[NSString stringWithUTF8String:detectString]];
    return r;
}

int CArmDL::WaitForString(int timeout)
{
    int r = 0;
    r = [client waitString:timeout];
    return r;
    
}

char* CArmDL::ReadString()
{
    if (client) {
        return (char*)[[client readString] UTF8String];
    }
    return NULL;
}

const char* CArmDL::SendReceive(char* str, int timeout)
{
    if(client)
        return [[client sendRecv:[NSString stringWithFormat:@"%s",str] :timeout ]UTF8String];
    else return NULL;
}

const char* CArmDL::getStubData()
{
    const void * dataTmp = [[client getStubData]bytes];
    if(dataTmp) return (const char*)dataTmp;
    else return NULL;
}

int CArmDL::clearStubData()
{
    [client clearStubData];
    return 0;
}

void CArmDL::RemoveTCPClient()
{
    [client release];
}


int CArmDL::getID()
{
    return mId;
}

const char * CArmDL::GetModuleName()
{
    return libName;
}


int  CArmDL::startDataLogger()
{
    NSLog(@"start DataLogger...");
    [client clearDataLast];
    [client StartDL];
    return 0;
}

int  CArmDL::stopDataLogger()
{
    //NSLog(@"stop DataLogger...");
//    client.logOn = NO;
//    [client clearDataLast];
    [client StopDL];
    return 0;
}

//RMS
const char * CArmDL::startRMS(int chn)
{
    NSString * str = [client startRMS:chn];
    if(str==nil)return nullptr;
    return [str UTF8String];
}

const char * CArmDL::endRMS(int chn)
{
    NSString * str = [client endRMS:chn];
    if(str ==nil) return nullptr;
    return [str UTF8String];
}

double CArmDL::getRMS(int chn)
{
    return [client getRMS:chn];
}

double CArmDL::getAverage(int chn)
{
    return [client getAverage:chn];
}

float CArmDL::getMax(int chn)
{
    return [client getMax:chn];
}

float CArmDL::getMin(int chn)
{
    return [client getMin:chn];
}

unsigned long CArmDL::getCount(int chn)
{
    return [client getCount:chn];
}

void CArmDL::setArmChannel(int ch)
{
    [client setArmChannel:ch];
}

int CArmDL::getArmChannel()
{
    return [client getArmChannel];
}


