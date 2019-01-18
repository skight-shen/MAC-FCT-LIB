//
//  main.m
//  ArmDLTest
//
//  Created by IvanGan on 15/7/2.
//  Copyright (c) 2015年 IA. All rights reserved.
//

#import <Foundation/Foundation.h>

struct command
{
    char *arg[128];
    /*用于存放命令行参数的指针数组*/
    char *in;  /*存放输入重定向的文件名,其实这个变量也可以直接存放到arg中的,将他们分开存放方便读取数值*/
    char *out;  /*存放输出重定向的文件名*/
};
typedef struct command cmd;




/*以空格符分开命令行字符串*/
int parse_command_line(char *buf,cmd *cmd_buf) /*cmd_buf是一个结构体指针*/
{
    int i=0;
    cmd_buf->in=NULL;
    cmd_buf->out=NULL;
    char *p=strtok(buf," ");
    while(p)
    {
        if(*p=='>')
        {
            if(*(p+1))      /*如果>后面有空格，那么执行完strtok后，空格被替换成'\0',*(p+1)就是'\0'，为假，不执行cmd_buf->out=p+1*/
                cmd_buf->out=p+1;
            else
                cmd_buf->out=strtok(NULL," ");
            /*如果>后面没有空格，那么执行完strtok后，>符号被替换成'\0'了，直接调用strtok函数*/
        }
        else if(*p=='<')
        {
            if(*(p+1))
                cmd_buf->in=p+1;
            else
                cmd_buf->in=strtok(NULL," ");
        }
        else
            cmd_buf->arg[i++]=p;
        /*如果获取的命令行参数不是>或者<,那么就将它们保存在arg中*/
        p=strtok(NULL," ");
        /*当提取完成时，p=NULL,跳出while循环，把命令行的所有参数分开存放到arg中了*/
    }
    cmd_buf->arg[i]=NULL;
    /*把没有赋值的指针数组元素赋值为NULL*/
    return 0;
}


/*以管道符分开命令行字符串*/
int parse_pipe(char *buf,cmd cmd_s[]) /*cmd是结构数组，它的每一个元素都是一个结构体*/
{
    int n=0;
    char *p;
    /*这里使用strtok函数是不行的,必须使用strtok_r函数，它们的区别见博客*/
    char *pt=strtok_r(buf,"|",&p);
    while(pt)
    {
        parse_command_line(pt,&cmd_s[n++]);   /*以管道符分开的第一个字符串存放在结构数组cmd_s[0]中，第二个字符串存放在结构数组cmd_s[1]中，依次递推*/
        pt=strtok_r(NULL,"|",&p);
    }
    return n;
}


