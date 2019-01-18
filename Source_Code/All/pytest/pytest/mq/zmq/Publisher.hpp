//
//  Publisher.hpp
//  SocketDev
//
//  Created by Ryan on 12/6/15.


#ifndef Publisher_hpp
#define Publisher_hpp

#include <stdio.h>
class CPubliser
{
public:
    CPubliser();
    ~CPubliser();
public:
    int connect(const char * address);
    int bind(const char * address);
    int close();

    int Pulish(void * data,long len);
    int PulishString(const char * str);
protected:
    void * m_context;
    void * m_socket;
    
};
#endif /* Publisher_hpp */
