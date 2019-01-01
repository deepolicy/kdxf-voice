/*
 * https://www.cnblogs.com/ashen/p/4474360.html
 * inkaci@qq.com
 */

#include <sys/socket.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* #include <linux/in.h> */
#include <netinet/in.h>
/* https://blog.csdn.net/akwang1/article/details/8281270 */

#include <unistd.h>
/* https://baike.baidu.com/item/write%E5%87%BD%E6%95%B0/5755349?fr=aladdin */

#include <sys/types.h>

#define PORT 7891

int main()
{
    int         socketfd, accsocfd;
    struct sockaddr_in  s_addr, r_addr;
    socklen_t       len;
    int         recdata;
    char            buf[1024];
    memset( buf, 0x00, sizeof(buf) );
    /* 创建套接字 */
    if ( -1 == (socketfd = socket( AF_INET, SOCK_STREAM, 0 ) ) )
    {
        printf( "socketfd is created failed!\n" );
        return(-1);
    }
    ;
    printf( "socket create success!\n" );

    /* 将本地协议地址与sockfd绑定 */
    memset( &s_addr, 0x00, sizeof(s_addr) );
    s_addr.sin_family   = PF_INET;
    s_addr.sin_port     = htons( PORT );
    s_addr.sin_addr.s_addr  = htons( INADDR_ANY ); /* inet_addr_any 一个服务器可能有多个网卡，随便从中选1个 */
    if ( -1 == bind( socketfd, (struct sockaddr *) &s_addr, sizeof(s_addr) ) )
    {
        printf( "bind failed!\n" );
        return(-1);
    }
    printf( "bind suc!\n" );

    /* 监听本地端口 */
    if ( -1 == listen( socketfd, 10 ) )
    {
        printf( "listen failed!\n" );
        return(-1);
    }
    printf( "listen suc!\n" );

    while ( 1 )
    {
        len     = sizeof(struct sockaddr);
        accsocfd    = accept( socketfd, (struct sockaddr *) &r_addr, &len );
        if ( -1 == accsocfd )
        {
            printf( "accept failed!\n" );
            return(-1);
        }
        printf( "accept suc !\nServer get connect from %x port is %x", ntohl( r_addr.sin_addr.s_addr ), ntohl( r_addr.sin_port ) );


        /* 向客服端发送数据 */
        if ( -1 == write( accsocfd, "this is first data from sr!\n", 50 ) )
        {
            printf( "write failed!\n" );
            return(-1);
        }
        printf( "write suc!\n" );


        printf( "*********************\n" );

        char recvBuf[100];

        if ( -1 == recv( accsocfd, recvBuf, 100, 0 ) )
        {
            printf( "recv failed!\n" );
            return(-1);
        }

        printf( "recv suc!\n" );
        printf( "recvBuf  = [%s]\n", recvBuf );
        printf( "recvBuf len is = [%d]\n", int(strlen( recvBuf ) ) );

        close( accsocfd );
    }
    close( socketfd );
    return(0);
}