﻿/*
* 语音合成（Text To Speech，TTS）技术能够自动将任意文字实时转换为连续的
* 自然语音，是一种能够在任何时间、任何地点，向任何人提供语音信息服务的
* 高效便捷手段，非常符合信息时代海量数据、动态更新和个性化查询的需求。
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#include "qtts.h"
#include "msp_cmn.h"
#include "msp_errors.h"










#include <sys/socket.h>

/* #include <linux/in.h> */
#include <netinet/in.h>
/* https://blog.csdn.net/akwang1/article/details/8281270 */

#include <unistd.h>
/* https://baike.baidu.com/item/write%E5%87%BD%E6%95%B0/5755349?fr=aladdin */

#include <sys/types.h>

#define PORT 15001














/* wav音频头部格式 */
typedef struct _wave_pcm_hdr
{
	char            riff[4];                // = "RIFF"
	int		size_8;                 // = FileSize - 8
	char            wave[4];                // = "WAVE"
	char            fmt[4];                 // = "fmt "
	int		fmt_size;		// = 下一个结构体的大小 : 16

	short int       format_tag;             // = PCM : 1
	short int       channels;               // = 通道数 : 1
	int		samples_per_sec;        // = 采样率 : 8000 | 6000 | 11025 | 16000
	int		avg_bytes_per_sec;      // = 每秒字节数 : samples_per_sec * bits_per_sample / 8
	short int       block_align;            // = 每采样点字节数 : wBitsPerSample / 8
	short int       bits_per_sample;        // = 量化比特数: 8 | 16

	char            data[4];                // = "data";
	int		data_size;              // = 纯数据长度 : FileSize - 44 
} wave_pcm_hdr;

/* 默认wav音频头部数据 */
wave_pcm_hdr default_wav_hdr = 
{
	{ 'R', 'I', 'F', 'F' },
	0,
	{'W', 'A', 'V', 'E'},
	{'f', 'm', 't', ' '},
	16,
	1,
	1,
	16000,
	32000,
	2,
	16,
	{'d', 'a', 't', 'a'},
	0  
};
/* 文本合成 */
int text_to_speech(const char* src_text, const char* des_path, const char* params)
{
	int          ret          = -1;
	FILE*        fp           = NULL;
	const char*  sessionID    = NULL;
	unsigned int audio_len    = 0;
	wave_pcm_hdr wav_hdr      = default_wav_hdr;
	int          synth_status = MSP_TTS_FLAG_STILL_HAVE_DATA;

	if (NULL == src_text || NULL == des_path)
	{
		printf("params is error!\n");
		return ret;
	}
	fp = fopen(des_path, "wb");
	if (NULL == fp)
	{
		printf("open %s error.\n", des_path);
		return ret;
	}
	/* 开始合成 */
	sessionID = QTTSSessionBegin(params, &ret);
	if (MSP_SUCCESS != ret)
	{
		printf("QTTSSessionBegin failed, error code: %d.\n", ret);
		fclose(fp);
		return ret;
	}
	ret = QTTSTextPut(sessionID, src_text, (unsigned int)strlen(src_text), NULL);
	if (MSP_SUCCESS != ret)
	{
		printf("QTTSTextPut failed, error code: %d.\n",ret);
		QTTSSessionEnd(sessionID, "TextPutError");
		fclose(fp);
		return ret;
	}
	printf("正在合成 ...\n");
	fwrite(&wav_hdr, sizeof(wav_hdr) ,1, fp); //添加wav音频头，使用采样率为16000
	while (1) 
	{
		/* 获取合成音频 */
		const void* data = QTTSAudioGet(sessionID, &audio_len, &synth_status, &ret);
		if (MSP_SUCCESS != ret)
			break;
		if (NULL != data)
		{
			fwrite(data, audio_len, 1, fp);
		    wav_hdr.data_size += audio_len; //计算data_size大小
		}
		if (MSP_TTS_FLAG_DATA_END == synth_status)
			break;
		printf(">");
		usleep(150*1000); //防止频繁占用CPU
	}
	printf("\n");
	if (MSP_SUCCESS != ret)
	{
		printf("QTTSAudioGet failed, error code: %d.\n",ret);
		QTTSSessionEnd(sessionID, "AudioGetError");
		fclose(fp);
		return ret;
	}
	/* 修正wav文件头数据的大小 */
	wav_hdr.size_8 += wav_hdr.data_size + (sizeof(wav_hdr) - 8);
	
	/* 将修正过的数据写回文件头部,音频文件为wav格式 */
	fseek(fp, 4, 0);
	fwrite(&wav_hdr.size_8,sizeof(wav_hdr.size_8), 1, fp); //写入size_8的值
	fseek(fp, 40, 0); //将文件指针偏移到存储data_size值的位置
	fwrite(&wav_hdr.data_size,sizeof(wav_hdr.data_size), 1, fp); //写入data_size的值
	fclose(fp);
	fp = NULL;
	/* 合成完毕 */
	ret = QTTSSessionEnd(sessionID, "Normal");
	if (MSP_SUCCESS != ret)
	{
		printf("QTTSSessionEnd failed, error code: %d.\n",ret);
	}

	return ret;
}

