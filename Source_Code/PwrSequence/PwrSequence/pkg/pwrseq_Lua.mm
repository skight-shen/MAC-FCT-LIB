/*
** Lua binding: pwrseq
** Generated automatically by tolua++-1.0.92 on Mon Jan  8 16:04:46 2018.
*/

#ifndef __cplusplus
#include "stdlib.h"
#endif
#include "string.h"

#include "tolua++.h"

/* Exported function */
TOLUA_API int  tolua_pwrseq_open (lua_State* tolua_S);

#include "CPwrSeq.h"

/* function to release collected object via destructor */
#ifdef __cplusplus

static int tolua_collect_CPWRSEQ (lua_State* tolua_S)
{
 CPWRSEQ* self = (CPWRSEQ*) tolua_tousertype(tolua_S,1,0);
	Mtolua_delete(self);
	return 0;
}
#endif


/* function to register type */
static void tolua_reg_types (lua_State* tolua_S)
{
 tolua_usertype(tolua_S,"CPWRSEQ");
}

/* method: new of class  CPWRSEQ */
#ifndef TOLUA_DISABLE_tolua_pwrseq_CPWRSEQ_new00
static int tolua_pwrseq_CPWRSEQ_new00(lua_State* tolua_S)
{
#ifndef TOLUA_RELEASE
 tolua_Error tolua_err;
 if (
     !tolua_isusertable(tolua_S,1,"CPWRSEQ",0,&tolua_err) ||
     !tolua_isnoobj(tolua_S,2,&tolua_err)
 )
  goto tolua_lerror;
 else
#endif
 {
  {
   CPWRSEQ* tolua_ret = (CPWRSEQ*)  Mtolua_new((CPWRSEQ)());
    tolua_pushusertype(tolua_S,(void*)tolua_ret,"CPWRSEQ");
  }
 }
 return 1;
#ifndef TOLUA_RELEASE
 tolua_lerror:
 tolua_error(tolua_S,"#ferror in function 'new'.",&tolua_err);
 return 0;
#endif
}
#endif //#ifndef TOLUA_DISABLE

/* method: new_local of class  CPWRSEQ */
#ifndef TOLUA_DISABLE_tolua_pwrseq_CPWRSEQ_new00_local
static int tolua_pwrseq_CPWRSEQ_new00_local(lua_State* tolua_S)
{
#ifndef TOLUA_RELEASE
 tolua_Error tolua_err;
 if (
     !tolua_isusertable(tolua_S,1,"CPWRSEQ",0,&tolua_err) ||
     !tolua_isnoobj(tolua_S,2,&tolua_err)
 )
  goto tolua_lerror;
 else
#endif
 {
  {
   CPWRSEQ* tolua_ret = (CPWRSEQ*)  Mtolua_new((CPWRSEQ)());
    tolua_pushusertype(tolua_S,(void*)tolua_ret,"CPWRSEQ");
    tolua_register_gc(tolua_S,lua_gettop(tolua_S));
  }
 }
 return 1;
#ifndef TOLUA_RELEASE
 tolua_lerror:
 tolua_error(tolua_S,"#ferror in function 'new'.",&tolua_err);
 return 0;
#endif
}
#endif //#ifndef TOLUA_DISABLE

/* method: new of class  CPWRSEQ */
#ifndef TOLUA_DISABLE_tolua_pwrseq_CPWRSEQ_new01
static int tolua_pwrseq_CPWRSEQ_new01(lua_State* tolua_S)
{
 tolua_Error tolua_err;
 if (
     !tolua_isusertable(tolua_S,1,"CPWRSEQ",0,&tolua_err) ||
     !tolua_isnumber(tolua_S,2,0,&tolua_err) ||
     !tolua_isnoobj(tolua_S,3,&tolua_err)
 )
  goto tolua_lerror;
 else
 {
  int mid = ((int)  tolua_tonumber(tolua_S,2,0));
  {
   CPWRSEQ* tolua_ret = (CPWRSEQ*)  Mtolua_new((CPWRSEQ)(mid));
    tolua_pushusertype(tolua_S,(void*)tolua_ret,"CPWRSEQ");
  }
 }
 return 1;
tolua_lerror:
 return tolua_pwrseq_CPWRSEQ_new00(tolua_S);
}
#endif //#ifndef TOLUA_DISABLE