/*cd内部命令*/
int cd_command(char *cd_command,char *path)
{
    int return_value=0;
    
    
    if(strncmp(cd_command,"cd",2)==0)
        if((return_value=chdir(path))<0)
            perror("chdir");
    return return_value;
}

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        // insert code here...
        
        
        NSArray * arrColorCode = [NSArray arrayWithObjects:
                                  @"[0m",
                                  @"[1m ",
                                  @"[4m ",
                                  @"[5m ",
                                  @"[7m ",
                                  @"[8m ",
                                  @"[30m  ",
                                  @"[31m  ",
                                  @"[32m  ",
                                  @"[33m  ",
                                  @"[34m  ",
                                  @"[35m  ",
                                  @"[36m  ",
                                  @"[37m  ",
                                  @"[40m  ",
                                  @"[41m  ",
                                  @"[42m  ",
                                  @"[43m  ",
                                  @"[44m  ",
                                  @"[45m  ",
                                  @"[46m  ",
                                  @"[47m  ",
                                  @"[nA ",
                                  @"[nB ",
                                  @"[nC ",
                                  @"[nD ",
                                  @"[25;01H ",
                                  @"[2J ",
                                  @"[K ",
                                  @"[s ",
                                  @"[u ",
                                  @"[?25l ",
                                  @"[?25h ",
                                  nil];
        NSMutableString * m_reT = [[NSMutableString alloc]init];
        [m_reT setString:@"[0m[37m[40m  [1m[33m[40m[1m[33m[40mhd0 [0m[37m[40m[0m[37m[40m : HardDisk [EFI] - [1m[37m[40m[1m[37m[40mAlias[0m[37m[40m[0m[37m[40m [1m[33m[40m[1m[33m[40mfs0 blk0 [0m[37m[40m[0m[37m[40m"];
        char * x = "[0m[37m[40m  [1m[33m[40m[1m[33m[40mhd0 [0m[37m[40m[0m[37m[40m : HardDisk [EFI] - [1m[37m[40m[1m[37m[40mAlias[0m[37m[40m[0m[37m[40m [1m[33m[40m[1m[33m[40mfs0 blk0 [0m[37m[40m[0m[37m[40m";
        char *p = malloc(strlen(x));
        memcpy(p, x, strlen(x));
        for (int i=0; i<strlen(p); i++) {
            if (p[i] == '\0') {
                p[i] = '.';
            }
            if (1) {
                if (p[i] < 32 || p[i] >= 127) {   //skip unvisible character
                    p[i] = ' ';
                }
            }
        }
        NSString *sss = [NSString stringWithUTF8String:p];
        for (NSString *line in arrColorCode) {
            while (true) {
                NSRange range = [m_reT rangeOfString:line];
                if (range.location!=NSNotFound) {
                    NSArray * Array = [sss componentsSeparatedByString:line];
                    int i =999;
                    i++;
                    ;
                }else{
                    break;
                }
            }
            
            
            //str=[str stringByReplacingOccurrencesOfString:@"itcast" withString:@"ios"];
            NSMutableString *String1 = [[NSMutableString alloc] initWithString:@"This is a NSMutableString"];
            [String1 replaceCharactersInRange:NSMakeRange(0, 4) withString:@"That"];
            NSLog(@"String1:%@",String1);
            
        }
        
            char buff[50];
            char pathname[50];
            cmd cmds[10];  /*结构数组，它的每一个元素都是一个结构体*/
            pid_t pid;
            int fd_in;  /*输入重定向文件描述符*/
            int fd_out;  /*输出重定向文件描述符*/
            int i=0;
            int pipe_num=0;
            int j=0;
            int fd[10][2];
            /*开辟10个管道描述符*/
            int cmd_num=0;
            /*以管道符号分开的命令数目*/
        
        
            while(1)
            {
                /*获取初始的工作路径*/
                memset(pathname,50,0);
                getcwd(pathname,50);
                /*获取当前工作路经*/
                printf("[my@localhost %s]",pathname);
                fflush(stdout);
                /*刷新缓冲区*/
                
                
                
                memset(buff,50,0);
                fgets(buff,50,stdin);
                /*获取命令行所有参数*/
                buff[strlen(buff)-1]='\0';
                /*这点处理非常有必要，直接输入内容给一个buffer赋值时，最好给buffer后面添加一个'\0'*/
                /*cmds存放的是以管道符|分开的命令行字符串，该字符串中又包含若干个命令参数，而arg中存放的是单个的命令行参数*/
                
                
                cmd_num=parse_pipe(buff,cmds);
                /*cmd_num就是以管道符号分开的命令字符串的个数*/
                
                
                cd_command(cmds[0].arg[0],cmds[0].arg[1]);  /*调用cd命令函数*/
                
                /*便于分析结构数组的值而打印输出*//*
                 printf("cmds[0]=        %s\n",cmds[0]);
                 printf("cmds[0].arg[0]=          %s\n",cmds[0].arg[0]);
                 printf("cmds[0].arg[1]=          %s\n",cmds[0].arg[1]);
                 printf("cmds[0].in=       %s\n",cmds[0].in);
                 printf("cmds[0].out=          %s\n",cmds[0].out);
                 
                 
                 printf("cmds[1]=        %s\n",cmds[1]);
                 printf("cmds[1].arg[0]=          %s\n",cmds[1].arg[0]);
                 printf("cmds[1].arg[1]=          %s\n",cmds[1].arg[1]);
                 printf("cmds[1].in=       %s\n",cmds[1].in);
                 printf("cmds[1].out=          %s\n",cmds[1].out);
                 fflush(stdout);
                */
                
                pipe_num=cmd_num- 1;
                
                
                if(pipe_num>10)
                /*因为预先最多分配了10个管道描述符，所以如果从终端获取的管道个数大于10，就重新输入命令行*/
                    continue;
                for(i=0;i<pipe_num;i++)
                    pipe(fd[i]);
                
                
                for(i=0;i<cmd_num;i++)
                /*i等于以管道符分开的命令个数*/
                {
                    if((pid=fork())==0)
                    /*创建进程，如果子进程先执行，跳出循环，执行子进程代码段，如果父进程先执行，接着创建，最后的结果就是产生一个父进程，cmd_num个子进程*/
                        
                        break;
                    if(pid<0)
                        perror("fork");
                }
                if(pid==0)   /*这里有多少个子进程就执行多少次*/
                {
                    /*重定向输入*/
                    if(cmds[i].in)  /*执行第一个子进程时i=0,执行第二个子进程时i=1,依次递增*/
                    {
                        fd_in=open(cmds[i].in,O_RDONLY);
                        if(fd_in<0)
                            perror("open");
                        dup2(fd_in,STDIN_FILENO);
                        close(fd_in);
                    }
                    /*重定向输出*/
                    if(cmds[i].out)
                    {
                        fd_out=open(cmds[i].out,O_RDWR|O_CREAT|O_TRUNC,0644);
                        if(fd_out<0)
                            perror("open_out");
                        dup2(fd_out,STDOUT_FILENO);
                        close(fd_out);
                    }
                    /*管道: 它是进程间的一种通信方式，这里采取的是多个子进程间通信*/
                    if(pipe_num)  /*如果管道个数为0则不执行，否则执行*/
                    {
                        if(i==0)
                        {
                            close(fd[i][0]);
                            /*i=0肯定是第一个子进程，关闭第一个子进程的管道的读端*/
                            dup2(fd[i][1],1);
                            /*将标准输出重定向到第一个子进程管道的写端,本来第一个命令字符串的执行结果输出到屏幕的，现在输出到管道的读端*/
                            close(fd[i][1]);
                            /*关闭第一个子进程管道的写端*/
                            for(j=1;j<pipe_num;++j)
                            /*关闭多余的管道，当然这里只创建了一个管道*/
                                close(fd[j][0]),close(fd[j][1]);
                        }
                        else if(i==pipe_num)
                        /*假设i=1肯定是第二个子进程，并且只有一个管道，那么条件成立*/
                        {
                            close(fd[i-1][1]);
                            /*关闭管道的写端*/
                            dup2(fd[i-1][0],0);
                            /*将标准输入重定向到第二个子进程的读端，本来第二个命令字符串的输入是直接由键盘输入的，现在直接从管道的读端获取，从而达到了两个进程的通信*/
                            close(fd[i-1][0]);
                            /*关闭第二个子进车管道的读端*/
                            for(j=0;j<pipe_num-1;++j)
                                close(fd[j][0]),close(fd[j][1]);
                        }
                        else
                        {
                            dup2(fd[i - 1][0], 0);
                            close(fd[i][0]);
                            dup2(fd[i][1], 1);
                            close(fd[i][1]);
                            for (j = 0; j < pipe_num; ++j)
                            {
                                if((j!=i-1)||(j!=i))
                                    close(fd[j][0]),close(fd[j][1]);
                            }
                        }
                    }
                    /*execlp(cmds[0].arg[0],cmds[0].arg[0],cmds[0].arg[1],cmds[0].arg[2],cmds[0].arg[3],NULL);*/
                    /*结构数组中指针数组元素的第0个参数一定是命令(这是由命令行输入决定的)，第二个参数是命令参数*/
                    execvp(cmds[i].arg[0],cmds[i].arg);
                }
                if(pid>0)
                {
                    for(i=0;i<pipe_num;++i)
                        close(fd[i][0]),close(fd[i][1]);
                    for(i=0;i<cmd_num;i++)
                        wait(NULL);
                }
            }
            return 0;
    }
    return 0;
}