int main(int argc, char* argv[])
{
	int         ret                  = MSP_SUCCESS;
	const char* login_params         = "appid = 5bfcc6d7, work_dir = .";//登录参数,appid与msc库绑定,请勿随意改动
	/*
	* rdn:           合成音频数字发音方式
	* volume:        合成音频的音量
	* pitch:         合成音频的音调
	* speed:         合成音频对应的语速
	* voice_name:    合成发音人
	* sample_rate:   合成音频采样率
	* text_encoding: 合成文本编码格式
	*
	*/
	const char* session_begin_params = "voice_name = xiaoyan, text_encoding = utf8, sample_rate = 16000, speed = 50, volume = 50, pitch = 50, rdn = 2";
	const char* filename             = "tts_sample.wav"; //合成的语音文件名称
	const char* text                 = "您好，这是一个语音合成示例程序"; //合成文本

	/* 用户登录 */
	ret = MSPLogin(NULL, NULL, login_params);//第一个参数是用户名，第二个参数是密码，第三个参数是登录参数，用户名和密码可在http://www.xfyun.cn注册获取
	if (MSP_SUCCESS != ret)
	{
		printf("MSPLogin failed, error code: %d.\n", ret);
		goto exit ;//登录失败，退出登录
	}
	printf("\n###########################################################################\n");
	printf("## 语音合成（Text To Speech，TTS）技术能够自动将任意文字实时转换为连续的 ##\n");
	printf("## 自然语音，是一种能够在任何时间、任何地点，向任何人提供语音信息服务的  ##\n");
	printf("## 高效便捷手段，非常符合信息时代海量数据、动态更新和个性化查询的需求。  ##\n");
	printf("###########################################################################\n\n");












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




        // // receive
        // char recvBuf[1024];

        // if ( -1 == recv( accsocfd, recvBuf, 1024, 0 ) )
        // {
        //     printf( "recv failed!\n" );
        //     return(-1);
        // }

        // printf( "recv suc!\n" );
        // printf( "recvBuf  = [%s]\n", recvBuf );
        // // printf( "recvBuf len is = [%d]\n", int(strlen( recvBuf ) ) );


    // receive
    if ( -1 == (recdata = read( accsocfd, buf, sizeof(buf) ) ) )
    {
        printf( "read failed!\n" );
        return(-1);
    }
    printf( "read suc!\n" );
    buf[recdata] = '\0';
    printf( "recdata  = [%s]\n", buf );
    printf( "recdata len is = [%d]\n", recdata );




		/* 文本合成 */
		printf("开始合成 ...\n");
		ret = text_to_speech( buf , filename, session_begin_params);
		if (MSP_SUCCESS != ret)
		{
			printf("text_to_speech failed, error code: %d.\n", ret);
		}
		printf("合成完毕\n");

		system("play tts_sample.wav");







        close( accsocfd );




    }
    close( socketfd );






















exit:
	printf("按任意键退出 ...\n");
	getchar();
	MSPLogout(); //退出登录

	return 0;
}