/* method: new_local of class  CPWRSEQ */
#ifndef TOLUA_DISABLE_tolua_pwrseq_CPWRSEQ_new01_local
static int tolua_pwrseq_CPWRSEQ_new01_local(lua_State* tolua_S)
{
 tolua_Error tolua_err;
 if (
     !tolua_isusertable(tolua_S,1,"CPWRSEQ",0,&tolua_err) ||
     !tolua_isnumber(tolua_S,2,0,&tolua_err) ||
     !tolua_isnoobj(tolua_S,3,&tolua_err)
 )
  goto tolua_lerror;
 else
 {
  int mid = ((int)  tolua_tonumber(tolua_S,2,0));
  {
   CPWRSEQ* tolua_ret = (CPWRSEQ*)  Mtolua_new((CPWRSEQ)(mid));
    tolua_pushusertype(tolua_S,(void*)tolua_ret,"CPWRSEQ");
    tolua_register_gc(tolua_S,lua_gettop(tolua_S));
  }
 }
 return 1;
tolua_lerror:
 return tolua_pwrseq_CPWRSEQ_new00_local(tolua_S);
}
#endif //#ifndef TOLUA_DISABLE

/* method: new of class  CPWRSEQ */
#ifndef TOLUA_DISABLE_tolua_pwrseq_CPWRSEQ_new02
static int tolua_pwrseq_CPWRSEQ_new02(lua_State* tolua_S)
{
 tolua_Error tolua_err;
 if (
     !tolua_isusertable(tolua_S,1,"CPWRSEQ",0,&tolua_err) ||
     !tolua_isnumber(tolua_S,2,0,&tolua_err) ||
     !tolua_isstring(tolua_S,3,0,&tolua_err) ||
     !tolua_isnoobj(tolua_S,4,&tolua_err)
 )
  goto tolua_lerror;
 else
 {
  int mid = ((int)  tolua_tonumber(tolua_S,2,0));
  const char* name = ((const char*)  tolua_tostring(tolua_S,3,0));
  {
   CPWRSEQ* tolua_ret = (CPWRSEQ*)  Mtolua_new((CPWRSEQ)(mid,name));
    tolua_pushusertype(tolua_S,(void*)tolua_ret,"CPWRSEQ");
  }
 }
 return 1;
tolua_lerror:
 return tolua_pwrseq_CPWRSEQ_new01(tolua_S);
}
#endif //#ifndef TOLUA_DISABLE

/* method: new_local of class  CPWRSEQ */
#ifndef TOLUA_DISABLE_tolua_pwrseq_CPWRSEQ_new02_local
static int tolua_pwrseq_CPWRSEQ_new02_local(lua_State* tolua_S)
{
 tolua_Error tolua_err;
 if (
     !tolua_isusertable(tolua_S,1,"CPWRSEQ",0,&tolua_err) ||
     !tolua_isnumber(tolua_S,2,0,&tolua_err) ||
     !tolua_isstring(tolua_S,3,0,&tolua_err) ||
     !tolua_isnoobj(tolua_S,4,&tolua_err)
 )
  goto tolua_lerror;
 else
 {
  int mid = ((int)  tolua_tonumber(tolua_S,2,0));
  const char* name = ((const char*)  tolua_tostring(tolua_S,3,0));
  {
   CPWRSEQ* tolua_ret = (CPWRSEQ*)  Mtolua_new((CPWRSEQ)(mid,name));
    tolua_pushusertype(tolua_S,(void*)tolua_ret,"CPWRSEQ");
    tolua_register_gc(tolua_S,lua_gettop(tolua_S));
  }
 }
 return 1;
tolua_lerror:
 return tolua_pwrseq_CPWRSEQ_new01_local(tolua_S);
}
#endif //#ifndef TOLUA_DISABLE

/* method: delete of class  CPWRSEQ */
#ifndef TOLUA_DISABLE_tolua_pwrseq_CPWRSEQ_delete00
static int tolua_pwrseq_CPWRSEQ_delete00(lua_State* tolua_S)
{
#ifndef TOLUA_RELEASE
 tolua_Error tolua_err;
 if (
     !tolua_isusertype(tolua_S,1,"CPWRSEQ",0,&tolua_err) ||
     !tolua_isnoobj(tolua_S,2,&tolua_err)
 )
  goto tolua_lerror;
 else
#endif
 {
  CPWRSEQ* self = (CPWRSEQ*)  tolua_tousertype(tolua_S,1,0);
#ifndef TOLUA_RELEASE
  if (!self) tolua_error(tolua_S,"invalid 'self' in function 'delete'", NULL);
#endif
  Mtolua_delete(self);
 }
 return 0;
#ifndef TOLUA_RELEASE
 tolua_lerror:
 tolua_error(tolua_S,"#ferror in function 'delete'.",&tolua_err);
 return 0;
#endif
}
#endif //#ifndef TOLUA_DISABLE

/* method: CreateTCPClient of class  CPWRSEQ */
#ifndef TOLUA_DISABLE_tolua_pwrseq_CPWRSEQ_CreateTCPClient00
static int tolua_pwrseq_CPWRSEQ_CreateTCPClient00(lua_State* tolua_S)
{
#ifndef TOLUA_RELEASE
 tolua_Error tolua_err;
 if (
     !tolua_isusertype(tolua_S,1,"CPWRSEQ",0,&tolua_err) ||
     !tolua_isstring(tolua_S,2,0,&tolua_err) ||
     !tolua_isstring(tolua_S,3,0,&tolua_err) ||
     !tolua_isnumber(tolua_S,4,0,&tolua_err) ||
     !tolua_isnoobj(tolua_S,5,&tolua_err)
 )
  goto tolua_lerror;
 else
#endif
 {
  CPWRSEQ* self = (CPWRSEQ*)  tolua_tousertype(tolua_S,1,0);
  const char* name = ((const char*)  tolua_tostring(tolua_S,2,0));
  const char* ip = ((const char*)  tolua_tostring(tolua_S,3,0));
  short port = ((short)  tolua_tonumber(tolua_S,4,0));
#ifndef TOLUA_RELEASE
  if (!self) tolua_error(tolua_S,"invalid 'self' in function 'CreateTCPClient'", NULL);
#endif
  {
   int tolua_ret = (int)  self->CreateTCPClient(name,ip,port);
   tolua_pushnumber(tolua_S,(lua_Number)tolua_ret);
  }
 }
 return 1;
#ifndef TOLUA_RELEASE
 tolua_lerror:
 tolua_error(tolua_S,"#ferror in function 'CreateTCPClient'.",&tolua_err);
 return 0;
#endif
}
#endif //#ifndef TOLUA_DISABLE

/* method: CreatZmqPub of class  CPWRSEQ */
#ifndef TOLUA_DISABLE_tolua_pwrseq_CPWRSEQ_CreatZmqPub00
static int tolua_pwrseq_CPWRSEQ_CreatZmqPub00(lua_State* tolua_S)
{
#ifndef TOLUA_RELEASE
 tolua_Error tolua_err;
 if (
     !tolua_isusertype(tolua_S,1,"CPWRSEQ",0,&tolua_err) ||
     !tolua_isstring(tolua_S,2,0,&tolua_err) ||
     !tolua_isnumber(tolua_S,3,1,&tolua_err) ||
     !tolua_isnoobj(tolua_S,4,&tolua_err)
 )
  goto tolua_lerror;
 else
#endif
 {
  CPWRSEQ* self = (CPWRSEQ*)  tolua_tousertype(tolua_S,1,0);
  const char* address = ((const char*)  tolua_tostring(tolua_S,2,0));
  int writeLog = ((int)  tolua_tonumber(tolua_S,3,0));
#ifndef TOLUA_RELEASE
  if (!self) tolua_error(tolua_S,"invalid 'self' in function 'CreatZmqPub'", NULL);
#endif
  {
   int tolua_ret = (int)  self->CreatZmqPub(address,writeLog);
   tolua_pushnumber(tolua_S,(lua_Number)tolua_ret);
  }
 }
 return 1;
#ifndef TOLUA_RELEASE
 tolua_lerror:
 tolua_error(tolua_S,"#ferror in function 'CreatZmqPub'.",&tolua_err);
 return 0;
#endif
}
#endif //#ifndef TOLUA_DISABLE

/* method: CreatZmqPub_BKLT of class  CPWRSEQ */
#ifndef TOLUA_DISABLE_tolua_pwrseq_CPWRSEQ_CreatZmqPub_BKLT00
static int tolua_pwrseq_CPWRSEQ_CreatZmqPub_BKLT00(lua_State* tolua_S)
{
#ifndef TOLUA_RELEASE
 tolua_Error tolua_err;
 if (
     !tolua_isusertype(tolua_S,1,"CPWRSEQ",0,&tolua_err) ||
     !tolua_isstring(tolua_S,2,0,&tolua_err) ||
     !tolua_isnumber(tolua_S,3,1,&tolua_err) ||
     !tolua_isnoobj(tolua_S,4,&tolua_err)
 )
  goto tolua_lerror;
 else
#endif
 {
  CPWRSEQ* self = (CPWRSEQ*)  tolua_tousertype(tolua_S,1,0);
  const char* address = ((const char*)  tolua_tostring(tolua_S,2,0));
  int writeLog = ((int)  tolua_tonumber(tolua_S,3,0));
#ifndef TOLUA_RELEASE
  if (!self) tolua_error(tolua_S,"invalid 'self' in function 'CreatZmqPub_BKLT'", NULL);
#endif
  {
   int tolua_ret = (int)  self->CreatZmqPub_BKLT(address,writeLog);
   tolua_pushnumber(tolua_S,(lua_Number)tolua_ret);
  }
 }
 return 1;
#ifndef TOLUA_RELEASE
 tolua_lerror:
 tolua_error(tolua_S,"#ferror in function 'CreatZmqPub_BKLT'.",&tolua_err);
 return 0;
#endif
}
#endif //#ifndef TOLUA_DISABLE

/* method: startDataLogger of class  CPWRSEQ */
#ifndef TOLUA_DISABLE_tolua_pwrseq_CPWRSEQ_startDataLogger00
static int tolua_pwrseq_CPWRSEQ_startDataLogger00(lua_State* tolua_S)
{
#ifndef TOLUA_RELEASE
 tolua_Error tolua_err;
 if (
     !tolua_isusertype(tolua_S,1,"CPWRSEQ",0,&tolua_err) ||
     !tolua_isstring(tolua_S,2,0,&tolua_err) ||
     !tolua_isnumber(tolua_S,3,0,&tolua_err) ||
     !tolua_isnoobj(tolua_S,4,&tolua_err)
 )
  goto tolua_lerror;
 else
#endif
 {
  CPWRSEQ* self = (CPWRSEQ*)  tolua_tousertype(tolua_S,1,0);
  const char* logPath = ((const char*)  tolua_tostring(tolua_S,2,0));
  int flag = ((int)  tolua_tonumber(tolua_S,3,0));
#ifndef TOLUA_RELEASE
  if (!self) tolua_error(tolua_S,"invalid 'self' in function 'startDataLogger'", NULL);
#endif
  {
   int tolua_ret = (int)  self->startDataLogger(logPath,flag);
   tolua_pushnumber(tolua_S,(lua_Number)tolua_ret);
  }
 }
 return 1;
#ifndef TOLUA_RELEASE
 tolua_lerror:
 tolua_error(tolua_S,"#ferror in function 'startDataLogger'.",&tolua_err);
 return 0;
#endif
}
#endif //#ifndef TOLUA_DISABLE

/* method: stopDataLogger of class  CPWRSEQ */
#ifndef TOLUA_DISABLE_tolua_pwrseq_CPWRSEQ_stopDataLogger00
static int tolua_pwrseq_CPWRSEQ_stopDataLogger00(lua_State* tolua_S)
{
#ifndef TOLUA_RELEASE
 tolua_Error tolua_err;
 if (
     !tolua_isusertype(tolua_S,1,"CPWRSEQ",0,&tolua_err) ||
     !tolua_isnumber(tolua_S,2,0,&tolua_err) ||
     !tolua_isnoobj(tolua_S,3,&tolua_err)
 )
  goto tolua_lerror;
 else
#endif
 {
  CPWRSEQ* self = (CPWRSEQ*)  tolua_tousertype(tolua_S,1,0);
  int flag = ((int)  tolua_tonumber(tolua_S,2,0));
#ifndef TOLUA_RELEASE
  if (!self) tolua_error(tolua_S,"invalid 'self' in function 'stopDataLogger'", NULL);
#endif
  {
   int tolua_ret = (int)  self->stopDataLogger(flag);
   tolua_pushnumber(tolua_S,(lua_Number)tolua_ret);
  }
 }
 return 1;
#ifndef TOLUA_RELEASE
 tolua_lerror:
 tolua_error(tolua_S,"#ferror in function 'stopDataLogger'.",&tolua_err);
 return 0;
#endif
}
#endif //#ifndef TOLUA_DISABLE

/* method: updateConfig of class  CPWRSEQ */
#ifndef TOLUA_DISABLE_tolua_pwrseq_CPWRSEQ_updateConfig00
static int tolua_pwrseq_CPWRSEQ_updateConfig00(lua_State* tolua_S)
{
#ifndef TOLUA_RELEASE
 tolua_Error tolua_err;
 if (
     !tolua_isusertype(tolua_S,1,"CPWRSEQ",0,&tolua_err) ||
     !tolua_isstring(tolua_S,2,0,&tolua_err) ||
     !tolua_isnumber(tolua_S,3,0,&tolua_err) ||
     !tolua_isnumber(tolua_S,4,0,&tolua_err) ||
     !tolua_isnoobj(tolua_S,5,&tolua_err)
 )
  goto tolua_lerror;
 else
#endif
 {
  CPWRSEQ* self = (CPWRSEQ*)  tolua_tousertype(tolua_S,1,0);
  const char* config = ((const char*)  tolua_tostring(tolua_S,2,0));
  int flag = ((int)  tolua_tonumber(tolua_S,3,0));
  int configID = ((int)  tolua_tonumber(tolua_S,4,0));
#ifndef TOLUA_RELEASE
  if (!self) tolua_error(tolua_S,"invalid 'self' in function 'updateConfig'", NULL);
#endif
  {
   self->updateConfig(config,flag,configID);
  }
 }
 return 0;
#ifndef TOLUA_RELEASE
 tolua_lerror:
 tolua_error(tolua_S,"#ferror in function 'updateConfig'.",&tolua_err);
 return 0;
#endif
}
#endif //#ifndef TOLUA_DISABLE

/* method: setPwrSeqChannel of class  CPWRSEQ */
#ifndef TOLUA_DISABLE_tolua_pwrseq_CPWRSEQ_setPwrSeqChannel00
static int tolua_pwrseq_CPWRSEQ_setPwrSeqChannel00(lua_State* tolua_S)
{
#ifndef TOLUA_RELEASE
 tolua_Error tolua_err;
 if (
     !tolua_isusertype(tolua_S,1,"CPWRSEQ",0,&tolua_err) ||
     !tolua_isnumber(tolua_S,2,0,&tolua_err) ||
     !tolua_isnoobj(tolua_S,3,&tolua_err)
 )
  goto tolua_lerror;
 else
#endif
 {
  CPWRSEQ* self = (CPWRSEQ*)  tolua_tousertype(tolua_S,1,0);
  int ch = ((int)  tolua_tonumber(tolua_S,2,0));
#ifndef TOLUA_RELEASE
  if (!self) tolua_error(tolua_S,"invalid 'self' in function 'setPwrSeqChannel'", NULL);
#endif
  {
   self->setPwrSeqChannel(ch);
  }
 }
 return 0;
#ifndef TOLUA_RELEASE
 tolua_lerror:
 tolua_error(tolua_S,"#ferror in function 'setPwrSeqChannel'.",&tolua_err);
 return 0;
#endif
}
#endif //#ifndef TOLUA_DISABLE

/* method: getPwrSeqChannel of class  CPWRSEQ */
#ifndef TOLUA_DISABLE_tolua_pwrseq_CPWRSEQ_getPwrSeqChannel00
static int tolua_pwrseq_CPWRSEQ_getPwrSeqChannel00(lua_State* tolua_S)
{
#ifndef TOLUA_RELEASE
 tolua_Error tolua_err;
 if (
     !tolua_isusertype(tolua_S,1,"CPWRSEQ",0,&tolua_err) ||
     !tolua_isnoobj(tolua_S,2,&tolua_err)
 )
  goto tolua_lerror;
 else
#endif
 {
  CPWRSEQ* self = (CPWRSEQ*)  tolua_tousertype(tolua_S,1,0);
#ifndef TOLUA_RELEASE
  if (!self) tolua_error(tolua_S,"invalid 'self' in function 'getPwrSeqChannel'", NULL);
#endif
  {
   int tolua_ret = (int)  self->getPwrSeqChannel();
   tolua_pushnumber(tolua_S,(lua_Number)tolua_ret);
  }
 }
 return 1;
#ifndef TOLUA_RELEASE
 tolua_lerror:
 tolua_error(tolua_S,"#ferror in function 'getPwrSeqChannel'.",&tolua_err);
 return 0;
#endif
}
#endif //#ifndef TOLUA_DISABLE

/* method: ConnectClient of class  CPWRSEQ */
#ifndef TOLUA_DISABLE_tolua_pwrseq_CPWRSEQ_ConnectClient00
static int tolua_pwrseq_CPWRSEQ_ConnectClient00(lua_State* tolua_S)
{
#ifndef TOLUA_RELEASE
 tolua_Error tolua_err;
 if (
     !tolua_isusertype(tolua_S,1,"CPWRSEQ",0,&tolua_err) ||
     !tolua_isnoobj(tolua_S,2,&tolua_err)
 )
  goto tolua_lerror;
 else
#endif
 {
  CPWRSEQ* self = (CPWRSEQ*)  tolua_tousertype(tolua_S,1,0);
#ifndef TOLUA_RELEASE
  if (!self) tolua_error(tolua_S,"invalid 'self' in function 'ConnectClient'", NULL);
#endif
  {
   int tolua_ret = (int)  self->ConnectClient();
   tolua_pushnumber(tolua_S,(lua_Number)tolua_ret);
  }
 }
 return 1;
#ifndef TOLUA_RELEASE
 tolua_lerror:
 tolua_error(tolua_S,"#ferror in function 'ConnectClient'.",&tolua_err);
 return 0;
#endif
}
#endif //#ifndef TOLUA_DISABLE

/* method: DisconnectClient of class  CPWRSEQ */
#ifndef TOLUA_DISABLE_tolua_pwrseq_CPWRSEQ_DisconnectClient00
static int tolua_pwrseq_CPWRSEQ_DisconnectClient00(lua_State* tolua_S)
{
#ifndef TOLUA_RELEASE
 tolua_Error tolua_err;
 if (
     !tolua_isusertype(tolua_S,1,"CPWRSEQ",0,&tolua_err) ||
     !tolua_isnoobj(tolua_S,2,&tolua_err)
 )
  goto tolua_lerror;
 else
#endif
 {
  CPWRSEQ* self = (CPWRSEQ*)  tolua_tousertype(tolua_S,1,0);
#ifndef TOLUA_RELEASE
  if (!self) tolua_error(tolua_S,"invalid 'self' in function 'DisconnectClient'", NULL);
#endif
  {
   int tolua_ret = (int)  self->DisconnectClient();
   tolua_pushnumber(tolua_S,(lua_Number)tolua_ret);
  }
 }
 return 1;
#ifndef TOLUA_RELEASE
 tolua_lerror:
 tolua_error(tolua_S,"#ferror in function 'DisconnectClient'.",&tolua_err);
 return 0;
#endif
}
#endif //#ifndef TOLUA_DISABLE

/* method: ResetTimeStamp of class  CPWRSEQ */
#ifndef TOLUA_DISABLE_tolua_pwrseq_CPWRSEQ_ResetTimeStamp00
static int tolua_pwrseq_CPWRSEQ_ResetTimeStamp00(lua_State* tolua_S)
{
#ifndef TOLUA_RELEASE
 tolua_Error tolua_err;
 if (
     !tolua_isusertype(tolua_S,1,"CPWRSEQ",0,&tolua_err) ||
     !tolua_isnoobj(tolua_S,2,&tolua_err)
 )
  goto tolua_lerror;
 else
#endif
 {
  CPWRSEQ* self = (CPWRSEQ*)  tolua_tousertype(tolua_S,1,0);
#ifndef TOLUA_RELEASE
  if (!self) tolua_error(tolua_S,"invalid 'self' in function 'ResetTimeStamp'", NULL);
#endif
  {
   self->ResetTimeStamp();
  }
 }
 return 0;
#ifndef TOLUA_RELEASE
 tolua_lerror:
 tolua_error(tolua_S,"#ferror in function 'ResetTimeStamp'.",&tolua_err);
 return 0;
#endif
}
#endif //#ifndef TOLUA_DISABLE

/* Open function */
TOLUA_API int tolua_pwrseq_open (lua_State* tolua_S)
{
 tolua_open(tolua_S);
 tolua_reg_types(tolua_S);
 tolua_module(tolua_S,NULL,0);
 tolua_beginmodule(tolua_S,NULL);
  #ifdef __cplusplus
  tolua_cclass(tolua_S,"CPWRSEQ","CPWRSEQ","",tolua_collect_CPWRSEQ);
  #else
  tolua_cclass(tolua_S,"CPWRSEQ","CPWRSEQ","",NULL);
  #endif
  tolua_beginmodule(tolua_S,"CPWRSEQ");
   tolua_function(tolua_S,"new",tolua_pwrseq_CPWRSEQ_new00);
   tolua_function(tolua_S,"new_local",tolua_pwrseq_CPWRSEQ_new00_local);
   tolua_function(tolua_S,".call",tolua_pwrseq_CPWRSEQ_new00_local);
   tolua_function(tolua_S,"new",tolua_pwrseq_CPWRSEQ_new01);
   tolua_function(tolua_S,"new_local",tolua_pwrseq_CPWRSEQ_new01_local);
   tolua_function(tolua_S,".call",tolua_pwrseq_CPWRSEQ_new01_local);
   tolua_function(tolua_S,"new",tolua_pwrseq_CPWRSEQ_new02);
   tolua_function(tolua_S,"new_local",tolua_pwrseq_CPWRSEQ_new02_local);
   tolua_function(tolua_S,".call",tolua_pwrseq_CPWRSEQ_new02_local);
   tolua_function(tolua_S,"delete",tolua_pwrseq_CPWRSEQ_delete00);
   tolua_function(tolua_S,"CreateTCPClient",tolua_pwrseq_CPWRSEQ_CreateTCPClient00);
   tolua_function(tolua_S,"CreatZmqPub",tolua_pwrseq_CPWRSEQ_CreatZmqPub00);
   tolua_function(tolua_S,"CreatZmqPub_BKLT",tolua_pwrseq_CPWRSEQ_CreatZmqPub_BKLT00);
   tolua_function(tolua_S,"startDataLogger",tolua_pwrseq_CPWRSEQ_startDataLogger00);
   tolua_function(tolua_S,"stopDataLogger",tolua_pwrseq_CPWRSEQ_stopDataLogger00);
   tolua_function(tolua_S,"updateConfig",tolua_pwrseq_CPWRSEQ_updateConfig00);
   tolua_function(tolua_S,"setPwrSeqChannel",tolua_pwrseq_CPWRSEQ_setPwrSeqChannel00);
   tolua_function(tolua_S,"getPwrSeqChannel",tolua_pwrseq_CPWRSEQ_getPwrSeqChannel00);
   tolua_function(tolua_S,"ConnectClient",tolua_pwrseq_CPWRSEQ_ConnectClient00);
   tolua_function(tolua_S,"DisconnectClient",tolua_pwrseq_CPWRSEQ_DisconnectClient00);
   tolua_function(tolua_S,"ResetTimeStamp",tolua_pwrseq_CPWRSEQ_ResetTimeStamp00);
  tolua_endmodule(tolua_S);
 tolua_endmodule(tolua_S);
 return 1;
}


#if defined(LUA_VERSION_NUM) && LUA_VERSION_NUM >= 501
 TOLUA_API int luaopen_pwrseq (lua_State* tolua_S) {
 return tolua_pwrseq_open(tolua_S);
};
#endif

